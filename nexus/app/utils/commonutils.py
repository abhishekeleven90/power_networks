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
        return str(currvalue)

    def copyListOfStrings(self, listofstr):
        ret = []
        for val in listofstr:
            val = self.processString(val)
            ret.append(val)
        return ret

    def copyList(self, somelist):
        ret = []
        for val in somelist:
            ret.append(val)
        return ret

    def getDateTimeFromTimestamp(self, timestamp):
        from datetime import datetime
        from app.constants import DATE_FORMAT
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime(DATE_FORMAT)

    def getCurrentDateTime(self):
        from datetime import datetime
        from app.constants import DATE_FORMAT
        dt = datetime.now()
        return dt.strftime(DATE_FORMAT)

    def changeTypeDescribe(self, changeType):
        from app.constants import CHANGE_DELETE, CHANGE_INSERT, CHANGE_MODIFY
        if changeType == CHANGE_DELETE:
            return 'deletion'
        if changeType == CHANGE_INSERT:
            return 'insertion'
        if changeType == CHANGE_MODIFY:
            return 'modification'

    @classmethod
    def currentTimeStamp(cls):
        import time
        return time.time()

    ## idea is to use a dict and then construct
    ## names, types, vals as in mysql
    ## to handle the issue of None
    ## i think can be done
    ## TODO
    def mysqlHepler(self, dictvals, dicttypes):
        dictuseful = {}
        for key in dictvals:
            if dictvals[key] is not None:
                dictuseful[key] = dictvals[key]
        print dictuseful
        str1 = ''
        for key in dictuseful:
            str1=str1+key+','
            # str2 if
        print str1

    @classmethod
    def isStringEmptyNone(cls, givenstr):
        if givenstr is None:
            return True
        if len(self.processString(givenstr))==0:
            return True
        return False

    @classmethod
    def convertToRegularList(cls, somelist):
        retlist = []
        for l in somelist:
            retlist.append(str(l))
        return retlist

    @classmethod
    def toPrintString(cls,someobj):
        '''
        Will be useful when printing to a jinga template
        '''
        currtype = str(type(someobj)).lower()
        if currtype.find('list')!=-1 or currtype.find('set')!=-1:
            toret = ''
            for item in cls.convertToRegularList(someobj):
                toret = toret + item +', '
            return toret
        else:
            return str(someobj)
