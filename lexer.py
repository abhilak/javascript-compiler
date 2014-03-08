#!/usr/bin/python
import pprint
from ply import lex, yacc
from sys import argv

######################################################################################################
symbol_table = {}

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

########################################
############# DECLARATION ##############
########################################
def p_declaration_statement(p):
    '''declaration : VAR IDENTIFIER SEP_SEMICOLON'''
    symbol_table[p[2]] = { 'type' : 'UNDEFINED', 'value': None}

########################################
############# ASSIGNMENT ###############
########################################
def p_assignment_statment(p):
    '''assignment : VAR IDENTIFIER OP_ASSIGNMENT expression SEP_SEMICOLON
                  | IDENTIFIER OP_ASSIGNMENT expression SEP_SEMICOLON'''
    if p[1] == 'var':
        symbol_table[p[2]] = { 'type' : p[4]['type'], 'value' : p[4]['value']}
    else :
        symbol_table[p[1]] = { 'type' : p[3]['type'], 'value' : p[4]['value']}
    print
    pprint.pprint( symbol_table )

########################################
######## EXPRESSION STATEMENT ##########
########################################
def p_expression_statement(p):
    'expression_statement : expression SEP_SEMICOLON'
    p[0] = p[1]
    print p[0]

########################################
######## TYPEOF EXPRESSIONS ############
########################################
def p_expression_typeof(p):
    'expression : OP_TYPEOF expression'
    p[0] = { 'type' : 'STRING', 'value' : p[2]['type'] }

########################################
######## OBJECT EXPRESSIONS ############
########################################
def p_expression_object(p):
    'expression : object'
    p[0] = { 'type' : 'OBJECT', 'value': p[1]}

def p_object(p):
    '''object : SEP_OPEN_BRACE items SEP_CLOSE_BRACE
              | SEP_OPEN_BRACE SEP_CLOSE_BRACE'''
    if p[2] == '}':
        p[0] = {} 
    else :
        p[0] = p[2]

def p_items(p):
    'items : property SEP_COMMA items'
    if p[3] == None:
        p[0] = p[1]
    else :
        p[0] = dict(p[1], **p[3])

def p_items_base(p):
    'items : property'
    p[0] = p[1]

def p_property(p):
    '''property : STRING OP_COLON expression'''
    p[0] = { p[1] : p[3]['value'] }

########################################
######## ARRAY EXPRESSION ##############
########################################
def p_expression_array(p):
    'expression : array'
    p[0] = { 'type' : 'ARRAY', 'value': p[1]}

def p_array(p):
    '''array : SEP_OPEN_BRACKET list SEP_CLOSE_BRACKET
             | SEP_OPEN_BRACKET SEP_CLOSE_BRACKET'''
    if p[2] == ']':
        p[0] = []
    else :
        p[0] = p[2]

def p_list(p):
    'list : expression SEP_COMMA list'
    if p[3] == None:
        p[0] = [ p[1]['value'] ]
    else :
        p[0] = [ p[1]['value'] ] + p[3]

def p_list_base(p):
    'list : expression'''
    p[0] = [ p[1]['value'] ]

########################################
########## NUMERIC EXPRESSIONS #########
########################################
def p_expression_num(p):
    'expression : num_expression'
    p[0] = { 'type' : 'NUMBER', 'value': p[1]}

# Precedence of operators
precedence = (
        ('left', 'OP_PLUS', 'OP_MINUS'),
        ('left', 'OP_MULTIPLICATION', 'OP_DIVISION', 'OP_MODULUS'),
        ('right', 'UMINUS', 'UPLUS'),
        )

def p_num_expression_unary(p):
    '''num_expression : OP_MINUS num_expression %prec UMINUS
                      | OP_PLUS num_expression %prec UPLUS'''
    if p[1] == '-':
        p[0] = -p[2]
    else :
        p[0] = +p[2]

def p_num_expression_binop(p):
    '''num_expression : num_expression OP_PLUS num_expression
                      | num_expression OP_MINUS num_expression
                      | num_expression OP_MULTIPLICATION num_expression
                      | num_expression OP_DIVISION num_expression
                      | num_expression OP_MODULUS num_expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]
    elif p[2] == '%': p[0] = p[1] % p[3]

def p_num_expression_group(p):
    'num_expression : SEP_OPEN_PARENTHESIS num_expression SEP_CLOSE_PARENTHESIS'
    p[0] = p[2]

def p_num_expression_base(p):
    'num_expression : NUMBER'
    p[0] = p[1]

########################################
########## STRING EXPRESSIONS ##########
########################################
def p_expression_string(p):
    'expression : str_expression'
    p[0] = { 'type' : 'STRING', 'value': p[1]}

def p_str_expression_binop(p):
    '''str_expression : str_expression OP_PLUS str_expression'''
    p[0] = p[1] + p[3]

def p_str_expression_base(p):
    '''str_expression : STRING'''
    p[0] = p[1]

########################################
######## RELATIONAL EXPRESSIONS ########
########################################
def p_expression_relational(p):
    'expression : rel_expression'
    p[0] = { 'type' : 'BOOLEAN', 'value': p[1]}

def p_rel_expression_base(p):
    'rel_expression : BOOLEAN'
    p[0] = p[1]

########################################
########## SPECIAL-TYPES ###############
########################################
def p_expression_special_type(p):
    'expression : special_type'
    p[0] = p[1]

def p_special_type_undefined(p):
    'special_type : UNDEFINED'
    p[0] = { 'type' : 'UNDEFINED', 'value': None}

def p_special_type_infinity(p):
    'special_type : INFINITY'
    p[0] = { 'type' : 'INFINITY', 'value': float("inf")}

def p_data_type_null(p):
    'data_type : NULL'
    p[0] = { 'type' : 'NULL', 'value': p[1]}

def p_data_type_nan(p):
    'data_type : NAN'
    p[0] = { 'type' : 'NAN', 'value': p[1]}

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
