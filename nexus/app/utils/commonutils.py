class Utils:

    def __init__(self):
        pass

    def processString(self, currvalue):
        currvalue = str(currvalue)
        currvalue = currvalue.strip()
        currvalue = currvalue.lower()
        currvalue = currvalue.replace("'",'')
        currvalue = currvalue.replace('"','')
        currvalue = currvalue.replace(',','')
        currvalue = currvalue.replace(';','')
        currvalue = currvalue.replace('`','')
        currvalue = currvalue.replace(";",'')
        return currvalue

    def copyListOfStrings(self, listofstr):
    
        ret = []
        for val in listofstr:
            val = self.processString(val)
            ret.append(val)

        return ret




