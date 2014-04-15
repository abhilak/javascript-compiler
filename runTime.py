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

# First we dump the entire string list of the functions
print ".data"
for functionName in TAC.code:
    functionEntry = ST.functionList[functionName]
    for stringEntry in functionEntry['__stringList__']:
        print '\t%s:\t.asciiz\t"%s"' %(stringEntry[0], stringEntry[1])

print ".text"

for function in TAC.code:
    RTC.addFunction(function)
    i = 0
    for line in TAC.code[function]:
        i += 1
        if line[3] == 'JUMPLABEL':
            RTC.addLine(['SP', ST.getAttributeFromFunctionList(function, 'width'), '', 'ADD_STACK'])
            RTC.addLine(['*SP', '', 4 * (i + 2), 'MOVE'])
            RTC.addLine(line)
        elif line[3] == 'JUMPBACK':
            RTC.addLine(['', '', '0(SP)', 'JUMPBACK'])
        else:
            RTC.addLine(line)

# RTC.printCode()

# For the strings, we have to create a label in the data region

# Then we have to create the display
