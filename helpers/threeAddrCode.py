# An array to store the three address code
import pprint
code = {'main': []}
quad = {'main': -1}
nextQuad = {'main': 0}

tempBase = "t"
tempCount = 0
printCodeValue = True

# Function to create new temporaries
def newTemp():
    global tempBase, tempCount
    tempCount = tempCount + 1
    return tempBase + str(tempCount)

# Increment the quad for a given function
def incrementQuad(functionName):
    global quad, nextQuad
    quad[functionName] = nextQuad[functionName]
    nextQuad[functionName] = nextQuad[functionName] + 1
    return quad[functionName]

# Get the next quad of a given function
def getNextQuad(functionName):
    return nextQuad[functionName]

# This function will return the code length of a given function
def getCodeLength(functionName):
    global quad
    return quad[functionName]

# Function to emit code
def emit(functionName, regDest, regSrc1, regSrc2, op):
    global code
    incrementQuad(functionName)
    code[functionName].append([regDest, regSrc1, regSrc2, op])

# This creates a new TAC for a given function name
def createFunctionCode(functionName):
    code[functionName] = []
    quad[functionName] = -1
    nextQuad[functionName] = 0

# Function to print code
def printCode():
    for functionName in code.keys():
        print "\n%s:" %functionName
        for i in range(len(code[functionName])):
            print "%5d: \t" %i, code[functionName][i]

# Function to merge two lists
def merge(list1, list2):
    list3 = list(list1)
    list3.extend(list2)
    return list3

# Function to backpatch
def backPatch(functionName, locationList, location):
    global code
    for position in locationList:
        code[functionName][position][2] = location
    
# This function converts every location in the locationList to null
def noop(functionName, locationList):
    global code
    for position in locationList:
        code[functionName][position][3] = 'NOOP'

