def isValidToken(token, roleOfCalledUnit):
    roleFromDB = 2
    tokenList = ['NexusToken1', 'NexusToken2']
    return token in tokenList and roleFromDB >= roleOfCalledUnit

def getTimeNow():
    import time
    return time.time()