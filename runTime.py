from sys import argv
from parser import ST, parseProgram , TAC, debug, ThreeAddressCode
from helpers import runtimeCode as RuntimeCode
import pprint

#########################################################################################

# Parse the program to get the threeAddressCode
filename, input_file = argv 
program = open(input_file).read()
parseProgram(program)

# Log the data
TAC.printCode('TAC_code')
debug.log(ST.symbol_table, 'symbols')
debug.log(ST.functionList, 'functionList')

# We create a new object which will store the code
RTC = RuntimeCode.RuntimeCode(ST, TAC)

for function in TAC.code:
    RTC.addFunction(function)
    i = -1
    for line in TAC.code[function]:
        i += 1
        # We set up the instructions for the activation record over here
        if i == 0:
            pass
            # set the frame pointer
            # save the value of display
            # save registers
            # update the stack pointer to the value above this

        # Expand upon the TAC
        if line[3] == 'JUMPLABEL':
            RTC.addLine(['SP', ST.getAttributeFromFunctionList(function, 'width'), '', 'ADD_STACK'])
            RTC.addLine(['*SP', '', 4 * (i + 2), 'MOVE'])
            RTC.addLine(line)

        elif line[3] == 'JUMPBACK':
            RTC.addLine(['jr', '$ra', '', ''])

        elif line[3] == '=':
            reg1 = RTC.nextReg(line[0])
            reg2 = RTC.nextReg(line[1])
            RTC.addLine(['move', reg1, reg2, ''])
        elif line[3] == '=i':
            reg = RTC.nextReg(line[0])
            RTC.addLine(['li', reg, line[1], ''])

        elif line[3] == '=REF':
            reg = RTC.nextReg(line[0])
            RTC.addLine(['la', reg, line[1], ''])

        elif line[3] == 'uni-':
            RTC.addLine(['neg',line[0],line[1],''])

        elif line[3] == '+':
            reg1 = RTC.nextReg(line[0])
            reg2 = RTC.nextReg(line[1])
            reg3 = RTC.nextReg(line[2])
            RTC.addLine(['add',reg1,reg2,reg3])

        elif line[3] == '-':
            reg1 = RTC.nextReg(line[0])
            reg2 = RTC.nextReg(line[1])
            reg3 = RTC.nextReg(line[2])
            RTC.addLine(['sub',reg1,reg2,reg3])

        elif line[3] == '*':
            reg1 = RTC.nextReg(line[1])
            reg2 = RTC.nextReg(line[2])
            reg3 = RTC.nextReg(line[0])
            RTC.addLine(['mult',reg1,reg2,''])
            RTC.addLine(['mflo',reg3,'',''])

        elif line[3] == '/':
            reg1 = RTC.nextReg(line[1])
            reg2 = RTC.nextReg(line[2])
            reg3 = RTC.nextReg(line[0])
            RTC.addLine(['div',reg1,reg2,''])
            RTC.addLine(['mflo',reg3,'',''])

        elif line[3] == '%':
            reg1 = RTC.nextReg(line[1])
            reg2 = RTC.nextReg(line[2])
            reg3 = RTC.nextReg(line[0])
            RTC.addLine(['div',reg1,reg2,''])
            RTC.addLine(['mfhi',reg3,'',''])

        elif line[3] == '<':
            reg1 = RTC.nextReg(line[0])
            reg2 = RTC.nextReg(line[1])
            reg3 = RTC.nextReg(line[2])
            RTC.addLine(['slt',reg1,reg2,reg3])

        elif line[3] == '>':
            reg1 = RTC.nextReg(line[0])
            reg2 = RTC.nextReg(line[1])
            reg3 = RTC.nextReg(line[2])
            RTC.addLine(['sgt',reg1,reg2,reg3])

        elif line[3] == '<=':
            reg1 = RTC.nextReg(line[0])
            reg2 = RTC.nextReg(line[1])
            reg3 = RTC.nextReg(line[2])
            RTC.addLine(['sle',reg1,reg2,reg3])

        elif line[3] == '>=':
            reg1 = RTC.nextReg(line[0])
            reg2 = RTC.nextReg(line[1])
            reg3 = RTC.nextReg(line[2])
            RTC.addLine(['sge',reg1,reg2,reg3])

        elif line[3] == '==':
            reg1 = RTC.nextReg(line[0])
            reg2 = RTC.nextReg(line[1])
            reg3 = RTC.nextReg(line[2])
            RTC.addLine(['seq',reg1,reg2,reg3])

        elif line[3] == '!=':
            reg1 = RTC.nextReg(line[0])
            reg2 = RTC.nextReg(line[1])
            reg3 = RTC.nextReg(line[2])
            RTC.addLine(['sne',reg1,reg2,reg3])

        elif line[3] == 'COND_GOTO_Z':
            reg1 = RTC.nextReg(line[0])
            RTC.addLine(['beq',reg1,'$0',line[2]])

        elif line[3] == 'GOTO':
            RTC.addLine(['b',line[2],'',''])

        elif line[3] == 'FUNCTION_RETURN':
            reg1 = RTC.nextReg(line[0])
            RTC.addLine(['move',reg1,'$v0',''])

        elif line[3] == 'RETURN':
            reg1 = RTC.nextReg(line[0])
            RTC.addLine(['move','$v0',reg1,''])

        elif line[3] == 'HALT':
            RTC.addLine(['jal', 'exit', '', ''])

        elif line[3] == 'PRINT' and line[0] == '':
            RTC.addLine(['jr', 'print_newline', '', ''])

        elif line[3] == 'PRINT' and line[2] == 'UNDEFINED':
            RTC.addLine(['jr', 'print_undefined', '', ''])

        elif line[3] == 'PRINT':
            # get a free register
            reg = RTC.nextReg(line[0])
            RTC.addLine(['move', '$a0', reg, ''])

            if line[2] == 'NUMBER':
                RTC.addLine(['jr', 'print_integer', '', ''])
            elif line[2] == 'STRING':
                RTC.addLine(['jr', 'print_string', '', ''])
            else:
                RTC.addLine(['jr', 'print_boolean', '', ''])

        else:
            RTC.addLine(line)


# Print the generated code
RTC.printCode('pro')
# TAC.printCode()

# pprint.pprint(RTC.registerDescriptor)
# pprint.pprint(ST.addressDescriptor)
