# An array to store the three address code
import pprint
code = []
nextQuad = 0

tempBase = "t"
tempCount = 0
printCodeValue = False

# Function to create new temporaries
def newTemp():
    global tempBase, tempCount
    tempCount = tempCount + 1
    return tempBase + str(tempCount)

# Function to emit code
def emit(regDest, regSrc1, regSrc2, op):
    global code, nextQuad
    nextQuad = nextQuad + 1
    code.append([regDest, regSrc1, regSrc2, op])

# Function to print code
def printCode():
    if printCodeValue:
        pprint.pprint(code)
