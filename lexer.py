#!/usr/bin/python
import pprint
from ply import lex, yacc
from sys import argv

######################################################################################################
symbol_table = {}
line_number = 1

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
        "DO", 
        "SWITCH", 
        "CASE", 
        "BREAK", 
        "CONTINUE", 
        "FUNCTION", 
        "RETURN", 
        "THROW", 
        "TRY", 
        "CATCH", 
        "FINALLY", 
        "IDENTIFIER",
        "OP_INSTANCEOF", 
        "OP_TYPEOF", 
        "OP_ASSIGNMENT",
        "OP_COLON",
        "OP_EQUALS",
        "OP_NOT_EQUALS",
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
    r"\d+(\.\d+)?"
    t.value = float(t.value)
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

def t_SWITCH(t):
    r"switch"
    return t

def t_CASE(t):
    r"case"
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

# typeof is an operator but needs to be defined before
# identifiers
def t_OP_TYPEOF(t):
    r"typeof"
    return t

########################################
############# IDENTIFIER ###############
########################################
def t_IDENTIFIER(t):
    r"[a-zA-Z$_][\w$]*"
    return t

########################################
############# OPERATORS ################
########################################
def t_OP_ASSIGNMENT(t):
    r"=|"r"\+=|"r"-=|"r"\*=|"r"/=|"r"%="
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

def t_OP_EQUALS(t):
    r"==|"r"==="
    return t

def t_OP_NOT_EQUALS(t):
    r"!=|"r"!=="
    return t

def t_OP_GREATER_THEN(t):
    r">"
    return t

def t_OP_GREATER_THEN_E(t):
    r">="
    return t

def t_OP_LESS_THEN(t):
    r"<"
    return t

def t_OP_LESS_THEN_E(t):
    r"<="
    return t

def t_OP_AND(t):
    r"&&"
    return t

def t_OP_OR(t):
    r"\|\|"
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
    program = open(input_file).read()
    lex.input(program)

    # This iterates over the function lex.token and converts the returned object into an iterator
    print "\tTYPE \t\t\t\t\t\t VALUE"
    print "\t---- \t\t\t\t\t\t -----"
    for tok in iter(lex.token, None):
        print "%-25s \t\t\t\t %s" %(repr(tok.type), repr(tok.value))

######################################################################################################

########################################
############# STATEMENTS ###############
########################################
def p_start(p):
    '''start : block
             | statements'''

def p_block(p): 
    '''block : SEP_OPEN_BRACE statements SEP_CLOSE_BRACE'''

def p_statments(p):
    '''statements : statement statements
                  | statement'''

def p_statment(p):
    '''statement : assignment
                 | declaration
                 | expression_statement'''

    # Update line_number
    global line_number
    line_number += 1 

########################################
############# DECLARATION ##############
########################################
def p_declaration_statement(p):
    '''declaration : VAR IDENTIFIER SEP_SEMICOLON'''

########################################
############# ASSIGNMENT ###############
########################################
def p_assignment_statment(p):
    '''assignment : VAR IDENTIFIER OP_ASSIGNMENT expression SEP_SEMICOLON
                  | IDENTIFIER OP_ASSIGNMENT expression SEP_SEMICOLON'''

########################################
######## EXPRESSION STATEMENT ##########
########################################
def p_expression_statement(p):
    'expression_statement : expression SEP_SEMICOLON'

    # Type rules
    p[0] = { 'type' : p[1]['type'] }

########################################
########## NUMERIC EXPRESSIONS #########
########################################
# Precedence of operators
precedence = (
        ('left', 'OP_PLUS', 'OP_MINUS'),
        ('left', 'OP_MULTIPLICATION', 'OP_DIVISION', 'OP_MODULUS'),
        ('right', 'UMINUS', 'UPLUS', 'OP_TYPEOF'),
        )

def p_expression_unary(p):
    '''expression : OP_MINUS expression %prec UMINUS
                  | OP_PLUS expression %prec UPLUS
                  | OP_TYPEOF expression'''

    global line_number

    # Type rules
    if p[1] == '+':
        if p[2]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        elif p[2]['type'] == 'STRING':
            p[0] = { 'type' : 'STRING' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            print "line ", line_number, ": Type Error"
    elif p[1] == '-':
        if p[2]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            print "line", line_number, ": Type Error"
    elif p[1] == 'typeof':
        p[0] = { 'type' : 'STRING' }

def p_expression_binop(p):
    '''expression : expression OP_PLUS expression
                  | expression OP_MINUS expression
                  | expression OP_MULTIPLICATION expression
                  | expression OP_DIVISION expression
                  | expression OP_MODULUS expression'''

    global line_number

    # Type rules
    if p[2] == '+':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        elif p[1]['type'] == 'STRING' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'STRING' }
        elif p[3]['type'] == 'STRING' and p[1]['type'] == 'NUMBER':
            p[0] = { 'type' : 'STRING' }
        elif p[1]['type'] == 'STRING' and p[3]['type'] == 'STRING':
            p[0] = { 'type' : 'STRING' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            print "line", line_number, ": Type Error"
    elif p[2] == '-':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            print "line", line_number, ": Type Error"
    elif p[2] == '*':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            print "line", line_number, ": Type Error"
    elif p[2] == '/':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            print "line", line_number, ": Type Error"
    elif p[2] == '%':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            print "line ", line_number, ": Type Error"

def p_expression_group(p):
    'expression : SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS'

    # Type rules
    p[0] = { 'type' : p[2]['type'] }

def p_expression_base_type(p):
    'expression : base_type'

    # Type rules
    p[0] = { 'type' : p[1]['type'] }

########################################
########## BASE TYPES ##################
########################################
def p_base_type_number(p):
    'base_type : NUMBER'

    # Type rules
    p[0] = { 'type' : 'NUMBER' }

def p_base_type_inf(p):
    'base_type : INFINITY'
    p[0] = { 'type' : 'NUMBER'}

def p_base_type_boolean(p):
    'base_type : BOOLEAN'

    # Type rules
    p[0] = { 'type' : 'BOOLEAN' }

def p_base_type_string(p):
    'base_type : STRING'

    # Type rules
    p[0] = { 'type' : 'STRING' }

def p_base_type_undefine(p):
    'base_type : UNDEFINED'

    # Type rules
    p[0] = { 'type' : 'UNDEFINED'}

def p_base_type_null(p):
    'base_type : NULL'

    # Type rules
    p[0] = { 'type' : 'NULL'}

def p_base_type_nan(p):
    'base_type : NAN'

    # Type rules
    p[0] = { 'type' : 'NAN'}

# ########################################
# ######## OBJECT EXPRESSIONS ############
# ########################################
# def p_expression_object(p):
#     'expression : object'
#     p[0] = { 'type' : 'OBJECT', 'value': p[1]}
#
# def p_object(p):
#     '''object : SEP_OPEN_BRACE items SEP_CLOSE_BRACE
#               | SEP_OPEN_BRACE SEP_CLOSE_BRACE'''
#     if p[2] == '}':
#         p[0] = {} 
#     else :
#         p[0] = p[2]
#
# def p_items(p):
#     'items : property SEP_COMMA items'
#     if p[3] == None:
#         p[0] = p[1]
#     else :
#         p[0] = dict(p[1], **p[3])
#
# def p_items_base(p):
#     'items : property'
#     p[0] = p[1]
#
# def p_property(p):
#     '''property : STRING OP_COLON expression'''
#     p[0] = { p[1] : p[3]['value'] }
#

# ########################################
# ######## ARRAY EXPRESSION ##############
# ########################################
# def p_expression_array(p):
#     'expression : array'
#     p[0] = { 'type' : 'ARRAY', 'value': p[1]}
#
# def p_array(p):
#     '''array : SEP_OPEN_BRACKET list SEP_CLOSE_BRACKET
#              | SEP_OPEN_BRACKET SEP_CLOSE_BRACKET'''
#     if p[2] == ']':
#         p[0] = []
#     else :
#         p[0] = p[2]
#
# def p_list(p):
#     'list : expression SEP_COMMA list'
#     if p[3] == None:
#         p[0] = [ p[1]['value'] ]
#     else :
#         p[0] = [ p[1]['value'] ] + p[3]
#
# def p_list_base(p):
#     'list : expression'''
#     p[0] = [ p[1]['value'] ]
#
########################################
############# ERROR ####################
########################################
def p_error(p):
    raise TypeError("unknown text at %r" % (p.value,))

######################################################################################################
if __name__ == "__main__":
    # Here the lexer is initialized so that it can be used in another file
    lex.lex()

    filename, flag, input_file = argv 
    program = open(input_file).read()

    if flag == '-l': 
        test_lex(input_file)
    else:
        yacc.yacc()
        yacc.parse(program)
