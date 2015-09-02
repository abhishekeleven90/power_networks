"""

Module -resolve_single_doc
Function - resolve_duplicates in duplicate dataframe.
            Returns duplicates with similar company id.

Function - resolver 
"""
from collections import defaultdict
import pandas as pd
import pkg_resources as pr
import sys


def resolve_dups(df_unique,df_dups):

    dic = defaultdict(int)
    field_dups  = ['cid_y','did_y']
    df_new_dup = pd.DataFrame(columns=field_dups) 
    row =0
    print "[resolve_dups]- resolving ids"
    for i,r in df_dups.iterrows():

        key = r['did_x']
        if(dic.has_key(key)): 
            print "key exists -{} -- {}".format(key,r['did_y'])
            dic[r['did_y']] = dic[key]
        else: 
            print "new key- {} -- {}".format( key,r['did_y'])
            dic[key] = key
            dic[r['did_y']] = dic[key]

        r['did_y'] = dic[r['did_y']]
        df_new_dup.loc[row] = r[field_dups]
        row += 1

    print "[resolve_dups]- resolving done"
    field_unqs = ['cid','did']
    df_new_dup.columns = field_unqs
    df_new_uniq = df_unique[field_unqs];

    dfret = pd.concat([df_new_dup,df_new_uniq],ignore_index = True)
    dfret = dfret.sort(columns = 'did')
    print "[resolve_dups] - Dumping to csv"
    dfret.to_csv("single_doc_resolved.csv")

if __name__== "__main__":


    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    inp_file1 = pr.resource_filename('src.resolver',filename1)
    inp_file2 = pr.resource_filename('src.resolver',filename2)

    dfu = pd.read_csv(inp_file1)
    dfd = pd.read_csv(inp_file2)
    print "[main] - sending for resolution"

    resolve_dups(dfu,dfd)
    print "[main] - complete!"
