class Validate:

    def __init__(self):
        pass

    def isValidNonMetaProp(self, propname):
        if propname[0]=='_' or propname[-1]=='_':
            return False
        return True

    def checkAllPropnamesValid(self, propvaljson):
        for prop in propvaljson:
            if not self.isValidNonMetaProp(prop):
                return False, prop
        return True, None

