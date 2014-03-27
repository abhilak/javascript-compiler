#!/usr/bin/python
import pprint
from ply import lex, yacc
from sys import argv, exit
from helpers import symbol_table as ST
from helpers import debug
from helpers import features

######################################################################################################

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
                 | function_statement
                 | if_then_else
                 | if_then'''

    # Update lineNumber
    debug.incrementLineNumber()
    pprint.pprint(ST.symbol_table)

########################################
############# DECLARATION ##############
########################################
def p_declaration_statement(p):
    '''declaration : VAR IDENTIFIER SEP_SEMICOLON'''

    # Put the identifier into the symbol_table
    ST.addIdentifier(p[2])
    ST.addAttribute(p[2], 'type', 'UNDEFINED')

    debug.printStatement("DECLARATION")

########################################
############# ASSIGNMENT ###############
########################################
def p_assignment_statment(p):
    '''assignment : VAR IDENTIFIER OP_ASSIGNMENT expression SEP_SEMICOLON
                  | MARK_VAR IDENTIFIER OP_ASSIGNMENT expression SEP_SEMICOLON'''

    # Put the identifier into the symbol_table
    ST.addIdentifier(p[2])
    ST.addAttribute(p[2], 'type', p[4]['type'])
    debug.printStatement("ASSIGNMENT")

def p_mark_var(p):
    'MARK_VAR : empty'

########################################
############## FUNCTIONS ###############
########################################
def p_function_statement(p):
    '''function_statement : FUNCTION IDENTIFIER scope SEP_OPEN_PARENTHESIS argList SEP_CLOSE_PARENTHESIS block
                          | FUNCTION anonName scope SEP_OPEN_PARENTHESIS argList SEP_CLOSE_PARENTHESIS block'''

    # Add identifiers to local scope
    for identifier in p[5]:
        ST.addIdentifier(identifier)
        ST.addAttribute(identifier, 'type', 'UNDEFINED')

    # get the function name
    functionName = p[2]
    debug.printArguments(functionName , p[5])
    ST.deleteScope(functionName)

def p_arg_list(p):
    'argList : IDENTIFIER SEP_COMMA argList'
    
    # Creating the argList to be passed to the function
    if p[3] == None:
        p[0] = [ p[1] ]
    else :
        p[0] = [ p[1] ] + p[3]

def p_arg_list_base(p):
    'argList : IDENTIFIER'''
    p[0] = [ p[1] ]

def p_arg_list_empty(p):
    'argList : empty'''
    p[0] = [ ]

def p_scope(p):
    'scope : empty'

    # Create a function scope
    ST.addScope(p[-1])

def p_anon_name(p):
    'anonName : empty'

    # Create the name of the function
    p[0] = features.nameAnon()

########################################
############# IF THEN ##################
########################################
def p_if_then(p):
    'if_then : IF SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS block'

    debug.printStatement("IF THEN")

    # Type rules
    if p[3]['type'] != 'BOOLEAN':
        pass

########################################
############# IF THEN ELSE #############
########################################
def p_if_then_else(p):
    'if_then_else : IF SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS block ELSE block'

    debug.printStatement("IF THEN ELSE")

    # Type rules
    if p[3]['type'] != 'BOOLEAN':
        pass

########################################
############## EXPRESSIONS #############
########################################
# Precedence of operators
precedence = (
        ('left', 'OP_OR'),
        ('left', 'OP_AND'),
        ('left', 'OP_EQUALS', 'OP_NOT_EQUALS'),
        ('left', 'OP_LESS_THEN', 'OP_GREATER_THEN', 'OP_LESS_THEN_E', 'OP_GREATER_THEN_E'),
        ('left', 'OP_PLUS', 'OP_MINUS', 'OP_STRING_CONCAT'),
        ('left', 'OP_MULTIPLICATION', 'OP_DIVISION', 'OP_MODULUS'),
        ('right', 'UMINUS', 'UPLUS', 'OP_TYPEOF', 'OP_NOT'),
        )

def p_expression_unary(p):
    '''expression : OP_MINUS expression %prec UMINUS
                  | OP_PLUS expression %prec UPLUS
                  | OP_TYPEOF expression
                  | OP_NOT expression'''

    # Type rules
    if p[1] == '+':
        if p[2]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        elif p[2]['type'] == 'STRING':
            p[0] = { 'type' : 'STRING' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            debug.printError("Type Error")
    elif p[1] == '-':
        if p[2]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            debug.printError("Type Error")
    elif p[1] == 'typeof':
        p[0] = { 'type' : 'STRING' }

def p_expression_binop(p):
    '''expression : expression OP_PLUS expression
                  | expression OP_STRING_CONCAT expression
                  | expression OP_MINUS expression
                  | expression OP_MULTIPLICATION expression
                  | expression OP_DIVISION expression
                  | expression OP_MODULUS expression'''

    # Type rules
    if p[2] == '+':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        elif p[1]['type'] == 'STRING' and p[3]['type'] == 'STRING':
            p[0] = { 'type' : 'STRING' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            debug.printError("Type Error")
    elif p[2] == '-':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            debug.printError("Type Error")
    elif p[2] == '*':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            debug.printError("Type Error")
    elif p[2] == '/':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            debug.printError("Type Error")
    elif p[2] == '%':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            p[0] = { 'type' : 'NUMBER' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            debug.printError("Type Error")
    elif p[2] == '**':
        if p[1]['type'] == 'STRING' and p[3]['type'] == 'STRING':
            p[0] = { 'type' : 'STRING' }
        else:
            p[0] = { 'type' : 'TYPE_ERROR' }
            debug.printError("Type Error")

def p_expression_relational(p):
    '''expression : expression OP_AND expression
                  | expression OP_OR expression
                  | expression OP_GREATER_THEN expression
                  | expression OP_GREATER_THEN_E expression
                  | expression OP_LESS_THEN expression
                  | expression OP_LESS_THEN_E expression
                  | expression OP_EQUALS expression
                  | expression OP_NOT_EQUALS expression'''

    if p[0] == '===' or p[0] == '==' or p[0] == '!==' or p[0] == '!=':
        if p[1]['type'] == p[3]['type']:
            p[0] = { 'type' : 'BOOLEAN' }
        else:
            debug.printError("Type Error")
    
    # we do not support overloading as of yet
    # Type coercion if either of the expressions is a boolean
    if p[1]['type'] == 'BOOLEAN':
        p[0] = { 'type': 'BOOLEAN' }
    elif p[3]['type'] == 'BOOLEAN':
        p[0] = { 'type': 'BOOLEAN' }
    else:
        p[0] = { 'type': 'BOOLEAN' }

def p_expression_group(p):
    'expression : SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS'

    # Type rules
    p[0] = { 'type' : p[2]['type'] }

def p_expression_base_type(p):
    'expression : base_type'

    # Type rules
    p[0] = { 'type' : p[1]['type'] }

def p_expression_identifier(p):
    'expression : IDENTIFIER'

    # Type rules
    entry = ST.lookup(p[1])
    if entry != None:
        p[0] = { 'type' : entry['type']}
    else:
        debug.printError("Undefined Variable")

def p_expression_function(p):
    'expression : function_statement'

    # Type rules
    p[0] = { 'type': 'FUNCTION' }

########################################
########## BASE TYPES ##################
########################################
def p_base_type_number(p):
    'base_type : NUMBER'

    # Type rules
    p[0] = { 'type' : 'NUMBER' }

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

########################################
################ EMPTY #################
########################################
def p_empty(p):
    'empty :'

########################################
######## OBJECT EXPRESSIONS ############
########################################
# def p_expression_object(p):
#     'data_type : object'
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
#     'data_type : array'
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

########################################
############# ERROR ####################
########################################
def p_error(p):
    raise TypeError("unknown text at %r" % (p.value,))

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

# a function to test the parser
def test_yacc(input_file):
    program = open(input_file).read()
    lex.lex()
    yacc.yacc()
    yacc.parse(program)

if __name__ == "__main__":
    filename, flag, input_file = argv 

    # according to the given flag, perform operations
    if flag == '-l': 
        test_lex(input_file)
    else:
        test_yacc(input_file)
