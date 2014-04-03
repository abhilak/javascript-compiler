import pprint

showSymbolTable = True
symbol_table = {'__scopeName__': 'main' }

# Two stacks one for offset and other for the current scope
offset = [0]
scope = [symbol_table]

def printSymbolTable():
    if showSymbolTable:
        print
        pprint.pprint(symbol_table)

# function to lookup an element in the stack
def lookup(identifier):
    global scope

    # Obtain the currentScope
    currentScope = len(scope)

    return lookupScope(identifier, currentScope - 1)

def lookupScope(identifier, scopeLocation):
    if scopeLocation == -1:
        return None

    global scope

    # add the scope to the symbol_table
    currentScope = scope[len(scope) - 1]
    if currentScope.has_key(identifier):
        return currentScope[identifier]
    else:
        return lookupScope(identifier, scopeLocation - 1)

# function to return currentScope name
def getCurrentScope():
    global scope
    return scope[len(scope) - 1]['__scopeName__']

# function to add a Scope
def addScope(functionName):
    global scope

    # add the scope to the symbol_table
    currentScope = scope[len(scope) - 1]
    currentScope[functionName] = {'__scopeName__': functionName, '__parentName__': currentScope['__scopeName__'] }
    scope.append(currentScope[functionName])

    # Marks a new relative address
    offset.append(0)

# function to add an element to the current scope
def addIdentifier(identifier, IdentifierType):
    global scope

    # add the scope to the symbol_table
    currentScope = scope[len(scope) - 1]

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

    # Update the entry
    if not currentScope.has_key(identifier):
        currentScope[identifier] = {}
    currentScope[identifier]['__offset__'] = IdentifierWidth
    currentScope[identifier]['__type__'] = IdentifierType

    # increment the offset of the top
    currentOffset = offset.pop() + IdentifierWidth
    offset.append(currentOffset)

# add an attribute to the identifier
def addAttribute(identifier, attributeName, attributeValue):
    entry = lookup(identifier)
    entry['__' + attributeName + '__'] = attributeValue

def getAttribute(identifier, attributeName):
    identifierEntry = lookup(identifier)
    return identifier['__' + attributeName + '__']

def exists(identifier):
    identifierEntry = lookup(identifier)
    if identifier != None:
        return True
    else:
        return False

# function to delete a scope
def deleteScope(functionName):
    global scope
    
    # Update the width of the function
    currentScope = scope.pop()
    currentScope['__width__'] = offset.pop()
    
