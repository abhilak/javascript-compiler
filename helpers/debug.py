showStatement = False
printErrors = True

# a function to print the name of the statement
def printStatement(statement):
    global showStatement
    if showStatement:
        print statement

def printError(statement):
    global printErrors
    if printErrors:
        print statement
