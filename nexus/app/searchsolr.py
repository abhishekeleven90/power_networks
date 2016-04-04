import requests as rq
import ast

def get_uuid(propnames=None,propvalues=None,thresvalues=None,label = None):
    default_url = "http://localhost:8983/solr/mtp/select?q=*%3A*&wt=python&rows=1000&indent=true"
    if thresvalues == None:
        thresvalues = ['0.2' for i in range(len(propnames))]
    if label == None:
        label = '*'
    if propvalues == None or propnames == None:
        req_url = default_url
    else:

        base_url = "http://localhost:8983/solr/mtp/select?q="
        rest_url = "&wt=python&rows=1000&indent=true"
        propnames_n_values = zip(propnames,propvalues,thresvalues)

        for propname,propvalue,thresval in propnames_n_values:
            if propname == "name":
                initials = propval.split(' ')
                initials = [x+'~'+thresval for x in initials]
                const_str = '+AND+propvalue%3A'
                propvalue_str = const_str.join(initials)
                propvalue_str = const_str[1:]+propvalue_str
                print "propvalue_str"

            else:
                propvalue_str = '+AND+propvalue%3A'+propvalue+'~'+thresval

            label_str = 'label%3A'+label
            propname_str = '+AND+propname%3A'+propname
            arg_url = label_str+propname_str+propvalue_str

        req_url = base_url+arg_url+rest_url

    print "## Requesting to Solr ... "
    print "## Request url ..."+req_url
    r = rq.get(req_url)
    print type(r.text)
    print r.text
    d = ast.literal_eval(r.text)
    n_results = d['response']['numFound']
    docs = d['response']['docs']
    uuid_list = []
    for doc in docs:
        if doc['uuid'] not in uuid_list:
            uuid_list.append(doc['uuid'])

    print "##UUid list length -{}".format(len(uuid_list))
    return uuid_list

if __name__=="__main__":
    #l = get_uuid()
    #print l
    l1 = get_uuid(['candidate'],['navn'])
    print l1
