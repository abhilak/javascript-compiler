lineNumber = 0
showStatement = 1
printArguments = 1

# a function to print the name of the statement
def printStatement(statement):
    global showStatement
    if showStatement:
        print statement

# a function to print the arguments of a function
def printArguments(function_name, arguments):
    global printArguments
    if printArguments:
        print 'Argument of function "', function_name, '" are:', arguments
