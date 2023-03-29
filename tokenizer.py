import re


# Tokens Specifications
spec = [ 
    # Numbers
    [r"^\d+", "NUMBER"],

    # Strings
    [r"\"[^\"]*\"", "STRING"],
    [r"\'[^\"]*\'", "STRING"],

    # White Spaces
    [r"^\s+", None],

    # Single Line Comments
    [r"^//.*", None],

    # Multi-Line Comments
    [r"^/\*[\s\S]*?\*/", None],

    # Equality Operator
    [r"^[=!]=", "EQUALITY_OPERATOR"],

    # Binary Operators
    [r"^[+\-]", "ADDITIVE_OPERATOR"],
    [r"^[*\/]", "ADDITIVE_OPERATOR"],

    # Keywords
    [r"^\blet\b", "let"],
    [r"^\bif\b", "if"],
    [r"^\belse\b", "else"],
    [r"^\bTrue\b", "True"],
    [r"^\bFalse\b", "False"],
    [r"^\bNone\b", "None"],

    # Identifiers
    [r"^\w+", "IDENTIFIER"],

    # Assignment Operators
    [r"^=", "SIMPLE_ASSIGN"],

    # Operators
    [r"^[\*\/\+\-]=", "COMPLEX_ASSIGN"],
    [r"^[><]=?", "RELATIONAL_OPERATOR"],

    # logical operators
    [r"^\|\|", "LOGICAL_AND"],
    [r"^&&", "LOGICAL_OR"],
    [r"^!", "LOGICAL_NOT"],

    # Symbols
    [r"^\;", ";"],
    [r"^\{", "{"],
    [r"^\}", "}"],
    [r"^\(", "("],
    [r"^\)", ")"],
    [r"^\,", ","]
]


# Tokenizer Class
class Tokenizer:
    def __init__(self) -> None:
        self._string = ""
        self._cursor = 0;


    # Initializer Method
    def init(self, string):
        self._string = string
        self._cursor = 0;


    # obtain next token
    def getNextToken(self):
        if (not self.hasMoreTokens()):
            return None
        
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
        matched = re.match(regexp, string)
        if (matched):
            self._cursor += len(matched[0])
            return matched[0]
        
        return None