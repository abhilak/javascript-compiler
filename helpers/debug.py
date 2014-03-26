showStatement = 0
lineNumber = 0

def printStatement(statement):
    global showStatement
    if showStatement:
        print statement

def incrementLineNumber():
    global lineNumber
    lineNumber += 1
