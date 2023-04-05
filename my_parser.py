from tokenizer import Tokenizer


# Recursive Decent Parser
class my_parser:
    def __init__(self) -> None:
        self._string = ''
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
    '''
       Program
          : StatementList
          ;
    '''
    def program(self):
        return { 'type': 'Program', 
                  'body': self.statement_list() }
    

    # Literal
    def literal(self):
        if (self._lookahead['type'] == 'NUMBER'): return self.numeric_literal()
        elif (self._lookahead['type'] == 'STRING'): return self.string_literal()
        elif (self._lookahead['type'] == 'True'): return self.boolean_literal(True)
        elif (self._lookahead['type'] == 'False'): return self.boolean_literal(False)
        elif (self._lookahead['type'] == 'None'): return self.null_literal()
        else: raise ValueError('Error: Unexpected Literal')


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


    # Boolean Literal
    def boolean_literal(self, value):
        if value: self._eat('True')
        else: self._eat('False')
        return {'type': 'BooleanLiteral', 'value': value}
    

    # Null Literal
    def null_literal(self):
        self._eat('None')
        return {'type': 'NullLiteral', 'value': None}


    # Expression
    def expression(self):
        return self.assignment_expression()


    # Expression Statement
    def expression_statement(self):
        _expression = self.expression()
        self._eat(';')
        return {'type': 'ExpressionStatement', 'expression':_expression}


    # Statement
    def statement(self):
        if (self._lookahead.get('type') == ';' ):
            return self.empty_statement()
        elif (self._lookahead.get('type') == 'if' ):
            return self.if_statement()
        elif (self._lookahead.get('type') == '{' ):
            return self.block_statement()
        elif (self._lookahead.get('type') == 'let' ):
            return self.variable_statement()
        elif (self._lookahead.get('type') == 'def' ):
            return self.function_declaration()
        elif (self._lookahead.get('type') == 'return' ):
            return self.return_statement()
        elif (self._lookahead.get('type') == 'class' ):
            return self.class_declaration()
        elif (self._lookahead.get('type') == 'while' or self._lookahead.get('type') == 'for' or (self._lookahead.get('type') == 'do' )):
            return self.iterator_statement()
        else:
            return self.expression_statement()


    # Class Declaration
    def class_declaration(self):
        self._eat('class')
        id = self.identifer()

        superClass = self.class_extends() if self._lookahead['type'] == 'extends' else None

        body = self.block_statement()

        return {'type': 'ClassDeclaration', 'id':id, 'superClass':superClass, 'body':body}
    

    # class extends
    def class_extends(self):
        self._eat('extends')
        return self.identifer()


    # function declaration
    def function_declaration(self):
        self._eat('def')
        name = self.identifer()

        self._eat('(')
        params = self.formal_parameter_list() if self._lookahead['type'] != ')' else [] 
        self._eat(')')

        body = self.block_statement()

        return {'type': 'FunctionDeclaration', 'name':name, 'params': params, 'body':body}


    # Formal Parameter List
    def formal_parameter_list(self):
        params = []
        params.append(self.identifer())

        while (self._lookahead['type'] == ',' and self._eat(',')):
            params.append(self.identifer())

        return params


    # return statement
    def return_statement(self):
        self._eat('return')
        argument = self.expression() if self._lookahead['type'] != ';' else None
        self._eat(';')
        return {
            'type': 'ReturnStatement', 'argument': argument
        }

    # Iterator Statement
    def iterator_statement(self):
        if (self._lookahead['type'] == 'while'): return self.while_statement()
        elif (self._lookahead['type'] == 'do'): return self.do_while_statement()
        elif (self._lookahead['type'] == 'for'): return self.for_statement()

    # Statement List
    def statement_list(self, stopLookahead =None):
        _statement_list = [self.statement()]

        while (self._lookahead != None and self._lookahead['type'] != stopLookahead):
            _statement_list.append(self.statement())

        return _statement_list


    # Primary Expression
    def primary_expression(self):
        if (self._is_literal(self._lookahead['type'])): return self.literal()
        if (self._lookahead['type'] == '('): return self.parenthesized_expression()
        elif (self._lookahead['type'] == 'IDENTIFIER'): return self.identifer()
        elif (self._lookahead['type'] == 'this'): return self.this_expression()
        elif (self._lookahead['type'] == 'new'): return self.new_expression()
        else: raise SyntaxError(f"Unexpected Primary Expression {self._lookahead}")


    # New Expression
    def new_expression(self):
        self._eat('new')
        return {
            'type': 'NewExpression', 'callee': self.member_expression(), 'arguments': self.arguments()
        }


    # Left Hand Side Expression
    def left_hand_side_expression(self):
        return self.call_member_expression()


    # Call Member Expression
    def call_member_expression(self):

        if (self._lookahead['type'] == 'super'):
            return self._call_expression(self.super_expression())

        member = self.member_expression()
        if (self._lookahead['type'] == '('):
            return self._call_expression(member)
        
        return member

    # Member Expression 
    def member_expression(self):
        _object = self.primary_expression()
        while (self._lookahead['type'] == '.' or self._lookahead['type'] == '['):
            if (self._lookahead['type'] == '.'):
                self._eat('.')
                property = self.identifer()
                _object = {'type': 'MemberExpression', 'computed': False, 'object': _object, 'property': property}


            if (self._lookahead['type'] == '['):
                self._eat('[')
                property = self.expression()
                self._eat(']')
                _object = {'type': 'MemberExpression', 'computed': True, 'object': _object, 'property': property}

        return _object


    # IF-ELSE Expression
    def if_statement(self):
        self._eat('if')
        self._eat('(')
        test = self.expression()
        self._eat(')')

        consequent = self.statement()
        alternate = None
        if (self._lookahead != None and self._lookahead.get('type') == 'else'):
            self._eat('else')
            alternate = self.statement()

        return {
            'type': 'IfStatement', 'test': test, 'consequent': consequent, 'alternate': alternate
        } 
    

    # while statement
    def while_statement(self):
        self._eat('while')

        self._eat('(')
        test = self.expression()
        self._eat(')')

        body = self.statement()

        return {'type': 'WhileStatement', 'test':test, 'body':body}


    # do while statement
    def do_while_statement(self):
        self._eat('do')

        body = self.statement()


        self._eat('while')
        self._eat('(')
        test = self.expression()
        self._eat(')')
        self._eat(';')

        return {'type': 'DoWhileStatement', 'test':test, 'body':body}


    # for statement
    def for_statement(self):
        self._eat('for')
        self._eat('(')

        init = self.for_statement_init() if self._lookahead['type'] != ';' else None
        self._eat(';')

        test = self.expression() if self._lookahead['type'] != ';' else None
        self._eat(';')

        update = self.expression() if self._lookahead['type'] != ')' else None
        self._eat(')')

        body = self.statement()

        return {'type': 'ForStatement', 'init': init, 'test':test, 'update': update, 'body':body}


    # for statement initializer
    def for_statement_init(self):
        if (self._lookahead['type'] == 'let'):
            return self.variable_statement_init()
        return self.expression()
    

    # Variable Statement
    def variable_statement(self):
        _variable_statement = self.variable_statement_init()
        self._eat(';')
        return _variable_statement


    # variable statement initializer
    def variable_statement_init(self):
        self._eat('let')
        declarations = self.variable_declaration_list()
        return { 'type': 'VariableStatement', 'declarations':declarations}


    # Variable Declaration List
    def variable_declaration_list(self):
        declarations = []
        declarations.append(self.variable_declaration())

        while (self._lookahead['type'] == ',' and self._eat(',')):
            declarations.append(self.variable_declaration())

        return declarations


    # Variable Declaration
    def variable_declaration(self):
        id = self.identifer()
        init = self.variable_initializer() if (self._lookahead['type'] != ';' and self._lookahead['type'] != ',') else None
        return {'type': 'VariableDeclaration', 'id':id, 'init':init}


    # Variable Initializer
    def variable_initializer(self):
        self._eat('SIMPLE_ASSIGN')
        return self.assignment_expression()
    

    # Block Statement
    def block_statement(self):
        self._eat('{')
        body = [] if self._lookahead['type']  == '}' else self.statement_list('}')
        self._eat('}')
        return {'type': 'BlockStatement', 'body': body}


    # Empty Statement
    def empty_statement(self):
        self._eat(';')
        return {'type': 'EmptyStatement'}
    

    # Assignment Expression
    def assignment_expression(self):
        left = self.logical_or_expression()

        if (not self._is_assignment_operator(self._lookahead['type'])): return left

        return {'type': 'AssignmentExpression', 'operator': self.assignment_operator()['value'],
                'left': self._check_valid_asignment_target(left),
                'right': self.assignment_expression()}


    # Assignment Operator
    def assignment_operator(self):
        if (self._lookahead['type'] == 'SIMPLE_ASSIGN'): return self._eat('SIMPLE_ASSIGN')
        else: return self._eat('COMPLEX_ASSIGN')


    # Logical And Expression
    def logical_and_expression(self): 
        return self._logical_expression('equality_expression',  'LOGICAL_AND')


    # Logical OR Expression
    def logical_or_expression(self): 
        return self._logical_expression('logical_and_expression',  'LOGICAL_OR')


    # Equality Expression
    def equality_expression(self):
        return self._binary_expression('relational_expression',  'EQUALITY_OPERATOR')


    # Relational Expression
    def relational_expression(self): 
        return self._binary_expression('additive_expression',  'RELATIONAL_OPERATOR')


    # Identifer
    def identifer(self):
        name = self._eat('IDENTIFIER')['value']
        return {'type': 'Identifer',
                'name': name}


    # Additive Expression
    def additive_expression(self):
        return self._binary_expression('multiplicative_expression', 'ADDITIVE_OPERATOR')


    # Multiplicative Expression
    def multiplicative_expression(self):
        return self._binary_expression('unary_expression', 'MULTIPLICATIVE_OPERATOR')


    # Parenthesized Expression
    def parenthesized_expression(self):
        self._eat('(')
        _expression = self.expression()
        self._eat(')')
        return _expression


    # Unary Expression
    def unary_expression(self):
        operator = None
        if (self._lookahead['type'] == 'ADDITIVE_OPERATOR'):
            operator = self._eat('ADDITIVE_OPERATOR')['value']
        elif (self._lookahead['type'] == 'LOGICAL_NOT'):
            operator = self._eat('LOGICAL_NOT')['value']

        if (operator != None):
            return {'type' :'UnaryExpression', 'operator':operator, 'argument': self.unary_expression() }
        
        return self.left_hand_side_expression()


    # This Expression
    def this_expression(self):
        self._eat('this')
        return {'type': 'ThisExpression'}


    # This Expression
    def super_expression(self):
        self._eat('super')
        return {'type': 'Super'}


    # Check literal
    def _is_literal(self, tokenType):
        return tokenType == 'NUMBER' or tokenType == 'STRING' or tokenType == 'True' or tokenType == 'False' or tokenType == 'None'


    # Generic Binary Expression
    def _binary_expression(self, builder_name, operatorToken):
        left = getattr(self, builder_name)()

        while (self._lookahead['type'] == operatorToken):
            # Operators
            operator = self._eat(operatorToken)['value']
            right = getattr(self, builder_name)()
            left = {'type': 'BinaryExpression',
                    'operator': operator, 'left': left, 'right': right}
            
        return left


    # Generic Logical Expression
    def _logical_expression(self, builder_name, operatorToken):
        left = getattr(self, builder_name)()

        while (self._lookahead['type'] == operatorToken):
            # Operators
            operator = self._eat(operatorToken)['value']
            right = getattr(self, builder_name)()
            left = {'type': 'LogicalExpression',
                    'operator': operator, 'left': left, 'right': right}
            
        return left


    # Valid Assignment Check
    def _check_valid_asignment_target(self, node):
        if (node['type']=='Identifer' or node['type'] == 'MemberExpression'): return node

        raise SyntaxError('Invalid left hand assignment expression')


    # Assignment Operator Check
    def _is_assignment_operator(self, tokenType):
        return tokenType == 'SIMPLE_ASSIGN' or tokenType == 'COMPLEX_ASSIGN'


    # Call Expression Helper
    def _call_expression(self, callee):
        callExpression = {
            'type': 'CallExpression', 'callee':callee, 'arguments':self.arguments()
        }

        if (self._lookahead['type'] == '('):
            callExpression = self._call_expression(callExpression)

        return callExpression
    

    # Arguments
    def arguments(self):
        self._eat('(')
        argumentsList = self.arguments_list() if self._lookahead['type'] != ')' else []
        self._eat(')')
        return argumentsList


    # Argument List
    def arguments_list(self):
        _argument_list = []

        _argument_list.append(self.assignment_expression())
        while (self._lookahead['type'] == ',' and self._eat(',')):
            _argument_list.append(self.assignment_expression())

        return _argument_list


    # Expects a token of given type
    def _eat(self, tokentype):
        token = self._lookahead

        if (token == None):
            raise ValueError('Unexpected end of input')

        if (token['type'] != tokentype):
            raise ValueError(f"Unexpected Token: {tokentype} whereas expected {token['type']}")

        self._lookahead = self._tokenizer.getNextToken()

        return token