from ply import lex
from sys import argv

filename, input_file = argv 


# The different token need to be defined as a tuple
tokens = (
        "KEYWORD",
        "IDENTIFIER",
        "WHITESPACE"
        )

# RegEx for KEYWORDS
t_KEYWORD = (
        r"var|"
        r"if|"
        r"else"
        )

# RegEx for IDENTIFIERS
t_IDENTIFIER = r"[a-zA-Z]\w+"

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
