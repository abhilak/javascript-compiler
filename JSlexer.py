#!/usr/bin/python
from ply import lex

from helpers import debug as debug

########################################
############# RESERVED #################
########################################
reserved = {
    'var' : 'VAR',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'function' : 'FUNCTION',
    'return' : 'RETURN',
    'typeof' : 'OP_TYPEOF',
    'undefined' : 'UNDEFINED',
    'num' : 'HINT_NUMBER',
    'string' : 'HINT_STRING',
    'callback': 'HINT_CALLBACK',
    'array' : 'HINT_ARRAY',
    'bool' : 'HINT_BOOLEAN',
    'console' : 'CONSOLE',
    'log': 'LOG'
}

########################################
############# TOKENS ###################
########################################
tokens = [
        "COMMENT",
        "WHITESPACE",
        "STRING",
        "NUMBER",
        "BOOLEAN",
        "IDENTIFIER",
        "OP_DOT",
        "OP_ASSIGNMENT",
        "OP_EQUALS",
        "OP_NOT_EQUALS",
        "OP_NOT",
        "OP_PLUS",
        "OP_MINUS",
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
        "SEP_COMMA",
        "OP_HINT"
        ] + list(reserved.values())

########################################
############# COMMENTS #################
########################################
def t_ignore_COMMENT(t):
    r"//[^\n]+|"r"/\*[^(\*/)]+(\*/)"

########################################
############# LINE NUMBER ##############
########################################
def t_newline(t):
    r'\n+'
    global prev
    t.lexer.lineno += prev
    prev = len(t.value)
    debug.setPrev(prev)
    debug.setLineNumber(t.lexer.lineno)

########################################
############# WHITESPACE ###############
########################################
t_ignore_WHITESPACE = r"\s"

########################################
############# TYPES ####################
########################################
def t_STRING(t):
    r"(?P<start>\"|')[^\"']*(?P=start)"
    t.value = t.value.replace("\"", "").replace("'", "")
    return t

def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r"true|false"
    return t

########################################
############# OPERATORS ################
########################################
def t_OP_HINT(t):
    r"::"
    return t

def t_OP_DOT(t):
    r"\."
    return t

def t_OP_EQUALS(t):
    r"===|"r"=="
    return t

def t_OP_NOT_EQUALS(t):
    r"!==|"r"!="
    return t

def t_OP_ASSIGNMENT(t):
    r"=|"r"\+=|"r"-=|"r"\*=|"r"/=|"r"%="
    return t

def t_OP_NOT(t):
    r"!"
    return t

def t_OP_COLON(t):
    r":"
    return t

def t_OP_PLUS(t):
    r"\+"
    return t

def t_OP_MINUS(t):
    r"-"
    return t

def t_OP_MULTIPLICATION(t):
    r"\*"
    return t

def t_OP_DIVISION(t):
    r"/"
    return t

def t_OP_MODULUS(t):
    r"%"
    return t

def t_OP_GREATER_THEN_E(t):
    r">="
    return t

def t_OP_GREATER_THEN(t):
    r">"
    return t

def t_OP_LESS_THEN_E(t):
    r"<="
    return t

def t_OP_LESS_THEN(t):
    r"<"
    return t

def t_OP_AND(t):
    r"&&"
    return t

def t_OP_OR(t):
    r"\|\|"
    return t

########################################
############# IDENTIFIER ###############
########################################
def t_IDENTIFIER(t):
    r"[a-zA-Z$_][\w$]*"
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

########################################
############# SEPERATORS ###############
########################################
# RegEx for SEPERATORS
def t_SEP_SEMICOLON(t):
    r";"
    return t

def t_SEP_OPEN_BRACE(t):
    r"\{"
    return t

def t_SEP_CLOSE_BRACE(t):
    r"\}"
    return t

def t_SEP_OPEN_BRACKET(t):
    r"\["
    return t

def t_SEP_CLOSE_BRACKET(t):
    r"\]"
    return t

def t_SEP_OPEN_PARENTHESIS(t):
    r"\("
    return t

def t_SEP_CLOSE_PARENTHESIS(t):
    r"\)"
    return t

def t_SEP_COMMA(t):
    r","
    return t

########################################
############# ERROR ####################
########################################
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

######################################################################################################
# Create a lexer which uses the above defined rules, this can be used by the any parser which
# includes this file

######### Required Globals #############
debug = debug.Debug()
lexer = lex.lex()
prev = 0
########################################

# A function to test the lexer
def testLex(inputFile):
    # Open the passed argument as an input file and then pass it to lex
    program = open(inputFile).read()
    lexer.input(program)

    # This iterates over the function lex.token and converts the returned object into an iterator
    print "\tTYPE \t\t\t\t\t\t VALUE"
    print "\t---- \t\t\t\t\t\t -----"
    for tok in iter(lexer.token, None):
        print "%-25s \t\t\t\t %s" %(repr(tok.type), repr(tok.value))

if __name__ == "__main__":
    from sys import argv
    filename, inputFile = argv
    testLex(inputFile)
