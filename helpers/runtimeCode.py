class RuntimeCode:
    def __init__(self, SymbolTable, ThreeAddressCode):
        self.code = {}
        self.ST = SymbolTable
        self.TAC = ThreeAddressCode
        self.currentFunction = ''
        self.regCount = 1
        self.labelCount = -1 
        self.labelBase = 'label'
        self.resetRegisters()

    def resetRegisters(self):
        self.registerDescriptor = {
                '$t0' : None,
                '$t1' : None,
                '$t2' : None,
                '$t3' : None,
                '$t4' : None,
                '$t5' : None,
                '$t6' : None,
                '$t7' : None,
                '$t8' : None,
                '$t9' : None,
                '$s0' : None,
                '$s1' : None,
                '$s2' : None,
                '$s3' : None,
                '$s4' : None,
                }
        self.freeReg = [ reg for reg in self.registerDescriptor.keys() ]
        self.regInUse = []

    def addLine(self, line):
        self.code[self.currentFunction].append(line)

    def addFunction(self, function):
        self.currentFunction = function
        self.code[function] = []

    # Function to print code
    def printCode(self, fileName=''):
        if fileName != '':
            # Open the file
            f = open('build/' + fileName + '.s', 'w')

            # Write out the data
            data = open('lib/data.s').read()
            f.write(data)

            # Print the strings in the file
            for functionName in self.TAC.code:
                functionEntry = self.ST.functionList[functionName]
                for stringEntry in functionEntry['__stringList__']:
                    f.write('\t%s:\t.asciiz\t"%s"\n' %(stringEntry[0], stringEntry[1]))

            # Start of the code
            f.write('\n.text\n')

            # For each function, we have to print the data
            for functionName in self.code.keys():
                f.write("\n%s:\n" %functionName)
                for i in range(len(self.code[functionName])):
                    codePoint = self.code[functionName][i]
                    if codePoint[0] == 'LABEL':
                        f.write("%s:\n" %codePoint[1])
                    elif codePoint[1] == '':
                        f.write("\t%s\n" %codePoint[0])
                    elif codePoint[2] == '':
                        f.write("\t%s\t\t%s\n" %(codePoint[0], codePoint[1]))
                    elif codePoint[3] == '':
                        f.write("\t%s\t\t%s,\t%s\n" %(codePoint[0], codePoint[1], codePoint[2]))
                    else:
                        f.write("\t%s\t\t%s,\t%s,\t%s\n" %(codePoint[0], codePoint[1], codePoint[2], codePoint[3]))

            # Write out the libraray routines
            data = open('lib/code.s').read()
            f.write(data)

            # CLose the file
            f.close()

        else:
            for functionName in self.code.keys():
                print "\n%s:" %functionName
                for i in range(len(self.code[functionName])):
                    codePoint = self.code[functionName][i]
                    # print "%5d: \t%s" %(self.ST.instructionSize * i, codePoint)
                    print "\t%s\t%s\t%s\t%s" %(codePoint[0], codePoint[1], codePoint[2], codePoint[3])

        # self.TAC.printCode()
        # pprint.pprint(self.ST.addressDescriptor)

    def nextReg(self, temporary):
        # If the temporary is already loaded in a register, we return the register
        if temporary in self.registerDescriptor.values():
            reg = self.ST.addressDescriptor[temporary]['register']
        else:
            if len(self.freeReg) == 0:
                # We use the register which was first used
                reg = self.regInUse.pop(0)

                # Now we flush this register
                correspondingTemporary = self.registerDescriptor[reg]
                self.ST.addressDescriptor[correspondingTemporary]['register'] = None

                # Update the registerDescriptor
                self.registerDescriptor[reg] = temporary

                # Now we have to store the temporary back to memory
                if self.ST.addressDescriptor[correspondingTemporary]['memory'] != None:
                    # Get the value of level and offset
                    (level, offset) = self.ST.addressDescriptor[correspondingTemporary]['memory']

                    # First we load in the value of the activation record where we have to store the value
                    self.addLine(['la', '$s5', '__display__', '']) # put the address of display into $s5
                    self.addLine(['li', '$s6', level, ''])         # put the index into $s5
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index again (now 4x)
                    self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

                    # Now we store the value to the location in the stack
                    self.addLine(['lw', '$s5', '0($s7)', ''])      # load the value into display
                    self.addLine(['li', '$s6', offset, ''])        # put the offset into $s6
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset again (now 4x)
                    self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

                    self.addLine(['sw', reg, '0($s7)', ''])        # store the value into the record

                    # Set the store bit
                    self.ST.addressDescriptor[correspondingTemporary]['store'] = True

                # We have to load the value from memory into the register
                if self.ST.addressDescriptor[temporary]['memory'] != None:
                    # Get the value of level and offset
                    (level, offset) = self.ST.addressDescriptor[temporary]['memory']

                    # First we load in the value of the activation record where we have to store the value
                    self.addLine(['la', '$s5', '__display__', '']) # put the address of display into $s5
                    self.addLine(['li', '$s6', level, ''])         # put the index into $s5
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index again (now 4x)
                    self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

                    # Now we store the value to the location in the stack
                    self.addLine(['lw', '$s5', '0($s7)', ''])      # load the value into display
                    self.addLine(['li', '$s6', offset, ''])        # put the offset into $s6
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset again (now 4x)
                    self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

                    self.addLine(['lw', reg, '0($s7)', ''])        # store the value into the record
            else:
                reg = self.freeReg.pop()

                if self.ST.addressDescriptor[temporary]['memory'] != None and self.ST.addressDescriptor[temporary]['store']:
                    # Get the value of level and offset
                    (level, offset) = self.ST.addressDescriptor[temporary]['memory']

                    # First we load in the value of the activation record where we have to store the value
                    self.addLine(['la', '$s5', '__display__', '']) # put the address of display into $s5
                    self.addLine(['li', '$s6', level, ''])         # put the index into $s5
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index again (now 4x)
                    self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

                    # Now we store the value to the location in the stack
                    self.addLine(['lw', '$s5', '0($s7)', ''])      # load the value into display
                    self.addLine(['li', '$s6', offset, ''])        # put the offset into $s6
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset again (now 4x)
                    self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

                    self.addLine(['lw', reg, '0($s7)', ''])        # store the value into the record

            # Now we allocate this register to the passed temporary
            self.ST.addressDescriptor[temporary]['register'] = reg
            self.regInUse.append(reg)

            self.registerDescriptor[reg] = temporary

        # Return the register
        return reg

    def nameLabel(self):
        self.labelCount += 1
        return '__' + self.labelBase + str(self.labelCount) + '__'

    # Reload all registers which belong to parents
    def reloadParents(self, level, function):
        for temporary in self.ST.addressDescriptor:
            temporaryEntry = self.ST.addressDescriptor[temporary]
            if temporaryEntry['memory'] != None and temporaryEntry['scope'] == function:
                if temporaryEntry['memory'][0] <= level and temporaryEntry['register'] != None:
                    print 'reloading', temporary
                    (level, offset) = temporaryEntry['memory']
                    reg = temporaryEntry['register']

                    # First we load in the value of the activation record where we have to store the value
                    self.addLine(['la', '$s5', '__display__', '']) # put the address of display into $s5
                    self.addLine(['li', '$s6', level, ''])         # put the index into $s5
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index again (now 4x)
                    self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

                    # Now we store the value to the location in the stack
                    self.addLine(['lw', '$s5', '0($s7)', ''])      # load the value into display
                    self.addLine(['li', '$s6', offset, ''])        # put the offset into $s6
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset again (now 4x)
                    self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

                    self.addLine(['lw', reg, '0($s7)', ''])        # store the value into the record

                    # Set the store bit
                    self.ST.addressDescriptor[temporary]['store'] = True

    # Flush all registers to memory which belong to this function
    def flushRegisters(self, level, function):
        for temporary in self.ST.addressDescriptor:
            temporaryEntry = self.ST.addressDescriptor[temporary]
            if temporaryEntry['memory'] != None and temporaryEntry['scope'] == function:
                if temporaryEntry['memory'][0] <= level and temporaryEntry['register'] != None:
                    print 'flushing', temporary
                    (level, offset) = temporaryEntry['memory']
                    reg = temporaryEntry['register']

                    # First we load in the value of the activation record where we have to store the value
                    self.addLine(['la', '$s5', '__display__', '']) # put the address of display into $s5
                    self.addLine(['li', '$s6', level, ''])         # put the index into $s5
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index again (now 4x)
                    self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

                    # Now we store the value to the location in the stack
                    self.addLine(['lw', '$s5', '0($s7)', ''])      # load the value into display
                    self.addLine(['li', '$s6', offset, ''])        # put the offset into $s6
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset
                    self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset again (now 4x)
                    self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

                    self.addLine(['sw', reg, '0($s7)', ''])        # store the value into the record

                    # Set the store bit
                    temporaryEntry['store'] = True

                    # Delete the register allocated to this
                    temporaryEntry['register'] = None
                    self.registerDescriptor[reg] = None
                    self.freeReg.append(reg)
                    self.regInUse.pop(self.regInUse.index(reg))

    # flush a given temporary to memory
    def flushTemporary(self, temporary):
        temporaryEntry = self.ST.addressDescriptor[temporary]
        reg = temporaryEntry['register']

        if temporaryEntry['memory'] != None and temporaryEntry['register'] != None:
            (level, offset) = temporaryEntry['memory']
            print 'flushing', temporary, 'to memory'
            (level, offset) = temporaryEntry['memory']
            reg = temporaryEntry['register']

            # First we load in the value of the activation record where we have to store the value
            self.addLine(['la', '$s5', '__display__', '']) # put the address of display into $s5
            self.addLine(['li', '$s6', level, ''])         # put the index into $s5
            self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index
            self.addLine(['add', '$s6', '$s6', '$s6'])     # double the index again (now 4x)
            self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

            # Now we store the value to the location in the stack
            self.addLine(['lw', '$s5', '0($s7)', ''])      # load the value into display
            self.addLine(['li', '$s6', offset, ''])        # put the offset into $s6
            self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset
            self.addLine(['add', '$s6', '$s6', '$s6'])     # double the offset again (now 4x)
            self.addLine(['add', '$s7', '$s5', '$s6'])     # combine the two components of the address

            self.addLine(['sw', reg, '0($s7)', ''])        # store the value into the record

            # Set the store bit
            temporaryEntry['store'] = True
            temporaryEntry['register'] = None

            # Delete the register allocated to this
            self.registerDescriptor[reg] = None
            self.freeReg.append(reg)
            self.regInUse.pop(self.regInUse.index(reg))

        elif temporaryEntry['register'] != None:
            print 'freeing', temporary

            # Delete the register allocated to this
            self.registerDescriptor[reg] = None
            self.freeReg.append(reg)
            self.regInUse.pop(self.regInUse.index(reg))

    # Patch all the labels in the functions
    def fixLabels(self): 
        for function in self.TAC.code:
            unresolvedLabels = {}
            for line in self.TAC.code[function]:
                if line[3] in ['COND_GOTO_Z', 'GOTO']:
                    # Generate label
                    if unresolvedLabels.has_key(line[2]):
                        label = unresolvedLabels[line[2]]
                    else:
                        label = self.nameLabel()
                        unresolvedLabels[line[2]] = label

                    line[2] = label

            lineNumber = -1
            count = 0
            for line in range(len(self.TAC.code[function])):
                lineNumber += 1

                if lineNumber in unresolvedLabels.keys():
                    effectiveLineNumber = lineNumber + count
                    self.TAC.code[function].insert(effectiveLineNumber, ['LABEL', unresolvedLabels[lineNumber], '', ''])
                    count += 1
                    del unresolvedLabels[lineNumber]
