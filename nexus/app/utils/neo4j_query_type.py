import requests
import json
from termcolor import colored
from app.constants import CORE_GRAPH_HOST, CORE_GRAPH_PORT, AUTHORIZATION_HASH


def isReadorWrite(query):
    url = "http://" + CORE_GRAPH_HOST + ":" + CORE_GRAPH_PORT +\
          "/db/data/transaction/commit"

    query = "explain "+query  #append an explain keyword to cypher query
    payload = {"statements":
            [{"statement": query}
                ]}

    headers = {
            'accept': "application/json; charset=UTF-8",
            'content-type': "application/json",
            'authorization': AUTHORIZATION_HASH,
            'cache-control': "no-cache",
            }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    res = json.loads(response.text)
    if len(res["errors"]) > 0:
        print colored('Error occured', 'red', attrs=['bold'])
    operatorType_list = []
    plan = res["results"][0]['plan']

    for p in plan.keys():
        if p == "root":
            operatorType_list.append(plan[p]['operatorType'])
        else:
            child = plan[p]
            if len(child) > 0:
                operatorType_list.append(child[0]['operatorType'])

    if "UpdateGraph" in operatorType_list:
        return 1
    else: return 2


if __name__ =="__main__":
    query = "explain match(n) return n"
    if isReadorWrite(query) == 1:
        print "Write"
    else: print "Read"
