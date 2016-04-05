import requests as rq
from collections import OrderedDict
from time import time
import ast

def get_uuid(propname=None,propvalue=None,thresvalue=None,label = None):
    default_url = "http://10.237.27.87:8983/solr/mtp/select?q=*%3A*&wt=python&rows=50000&indent=true"
    if thresvalue == None:
        thresvalue = '0.2'
    if label == None:
        label = '*'
    if propvalue == None or propname == None:
        req_url = default_url
    else:

        base_url = "http://10.237.27.87:8983/solr/mtp/select?q="
        rest_url = "&wt=python&rows=50000&indent=true"

        if propname == "name":
            initials = propvalue.split(' ')
            initials = [x+'~'+thresvalue for x in initials]
            const_str = '+AND+propvalue%3A'
            propvalue_str = const_str.join(initials)
            propvalue_str = const_str+propvalue_str
            print "propvalue_str"

        else:
            propvalue_str = '+AND+propvalue%3A'+propvalue+'~'+thresvalue

        label_str = 'label%3A'+label
        propname_str = '+AND+propname%3A'+propname
        arg_url = label_str+propname_str+propvalue_str

        req_url = base_url+arg_url+rest_url

    print "## Requesting to Solr ... "
    print "## Request url ..."+req_url
    r = rq.get(req_url)
    #print type(r.text)
    #print r.text
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

def get_uuid_helper(prop_names,prop_values,thresholds,label):
    results = []
    i = 0
    for pN,pV,tH in zip(prop_names,prop_values,thresholds):
        l = get_uuid(propname =pN,propvalue = pV, thresvalue = tH,label = label)
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
    test_lab = 'company'
    test_propN  = ['name','status' ] ##be careful! it takes the order of the first list!
    test_propV = ['jindal','alive']
    test_thres = ['0.2','0.5']
    t = time()
    res = get_uuid_helper(test_propN,test_propV,test_thres,test_lab)
    #print "##Final result:-"
    #print res
    print "##Num items found - [final] "
    print len(res)
    print "##Total time taken-{} s".format(time() - t)

