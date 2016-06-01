import sys
#given a cypher string return True/False accordingly


def isValidCypher(text):

    if text is None or text =="":
        return False
    if 'match' not in text.lower():
        print "No match keyword in query"
        return False
    if 'return' not in text.lower():
        print "No return keyword in query"
        return False

    invalid_keywords = ['CREATE', 'MERGE', 'DELETE', 'REMOVE', 'SET',
            'INDEX', 'LOAD', 'LOAD CSV', 'CONSTRAINT']

    if any([word.lower() in text.lower() for word in invalid_keywords]):
        print "Your query contains an invalid keyword"
        return False
    return True

if __name__ == "__main__":

    if len(sys.argv) > 1:
        q = sys.argv[1]
    else: q = "match n return n"

    print "Query given - {}".format(q)
    if isValidCypher(q):
        print "Valid query"
    else:
        print "Invalid query"
