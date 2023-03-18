from my_parser import my_parser
from json import dumps

NewParser = my_parser()

program = '''  
 '''

parse_ast = NewParser.parse(program)
print(dumps(parse_ast, indent=2))