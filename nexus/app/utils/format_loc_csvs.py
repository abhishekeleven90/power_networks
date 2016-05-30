import pandas as pd
from termcolor import colored
dfGState = pd.read_csv("./locdata/google_states.csv")
dfAll = pd.read_csv("./locdata/city_state.csv")
tot, e = len(dfAll), 1
df_list, df_err_list = [], []

for i, r in dfAll.iterrows():
    print colored("Processing {} of {}".format(i, tot), 'red', attrs=['bold'])
    if not pd.isnull(r['state']):
        print "State- {}".format(r['state'])
        sid = dfGState[dfGState['state'] == r['state']]
        print sid.iloc[0]['ID']
        name = r['city']
        temp_dict = {'id': i, 'city': name, 'SID': sid.iloc[0]['ID']}
        df_list.append(temp_dict)
    else:
        print colored("State not found!", 'red', attrs=['bold'])
        name = r['city']
        temp_dict2 = {'id': i, 'name': name}
        df_err_list.append(temp_dict2)
    e += 1

df_error = pd.DataFrame(df_err_list)
df_new = pd.DataFrame(df_list)
df_new.to_csv('google_cities.csv')
df_error.to_csv('google_cities_err.csv')
