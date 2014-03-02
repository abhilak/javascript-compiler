from ply import lex
from sys import argv

filename, input_file = argv 

# The different token need to be defined as a tuple
tokens = (
        "KEYWORD",
        "IDENTIFIER",
        "WHITESPACE",
        "NUMBER",
        "OP_ASSIGNMENT",
        "OP_COLON",
        "OP_EQUALS",
        "OP_NOT_EQUALS",
        "OP_ADDITION",
        "OP_SUBTRACTION",
        "OP_MULTIPLICATION",
        "OP_DIVISION",
        "OP_MODULUS",
        "SEP_SEMICOLON",
        "SEP_OPEN_BRACE",
        "SEP_CLOSE_BRACE",
        "SEP_QUOTES",
        "SEP_OPEN_BRACKET",
        "SEP_CLOSE_BRACKET"
        )

# RegEx for KEYWORDS
t_KEYWORD = (
        r"var|"
        r"let|"
        # Programming Constructs
        r"if|"
        r"else|"
        r"for|"
        r"in|"
        r"do|"
        r"while|"
        r"switch|"
        r"case|"
        r"break|"
        r"continue|"
        r"function|"
        r"return|"
        r"try|"
        r"throw|"
        r"catch|"
        r"finally|"
        # OOP features
        r"new|"
        r"this|"
        r"delete|"
        # Other operators
        r"instanceof|"
        r"typeof|"
        # Entities in the language
        r"Array|"
        r"Object|"
        r"Function|"
        r"true|"
        r"false|"
        r"undefined|"
        r"infinity|"
        r"null|"
        r"NaN"
        )

# RegEx for IDENTIFIERS
t_IDENTIFIER = r"[a-zA-Z]\w+"

# RegEx for NUMBERS
def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = float(t.value)
    return t

# RegEx for OPERATORS
t_OP_ASSIGNMENT = (
        r"=|"
        r"\+=|"
        r"-=|"
        r"/=|"
        r"%=|"
        r"\*="
        )
t_OP_COLON = r":"
t_OP_ADDITION = r"\+"
t_OP_SUBTRACTION = r"-"
t_OP_MULTIPLICATION = r"\*"
t_OP_DIVISION = r"/"
t_OP_MODULUS = r"%"
t_OP_EQUALS = (
        r"==|"
        r"==="
        )
t_OP_NOT_EQUALS = (
        r"!=|"
        r"!=="
        )

# RegEx for SEPERATORS
t_SEP_SEMICOLON = r";"
t_SEP_OPEN_BRACE = r"\{"
t_SEP_CLOSE_BRACE = r"\}"
t_SEP_OPEN_BRACKET = r"\["
t_SEP_CLOSE_BRACKET = r"\]"
t_SEP_QUOTES = (
        r"\"|"
        r"\'"
        )

# RegEx for WHITESPACE
def t_WHITESPACE(t): 
    r"\s"

# Necessary error function
def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lex.lex()

# Lex the input file
program = open(input_file).read()
lex.input(program)
for tok in iter(lex.token, None):
    print repr(tok.type), repr(tok.value)
