symbol_table = { }

# Two stacks one for offset and other for the current scope
offset = []
scope = [symbol_table]

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

# function to add a Scope
def addScope(functionName):
    global scope

    # add the scope to the symbol_table
    currentScope = scope[len(scope) - 1]
    currentScope[functionName] = {}
    scope.append(currentScope[functionName])

# function to add an element to the current scope
def addIdentifier(identifier):
    global scope

    # add the scope to the symbol_table
    currentScope = scope[len(scope) - 1]
    currentScope[identifier] = {}

# add an attribute to the identifier
def addAttribute(identifier, attributeName, attributeValue):
    entry = lookup(identifier)
    entry[attributeName] = attributeValue

# function to delete a scope
def deleteScope(functionName):
    global scope
    scope.pop()
