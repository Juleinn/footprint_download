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
    data = data.replace("(", " ( ").replace(")", " ) ")
    data = data.split()
    return parse_recursive(data)

def print_recursive(arr):
    ret = ""
    while True:
        if len(arr) == 0:
            return ret
        item = arr.pop(0)

        if type(item) == list:
            ret += "(" + print_recursive(item) + ") "
        else:
            # we should only have strings at this point
            ret += item + " "

def list_to_sexp(data):
    return print_recursive([data])

def update_footprint_field(symbol_sexp_data):
    # assume standard file layout ( this might break )
    for item in symbol_sexp_data:
        if item[0] == "symbol":
            for prop in item:
                if len(prop) >= 3 and prop[0] == "property" and prop[1] == '"Footprint"':
                    # TODO improve this. make footprint library configurable and 
                    # make sure footprint/symbol names are matching
                    footprint = prop[2].replace('"', '')
                    prop[2] = f'"footprint_download:{footprint}"'
    return symbol_sexp_data

def merge_symbol_libraries(destination_filename, source_filename):
    print(f"merging {source_filename} into {destination_filename}")
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

# this will break at some point, when directory structure changes
def extract_archive_mouser(zip_filename):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
        # find out the folders
        directories = next(os.walk(temp_dir))[1]
        if len(directories) != 1:
            print("Incorrect archive format")
            return None
        
        device_subdir = temp_dir + "/" + directories[0]
        # walk the subdir, we should have KiCad subdir and optionnaly 3D
        cads_subdirs = next(os.walk(device_subdir))[1]
        # find Kicad files
        if not "KiCad" in cads_subdirs:
            print("Kicad not found")
            return None
        
        kicad_subdir = device_subdir + "/KiCad"
        # looking for a .kicad_sym file
        kicad_files = next(os.walk(kicad_subdir))[2]
        symbol_libs = list(filter(lambda x: ".kicad_sym" in x, kicad_files))
        footprints = list(filter(lambda x: ".kicad_mod" in x, kicad_files))

        if len(symbol_libs) != 1 or len(footprints) != 1:
            print("Multiple symbol/footprints libs found. Cannot choose.")
            return None
        
        symbol_lib = kicad_subdir + '/' + symbol_libs[0]
        footprint = kicad_subdir + '/' + footprints[0]

        if not "3D" in cads_subdirs:
            print("No 3D file found. Returning symbol/footprint")
            return (symbol_lib, footprint, "")
        
        subdir_3d = device_subdir + '/3D'  
        files_3d = next(os.walk(subdir_3d))[2]
        if len(files_3d) == 0:
            print("No 3D file found. Returning symbol/footprint")
            return (symbol_lib, footprint, "")
        
        # TODO manage multi format here, wrl preferred over stp
        file_3d = subdir_3d + '/' + files_3d[0]
        return (symbol_lib, footprint, file_3d)

if __name__ == "__main__":
    symbol_lib, footprint, model_3d = extract_archive_mouser("test.zip")
    print(symbol_lib)
    print(footprint)
    print(model_3d)
    shutil.copy("./destination_template.kicad_sym","./destination.kicad_sym")
    # merge_symbol_libraries("destination.kicad_sym", "source_0.kicad_sym")
    # merge_symbol_libraries("destination.kicad_sym", "source_1.kicad_sym")

    # actually merge the extracted libraries into destination
    merge_symbol_libraries('./destination.kicad_sym', "/tmp/tmpajzh9p9n/TPS552872QWRYQRQ1/KiCad/TPS552872QWRYQRQ1.kicad_sym")
    with open("/tmp/tmpajzh9p9n/TPS552872QWRYQRQ1/KiCad/TPS552872QWRYQRQ1.kicad_sym", 'r') as source_file:
        source_data = source_file.read()
        source = sexp_to_list(source_data)
        update_footprint_field(source)

        with open('/tmp/modified.kicad_sym', 'w') as modified:
            modified.write(list_to_sexp(source))
        
     
