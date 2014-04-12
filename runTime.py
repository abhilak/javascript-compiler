# List of all the allowed statements
# - NOOP
# - GOTO
# - JUMP
# - COND_GOTO
#     - Not sure how to tackle this pesky thing, do we evaluate it directly and use COND_GOTO_Z?
# - COND_GOTO_Z
# - RETURN
# - PARAM
# - =
# - +
# - -
# - /
# - %
# - *
#

from parser import ST, parseProgram , TAC, debug

#########################################################################################
# a function to test the parser
def test_codeGen(input_file):
    program = open(input_file).read()
    parseProgram(program)

    # Log the data
    debug.log(TAC.code, 'TAC_code')
    debug.log(ST.symbol_table, 'symbol_table')
    debug.log(ST.functionList, 'functionList')

    # For the strings, we have to create a label in the data region

    # First order of buisness is to add the stack frame

    # Then we have to create the display

    # we have to update all the variables when we call a new function

if __name__ == "__main__":
    from sys import argv
    filename, input_file = argv 
    test_codeGen(input_file)
