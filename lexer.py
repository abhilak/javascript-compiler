from ply import lex
from sys import argv

filename, input_file = argv 

# The different token need to be defined as a tuple
tokens = (
        "COMMENT",
        "KEYWORD",
        "IDENTIFIER",
        "NUMBER",
        "OP_ASSIGNMENT",
        "SEP_QUOTES",
        "OP_COLON",
        "OP_EQUALS",
        "OP_NOT_EQUALS",
        "OP_ADDITION",
        "OP_SUBTRACTION",
        "OP_MULTIPLICATION",
        "OP_DIVISION",
        "OP_MODULUS",
        "OP_GREATER_THEN",
        "OP_GREATER_THEN_E",
        "OP_LESS_THEN",
        "OP_LESS_THEN_E",
        "OP_AND",
        "OP_OR",
        "SEP_SEMICOLON",
        "SEP_OPEN_BRACE",
        "SEP_CLOSE_BRACE",
        "SEP_OPEN_BRACKET",
        "SEP_CLOSE_BRACKET",
        "SEP_OPEN_PARENTHESIS",
        "SEP_CLOSE_PARENTHESIS",
        "WHITESPACE"
        )

# RegEx for comments
def t_COMMENT(t):
    (
            r"//[^\n]+|"
            r"/\*[^(\*/)]+(\*/)"
            )

# RegEx for KEYWORDS
t_KEYWORD = (
        # Programming Constructs
        r"var|"
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
        r"true|"
        r"false|"
        r"undefined|"
        r"infinity|"
        r"null|"
        r"NaN"
        )

# RegEx for IDENTIFIERS
t_IDENTIFIER = r"[a-zA-Z]\w*"

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
        r"\*=|"
        r"/=|"
        r"%="
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
t_OP_GREATER_THEN = r">"
t_OP_GREATER_THEN_E = r">="
t_OP_LESS_THEN = r"<"
t_OP_LESS_THEN_E = r"<="
t_OP_AND = r"&&"
t_OP_OR = r"\|\|"

# RegEx for SEPERATORS
t_SEP_SEMICOLON = r";"
t_SEP_OPEN_BRACE = r"\{"
t_SEP_CLOSE_BRACE = r"\}"
t_SEP_OPEN_BRACKET = r"\["
t_SEP_CLOSE_BRACKET = r"\]"
t_SEP_OPEN_PARENTHESIS = r"\("
t_SEP_CLOSE_PARENTHESIS = r"\)"
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

# Create he lexer by calling lex function of lex
lex.lex()

# Open the passed argument as an input file and then pass it to lex
program = open(input_file).read()
lex.input(program)

# This iterates over the function lex.token and converts the returned object into an iterator
print "\tTYPE \t\t\t\t\t\t VALUE"
print "\t---- \t\t\t\t\t\t -----"
for tok in iter(lex.token, None):
    print "%-25s \t\t\t\t %s" %(repr(tok.type), repr(tok.value))
