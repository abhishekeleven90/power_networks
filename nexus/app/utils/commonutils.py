class Utils:

    def __init__(self):
        pass

    @classmethod
    def processString(cls, currvalue):
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

    @classmethod
    def copyListOfStrings(cls, listofstr):
        ret = []
        for val in listofstr:
            val = cls.processString(val)
            ret.append(val)
        return ret

    @classmethod
    def copyList(cls, somelist):
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
        if len(cls.processString(givenstr))==0:
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

    @classmethod
    def convertToList(cls, val):
        '''
            checks type and if type not list
            converts to a list, useful before merge
        '''
        valtype = type(val)
        toreturn = []
        if valtype is not list:
            toreturn.append(str(val).strip())
        else:
            for item in val:
                toreturn.append(str(item).strip())
        return toreturn

    @classmethod
    def merge(cls, origval, newval):
        '''
            merges anything : you finally get a list of strings
            tries to remove duplicates
            note: call only after you have validated if you have to merge or not
        '''

        origval = cls.convertToList(origval)
        newval = cls.convertToList(newval)

        copyorig = cls.copyListOfStrings(origval)
        toappend = []

        for val in origval:
            toappend.append(str(val).strip())

        for val in newval:
            copycurrval = cls.processString(val)
            if copycurrval not in copyorig:
                toappend.append(str(val).strip()) ##converted val to string as list of strings!
        return toappend

    @classmethod
    def strType(cls,val):
        if type(val) is list:
            return 'list' ##else returns "<type 'list'>"
        if type(val) is int:
            return 'int'
        if type(val) is long:
            return 'long'
        if type(val) is str or type(val) is unicode:
            return 'str'
        if type(val) is bool:
            return 'bool'
        return 'unknown'

    @classmethod
    def convertListToSearchCSV(cls, list):
        toreturn = " "
        quotes = "'"
        space = ' '
        for val in list:
            currval = cls.processString(val)
            toreturn = toreturn + quotes + currval + quotes + space
        return toreturn

    @classmethod
    def csvtolist(cls, csv):
        somelist = csv.split(',')
        return cls.convertToList(somelist)
