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

from parser import ST, parseProgram , TAC

#########################################################################################
# a function to test the parser
def test_codeGen(input_file):
    program = open(input_file).read()
    parseProgram(program)
    TAC.printCode()
    ST.printSymbolTable()
    # ST.printFunctionList()

if __name__ == "__main__":
    from sys import argv
    filename, input_file = argv 
    test_codeGen(input_file)
