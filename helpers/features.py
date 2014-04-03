count = 0

# A function that returns a unique name for anonymous functions
def nameAnon():
    global count
    count += 1
    return '____anon' + str(count)
