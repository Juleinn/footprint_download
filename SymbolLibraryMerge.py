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

def merge_symbol_libraries(destination_filename, source_filename):
    with open(source_filename, "r") as source_file, open(destination_filename, "r+") as destination_file:
        source_data = source_file.read()
        source = sexp_to_list(source_data)
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

if __name__ == "__main__":
    shutil.copy("./destination_template.kicad_sym","./destination.kicad_sym")
    merge_symbol_libraries("destination.kicad_sym", "source_0.kicad_sym")
    merge_symbol_libraries("destination.kicad_sym", "source_1.kicad_sym")
