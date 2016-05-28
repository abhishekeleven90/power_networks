#Get the names of city and state from Google and dump 
#to 'city_state.csv'


import locprocess
import pandas as pd
from termcolor import colored

df = pd.read_csv('cities_all.csv')
dict_list, error_list = [], []
df_len = len(df)

for i, r in df.iterrows():
    print "Processing {} of {}".format(i, df_len)
    address = ' '.join([r['state'], r['city']])
    print "Address used- {}".format(address)

    try:
        city, state = locprocess.getCityState(address)
    except IndexError as e:
        print colored("Error - {}".format(e), 'red')
        err_dict = {"ID": r['ID'], "address_used": address, "error": e}
        error_list.append(err_dict)
    else:
        loc_dict = {"city": city, "state": state, "ID": r['ID'], "SID": r['SID']}
        dict_list.append(loc_dict)

print "Generated city, state names from Google"
df_new = pd.DataFrame(dict_list)
df_err = pd.DataFrame(error_list)
print df_new
df_new.to_csv('city_state.csv')
df_err.to_csv('city_state_err.csv')
