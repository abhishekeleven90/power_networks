import requests as rq
from collections import OrderedDict
from time import time
import ast
import re
import urllib

def get_uuid_phonetic(propname=None,propvalue=None,label = None,is_phonetic = False):

    default_url = "http://10.237.27.87:8983/solr/mtp/select?q=*%3A*&wt=python&rows=50000&indent=true"
    
    if label == None:
        print "[get_uuid_phonetic] - No label-returning empty uuid list"
        return []

    if propvalue == None or propname == None:
        print "[get_uuid_phonetic] - No propname/ provalue-returning empty uuid list"
        return []

    else:
        base_url = "http://10.237.27.87:8983/solr/mtp/select?q="
        rest_url = "&wt=python&rows=50000&indent=true"
        if is_phonetic: propvalue_str = '+AND+phonetic%3A('+urllib.quote_plus(propvalue)+')'
        else: propvalue_str = '+AND+propvalue%3A(%2B'+urllib.quote_plus(propvalue)+')'
        label_str = 'label%3A'+label
        propname_str = '+AND+propname%3A'+propname
        arg_url = label_str+propname_str+propvalue_str
        req_url = base_url+arg_url+rest_url

    print "## Requesting to Solr ... "
    print "## Request url ..."+req_url
    r = rq.get(req_url)
    d = ast.literal_eval(r.text)
    n_results = d['response']['numFound']
    docs = d['response']['docs']
    uuid_list = []
    
    for doc in docs:
    #    if doc['uuid'] not in uuid_list:
         uuid_list.append(doc['uuid'])

    print "##[get_uuid] - Time taken after append-{} s".format(time() - t)
    uuid_list = list(OrderedDict.fromkeys(uuid_list))
    print "##[get_uuid] - Time taken after removing duplicates-{} s".format(time() - t)
    print "##UUid list length -{}".format(len(uuid_list))

    return uuid_list

def get_uuid_spellcheck(propname=None,propvalue=None,label=None):
    
    if label == None:
        print "[get_uuid_spellcheck] - No label-returning empty uuid list"
        return []
    
    if propvalue == None or propname == None:
        print "[get_uuid_spellcheck] - No propname/ propvalue-returning empty uuid list"
        return []
    
    else:

        base_url = "http://10.237.27.87:8983/solr/mtp/select?wt=python&indent=true&spellcheck=true&spellcheck.q="
        propvalues = re.findall("[\w']+",propvalue)
        assert '' not in propvalues
        arg_url = '+'.join(propvalues)
        req_url = base_url+arg_url

    print "## Requesting to Solr ... "
    print "## Request url ..."+req_url
    r = rq.get(req_url)
    d = ast.literal_eval(r.text)
    n_results = d['spellcheck']['suggestions']
    sugg_list = []
    
    for suggestion in d:
        if type(suggestion) == dict:
            sugg_list = sugg_list+suggestion["suggestion"]

    #now remove duplicates
    sugg_list = list(OrderedDict.fromkeys(sugg_list))
    uuid_list = []
    for s in sugg_list:
        uuid_list = uuid_list + get_uuid(propname=propname,propvalue = s) 

    #as always, remove dupicates
    uuid_list = list(OrderedDict.fromkeys(uuid_list))

    return uuid_list

def get_uuid(propname,propvalue,label):

    uuids1 = get_uuid_phonetic(propname=propname,propvalue = propvalue,label = label,is_phonetic=True)
    #uuids2 = get_uuid_spellcheck(propname=propname,propvalue = propvalue,label = label)
    results = uuids1
    results = list(OrderedDict.fromkeys(results))

    return results

def get_uuid_helper(prop_names,prop_values,label):
    results = []
    i = 0
    for pN,pV in zip(prop_names,prop_values):
        l = get_uuid(propname =pN,propvalue = pV,label = label)
        #print "##Prnting output list- get_uuid "
        #print l
        print "##Num items found - [get_uuid_helper] "
        print len(l)

        if i == 0: results = [x for x in l]
        else: results = [x  for x in results if x in l]
        i = i+1
       

    return results

if __name__=="__main__":
    #l = get_uuid()
    #print l
    test_lab = 'businessperson'
    test_propN  = ['name'] ##be careful! it takes the order of the first property!
    test_propV = ['mr gautam adani']
    #test_thres = ['0.2','0.5']
    t = time()
    res = get_uuid_helper(test_propN,test_propV,test_lab)
    #print "##Final result:-"
    print "##Num items found - [final] "
    print len(res)
    #print res
    print "##Total time taken-{} s".format(time() - t)

