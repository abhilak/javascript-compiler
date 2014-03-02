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
        "SEP_SEMICOLON",
        "SEP_OPEN_BRACE",
        "SEP_CLOSE_BRACE"
        )

# RegEx for KEYWORDS
t_KEYWORD = (
        r"var|"
        r"if|"
        r"else|"
        r"for|"
        r"while|"
        r"typeof|"
        r"function|"
        r"undefined|"
        r"infinity|"
        r"null|"
        r"Array|"
        r"Object|"
        r"Function|"
        r"NaN"
        )

# RegEx for IDENTIFIERS
t_IDENTIFIER = r"[a-zA-Z]\w+"

# RegEx for NUMBERS
t_NUMBER = r"\d+(\.\d+)?"

# RegEx for OPERATORS
t_OP_ASSIGNMENT = r"="

# RegEx for SEPERATORS
t_SEP_SEMICOLON = r";"
t_SEP_OPEN_BRACE = r"{"
t_SEP_CLOSE_BRACE = r"{"

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
