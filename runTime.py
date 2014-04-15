from sys import argv
from parser import ST, parseProgram , TAC, debug, ThreeAddressCode
from helpers import runtimeCode as RuntimeCode

#########################################################################################

# Parse the program to get the threeAddressCode
filename, input_file = argv 
program = open(input_file).read()
parseProgram(program)

# Log the data
TAC.printCode('TAC_code')
debug.log(ST.symbol_table, 'symbols')
debug.log(ST.functionList, 'functionList')

# We have to parser the TAC to add the stack frame statements
# Everytime the word 'JUMPLABEL appears, we have to do this
RTC = RuntimeCode.RuntimeCode(ST)

for function in TAC.code:
    RTC.addFunction(function)
    for line in TAC.code[function]:
        if line[3] == 'JUMPLABEL':
            RTC.addLine(['SP', ST.getAttributeFromFunctionList(function, 'width'), '', 'ADD_STACK'])
            RTC.addLine(['*SP', ST.addressSize, '', 'MOVE'])
        else:
            RTC.addLine(line)

RTC.printCode()

# For the strings, we have to create a label in the data region

# Then we have to create the display
