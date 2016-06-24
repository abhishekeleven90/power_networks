'''
This file generates JSON from CSV files
Key things to make the genrator flexible -
fields = list of fields to look after to create relationships
field classes = this is reqd to give respective relationship labels and props
property names = list of fields to look after as a property for the base user
data row = data rows can be a json string or a Series in pandas
'''
import json
import pandas as pd
from collections import defaultdict
import ast
import formatFields
from termcolor import colored

id = 0

def getNextID():
    ''' Indirectly get the next value of id global '''
    global id
    id += 1
    return id

rid = 0

def getNextRID():
    ''' Indirectly get the next value of rid global (relations) '''
    global rid
    rid +=1
    return rid

def getField(dic, key, by=''):
    ''' Get field according to the key given. Return '' if no key of that name '''
    try:
        v = dic[key]
    except KeyError as e:
        import traceback
        print traceback.format_exc()
        print repr(e)
        return ''

    else:
        try:
            if by == 'date':
                v = formatFields.getTimeStampLong(v)
            elif by == 'name':
                v = formatFields.formatName(v)

            return str(v)
        except UnicodeEncodeError as ud:
            import traceback
            print traceback.format_exc()
            print repr(ud)
            v = v.encode('ascii', 'ignore')
            print colored("Encoding error. Returning as -{}".format(str(v)),
                          'red', attrs=['bold'])
            return str(v)

def getDictFromRow(row):
    ''' Returns a dict from row of the table '''

    d = ast.literal_eval(row)
    d = dict((k.strip().lower(), v) for k, v in d.iteritems())
    return d

def getSelfEntity(row, sourceurl, labels, fetchdate, i):
    ''' Create the base entity here with all its properties '''

    d = getDictFromRow(row)
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
    ''' Generate labels according to classes the field belong to'''
    field_class1 = ["mother's name", "father's name", "spouse's name"]
    #FIXME - constituency label??
    field_class2 = [ "constituency :"]

    if field in field_class1:
        return "relatedto"
    elif field in field_class2:
        return "contestedfrom"
    else: return "defaultlabel"
        
def getRelProps(field, independent="False"):
    ''' Get relationship properties as per classes of fields '''
    parent_class = ["mother's name", "father's name"]
    spouse_class = ["spouse's name"]
    #FIXME - constituency label?
    institute_class = ["constituency :"]

    if field in parent_class:
        kind = "ischildof"
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


def getRelatedEntities(row, entity, sourceurl, fetchdate, labels):
    ''' According to fields list generate all related entities and their relations '''

    # fields list with whom entity has a rel
    #FIXME - maybe the list is inputted as a param??
    fields_list = ["mother's name", "father's name", "spouse's name"
            , "constituency :"]

    baseEntityId = entity["id"]
    d = getDictFromRow(row)

    # - for all entries in list
    e_list, r_list = [], []
    for f in fields_list:
        # - fill up entity table with props
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

        # - fill relationship table with props
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

    # - return entity list and rel list
    return e_list, r_list


def generateJSON(df):
    # - for each row politician
    import time
    e_list, r_list = [], []
    df2 = df
    for i, r in df2.iterrows():

        # create self entity
        properties = r['props']
        sourceurl = 'http://loksabha.nic.in'
        fetchdate = formatFields.getTimeStampLong('22 Jun 2016')
        self_entity = getSelfEntity(properties, sourceurl, ['entity'], str(fetchdate), i)

        # - create list of related entities and relations
        related_entities, relations = getRelatedEntities(properties,
                                        self_entity, sourceurl, str(fetchdate), labels=['entity'])

        entities = related_entities
        entities.append(self_entity)
        e_list += entities
        r_list += relations
        print colored("Processing {} of {}".format(i,len(df2)), 'red', attrs=['bold'])

    # - wrap up in higher order obj
    #FIXME - use function params for taskid, userid later?
    result = dict(taskid=4, userid="amartyaamp@gmail.com", token="103a5b7dc528b08d4eeacde292a18b69",
                  entities=e_list, relations=r_list)

    # - convert obj to json and return
    return json.dumps(result)
    
if __name__ == "__main__":
    
    INPUT_DIRECTORY = '/home/amartyac/AlgoPractice/scrapy/L_R_Sabha/'
    df = pd.read_csv(INPUT_DIRECTORY + "L_output.csv")
    data= generateJSON(df)
    obj = open("data.json", "wb")
    obj.write(data)
    obj.close()
