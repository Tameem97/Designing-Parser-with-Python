import tokenizer


# recursive decent parser
class my_parser:
    def __init__(self) -> None:
        self._string = ""


    # parse a string into AST
    def parse(self, string):
        self._string = string
        return self.program()


    # main entry point
    def program(self):
        return self.numeric_literal()
    

    # Numeric Literal
    def numeric_literal(self):
        return {'type': 'NumericLiteral',
                 'value': int(self._string)}