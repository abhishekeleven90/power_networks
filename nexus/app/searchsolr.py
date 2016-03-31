import requests as rq
import ast

def get_uuid(propname=None,propvalue=None):
    default_url = "http://localhost:8983/solr/mtp/select?q=*%3A*&wt=python&rows=1000&indent=true"
    if propvalue == None:
        req_url = default_url
    else:
        req_url = "http://localhost:8983/solr/mtp/select?q=propvalue%3A"+propvalue+"~0.2+AND+propname%3A"+propname+"&wt=python&rows=1000&indent=true"
    r = rq.get(req_url)
    print type(r.text)
    print r.text
    d = ast.literal_eval(r.text)
    n_results = d['response']['numFound']
    docs = d['response']['docs']
    uuid_list = set()
    for doc in docs:
        uuid_list.add(doc['uuid'])

    return list(uuid_list)

if __name__=="__main__":
    l = get_uuid()
    print l
    l1 = get_uuid('candidate','navn')
    print l1
