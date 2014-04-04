# An array to store the three address code
import pprint
import debug
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

    def resolveWaitingFunctions(self):
        currentScope = self.ST.scope[len(self.ST.scope) - 1]
        currentFunction = self.ST.getCurrentScope()

        waitingFunctions = currentScope['__waitingList__']
        functionList = currentScope['__functionList__']

        for function in functionList:
            if waitingFunctions.has_key(function):
                for location in waitingFunctions[function]:
                    self.code[currentFunction][location][2] = self.ST.getAttribute(function, 'reference')
                del waitingFunctions[function]

        for function in waitingFunctions:
            debug.printError('line x: Undefined Function "%s" in "%s"' %(function, self.ST.getCurrentScope()))
            for location in waitingFunctions[function]:
                self.code[currentFunction][location][3] = 'NOOP'

        # Remove the list of waiting function
        del currentScope['__waitingList__']
                
