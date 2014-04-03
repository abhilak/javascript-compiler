# An array to store the three address code
import pprint
code = {}
quad = -1
nextQuad = 0

tempBase = "t"
tempCount = 0
printCodeValue = True

# Function to create new temporaries
def newTemp():
    global tempBase, tempCount
    tempCount = tempCount + 1
    return tempBase + str(tempCount)

# Function to emit code
def emit(functionName, regDest, regSrc1, regSrc2, op):
    global code, quad, nextQuad
    quad = nextQuad
    code[functionName].append([regDest, regSrc1, regSrc2, op])
    nextQuad = nextQuad + 1

def createFunctionCode(functionName):
    code[functionName] = []

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
    
