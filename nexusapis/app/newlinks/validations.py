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

    def validateNodeIsEntityOrHyperedge(self, en):
        required_en_labels_disjoint = ['entity','hyperedgenode']
        nodelabels = en['labels']
        count = 0
        for label in required_en_labels_disjoint:
            if label in nodelabels:
                count = count + 1
        return (count == 1)


