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
counter = 0;
for function in TAC.code:
    RTC.addFunction(function)
    lineNumber = -1
    unresolvedLabels = {}

    #allocate space for the registers by updating stack pointer
    RTC.addLine(['sub', '$sp','$sp','72'])
    #store return address of the caller
    RTC.addLine(['sw','$ra','0($sp)',''])
    #sstore the frame pointer of the caller
    RTC.addLine(['sw','$fp','4($sp)',''])
    #set fame pointer of the callee
    RTC.addLine(['la','$fp','72($sp)',''])
    #storing display[level]
    RTC.addLine(['li','$v0',ST.getAttributeFromFunctionList(function, 'level'),''])
    RTC.addLine(['la', '$s5', '_display__', ''])
    RTC.addLine(['add', '$v0', '$v0', '$v0'])
    RTC.addLine(['add', '$v0', '$v0', '$v0'])
    RTC.addLine(['add', '$s6', '$v0', '$s5'])
    RTC.addLine(['lw','$s7','0($s6)',''])
    RTC.addLine(['sw','$s7','8($sp)',''])
    #set display[level]
    RTC.addLine(['sw',str(ST.getAttributeFromFunctionList(function, 'width'))+'($sp)','$s6',''])
    #store remaining registers
    RTC.addLine(['sw','$t0','12($sp)',''])
    RTC.addLine(['sw','$t1','16($sp)',''])
    RTC.addLine(['sw','$t2','20($sp)',''])
    RTC.addLine(['sw','$t3','24($sp)',''])
    RTC.addLine(['sw','$t4','28($sp)',''])
    RTC.addLine(['sw','$t5','32($sp)',''])
    RTC.addLine(['sw','$t6','36($sp)',''])
    RTC.addLine(['sw','$t7','40($sp)',''])
    RTC.addLine(['sw','$t8','44($sp)',''])
    RTC.addLine(['sw','$t9','48($sp)',''])
    RTC.addLine(['sw','$s0','52($sp)',''])
    RTC.addLine(['sw','$s1','56($sp)',''])
    RTC.addLine(['sw','$s2','60($sp)',''])
    RTC.addLine(['sw','$s3','64($sp)',''])
    RTC.addLine(['sw','$s4','68($sp)',''])
    # RTC.addLine(['sw','$s5','72($sp)',''])
    # RTC.addLine(['sw','$s6','76($sp)',''])
    # RTC.addLine(['sw','$s7','80($sp)',''])
    RTC.addLine(['li','$v0',ST.getAttributeFromFunctionList(function, 'width'),''])
    RTC.addLine(['sub','$sp','$sp','$v0'])
    for x in range(ST.getAttributeFromFunctionList(function, 'numParam')):
        RTC.addLine(['sw','$a'+str(x),str(4*x)+'($sp)',''])

    for line in TAC.code[function]:
        lineNumber += 1

        # Here we have to add a label to this line
        if lineNumber in unresolvedLabels.keys():
            RTC.addLine(['LABEL', unresolvedLabels[lineNumber], '', '' ])

        if lineNumber == 0:
            pass
            # set the frame pointer
            # save the value of display
            # save registers
            # update the stack pointer to the value above this

        # Expand upon the TAC
        if line[3] == 'JUMPLABEL':
            # RTC.addLine(['SP', ST.getAttributeFromFunctionList(function, 'width'), '', 'ADD_STACK'])
            # RTC.addLine(['*SP', '', 4 * (i + 2), 'MOVE'])
            # RTC.addLine(line)
            counter = 0 ;
            RTC.addLine(['jal',line[2],'',''])

        elif line[3] == 'JUMPBACK':
            RTC.addLine(['b', function + 'end', '', ''])
        elif line[3] == 'PARAM':
            reg = RTC.nextReg(line[0])
            RTC.addLine(['move','$a'+str(counter),reg,''])
            counter = counter +1 ;

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

            # Generate label
            if unresolvedLabels.has_key(line[2]):
                label = unresolvedLabels[line[2]]
            else:
                label = RTC.nameLabel()
                unresolvedLabels[line[2]] = label

            RTC.addLine(['beq', reg1, '$0', label])

        elif line[3] == 'GOTO':
            # Generate label
            if unresolvedLabels.has_key(line[2]):
                label = unresolvedLabels[line[2]]
            else:
                label = RTC.nameLabel()
                unresolvedLabels[line[2]] = label

            RTC.addLine(['b', label, '', ''])

        elif line[3] == 'FUNCTION_RETURN':
            reg1 = RTC.nextReg(line[0])
            RTC.addLine(['move',reg1,'$v0',''])

        elif line[3] == 'RETURN':
            reg1 = RTC.nextReg(line[0])
            RTC.addLine(['move','$v0',reg1,''])
            RTC.addLine(['b', function + 'end', '', ''])

        elif line[3] == 'HALT':
            RTC.addLine(['jal', 'exit', '', ''])

        elif line[3] == 'PRINT' and line[0] == '':
            RTC.addLine(['jal', 'print_newline', '', ''])

        elif line[3] == 'PRINT' and line[2] == 'UNDEFINED':
            RTC.addLine(['jal', 'print_undefined', '', ''])

        elif line[3] == 'PRINT':
            # get a free register
            reg = RTC.nextReg(line[0])
            RTC.addLine(['move', '$a0', reg, ''])

            if line[2] == 'NUMBER':
                RTC.addLine(['jal', 'print_integer', '', ''])
            elif line[2] == 'STRING':
                RTC.addLine(['jal', 'print_string', '', ''])
            else:
                RTC.addLine(['jal', 'print_boolean', '', ''])

        else:
            RTC.addLine(line)

    RTC.addLine(['LABEL', function + 'end', '', ''])
    RTC.addLine(['addi','$sp','$sp',ST.getAttributeFromFunctionList(function,'width')])
    RTC.addLine(['lw','$ra','0($sp)',''])
    RTC.addLine(['lw','$fp','4($sp)',''])

    RTC.addLine(['lw','$a0','8($sp)',''])
    RTC.addLine(['li','$a1',ST.getAttributeFromFunctionList(function, 'level'),''])
    RTC.addLine(['la', '$s5', '_display__', ''])
    RTC.addLine(['add', '$a1', '$a1', '$a1'])
    RTC.addLine(['add', '$a1', '$a1', '$a1'])
    RTC.addLine(['add', '$s6', '$a1', '$s5'])
    RTC.addLine(['sw','$a0','$s6',''])

    RTC.addLine(['lw','$t0','12($sp)',''])
    RTC.addLine(['lw','$t1','16($sp)',''])
    RTC.addLine(['lw','$t2','20($sp)',''])
    RTC.addLine(['lw','$t3','24($sp)',''])
    RTC.addLine(['lw','$t4','28($sp)',''])
    RTC.addLine(['lw','$t5','32($sp)',''])
    RTC.addLine(['lw','$t6','36($sp)',''])
    RTC.addLine(['lw','$t7','40($sp)',''])
    RTC.addLine(['lw','$t8','44($sp)',''])
    RTC.addLine(['lw','$t9','48($sp)',''])
    RTC.addLine(['lw','$s0','52($sp)',''])
    RTC.addLine(['lw','$s1','56($sp)',''])
    RTC.addLine(['lw','$s2','60($sp)',''])
    RTC.addLine(['lw','$s3','64($sp)',''])
    RTC.addLine(['lw','$s4','68($sp)',''])
    # RTC.addLine(['lw','$s5','72($sp)',''])
    # RTC.addLine(['lw','$s6','76($sp)',''])
    # RTC.addLine(['lw','$s7','80($sp)',''])
    RTC.addLine(['addi','$sp','$sp','72'])
    RTC.addLine(['jr','$ra','',''])

# Print the generated code
RTC.printCode('pro')
# TAC.printCode()

# pprint.pprint(RTC.registerDescriptor)
# pprint.pprint(ST.addressDescriptor)
