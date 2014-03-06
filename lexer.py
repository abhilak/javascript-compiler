from ply import lex, yacc
from sys import argv

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
        # "NEW", 
        # "DELETE", 
        # "THIS", 
        "IDENTIFIER",
        "OP_INSTANCEOF", 
        "OP_TYPEOF", 
        "OP_ASSIGNMENT",
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
    r"NaN"
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

# RegEx for OOP
# t_NEW = r"new"
# t_DELETE = r"delete"
# t_THIS = r"this"

########################################
############# IDENTIFIER ###############
########################################
def t_IDENTIFIER(t):
    r"[a-zA-Z$_][\w$]*"
    return t

########################################
############# OPERATORS ################
########################################
def t_OP_INSTANCEOF(t):
    r"instanceof"
    return t

def t__OP_TYPEOF(t):
    r"typeof"
    return t

def t_OP_ASSIGNMENT(t):
    r"=|"r"\+=|"r"-=|"r"\*=|"r"/=|"r"%="
    return t

def t_OP_COLON(t):
    r":"
    return t

def t_OP_ADDITION(t):
    r"\+"
    return t

def t_OP_SUBTRACTION(t):
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
def p_start(p):
    '''start : block
             | statements'''
    return p[0]

# A group of statements
def p_block(p): 
    '''block : SEP_OPEN_BRACE statements SEP_CLOSE_BRACE'''
    return p[0]

# A group of statements
def p_statments(p):
    '''statements : statement statements
                  | statement'''
    return p[0]

# A single statement
def p_statment(p):
    '''statement : assignment
                 | expression'''
    return p[0]

# An expression statement
def p_expression(p):
    '''expression : num_expression SEP_SEMICOLON
                  | str_expression SEP_SEMICOLON'''

# Rules for allowing implicit typecast to string
# def p_expression_str_to_num1(p):
#     '''expression : str_expression OP_ADDITION num_expression SEP_SEMICOLON'''
#     p[0] = p[1] + str(p[3])
#
# def p_expression_str_to_num2(p):
#     '''expression : num_expression OP_ADDITION str_expression SEP_SEMICOLON'''
#     p[0] = p[3] + str(p[1])

# Rules for arithematic expressions
precedence = (
        ('left', 'OP_ADDITION', 'OP_SUBTRACTION'),
        ('left', 'OP_MULTIPLICATION', 'OP_DIVISION', 'OP_MODULUS')
        )

def p_num_expression_binop(p):
    '''num_expression : num_expression OP_ADDITION num_expression
                      | num_expression OP_SUBTRACTION num_expression
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

def p_num_expression_number(p):
    'num_expression : NUMBER'
    p[0] = p[1]

# Rules for string concatenation
def p_str_expression_binop(p):
    '''str_expression : str_expression OP_ADDITION str_expression'''
    p[0] = p[1] + p[3]

def p_str_expression_plain(p):
    '''str_expression : STRING'''
    p[0] = p[1]

# An assignment statement
def p_assign_statment(p):
    '''assignment : VAR IDENTIFIER SEP_SEMICOLON
                  | VAR IDENTIFIER OP_ASSIGNMENT data_type SEP_SEMICOLON
                  | IDENTIFIER OP_ASSIGNMENT data_type SEP_SEMICOLON'''
    print "assignment"

# Different types of data
def p_object(p):
    '''object : SEP_OPEN_BRACE items SEP_CLOSE_BRACE
              | SEP_OPEN_BRACE SEP_CLOSE_BRACE'''
    print "object"

def p_items(p):
    '''items : property SEP_COMMA items
             | property'''

def p_property(p):
    '''property : STRING OP_COLON data_type'''

def p_array(p):
    '''array : SEP_OPEN_BRACKET list SEP_CLOSE_BRACKET
             | SEP_OPEN_BRACKET SEP_CLOSE_BRACKET'''
    print "array"

def p_list(p):
    '''list : data_type SEP_COMMA list
            | data_type'''

def p_data_type(p):
    '''data_type : NUMBER 
                 | BOOLEAN
                 | STRING
                 | NULL
                 | NAN
                 | UNDEFINED
                 | INFINITY
                 | array
                 | object'''

def p_error(p):
    raise TypeError("unknown text at %r" % (p.value,))

if __name__ == "__main__":
    # Here the lexer is initialized so that it can be used in another file
    lex.lex()

    filename, input_file = argv 
    program = open(input_file).read()

    yacc.yacc()
    yacc.parse(program)
    # test_lex(input_file)
