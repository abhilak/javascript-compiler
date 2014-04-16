class RuntimeCode:
    def __init__(self, SymbolTable):
        self.code = {}
        self.ST = SymbolTable
        self.currentFunction = ''
        self.regCount = 1
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
                '$s5' : None,
                '$s6' : None,
                '$s7' : None
                }
        self.freeReg = [ reg for reg in self.registerDescriptor.keys() ]

    def addLine(self, line):
        self.code[self.currentFunction].append(line)

    def addFunction(self, function):
        self.currentFunction = function
        self.code[function] = []

    # Function to print code
    def printCode(self, fileName=''):
        if fileName != '':
            f = open('log/' + fileName + '.log', 'w')
            for functionName in self.code.keys():
                f.write("\n%s:\n" %functionName)
                for i in range(len(self.code[functionName])):
                    codePoint = self.code[functionName][i]
                    f.write("%5d: \t%s\n" %(self.ST.instructionSize * i, codePoint))
                    # f.write("%4d: \t%s\t\t%s\t\t%s\t\t%s\n" %(4 * i, codePoint[0], codePoint[1], codePoint[2], codePoint[3]))
            f.close()
        else:
            for functionName in self.code.keys():
                print "\n%s:" %functionName
                for i in range(len(self.code[functionName])):
                    codePoint = self.code[functionName][i]
                    # print "%5d: \t%s" %(self.ST.instructionSize * i, codePoint)
                    print "\t%s\t%s\t%s\t%s" %(codePoint[0], codePoint[1], codePoint[2], codePoint[3])

    def includeLibrary(self, library):
        print open(library).read()

    def nextReg(self, temporary):
        if len(self.freeReg) == 0:
            print 'Spilling Required'
            pass
        else:
            if temporary in self.registerDescriptor.values():
                reg = self.ST.addressDescriptor[temporary]['register']
            else:
                reg = self.freeReg.pop()
                self.ST.addressDescriptor[temporary]['register'] = reg
            self.registerDescriptor[reg] = temporary
            return reg

