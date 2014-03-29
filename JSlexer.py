#!/usr/bin/python
from ply import lex

########################################
############# TOKENS ###################
########################################
tokens = [
        "COMMENT",
        "STRING",
        "BOOLEAN",
        "NULL",
        "NAN",
        "UNDEFINED",
        "INFINITY",
        "NUMBER",
        "VAR", 
        "IF", 
        "ELSE", 
        "WHILE", 
        "FOR", 
        "IN", 
        "BREAK", 
        "CONTINUE", 
        "FUNCTION", 
        "RETURN", 
        "THROW", 
        "TRY", 
        "CATCH", 
        "FINALLY", 
        "IDENTIFIER",
        "OP_TYPEOF", 
        "OP_ASSIGNMENT",
        "OP_STRING_CONCAT",
        "OP_COLON",
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
        "WHITESPACE"
        ]

########################################
############# COMMENTS #################
########################################
def t_COMMENT(t):
    r"//[^\n]+|" r"/\*[^(\*/)]+(\*/)"

########################################
############# TYPES ####################
########################################
def t_BOOLEAN(t):
    r"true|false"
    return t

def t_UNDEFINED(t): 
    r"undefined"
    return t

def t_INFINITY(t): 
    r"inf"
    return t

def t_NULL(t): 
    r"null"
    return t

def t_NAN(t): 
    r"NAN"
    return t

def t_STRING(t): 
    r"(?P<start>\"|')[^\"']*(?P=start)"
    t.value = t.value.replace("\"", "").replace("'", "")
    return t

def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

########################################
############# CONSTRUCTS ###############
########################################
def t_VAR(t): 
    r"var"
    return t

def t_IF(t):
    r"if"
    return t

def t_ELSE(t):
    r"else"
    return t

def t_WHILE(t):
    r"while"
    return t

def t_FOR(t):
    r"for"
    return t

def t_IN(t):
    r"in"
    return t

def t_DO(t):
    r"do"
    return t

def t_BREAK(t):
    r"BREAK"
    return t

def t_CONTINUE(t):
    r"CONTINUE"
    return t

def t_FUNCTION(t):
    r"function"
    return t

def t_RETURN(t):
    r"return"
    return t

def t_THROW(t):
    r"throw"
    return t

def t_TRY(t):
    r"try"
    return t

def t_CATCH(t):
    r"catch"
    return t

def t_FINALLY(t):
    r"finally"
    return t

########################################
############# OPERATORS ################
########################################
def t_OP_TYPEOF(t):
    r"typeof"
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

def t_OP_STRING_CONCAT(t):
    r"\*\*"
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
############# WHITESPACE ###############
########################################
def t_WHITESPACE(t): 
    r"\s"

########################################
############# ERROR ####################
########################################
def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

######################################################################################################
# A function to test the lexer
def test_lex(input_file):
    # Open the passed argument as an input file and then pass it to lex
    lexer = lex.lex()
    program = open(input_file).read()
    lexer.input(program)

    # This iterates over the function lex.token and converts the returned object into an iterator
    print "\tTYPE \t\t\t\t\t\t VALUE"
    print "\t---- \t\t\t\t\t\t -----"
    for tok in iter(lexer.token, None):
        print "%-25s \t\t\t\t %s" %(repr(tok.type), repr(tok.value))

if __name__ == "__main__":
    filename, input_file = argv 

    test_lex(input_file)
