#!/usr/bin/python
import pprint
from ply import yacc
from sys import argv, exit
from helpers import symbol_table as ST
from helpers import debug
from helpers import features
from JSlexer import tokens, lexer
from helpers import threeAddrCode as TAC

########################################
############# STATEMENTS ###############
########################################
def p_start(p):
    '''start : block
             | statements'''

def p_block(p): 
    'block : SEP_OPEN_BRACE statements SEP_CLOSE_BRACE'

def p_statments(p):
    '''statements : statement statements
                  | statement'''
def p_statment(p):
    '''statement : assignment
                 | declaration
                 | function_statement
                 | return_statement
                 | if_then_else
                 | if_then'''

    # print line number
    ST.printSymbolTable()

# Marker to mark the nextQuad value
def p_mark_quad():
    'M_quad : empty'

    p[0] = { 'quad' : TAC.nextQuad }

########################################
############# DECLARATION ##############
########################################
def p_declaration_statement(p):
    'declaration : VAR IDENTIFIER SEP_SEMICOLON'

    # Put the identifier into the symbol_table
    ST.addIdentifier(p[2], 'UNDEFINED')

    # print the name of the statement
    debug.printStatement("DECLARATION of %s" %p[2])

    # Type rules
    p[0] = { 'type' : 'VOID' }

########################################
############# ASSIGNMENT ###############
########################################
def p_assignment_statment(p):
    '''assignment : VAR IDENTIFIER OP_ASSIGNMENT expression SEP_SEMICOLON
                  | M_VAR IDENTIFIER OP_ASSIGNMENT expression SEP_SEMICOLON'''

    # In case the var is not present
    statmentType = 'VOID'

    # To store information
    p[0] = {}

    if p[0] == None :
        identifierEntry = ST.lookup(p[2])
        if identifierEntry == None:
            statmentType = 'REFERENCE_ERROR'
            debug.printStatement('line %d: Undefined Variable "%s"' %(p.lineno(2), p[2]))
            # raise SyntaxError
        else:
            # Put the identifier into the symbol_table
            ST.addIdentifier(p[2], p[4]['type'])
            statmentType = p[4]['type']

            # Emit code
            p[1]['place'] = p[4]['place']
            ST.addAttribute('place', p[4]['place'])

    # print the name of the statement
    debug.printStatement("ASSIGNMENT of %s" %p[2])

    # Type rules
    p[0]['type'] =  statmentType

def p_mark_var(p):
    'M_VAR : empty'

    p[0] = None

########################################
############## FUNCTIONS ###############
########################################
def p_function_statement(p):
    '''function_statement : FUNCTION IDENTIFIER M_scope SEP_OPEN_PARENTHESIS argList SEP_CLOSE_PARENTHESIS M_insertArgs block
                          | FUNCTION M_anonName M_scope SEP_OPEN_PARENTHESIS argList SEP_CLOSE_PARENTHESIS M_insertArgs block'''

    # print the name of the statement
    functionName = p[2]
    debug.printStatement('Arguments of "%s" are: %s' %(functionName, p[5]))
    ST.deleteScope(functionName)

    # Type rules
    p[0] = { 'type' : 'FUNCTION' }

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
    'M_scope : empty'

    # Create a function scope
    ST.addScope(p[-1])

    ST.printSymbolTable()

def p_anon_name(p):
    'M_anonName : empty'

    # Create the name of the function
    p[0] = features.nameAnon()

def p_insert_args(p):
    'M_insertArgs : empty'

    # Add identifiers to local scope
    for argument in p[-2]:
        ST.addIdentifier(argument, 'UNDEFINED')

########################################
######## RETURN STATEMENT ##############
########################################
def p_return_statement(p):
    'return_statement : RETURN expression'

    # Type rules
    p[0] = { 'type' : p[2]['type'] }

########################################
######## FUNCTIONS CALLS ###############
########################################

########################################
######## BREAK STATEMENT ###############
########################################
def p_break_statement(p):
    'break_statement : BREAK'

    # Type rules
    p[0] = { 'type' : 'VOID' }

########################################
######## CONTINUE STATEMENT ############
########################################
def p_continue_statement(p):
    'continue_statement : CONTINUE'

    # Type rules
    p[0] = { 'type' : 'VOID' }

########################################
############# IF THEN ##################
########################################
def p_if_then(p):
    'if_then : IF SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS block'

    debug.printStatement("IF THEN")

    # Type rules
    errorFlag = 0
    statmentType = 'VOID'
    if p[3]['type'] != 'BOOLEAN':
        errorFlag = 1
        statmentType = 'TYPE_ERROR'
    p[0] = { 'type' : statmentType }

########################################
############# IF THEN ELSE #############
########################################
def p_if_then_else(p):
    'if_then_else : IF SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS block ELSE block'

    debug.printStatement("IF THEN ELSE")

    # Type rules
    errorFlag = 0
    statmentType = 'VOID'
    if p[3]['type'] != 'BOOLEAN':
        errorFlag = 1
        statmentType = 'TYPE_ERROR'
    p[0] = { 'type' : statmentType }

########################################
########## WHILE STATEMENT #############
########################################

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
    expType = 'UNDEFINED'
    errorFlag = 0

    # Emit code
    p[0] = {}
    p[0]['place'] = TAC.newTemp()

    # Conditional branch to figure out what code to emit and check types
    if p[1] == '+':
        if p[2]['type'] == 'NUMBER':
            expType = 'NUMBER'
            p[0]['place'] = p[2]['place']
        elif p[2]['type'] == 'STRING':
            expType = 'STRING'
            TAC.emit(p[0]['place'], p[2]['place'] , '' , 'str+')
        else:
            errorFlag = 1
    elif p[1] == '-':
        if p[2]['type'] == 'NUMBER':
            expType = 'NUMBER'
            TAC.emit(p[0]['place'], p[2]['place'] , '' , 'uni-')
        else:
            errorFlag = 1
    elif p[1] == 'typeof':
        expType = 'STRING'
        TAC.emit(p[0]['place'], p[2]['type'] , '' , '=')

    # In case of type errors
    if errorFlag:
        expType = 'TYPE_ERROR'
        # raise TypeError

    # Return type of the statment
    p[0]['type'] = expType

def p_expression_binop(p):
    '''expression : expression OP_PLUS expression
                  | expression OP_STRING_CONCAT expression
                  | expression OP_MINUS expression
                  | expression OP_MULTIPLICATION expression
                  | expression OP_DIVISION expression
                  | expression OP_MODULUS expression'''

    # Type rules
    expType = 'UNDEFINED'
    errorFlag = 0

    # To store information
    p[0] = {}
    p[0]['place'] = TAC.newTemp()

    # To emit codes
    if p[2] == '+' or p[2] == '-' or p[2] == '*' or p[2] == '/' or p[2] == '%':
        if p[1]['type'] == 'NUMBER' and p[3]['type'] == 'NUMBER':
            expType = 'NUMBER'
            TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
        else:
            errorFlag = 1
    else :
        if p[1]['type'] == 'STRING' and p[3]['type'] == 'STRING':
            expType = 'STRING'
            TAC.emit(p[0]['place'], p[1]['place'], p[3]['place'], p[2])
        else:
            errorFlag = 1

    # Type Error
    if errorFlag:
        expType = 'TYPE_ERROR'
        debug.printStatement('%s Type Error' %p.lineno(1))
        # raise TypeError

    p[0]['type'] = expType

def p_expression_relational(p):
    '''expression : expression OP_GREATER_THEN expression
                  | expression OP_GREATER_THEN_E expression
                  | expression OP_LESS_THEN expression
                  | expression OP_LESS_THEN_E expression
                  | expression OP_EQUALS expression
                  | expression OP_NOT_EQUALS expression'''

    # Type rules
    expType = 'UNDEFINED'
    errorFlag = 0

    if p[1]['type'] == p[3]['type']:
        expType = 'BOOLEAN'
    else:
        expType = 'TYPE_ERROR'
        debug.printStatement('%d Type Error' %p.lineno(1))
        # raise TypeError
    
    p[0] = { 'type' : expType }

    #-----------------------------------------------------------
    # Type coercion if either of the expressions is a boolean
    #-----------------------------------------------------------

def p_expression_logical_and(p):
    'expression : expression OP_AND expression'

    # Type rules
    expType = 'BOOLEAN'
    p[0] = { 'type' : expType }

def p_expression_logical_and(p):
    'expression : expression OP_OR expression'

    # Type rules
    expType = 'BOOLEAN'
    p[0] = { 'type' : expType }

def p_expression_group(p):
    'expression : SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS'

    # Type rules
    p[0] = { 'type' : p[2]['type'] }

    # emit code
    p[0]['place'] = p[2]['place']

def p_expression_base_type(p):
    'expression : base_type'

    # Type rules
    p[0] = { 'type' : p[1]['type'] }

    # emit code
    p[0]['place'] = TAC.newTemp()
    TAC.emit(p[0]['place'], p[1]['value'], '', '=')

def p_expression_identifier(p):
    'expression : IDENTIFIER'

    # Type rules
    p[0] = {}
    entry = ST.lookup(p[1])
    if entry != None:
        p[0] = { 'type' : entry['type']}
    else:
        debug.printStatement('%d Undefined Variable %s' %(p.lineno(1), p[1]))

    # Emit code
    p[0]['place'] = p[1]['place']

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
    p[0] = { 'type' : 'NUMBER', 'value' : int(p[1]) }

def p_base_type_boolean(p):
    'base_type : BOOLEAN'

    # Type rules
    p[0] = { 'type' : 'BOOLEAN' , 'value' : bool(p[1]) }

def p_base_type_string(p):
    'base_type : STRING'

    # Type rules
    p[0] = { 'type' : 'STRING' , 'value' : p[1] }

def p_base_type_undefine(p):
    'base_type : UNDEFINED'

    # Type rules
    p[0] = { 'type' : 'UNDEFINED', 'value' : 'UNDEFINED'}

########################################
######## ARRAY EXPRESSION ##############
########################################
def p_expression_array(p):
    'base_type : array'
    p[0] = { 'type' : 'ARRAY' }

def p_array(p):
    'array : SEP_OPEN_BRACKET list SEP_CLOSE_BRACKET'

def p_list(p):
    'list : expression SEP_COMMA list'

def p_list_base(p):
    'list : expression'''

def p_list_empty(p):
    'list : empty'''

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

########################################
############# ERROR ####################
########################################
def p_error(p):
    print "Whoa. You are seriously hosed."
    # Read ahead looking for a closing '}'
    while 1:
        tok = yacc.token()             # Get the next token
        if not tok or tok.type == 'SEP_SEMICOLON': 
            break
    # yacc.restart() 
    yacc.errok()

######################################################################################################
# a function to test the parser
def test_yacc(input_file):
    program = open(input_file).read()
    parser = yacc.yacc()
    parser.parse(program, lexer=lexer)
    # parser.parse(program, lexer=lexer, debug=1)

if __name__ == "__main__":
    filename, input_file = argv 

    test_yacc(input_file)
