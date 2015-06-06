
from collections import defaultdict
import jellyfish as jf
import pandas as pd

def can_join(text1,text2,thres = 0.6):

    if text1 == text2 :
        return True
    elif jf.jaro_distance(text1,text2) >= thres :
        #print 'jaro distance -'+str(jf.jaro_distance(text1,text2))
        return True
    else:
        return False


def custom_merge(df1,df2,df1_field,df2_field,thres = 0.6):

    #do a nested loop join on df1 df2

    if df1_field not in df1.columns:
        print df1_field+" should be present in dataframe 1"
        exit(1)

    if df2_field not in df2.columns:
        print df2_field+" should be present in dataframe 2"
        exit(1)

    df_columns = df1.columns + df2.columns
    df = pd.DataFrame()

    df_list = []
    for i1,row1 in df1.iterrows():
        for i2,row2 in df2.iterrows():

            key1 = df1[df1_field][i1]
            key2 = df2[df2_field][i2]

            if can_join(key1,key2):

                dictionary = defaultdict(list)
                for c in df1.columns:
                    dictionary[c].append(df1[c][i1])
                for c in df2.columns:
                    dictionary[c].append(df2[c][i2])
                    
                df_new = pd.DataFrame(dictionary, columns = df_columns)
                df_list.append(df_new)

    
    df  = pd.concat(df_list,ignore_index=True)
    return df


