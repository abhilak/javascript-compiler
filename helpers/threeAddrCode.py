# An array to store the three address code
import pprint
import symbol_table as SymbolTable

class ThreeAddressCode:
    def __init__(self, ST):
        self.code = {'main': []}
        self.quad = {'main': -1}
        self.nextQuad = {'main': 0}

        self.tempBase = "t"
        self.tempCount = 0
        self.printCodeValue = True

        # Contains an instance of the SymbolTable
        self.ST = ST
        
    # Function to create new temporaries
    def newTemp(self):
        self.tempCount = self.tempCount + 1
        return self.tempBase + str(self.tempCount)

    # Increment the quad for a given function
    def incrementQuad(self, functionName):
        self.quad[functionName] = self.nextQuad[functionName]
        self.nextQuad[functionName] = self.nextQuad[functionName] + 1
        return self.quad[functionName]

    # Get the next quad of a given function
    def getNextQuad(self, functionName):
        return self.nextQuad[functionName]

    # This function will return the code length of a given function
    def getCodeLength(self, functionName):
        return self.quad[functionName]

    # Function to emit code
    def emit(self, functionName, regDest, regSrc1, regSrc2, op):
        self.incrementQuad(functionName)
        self.code[functionName].append([regDest, regSrc1, regSrc2, op])

    # This creates a new TAC for a given function name
    def createFunctionCode(self, functionName):
        self.code[functionName] = []
        self.quad[functionName] = -1
        self.nextQuad[functionName] = 0

    # Function to print code
    def printCode(self):
        for functionName in self.code.keys():
            print "\n%s:" %functionName
            for i in range(len(self.code[functionName])):
                print "%5d: \t" %i, self.code[functionName][i]

    # Function to merge two lists
    def merge(self, list1, list2):
        list3 = list(list1)
        list3.extend(list2)
        return list3

    # Function to backpatch
    def backPatch(self, functionName, locationList, location):
        for position in locationList:
            self.code[functionName][position][2] = location
        
    # This function converts every location in the locationList to null
    def noop(self, functionName, locationList):
        for position in locationList:
            self.code[functionName][position][3] = 'NOOP'

    # Print the SymbolTable
    def printSymbolTable(self):
        self.ST.printSymbolTable()
