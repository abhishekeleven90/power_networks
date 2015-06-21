#resolver function

"""
Function -  resolver
Input - 
df1,df2 - dataframe to join
flist1,flist2 - list of features to compare should be in order
thres_list - list of thresholds
Remark - should be called from another python module
"""

from collections import defaultdict
import jellyfish as jf
import pandas as pd

def can_join(text1,text2,thres = 0.6,algo = jf.jaro_distance):

    if text1 == text2 :
        return True
    elif algo(text1,text2) >= thres :
        #print 'jaro distance -'+str(jf.jaro_distance(text1,text2))
        return True
    else:
        return False


def custom_merge(df1,df2,df1_field,df2_field,thres = 0.6,algo=jf.jaro_distance):

    #do a nested loop join on df1 df2

    if df1_field not in df1.columns:
        print df1_field+" should be present in dataframe 1"
        exit(1)

    if df2_field not in df2.columns:
        print df2_field+" should be present in dataframe 2"
        exit(1)

    df_columns = df1.columns + df2.columns
    df = pd.DataFrame()

    df_new = pd.DataFrame()
    df1_new = pd.DataFrame()
    df2_new = pd.DataFrame()

    df_list = []
    row_added = 0

    for i1,row1 in df1.iterrows():
        for i2,row2 in df2.iterrows():

            key1 = df1[df1_field][i1]
            key2 = df2[df2_field][i2]

            if can_join(key1,key2,thres,algo):

                print "Got match {} -- {}".format(key1,key2)
                df1_new.ix[0] = df1.ix[i1]
                df2_new.ix[0] = df2.ix[i2]
                df1_new['dupno']=row_added
                df2_new['dupno'] = row_added
                df_new = pd.merge(df1_new,df2_new,on='dupno')
                #dictionary = defaultdict(list)
                #column_list = []
                #for c in df1.columns:
                #    s = c+'_df1' #done so that both the dataframes have unique column names
                #    dictionary[s].append(df1[c][i1])
                #    column_list.append(s)
                #for c in df2.columns:
                #    s = c+'_df2'#done so that both the dataframes have unique column names
                #    dictionary[s].append(df2[c][i2])
                #    column_list.append(s)
                    
                #df_new = pd.DataFrame(dictionary, columns = column_list)
                row_added += 1
                df_list.append(df_new)

    if not df_list:
        return df
    df  = pd.concat(df_list,ignore_index=True)
    return df


def resolver(df1,df2,flist1,flist2, thres_list,algo=jf.jaro_distance):

    assert (len(flist1) == len(flist2))
    assert(len(flist1) == len(thres_list))

    cols_df1 = list(df1.columns)
    cols_df2 = list(df2.columns)

    for i in range(len(flist1)):

        df = custom_merge(df1,df2,flist1[i],flist2[i],thres_list[i],algo)
        df1 = df[cols_df1]
        df2 = df[cols_df2]

    return df

