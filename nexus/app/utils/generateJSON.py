'''
This file generates JSON from CSV files
'''
import json
import pandas as pd
from collections import defaultdict
import ast
import formatFields
from termcolor import colored

id = 0

def getNextID():
    global id
    id += 1
    return id

rid = 0

def getNextRID():
    global rid
    rid +=1
    return rid

def getField(dic, key, by=''):

    try:
        v = dic[key]
    except KeyError as e:
        import traceback
        print traceback.format_exc()
        print repr(e)
        return ''

    else:
        if by == 'date':
            v = formatFields.getTimeStampLong(v)
        elif by == 'name':
            v = formatFields.formatName(v)

        return str(v)

def getSelfEntity(JSONstr, sourceurl, labels, fetchdate, i):

    d = ast.literal_eval(JSONstr)
    d = dict((k.strip().lower(), v) for k, v in d.iteritems())
    entity = defaultdict()
    entity["id"] = str(getNextID())
    entity["sourceurl"] = sourceurl
    entity["fetchdate"] = fetchdate
    entity["labels"] = labels[:] # make a copy of the list so that same reference is not updated
    entity["labels"].append("person")
    entity["labels"].append("politician")

    #get the properties of object
    #check all the field names and if possible change all keys to lower case
    properties = defaultdict()
    properties["name"] = getField(d, "name", by='name')
    properties["profession"] = getField(d, "profession")
    properties["dob"] = getField(d, "date of birth")
    properties["education"] = getField(d, "educational qualifications")
    properties["startplace"] = getField(d, "place of birth")
    properties["iscurrent"] = str(True)
    properties["rawdatainternalid"] = str(i)
    properties["address"] = [(getField(d, "permanent address"))]
    properties["startdate"] = getField(d, "date of birth", by='date')

    entity["properties"] = properties

    return entity

def isBidirectional(field):
    
    bidirectional_fields = ["spouse's name"]
    if field in bidirectional_fields:
        return True
    return False

def getRelLabel(field):

    field_class1 = ["mother's name", "father's name", "spouse's name"]
    #FIXME - constituency label??
    field_class2 = [ "constituency :"]

    if field in field_class1:
        return "relatedto"
    elif field in field_class2:
        return "contestedfrom"
    else: return "defaultlabel"
        
def getRelProps(field, independent="False"):

    props = defaultdict()
    parent_class = ["mother's name", "father's name"]
    spouse_class = ["spouse's name"]
    #FIXME - constituency label?
    institute_class = ["constituency :"]

    if field in parent_class:
        kind = "childof"
        if field == "mother's name":
            subkind = "hasmother"
        else:
            subkind = "hasfather"
        return dict(kind=kind, subkind=subkind)
    elif field in spouse_class:
        kind = "spouseof"
        return dict(kind=kind)
    else:
        kind, result, asindependent = "ls2014", "won", independent
        return dict(kind=kind, result=result, asindependent=asindependent)

    return dict()

def getRelatedEntities(JSONstr, entity, sourceurl, fetchdate, labels):

    # fields list with whom entity has a rel
    #FIXME - maybe the list is inputted as a param??
    fields_list = ["mother's name", "father's name", "spouse's name"
            , "constituency :"]

    baseEntityId = entity["id"]
    d = ast.literal_eval(JSONstr)
    d = dict((k.strip().lower(), v) for k, v in d.iteritems())

    #TODO - for all entries in list
    e_list, r_list = [], []
    for f in fields_list:
        #TODO - fill up entity table with props
        name = getField(d, f, by='name')
        if name == "":
            print colored("No field- {} ".format(f), 'red', attrs=['bold'])
            print colored("Skipping it!", 'red', attrs=['bold'])
            continue
        rid = getNextID()
        r_entity = defaultdict()
        r_entity["sourceurl"] = sourceurl
        r_entity["fetchdate"] = fetchdate
        r_entity["id"] = str(rid)
        r_entity["labels"] = labels[:] # make a copy to avoid same reference problem

        if f == "constituency :":
            r_entity["labels"].append('constituency')
        else: r_entity["labels"].append('person')

        ##entity props
        properties = defaultdict()
        properties["name"] = name 
        r_entity["properties"] = properties
        
        e_list.append(r_entity)

        #TODO - fill relationship table with props
        relation = defaultdict()
        relation["sourceurl"] = sourceurl
        relation["fetchdate"] = fetchdate
        relation["id"] = str(getNextRID())
        relation["start_entity"] = baseEntityId
        relation["end_entity"] = r_entity["id"]
        relation["label"] = getRelLabel(f)
        relation["bidirectional"] = str(isBidirectional(f))
        relation["properties"] = getRelProps(f)
        
        r_list.append(relation)

    #TODO - return entity list and rel list
    return e_list, r_list


def generateJSON(df):
    #TODO - for each row politician
    import time
    e_list, r_list = [], []
    df2 = df[1:2]
    for i, r in df2.iterrows():

        # create self entity
        properties = r['props']
        sourceurl, fetchdate = 'www.abc123.com', time.time()
        self_entity = getSelfEntity(properties, sourceurl,['entity'], str(fetchdate), i)

        #TODO - create list of related entities and relations
        related_entities, relations = getRelatedEntities(properties,
                                        self_entity, sourceurl, str(fetchdate), labels=['entity'])

        entities = related_entities
        entities.append(self_entity)
        e_list += entities
        r_list += relations
        print colored("Processing {} of {}".format(i,len(df2)), 'red', attrs=['bold'])

    #TODO - wrap up in higher order obj
    #FIXME - use function params for taskid, userid later?
    result = dict(taskid=1, userid="abhi2@gmail.com", token="token2",
                  entities=e_list, relations=r_list)

    #TODO - convert obj to json and return
    return json.dumps(result)
    
if __name__ == "__main__":
    
    INPUT_DIRECTORY = './'
    df = pd.read_csv(INPUT_DIRECTORY + "L_output.csv")
    data= generateJSON(df)
    obj = open("data.json", "wb")
    obj.write(data)
    obj.close()

