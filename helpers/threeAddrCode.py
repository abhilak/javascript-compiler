# An array to store the three address code
code = []
nextQuad = 0

tempBase = "t"
tempCount = 0

# Function to create new temporaries
def newTemp():
    global tempBase, tempCount
    tempCount = tempCount + 1
    return tempBase + str(tempCount)

# Function to emit code
def emit(regDest, regSrc1, regSrc2, op):
    global code
    code[nextQuad] = [regDest, regSrc1, regSrc2, op]
