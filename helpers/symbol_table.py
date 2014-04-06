import pprint

class SymbolTable:
    # Constructor for the function
    def __init__(self):
        self.showSymbolTable = True
        self.symbol_table = {
                'main': {
                    '__scopeName__': 'main', 
                    '__parentName__': 'main', 
                    '__type__':'FUNCTION', 
                    '__returnType__': None,
                    '__functionList__' : [],
                    '__waitingList__' : {}
                    }
                }
        self.temporaryCount = 0

        # Two stacks one for offset and other for the current scope
        self.offset = [0]
        self.scope = [self.symbol_table['main']]

    # Print the symbol_table
    def printSymbolTable(self):
        if self.showSymbolTable:
            print "\n"
            pprint.pprint(self.symbol_table)

    # function to lookup an element in the stack
    def lookup(self, identifier):
        # Obtain the currentScope
        scopeLocation = len(self.scope)
        return self.lookupScope(identifier, scopeLocation - 1)

    def lookupScope(self, identifier, scopeLocation):
        if scopeLocation == -1:
            return None

        # add the scope to the symbol_table
        currentScope = self.scope[len(self.scope) - 1]
        if currentScope.has_key(identifier):
            return currentScope[identifier]
        else:
            return self.lookupScope(identifier, scopeLocation - 1)

    # function to return currentScope name
    def getCurrentScope(self):
        return self.scope[len(self.scope) - 1]['__scopeName__']

    # function to add a Scope
    def addScope(self, functionName):
        # add the scope to the symbol_table
        currentScope = self.scope[len(self.scope) - 1]
        currentScope[functionName] = {
                '__scopeName__': functionName, 
                '__parentName__': currentScope['__scopeName__'],
                '__returnType__': None,
                '__type__': 'FUNCTION',
                '__functionList__': [],
                '__waitingList__' : {}
                }
        self.scope.append(currentScope[functionName])

        # Marks a new relative address
        self.offset.append(0)

    # function to add an element to the current scope
    def addIdentifier(self, identifier, IdentifierType):
        # add the scope to the symbol_table
        currentScope = self.scope[len(self.scope) - 1]

        # Ladder to decide the width of the Identifier
        if IdentifierType == 'NUMBER':
            IdentifierWidth = 4
        elif IdentifierType == 'BOOLEAN':
            IdentifierWidth = 1
        elif IdentifierType == 'STRING':
            IdentifierWidth = 100
        elif IdentifierType == 'UNDEFINED':
            IdentifierWidth = 0
        elif IdentifierType == 'ARRAY':
            IdentifierWidth = 1000
        elif IdentifierType == 'FUNCTION':
            IdentifierWidth = 4

        # Update the entry
        if not currentScope.has_key(identifier):
            currentScope[identifier] = {}
        currentScope[identifier]['__offset__'] = IdentifierWidth
        currentScope[identifier]['__type__'] = IdentifierType

        # increment the offset of the top
        currentOffset = self.offset.pop() + IdentifierWidth
        self.offset.append(currentOffset)

    # add an attribute to the identifier
    def addAttribute(self, identifier, attributeName, attributeValue):
        entry = self.lookup(identifier)
        entry['__' + attributeName + '__'] = attributeValue

    # add an attribute to the identifier
    def addAttributeToCurrentScope(self, attributeName, attributeValue):
        currentScope = self.scope[len(self.scope) - 1]
        currentScope['__' + attributeName + '__'] = attributeValue

    # add an attribute to the identifier
    def getAttributeFromCurrentScope(self, attributeName):
        currentScope = self.scope[len(self.scope) - 1]
        return currentScope[ '__' + attributeName + '__']

    def getAttribute(self, identifier, attributeName):
        identifierEntry = self.lookup(identifier)
        if identifierEntry.has_key('__' + attributeName + '__'):
            return identifierEntry['__' + attributeName + '__']
        else:
            return None

    def exists(self, identifier):
        identifierEntry = self.lookup(identifier)
        if identifierEntry != None:
            return True
        else:
            return False

    # function to delete a scope
    def deleteScope(self, functionName):
        # Update the width of the function
        currentScope = self.scope.pop()
        currentScope['__width__'] = self.offset.pop()
        
    # A function that returns a unique name for anonymous functions
    def nameAnon(self):
        self.temporaryCount += 1
        return '__anon' + str(self.temporaryCount) + '__'

    # Function to add a function to the currentScope
    def addToFunctionList(self, functionName):
        currentScope = self.scope[len(self.scope) - 1]
        currentScope['__functionList__'].append(functionName)

    def addToWaitingList(self, functionName, location):
        currentScope = self.scope[len(self.scope) - 1]
        if currentScope['__waitingList__'].has_key(functionName):
            currentScope['__waitingList__'][functionName].append(location)
        else:
            currentScope['__waitingList__'][functionName] = [location]

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
