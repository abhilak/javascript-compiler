class Debug:
    def __init__(self):
        self.showStatement = True
        self.printErrors = True 
        self.lineNumber = 1
        self.prev = 0

    # a function to print the name of the statement
    def printStatement(self, statement):
        if self.showStatement:
            print 'line %d:' %self.lineNumber, statement

    # This is only for functions with a block
    def printStatementBlock(self, statement):
        if self.showStatement:
            print 'line %d:' %(self.lineNumber + self.prev), statement

    def printError(self, statement):
        if self.printErrors:
            print '[ERROR] line %d:' %self.lineNumber, statement

    def incrementLineNumber(self):
        self.lineNumber += self.prev

    def setPrev(self, value):
        self.prev = value

    def setLineNumber(self, value):
        self.lineNumber = value

    def getPrev(self):
        return self.prev
