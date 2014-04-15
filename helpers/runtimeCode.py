class RuntimeCode:
    def __init__(self, SymbolTable):
        self.code = {}
        self.ST = SymbolTable
        self.currentFunction = ''

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
                    print "%5d: \t%s" %(self.ST.instructionSize * i, codePoint)

    def includeLibrary(self, library):
        print open(library).read()

