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

# function that increments the line number
def incrementLineNumber():
    global lineNumber
    lineNumber += 1

# function to print the line numbe and the name of the error
def printError(name):
    global lineNumber
    print "line ", lineNumber, ":", name
