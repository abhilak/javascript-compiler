import pprint

class SymbolTable:
    # Constructor for the function
    def __init__(self):
        self.symbol_table = {
                'main': {
                    '__scopeName__': 'main', 
                    '__parentName__': 'main', 
                    '__type__':'FUNCTION', 
                    '__returnType__': 'UNDEFINED',
                    '__stringList__' : [],
                    '__level__' : 1
                    }
                }
        self.temporaryCount = 0
        self.stringCount = 0
        self.functionList = { 'main': self.symbol_table['main']}
        self.instructionSize = 4
        self.addressSize = 4
        self.booleanSize = 1
        self.undefinedSize = 0
        self.numberSize = 4

        # Two stacks one for offset and other for the current scope
        self.offset = [0]
        self.scope = [self.symbol_table['main']]

    # Print the symbol_table
    def printSymbolTable(self):
        pprint.pprint(self.symbol_table)

    # Print the functionList
    def printFunctionList(self):
        pprint.pprint(self.functionList)

    # function to return currentScope name
    def getCurrentScope(self):
        return self.scope[len(self.scope) - 1]['__scopeName__']

    # function to lookup an element in the stack
    def lookup(self, identifier):
        # Obtain the currentScope
        scopeLocation = len(self.scope)
        return self.lookupScope(identifier, scopeLocation - 1)

    def lookupScope(self, identifier, scopeLocation):
        if scopeLocation == -1:
            return None

        # add the scope to the symbol_table
        currentScope = self.scope[scopeLocation]
        if currentScope.has_key(identifier):
            return currentScope[identifier]
        else:
            return self.lookupScope(identifier, scopeLocation - 1)

    # function to add a Scope
    def addScope(self, functionName):
        # add the scope to the symbol_table
        currentScope = self.scope[len(self.scope) - 1]
        level = currentScope['__level__'] + 1

        currentScope[functionName] = {
                '__scopeName__': functionName, 
                '__parentName__': currentScope['__scopeName__'],
                '__returnType__': 'UNDEFINED',
                '__type__': 'FUNCTION',
                '__stringList__' : [],
                '__level__' : level
                }
        self.scope.append(currentScope[functionName])

        # Marks a new relative address
        self.offset.append(0)
        self.functionList[functionName] = currentScope[functionName]

    # function to add an element to the current scope
    def addIdentifier(self, identifier, IdentifierType, IdentifierWidth=0):
        # add the scope to the symbol_table
        currentScope = self.scope[len(self.scope) - 1]

        # Ladder to decide the width of the Identifier
        if IdentifierWidth == 0:
            if IdentifierType in ['FUNCTION', 'CALLBACK', 'STRING']:
                IdentifierWidth = self.addressSize
            elif IdentifierType == 'BOOLEAN':
                IdentifierWidth = self.booleanSize
            elif IdentifierType == 'NUMBER':
                IdentifierWidth = self.numberSize
            else:
                # For UNDEFINED
                IdentifierWidth = self.undefinedSize

        # increment the offset of the top
        currentOffset = self.offset.pop()

        # Update the entry
        if not currentScope.has_key(identifier):
            currentScope[identifier] = {}

        currentScope[identifier]['__width__'] = IdentifierWidth
        currentScope[identifier]['__type__'] = IdentifierType
        currentScope[identifier]['__offset__'] = currentOffset
        currentScope[identifier]['__scopeLevel__'] = currentScope['__level__']

        self.offset.append(currentOffset + IdentifierWidth)

    # add an attribute to the identifier
    def addAttribute(self, identifier, attributeName, attributeValue):
        entry = self.lookup(identifier)
        entry['__' + attributeName + '__'] = attributeValue

    def addAttributeToCurrentScope(self, attributeName, attributeValue):
        currentScope = self.scope[len(self.scope) - 1]
        currentScope['__' + attributeName + '__'] = attributeValue

    def getAttributeFromCurrentScope(self, attributeName):
        currentScope = self.scope[len(self.scope) - 1]
        return currentScope[ '__' + attributeName + '__']

    def getFunctionAttribute(self, identifier, attribute):
        functionName = self.getAttribute(identifier, 'name')
        if self.functionList.has_key(functionName):
            return self.functionList[functionName]['__' + attribute + '__']
        else:
            return None

    def addToStringList(self, label, string):
        currentScope = self.scope[len(self.scope) - 1]
        currentScope['__stringList__'].append({ label : string })

    # Get the attribute of a given identifier
    def getAttribute(self, identifier, attributeName):
        identifierEntry = self.lookup(identifier)
        if identifierEntry.has_key('__' + attributeName + '__'):
            return identifierEntry['__' + attributeName + '__']
        else:
            return None

    # Function to check if an identifier exists in the lexical scope or not
    def exists(self, identifier):
        identifierEntry = self.lookup(identifier)
        if identifierEntry != None:
            return True
        else:
            return False

    # Lookup the variable in the current scope
    def existsInCurrentScope(self, identifier):
        return self.scope[len(self.scope) - 1].get(identifier, False) != False

    # function to delete a scope
    def deleteScope(self, functionName):
        # Update the width of the function
        currentScope = self.scope.pop()
        currentScope['__width__'] = self.offset.pop()
        
    # A function that returns a unique name for anonymous functions
    def nameAnon(self):
        self.temporaryCount += 1
        return '__anon' + str(self.temporaryCount) + '__'

    # A function to provide labels to strings
    def nameString(self):
        self.stringCount += 1
        return '__string' + str(self.stringCount) + '__'

    # Function to check if two lists are equal or not
    def equal(self, list1, list2):
        if len(list1) != len(list2):
            return False
        else:
            for i in range(len(list1)):
                if list1[i] == list2[i]:
                    pass
                else:
                    return False
            return True

    # Get the function attribute from functionlist
    def getAttributeFromFunctionList(self, function, attributeName):
        if self.functionList.has_key(function):
            return self.functionList[function]['__' + attributeName + '__']
        else:
            return None

