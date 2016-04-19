import requests 
import urllib

def update_props():
    delta_url = "http://localhost:8983/solr/mtp/dataimport?command=delta-import&clean=false&optimize=false"
    r = requests.get(delta_url)
    print r.text
    return 

def delete_index(index_id):
    delete_url = "http://localhost:8983/solr/jcg/update/json?wt=json"
    data = {"delete": { "query":"emp_no:1" },"commit": {}}

    r  = requests.post(delete_url,data=data)
    return None

def update_index(index_id,update_type):

    if update_type ==1: update_props()
    else: delete_index(index_id)
