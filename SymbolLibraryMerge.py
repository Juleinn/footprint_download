# a very basic s-exp parser just for merging libraries
# converts library file to array of arrays, then back
# all attributes are string
# formatting is lost, although easily fixable
# recursion should be OK because .kicad_sym files are 
# not deeply nested (usually 4-5 levels)
# this scales poorly with very large libraries but usually symbol 
# libraries are quite small files
# also avoids licensing issues (no dep management inside KiCad)
import shutil
import tempfile
import zipfile
import os
import IPython

def parse_recursive(flat):
    ret = []
    while True:
        if len(flat) == 0:
            return ret[0]
        item = flat.pop(0)
        if item == "(":
            sub = parse_recursive(flat)
            ret.append(sub)
        elif item == ")":
            return ret
        else:
            ret.append(item)

def sexp_to_list(data):
    # replace '(' with ' ( ' for whitespace splitting 
    # being carefull to leave quoted parentheses alone
    # first split around quotes 
    splits = data.split('"')
    for i in range(len(splits)):
        # quoted items are odd
        if i % 2 == 0:
            splits[i] = splits[i].replace("(", " ( ").replace(")", " ) ")
        else:
            # put the quotes back in (split removed them)
            splits[i] = f'"{splits[i]}"'

    data = "".join(splits)
    # whitespace split
    data = data.split()
    return parse_recursive(data)

def print_recursive(arr, offset):
    ret = ""
    while True:
        if len(arr) == 0:
            return ret
        item = arr.pop(0)

        if type(item) == list:
            ret += offset * " " + "(" + print_recursive(item, offset + 1) + offset * " " + ")\n"
        else:
            # we should only have strings at this point
            ret +=  item + " "

def list_to_sexp(data):
    return print_recursive([data], 0)

def has_3dmodel(footprint_sexp_data):
    for item in footprint_sexp_data:
        if item[0] == "model":
            return True 
    return False

def update_3dmodel(footprint_sexp_data, model3d_filename):
    model_sexp = f"""
(model {model3d_filename}
(at (xyz 0 0 0))
(scale (xyz 1 1 1))
(rotate (xyz 0 0 0))
)
    """
    model_data = sexp_to_list(model_sexp)
    # insert at base level 
    footprint_sexp_data.append(model_data)
    return footprint_sexp_data

def update_3dmodel_inplace(footprint_filename, model3d_filename):
    with open(footprint_filename, 'r+') as footprint_file: 
        footprint_sexp = footprint_file.read()
        footprint_data = sexp_to_list(footprint_sexp)

        if has_3dmodel(footprint_data):
            print("Footprint file has 3d model registered. Doing nothing")
            return
        else:
            model3d_filename = os.path.basename(model3d_filename)
            footprint_data = update_3dmodel(footprint_data, model3d_filename)

        footprint_file.seek(0)
        footprint_file.write(list_to_sexp(footprint_data))
        footprint_file.truncate()

def update_footprint_field(symbol_sexp_data):
    # assume standard file layout ( this might break )
    for item in symbol_sexp_data:
        if item[0] == "symbol":
            for prop in item:
                if len(prop) >= 3 and prop[0] == "property" and prop[1] == '"Footprint"':
                    # TODO improve this. make footprint library configurable and 
                    # make sure footprint/symbol names are matching

                    # we may have either 0 or 1 ':' separating library from the footprint
                    if prop[2].count(':') == 1:
                        footprint = prop[2].replace('"', '').split(':')[1]
                    else:
                        footprint = prop[2].replace('"', '')
                    prop[2] = f'"footprint_download:{footprint}"'

    return symbol_sexp_data

def merge_symbol_libraries(destination_filename, source_filename):
    with open(source_filename, "r") as source_file, open(destination_filename, "r+") as destination_file:
        source_data = source_file.read()
        source = sexp_to_list(source_data)
        source = update_footprint_field(source)
        destination_data = destination_file.read()
        destination = sexp_to_list(destination_data)

        # merge in symbol definitions from source (usually one)
        for item in source:
            if item[0] == "symbol":
                destination.append(item)

        destination_data = list_to_sexp(destination)
        destination_file.seek(0)
        destination_file.write(destination_data)
        destination_file.truncate()

def extract_archive(zip_filename):
    #check file exists and is less than 10MB
    if not os.path.exists(zip_filename) or not os.path.getsize(zip_filename) < 10e6: 
        print("Archive does not exist or is too large")
        return None

    temp_dir = tempfile.mkdtemp()
    try: 
        with zipfile.ZipFile(zip_filename) as zip_ref:
            # walk the zip for .kicad_sym, .kicad_mod and .stp/.step/.wrl files
            files_list = zip_ref.namelist()
            symbol_lib_filename = ""
            footprint_filenames = []
            model3d_filename = ""
            for filename in files_list:
                if ".kicad_sym" in filename:
                    symbol_lib_filename = filename
                if ".kicad_mod" in filename:
                    footprint_filenames.append(filename)
                if ".stp" in filename or ".step" in filename or ".wrl" in filename:
                    model3d_filename = filename

            # ignore archives containing only 3d models. Those would have to be added manually later
            if symbol_lib_filename == "" and len(footprint_filenames) == 0:
                print("Not a KiCAD archive. not unpacking")
                return None
            
            # only extract the required files
            if symbol_lib_filename != "":
                zip_ref.extract(symbol_lib_filename, temp_dir)
                symbol_lib_filename = f"{temp_dir}/{symbol_lib_filename}"
            if len(footprint_filenames) != 0:
                for i in range(len(footprint_filenames)):
                    footprint_filename = footprint_filenames[i]
                    zip_ref.extract(footprint_filename, temp_dir)
                    footprint_filenames[i] = f"{temp_dir}/{footprint_filename}"
            if model3d_filename != "":
                zip_ref.extract(model3d_filename, temp_dir)
                model3d_filename = f"{temp_dir}/{model3d_filename}"
            
            # return absolute path to extracted files 
            return (symbol_lib_filename, footprint_filenames, model3d_filename)
    except zipfile.BadZipFile:
        return None
