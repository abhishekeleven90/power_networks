import requests as rq
from collections import defaultdict
import pandas as pd
from time import time
import ast
import re
import urllib
import jellyfish as jf
from app.constants import SOLR_CORE, SOLR_HOST, SOLR_PORT

##TODO: use constants, and test with guest.route

def get_uuids(labels=None,name=None,aliases=None,keywords=None,jaro=True):

    default_url="http://10.237.27.87:8983/solr/mtp2/select?q=*%3A*&wt=python&rows=50000&indent=true"
    t = time()

    if labels == None or labels == []:
        print "[get_uuid_solr] - No labels-returning empty uuid list"
        return []

    if name == None:
        print "[get_uuid_solr] - No name-returning empty uuid list"
        return []

    base_url = "http://10.237.27.87:8983/solr/mtp2/select?q="
    rest_url = "&wt=python&rows=50000&indent=true"
    label_str = 'labels%3A('+urllib.quote_plus(' '.join(labels)) + ')'

    if aliases == None or aliases == []: 
        alias_ph_str = '' 
        alias_f_str = ''
    else: 
        alias_ph_str = 'alias_ph%3A('+urllib.quote_plus(' '.join(aliases)) +')'
        aliases_new = []
        for a in aliases:
            aliases_new.append('+'.join([x+'~' for x in re.findall("[\w]+",a)]))

        alias_f_str = 'aliases%3A(' + '+'.join(aliases_new)+')'

    if keywords == None or keywords == []: 
        keyword_str = '' 
    else: 
        keywords_new = []
        for k in keywords:
            keywords_new.append('+'.join([x+'~' for x in re.findall("[\w]+",k)]))
        keyword_str = 'keywords%3A('+ '+'.join(keywords_new) + ')'

    multiValued_str = '+'.join([alias_ph_str,alias_f_str,keyword_str])
    final_query_str = '+AND+'.join([label_str,multiValued_str])

    query = base_url+final_query_str+rest_url
    print "[get_uuid_solr] - printing query "
    print query
    r = rq.get(query)

    d = ast.literal_eval(r.text)
    n_results = d['response']['numFound']
    docs = d['response']['docs']
    uuid_list = []
    df_dic = defaultdict(list)
    
    for doc in docs:
         if jaro:
             df_dic['name'].append(name)
             df_dic['uuid'].append(doc['uuid'])
             alias_list = [re.findall("[ .\w]+",x)[0] for x in doc['aliases']]
             df_dic['score'].append(max([jf.jaro_winkler(x.lower(),name) for x in alias_list])) 
             df = pd.DataFrame(df_dic)
             df = df[df.score > 0.6 ] #take only those rows whose jaro threshold is >= 0.6
             df = df.sort('score',ascending = False)
             uuid_list = list(df.uuid)
         else: uuid_list.append(doc['uuid'])

    print "##printing df"
    #print df[df['uuid'] == '62458']
    print "##[get_uuid] - Time taken  -{} s".format(time() - t)
    print "##[get_uuid_solr]- UUid list length -{}".format(len(uuid_list))

    return uuid_list
 

if __name__=="__main__":
    #l = get_uuid()
    #print l
    test_lab = ['businessperson']
    test_kw = ['power']
    test_name = 'gautam adani'
    test_aliases = ['gautam adani']
    #test_thres = ['0.2','0.5']
    t = time()
    res = get_uuids(labels = test_lab,name = test_name,keywords = test_kw,aliases = test_aliases,jaro=True)
    #print "##Final result:-"
    print "##Num items found - [final] "
    print len(res)
    #print res
    print "##Total time taken-{} s".format(time() - t)

