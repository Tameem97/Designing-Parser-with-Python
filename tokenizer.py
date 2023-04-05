import re


# Tokens Specifications
spec = [ 
    # White Spaces
    [r"^\s+", None],

    # Single Line Comments
    [r"^//.*", None],

    # Multi-Line Comments
    [r"^/\*[\s\S]*?\*/", None],

    # Symbols
    [r"^;", ";"],
    [r"^\{", "{"],
    [r"^\}", "}"],
    [r"^\(", "("],
    [r"^\)", ")"],
    [r"^\,", ","],

    # Keywords
    [r"^\blet\b", "let"],
    [r"^\bif\b", "if"],
    [r"^\belse\b", "else"],
    [r"^\bTrue\b", "True"],
    [r"^\bFalse\b", "False"],
    [r"^\bNone\b", "None"],
    [r"^\bwhile\b", "while"],
    [r"^\bdo\b", "do"],
    [r"^\bfor\b", "for"],

    # Numbers
    [r"^\d+", "NUMBER"],

    # Identifiers
    [r"^\w+", "IDENTIFIER"],

    # Equality Operator
    [r"^[=!]=", "EQUALITY_OPERATOR"],

    # Assignment Operators
    [r"^=", "SIMPLE_ASSIGN"],

    # Operators
    [r"^[\*\/\+\-]=", "COMPLEX_ASSIGN"],

    # Binary Operators
    [r"^[+\-]", "ADDITIVE_OPERATOR"],
    [r"^[*\/]", "MULTIPLICATIVE_OPERATOR"],

    [r"^[><]=?", "RELATIONAL_OPERATOR"],

    # logical operators
    [r"^\|\|", "LOGICAL_OR"],
    [r"^&&", "LOGICAL_AND"],
    [r"^!", "LOGICAL_NOT"],

    # Strings
    [r"\"[^\"]*\"", "STRING"],
    [r"\'[^\"]*\'", "STRING"]
]


# Tokenizer Class
class Tokenizer:
    def __init__(self) -> None:
        self._string = ""
        self._cursor = 0;


    # Initializer Method
    def init(self, string):
        self._string = string
        self._cursor = 0


    # obtain next token
    def getNextToken(self):
        if (not self.hasMoreTokens()):  return None
        
        string = self._string[self._cursor:]

        for i in spec:
            tokenValue = self._match(i[0], string)

            if (tokenValue == None): continue
            if (i[1] == None): return self.getNextToken()

            return {"type": i[1], "value": tokenValue}

        raise ValueError(f"Unexpected Token: {i[0]}")
        

    # Check if there are tokens remaining or not
    def hasMoreTokens(self):
        return self._cursor < len(self._string)
    

    # Match Regular Expression
    def _match(self, regexp, string):
        matched = re.search(regexp, string)     # match is alternative
        if (matched):
            self._cursor += len(matched[0])
            return matched[0]
        
        return None
    

    # Whether the tokenizer reached EOF
    def isEOF(self):
        return self._cursor == len(self._string)