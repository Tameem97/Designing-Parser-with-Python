from my_parser import my_parser
from json import dumps
import sys
import os


# Recursive Decent Parser
rParser = my_parser()


mode = None
print_ast = False
raw_string = ""
_dir = os.listdir("./Tests")


if "--t" in sys.argv: mode = "-test"
if "--p" in sys.argv: print_ast = True
if ("--t" not in sys.argv and len(sys.argv)>=2): mode = "-file"


if (mode=='-test'):
    # Run Tests in the directory
    for i in _dir:
        read_file = open("./Tests/"+i, "r")

        print("\nRunning Test: ", "Tests/"+i)   
        parse_ast = rParser.parse(read_file.read())

        if (print_ast): print(dumps(parse_ast, indent=2))

        read_file.close()
        
    print("\nAll Tests Passed...\nTotal Tests:", len(_dir))

elif (mode == "-file"):
    # Execute the file
    read_file = open(sys.argv[-1], "r")
    parse_ast = rParser.parse(read_file.read())
    if (print_ast): print(dumps(parse_ast, indent=2))
    read_file.close()

else:
    # User-Input
    raw_string = input(">>> ")
    st = "\n"
    while (st != ""): 
        st = input(">>> ")
        raw_string += "\n" + st
    parse_ast = rParser.parse(raw_string)
        
    print(dumps(parse_ast, indent=2))