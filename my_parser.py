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
                  'body': self.statement_list() }
    

    # Literal
    def literal(self):
        if (self._lookahead['type'] == 'NUMBER'): return self.numeric_literal()
        elif (self._lookahead['type'] == 'STRING'): return self.string_literal()
        else: raise ValueError("Error: Unexpected Literal")


    # Numeric Literal
    def numeric_literal(self):
        token = self._eat('NUMBER')
        return {'type': 'NumericLiteral',
                 'value': int(token['value']) }
    

    # String Literal
    def string_literal(self):
        token = self._eat('STRING')
        return {'type': 'StringLiteral',
                 'value': token['value'][1:-1] }


    # Statement List
    def statement_list(self, stopLookahead =None):
        _statement_list = [self.statement()]

        while (self._lookahead != None and self._lookahead["type"] != stopLookahead):
            _statement_list.append(self.statement())

        return _statement_list


    # Statement
    def statement(self):
        if (self._lookahead.get("type") == "{" ):
            return self.block_statement()
        
        if (self._lookahead.get("type") == ";" ):
            return self.empty_statement()
        
        return self.expression_statement()


    # Expression Statement
    def expression_statement(self):
        _expression = self.expression()
        self._eat(';')
        return {"type": 'ExpressionStatement', "expression":_expression}
    

    # Block Statement
    def block_statement(self):
        self._eat("{")
        body = [] if self._lookahead["type"]  == "}" else self.statement_list('}')
        self._eat("}")
        return {"type": "BlockStatement", "body": body}


    # Empty Statement
    def empty_statement(self):
        self._eat(";")
        return {"type": "EmptyStatement"}


    # Expression
    def expression(self):
        return self.additive_expression()
    

    # Additive Expression
    def additive_expression(self):
        left = self.multiplicative_expression()

        while (self._lookahead['type'] == 'ADDITIVE_OPERATOR'):
            # Operators
            operator = self._eat('ADDITIVE_OPERATOR')['value']
            right = self.multiplicative_expression()
            left = {'type': 'BinaryExpression',
                    'operator': operator, 'left': left, 'right': right}
            
        return left


    # Multiplicative Expression
    def multiplicative_expression(self):
        left = self.primary_expression()

        while (self._lookahead['type'] == 'MULTILPICATIVE_OPERATOR'):
            # Operators
            operator = self._eat('MULTILPICATIVE_OPERATOR')['value']
            right = self.primary_expression()
            left = {'type': 'BinaryExpression',
                    'operator': operator, 'left': left, 'right': right}
            
        return left


    # Primary Expression
    def primary_expression(self):
        if (self._lookahead['type'] == '('): return self.parenthesized_expression()
        else: return self.literal()


    # Parenthesized Expression
    def parenthesized_expression(self):
        self._eat('(')
        _expression = self.expression()
        self._eat(')')
        return _expression


    # Expects a token of given type
    def _eat(self, tokentype):
        token = self._lookahead

        if (token == None):
            raise ValueError("Unexpected end of input")

        if (token["type"] != tokentype):
            raise ValueError("Unexpected Token")

        self._lookahead = self._tokenizer.getNextToken()

        return token