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

from sys import argv
from parser import ST, TAC, lexer, parser
import pprint

# a function to test the parser
def test_codeGen(input_file):
    program = open(input_file).read()
    parser.parse(program, lexer=lexer)
    # parser.parse(program, lexer=lexer, debug=1)
    TAC.prune()

if __name__ == "__main__":
    filename, input_file = argv 

    test_codeGen(input_file)
