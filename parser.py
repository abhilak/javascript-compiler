#!/usr/bin/python
import pprint
from ply import yacc
from sys import argv, exit
from helpers import symbol_table as SymbolTable
from helpers import debug
from JSlexer import tokens, lexer
from helpers import threeAddrCode as ThreeAddressCode

# Singletons of the helper classes
ST = SymbolTable.SymbolTable()
TAC = ThreeAddressCode.ThreeAddressCode(ST)

########################################
############# STATEMENTS ###############
########################################
def p_start(p):
    '''start : block
             | statements'''

    # Any remaining breaks and continues need to be purged
    TAC.noop(p[1]['loopEndList'])
    TAC.noop(p[1]['loopBeginList'])

    # Here we have to have statements so that we can return back to the calling function
    TAC.emit('', '' , -1, 'EXIT')

    # Resolve all functions that are waiting
    TAC.resolveWaitingFunctions()
    
    # Emit code
    p[0] = {}

    # print line number
    TAC.printSymbolTable()

    # print the code
    TAC.printCode()

def p_block(p): 
    'block : SEP_OPEN_BRACE statements SEP_CLOSE_BRACE'

    # Emit code
    p[0] = {}
    p[0]['nextList'] = []

    # For break statement
    p[0]['loopEndList'] = p[2]['loopEndList']
    p[0]['loopBeginList'] = p[2]['loopBeginList']

def p_statments(p):
    '''statements : statement statements
                  | statement M_statements'''

    # For statements waiting till the loop end
    p[0] = {}

    # For break statement
    p[0]['loopEndList'] = TAC.merge(p[1]['loopEndList'], p[2]['loopEndList'])
    p[0]['loopBeginList'] = TAC.merge(p[1]['loopBeginList'], p[2]['loopBeginList'])

def p_statment(p):
    '''statement : assignment M_quad
                 | declaration M_quad
                 | if_then M_quad
                 | if_then_else M_quad
                 | while_statement M_quad
                 | break_statement M_quad
                 | continue_statement M_quad
                 | return_statement M_quad
                 | function_statement M_quad
                 | function_call M_quad'''

    # Emit code
    p[0] = {}
    p[0]['nextList'] = []

    # Backpatch statements here
    TAC.backPatch(p[1]['nextList'], p[2]['quad'])

    # For break statement
    p[0]['loopEndList'] = p[1]['loopEndList']
    p[0]['loopBeginList'] = p[1]['loopBeginList']

# Marker to mark the nextQuad value
def p_mark_quad(p):
    'M_quad : empty'

    p[0] = { 'quad' : TAC.getNextQuad()}

# Marker for blanck statements
def p_mark_statements(p):
    'M_statements : empty'

    # emit code
    p[0] = { 'nextList' : [] }
    p[0]['loopEndList'] = []
    p[0]['loopBeginList'] = []

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

    # Emit code
    p[0]['nextList'] = []
    p[0]['loopEndList'] = []
    p[0]['loopBeginList'] = []

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

    identifierEntry = ST.exists(p[2])
    if identifierEntry == False:
        # Put the identifier into the symbol_table
        ST.addIdentifier(p[2], p[4]['type'])
        statmentType = p[4]['type']

        # In case of an assignment, this is a function reference, so we store the name of the function
        if p[4]['type'] == 'FUNCTION':
            ST.addAttribute(p[2], 'reference', p[4]['name'])
            ST.addToFunctionList(p[2])

        # Emit code
        ST.addAttribute(p[2], 'place', p[4]['place'])

        # If they are booleans then noop their lists as this is not a relational expression
        if statmentType == 'BOOLEAN':
            TAC.noop(p[4]['trueList'])
            TAC.noop(p[4]['falseList'])
    else:
        statmentType = 'REFERENCE_ERROR'
        debug.printError('line %d: Redefined Variable "%s"' %(p.lineno(2), p[2]))
        # raise SyntaxError

    # print the name of the statement
    debug.printStatement("ASSIGNMENT of %s" %p[2])

    # Type rules
    p[0]['type'] =  statmentType

    # Emit code
    p[0]['nextList'] = []
    p[0]['loopEndList'] = []
    p[0]['loopBeginList'] = []

def p_mark_var(p):
    'M_VAR : empty'

    p[0] = None

########################################
############## FUNCTIONS ###############
########################################
def p_function_statement(p):
    '''function_statement : FUNCTION IDENTIFIER M_scope SEP_OPEN_PARENTHESIS argList SEP_CLOSE_PARENTHESIS M_insertArgs block
                          | FUNCTION M_anonName M_scope SEP_OPEN_PARENTHESIS argList SEP_CLOSE_PARENTHESIS M_insertArgs block'''

    # Any remaining breaks and continues need to be purged
    TAC.noop(p[8]['loopEndList'])
    TAC.noop(p[8]['loopBeginList'])

    # Here we have to have statements so that we can return back to the calling function
    TAC.emit('', '' , -1, 'RETURN')

    # Resolve all functions that are waiting
    TAC.resolveWaitingFunctions()
    
    # print the name of the statement
    functionName = p[3]['name'] 
    debug.printStatement('Arguments of "%s" are: %s' %(functionName, p[5]))
    ST.deleteScope(functionName)

    # Update the code Length of the given function
    ST.addAttribute(functionName, 'codeLength', TAC.getCodeLength(functionName))

    # Type rules
    p[0] = { 'type' : 'FUNCTION', 'name': functionName }

    # Emit code
    p[0]['nextList'] = []
    p[0]['loopEndList'] = []
    p[0]['loopBeginList'] = []

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

    p[0] = {}

    # Add this function to the functionList of its parent
    ST.addToFunctionList(p[-1])

    # Name the function
    p[0]['name'] = ST.nameAnon()

    # Now add the identifier as a function reference
    if p[-1] != None:
        ST.addIdentifier(p[-1], 'FUNCTION')
        ST.addAttribute(p[-1], 'reference', p[0]['name'])

    # We store the identifier as a function reference
    # Create a function scope
    ST.addScope(p[0]['name'])
    TAC.createFunctionCode(p[0]['name'])
    
def p_anon_name(p):
    'M_anonName : empty'

    p[0] = None

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

    # Assign a returnType to the function
    ST.addAttribute(ST.getCurrentScope(), 'returnType', p[2]['type'])

    # Emit code
    p[0]['nextList'] = []
    p[0]['loopEndList'] = []
    p[0]['loopBeginList'] = []

########################################
######## FUNCTIONS CALLS ###############
########################################
def p_function_call(p):
    'function_call : IDENTIFIER SEP_OPEN_PARENTHESIS actualParameters SEP_CLOSE_PARENTHESIS SEP_SEMICOLON'

    p[0] = {}

    # Semantic actions
    # If the identifier does not exist then we output error
    if not ST.exists(p[1]):
        ST.addToWaitingList(p[1], TAC.getNextQuad())
        TAC.emit('', '', -1, 'JUMP')
    else:
        # We check whether the identifier is a function or a reference
        if ST.getAttribute(p[1], 'type') == 'FUNCTION':
            referenceName = ST.getAttribute(p[1], 'reference')
            if referenceName != None:
                TAC.emit('', '', referenceName, 'JUMP')
            else:
                TAC.emit('', '', p[1], 'JUMP')
        else:
            p[0]['type'] = 'REFERENCE_ERROR'
            debug.printError('line %d: Not a function "%s"' %(p.lineno(2), p[1]))
            # raise SyntaxError

    # Emit code
    p[0]['nextList'] = []
    p[0]['loopEndList'] = []
    p[0]['loopBeginList'] = []

def p_parameters(p):
    'actualParameters : expression SEP_COMMA actualParameters'

    # Emit code
    TAC.emit(p[1]['place'], '', '', 'PARAM')

def p_parameters_base(p):
    'actualParameters : expression'

    # Emit code
    TAC.emit(p[1]['place'], '', '', 'PARAM')

    p[0] = {}

def p_parameters_empty(p):
    'actualParameters : empty'

    p[0] = {}

########################################
######## BREAK STATEMENT ###############
########################################
def p_break_statement(p):
    'break_statement : BREAK SEP_SEMICOLON'

    debug.printStatement('BREAK')

    # Type rules
    p[0] = { 'type' : 'VOID' }

    # Emit code
    p[0]['nextList'] = []
    p[0]['loopBeginList'] = []
    p[0]['loopEndList'] = [TAC.getNextQuad()]
    TAC.emit('', '', -1, 'GOTO')

########################################
######## CONTINUE STATEMENT ############
########################################
def p_continue_statement(p):
    'continue_statement : CONTINUE SEP_SEMICOLON'

    debug.printStatement('CONTINUE')

    # Type rules
    p[0] = { 'type' : 'VOID' }

    # Emit code
    p[0]['nextList'] = []
    p[0]['loopEndList'] = []
    p[0]['loopBeginList'] = [TAC.getNextQuad()]
    TAC.emit('', '', -1, 'GOTO')

########################################
############# IF THEN ##################
########################################
def p_if_then(p):
    'if_then : IF SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS M_quad block'

    debug.printStatement("IF THEN")

    # Type rules
    errorFlag = 0
    statmentType = 'VOID'
    if p[3]['type'] != 'BOOLEAN':
        errorFlag = 1
        statmentType = 'TYPE_ERROR'
    p[0] = { 'type' : statmentType }

    # Emit code
    # Backpatch the truelist of the expression
    TAC.backPatch(p[3]['trueList'] , p[5]['quad'])
    p[0]['nextList'] = TAC.merge(p[3]['falseList'], p[6]['nextList'])

    # For break statement
    p[0]['loopEndList'] = p[6]['loopEndList']
    p[0]['loopBeginList'] = p[6]['loopBeginList']

########################################
############# IF THEN ELSE #############
########################################
def p_if_then_else(p):
    'if_then_else : IF SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS M_quad block ELSE M_quad block'

    debug.printStatement("IF THEN ELSE")

    # Type rules
    errorFlag = 0
    statmentType = 'VOID'
    if p[3]['type'] != 'BOOLEAN':
        errorFlag = 1
        statmentType = 'TYPE_ERROR'
    p[0] = { 'type' : statmentType }

    # Emit code
    # Backpatch the truelist of the expression and the falselist as well
    TAC.backPatch(p[3]['trueList'] , p[5]['quad'])
    TAC.backPatch(p[3]['falseList'], p[8]['quad'])
    p[0]['nextList'] = TAC.merge(p[6]['nextList'], p[9]['nextList'])

    # For break statement
    p[0]['loopEndList'] = p[9]['loopEndList']
    p[0]['loopBeginList'] = p[9]['loopBeginList']

########################################
########## WHILE STATEMENT #############
########################################
def p_while(p):
    'while_statement : WHILE M_quad SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS M_quad block'

    debug.printStatement('WHILE')

    # Type rules
    errorFlag = 0
    statmentType = 'VOID'

    # Emit code
    p[0] = {}
    p[0]['nextList'] = []

    # Backpatch
    if p[4]['type'] == 'BOOLEAN':
        # Backpatch continue statements and break statements
        TAC.backPatch(p[7]['loopBeginList'], p[2]['quad'])
        p[0]['nextList'] = p[7]['loopEndList']

        # Backpatch other statements
        TAC.backPatch(p[4]['trueList'] , p[6]['quad'])
        p[0]['nextList'] = TAC.merge(p[4]['falseList'], p[0]['nextList'])
        p[0]['nextList'] = TAC.merge(p[7]['nextList'], p[0]['nextList'])
    else:
        errorFlag = 1
        statmentType = 'TYPE_ERROR'

    p[0]['type'] = statmentType
    p[0]['loopEndList'] = []
    p[0]['loopBeginList'] = []

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
        ('right', 'UMINUS', 'OP_TYPEOF', 'OP_NOT'),
        )

######## UNARY EXPRESSIONS ############

def p_expression_unary(p):
    '''expression : OP_MINUS expression %prec UMINUS
                  | OP_TYPEOF expression'''

    # Type rules
    expType = 'UNDEFINED'
    errorFlag = 0

    # Emit code
    p[0] = {}
    p[0]['place'] = TAC.newTemp()

    # Conditional branch to figure out what code to emit and check types
    if p[1] == '-':
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
        debug.printError('line %d: Type Error' %p.lineno(2))
        # raise TypeError

    # Return type of the statment
    p[0]['type'] = expType

######## BINARY EXPRESSIONS ############

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
        debug.printError('line %d: Type Error' %p.lineno(1))
        # raise TypeError

    p[0]['type'] = expType

######## RELATIONAL EXPRESSION ############

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
        debug.printError('line %d: Type Error' %p.lineno(1))
        # raise TypeError
    
    p[0] = { 'type' : expType }

    # Backpatching code
    p[0]['trueList'] = [TAC.getNextQuad()]
    p[0]['falseList'] = [TAC.getNextQuad() + 1]

    # Emit code
    TAC.emit(p[1]['place'] + p[2] + p[3]['place'], 'GOTO', -1, 'COND_GOTO')
    TAC.emit('', '', -1, 'GOTO')

######## LOGICAL EXPRESSION ##############

def p_expression_logical_and(p):
    'expression : expression OP_AND M_quad expression'

    # Type rules
    expType = 'BOOLEAN'

    # Backpatching code
    p[0] = {}
    p[0]['trueList'] = []
    p[0]['falseList'] = []

    if p[1]['type'] == p[4]['type'] == 'BOOLEAN':
        expType = 'BOOLEAN'

        # Emit code
        TAC.backPatch(p[1]['trueList'], p[3]['quad'])
        p[0]['falseList'] = TAC.merge(p[1]['falseList'], p[4]['falseList'])
        p[0]['trueList'] = p[4]['trueList']
    else:
        expType = 'TYPE_ERROR'
        debug.printStatement('line %d: Type Erro' %p.lineno(1))

    # Type of the expression
    p[0]['type'] = expType

def p_expression_logical_or(p):
    'expression : expression OP_OR M_quad expression'

    # Type rules
    expType = 'UNDEFINED'

    # Backpatching code
    p[0] = {}
    p[0]['trueList'] = []
    p[0]['falseList'] = []

    if p[1]['type'] == p[4]['type'] == 'BOOLEAN':
        expType = 'BOOLEAN'

        # Emit code
        TAC.backPatch(p[1]['falseList'], p[3]['quad'])
        p[0]['trueList'] = TAC.merge(p[1]['trueList'], p[4]['trueList'])
        p[0]['falseList'] = p[4]['falseList']
    else:
        expType = 'TYPE_ERROR'
        debug.printStatement('line %d: Type Erro' %p.lineno(1))

    # Type of the expression
    p[0]['type'] = expType

def p_expression_logical_not(p):
    'expression : OP_NOT expression'

    # Type rules
    expType = 'BOOLEAN'

    # Backpatching code
    p[0] = {}
    p[0]['trueList'] = []
    p[0]['falseList'] = []

    if p[2]['type'] != 'BOOLEAN':
        expType = 'TYPE_ERROR'
        debug.printStatement('line %d: Type Erro' %p.lineno(1))
    else:
        p[0]['trueList'] = p[2]['falseList']
        p[0]['falseList'] = p[2]['trueList']

    # Type of the expression
    p[0]['type'] = expType

######## GROUP EXPRESSION ##############

def p_expression_group(p):
    'expression : SEP_OPEN_PARENTHESIS expression SEP_CLOSE_PARENTHESIS'

    # Type rules
    p[0] = { 'type' : p[2]['type'] }

    # emit code
    p[0]['place'] = p[2]['place']

    # Backpatching code
    if p[1]['type'] == 'BOOLEAN':
        p[0]['trueList'] = p[2]['trueList']
        p[0]['falseList'] = p[2]['falseList']

######## BASE TYPE EXPRESSION ###########

def p_expression_base_type(p):
    'expression : base_type'

    # Type rules
    p[0] = { 'type' : p[1]['type'] }

    p[0]['place'] = TAC.newTemp()
    p[0]['trueList'] = []
    p[0]['falseList'] = []

    # emit code for backPatch
    if p[1]['type'] == 'FUNCTION':
        TAC.emit(p[0]['place'], '', p[1]['name'], '=REF')
        p[0]['name'] = p[1]['name']
    else:
        if p[1]['value'] == 'true':
            p[0]['trueList'] = list([TAC.getNextQuad() + 1])
            TAC.emit(p[0]['place'], 1, '', '=')
            TAC.emit('', '', -1, 'GOTO')
        elif p[1]['value'] == 'false':
            p[0]['falseList'] = list([TAC.getNextQuad() + 1])
            TAC.emit(p[0]['place'], 0, '', '=')
            TAC.emit('', '', -1, 'GOTO')
        else :
            TAC.emit(p[0]['place'], p[1]['value'], '', '=')

######## IDENTIFIER EXPRESSION ###########

def p_expression_identifier(p):
    'expression : IDENTIFIER'

    # Type rules
    p[0] = {}
    identifierEntry = ST.exists(p[1])
    if identifierEntry!= False:
        p[0]['type'] = ST.getAttribute(p[1], 'type')
    else:
        p[0]['type'] = 'REFERENCE_ERROR'
        debug.printError('line %d: Undefined Variable "%s"' %(p.lineno(2), p[2]))
        # raise SyntaxError

    # Emit code
    p[0]['place'] = ST.getAttribute(p[1], 'place')
    p[0]['trueList'] = []
    p[0]['falseList'] = []
    p[0]['nextList'] = []

    if p[0]['type'] == 'BOOLEAN':
        p[0]['falseList'] = list([TAC.getNextQuad()])
        TAC.emit(ST.getAttribute(p[1], 'place') , 'GOTO', -1, 'COND_GOTO_Z')

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
    p[0] = { 'type' : 'BOOLEAN' , 'value' : p[1] }

def p_base_type_string(p):
    'base_type : STRING'

    # Type rules
    p[0] = { 'type' : 'STRING' , 'value' : p[1] }

def p_base_type_undefine(p):
    'base_type : UNDEFINED'

    # Type rules
    p[0] = { 'type' : 'UNDEFINED', 'value' : 'UNDEFINED'}

######## FUNCTION EXPRESSION ###########

def p_base_type_function(p):
    'base_type : function_statement'

    # Type rules
    p[0] = { 'type': 'FUNCTION', 'name': p[1]['name']}

######## ARRAY EXPRESSION ##############

def p_base_type_array(p):
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
############# ERROR ####################
########################################
def p_error(p):
    print "Whoa. You are seriously hosed."
    # Read ahead looking for a closing '}'
    while 1:
        tok = yacc.token()             # Get the next token
        if not tok or tok.type == 'SEP_SEMICOLON': 
            break
    yacc.restart() 
    # yacc.errok()

def handleError():
    while 1:
        tok = yacc.token()             # Get the next token
        if not tok or tok.type == 'SEP_SEMICOLON': 
            break

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
