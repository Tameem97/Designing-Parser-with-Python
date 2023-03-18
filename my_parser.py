from tokenizer import Tokenizer


# Recursive Decent Parser
class my_parser:
    def __init__(self) -> None:
        self._string = ""
        self._tokenizer = Tokenizer()
        self._lookahead = None


    # Parse a string into AST
    def parse(self, string):
        self._string = string
        self._tokenizer.init(string)

        # Prime the tokenizer to obtain the first token which is our lookahead
        # The lookahead is used for predictive parsing
        self._lookahead = self._tokenizer.getNextToken()

        # parse recursively starting from the main entry point, the program
        return self.program()


    # main entry point
    def program(self):
        return { 'type': 'Program', 
                  'body': self.numeric_literal() }
    

    # Numeric Literal
    def numeric_literal(self):
        token = self._eat('NUMBER')
        return {'type': 'NumericLiteral',
                 'value': int(token['value']) }
    

    # Expects a token of given type
    def _eat(self, tokentype):
        token = self._lookahead

        if (token == None):
            raise ValueError("Unexpected end of input")

        if (token["type"] != tokentype):
            raise ValueError("Unexpected Token")

        self._lookahead = self._tokenizer.getNextToken()

        return token