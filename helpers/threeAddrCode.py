# An array to store the three address code
import debug
import symbol_table as SymbolTable

class ThreeAddressCode:
    def __init__(self, ST):
        self.code = {'main': []}
        self.quad = {'main': -1}
        self.nextQuad = {'main': 0}

        # Contains an instance of the SymbolTable
        self.ST = ST
        
    # Increment the quad for a given function
    def incrementQuad(self):
        currentFunction = self.ST.getCurrentScope()
        self.quad[currentFunction] = self.nextQuad[currentFunction]
        self.nextQuad[currentFunction] = self.nextQuad[currentFunction] + 1
        return self.quad[currentFunction]

    # Get the next quad of a given function
    def getNextQuad(self):
        currentFunction = self.ST.getCurrentScope()
        return self.nextQuad[currentFunction]

    # This function will return the code length of a given function
    def getCodeLength(self, functionName):
        return self.quad[functionName]

    # Function to emit code
    def emit(self, regDest, regSrc1, regSrc2, op):
        currentFunction = self.ST.getCurrentScope()
        self.incrementQuad()
        self.code[currentFunction].append([regDest, regSrc1, regSrc2, op])

    # This creates a new TAC for a given function name
    def createFunctionCode(self, functionName):
        self.code[functionName] = []
        self.quad[functionName] = -1
        self.nextQuad[functionName] = 0

    # Function to print code
    def printCode(self, fileName=''):
        if fileName != '':
            f = open('log/' + fileName + '.log', 'w')
            for functionName in self.code.keys():
                f.write("\n%s:\n" %functionName)
                for i in range(len(self.code[functionName])):
                    codePoint = self.code[functionName][i]
                    f.write("%5d: \t%s\n" %(i, codePoint))
            f.close()
        else:
            for functionName in self.code.keys():
                print "\n%s:" %functionName
                for i in range(len(self.code[functionName])):
                    codePoint = self.code[functionName][i]
                    print "%5d: \t%s" %(i, codePoint)

    # Function to merge two lists
    def merge(self, list1, list2):
        list3 = list(list1)
        list3.extend(list2)
        return list3

    # Function to backpatch
    def backPatch(self, locationList, location):
        currentFunction = self.ST.getCurrentScope()
        for position in locationList:
            self.code[currentFunction][position][2] = location
        
    # This function converts every location in the locationList to null
    def noop(self, locationList):
        currentFunction = self.ST.getCurrentScope()
        for position in locationList:
            self.code[currentFunction][position][3] = 'NOOP'

    # Print the SymbolTable
    def printSymbolTable(self):
        self.ST.printSymbolTable()

    def prune(self):
        for item in self.code:
            for i in range(len(self.code[item])):
                if self.code[item][i][3] == 'GOTO' and self.code[item][i][2] == -1:
                    print self.code[item][i]
