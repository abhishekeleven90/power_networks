#search function

from collections import defaultdict
import jellyfish as jf
import pandas as pd
import sys
from time import time

def is_similar(text1,text2,thres = 0.6,algo = jf.jaro_distance):

    if text1 == text2 :
        return True
    elif algo(text1,text2) >= thres :
        #print 'jaro distance -'+str(jf.jaro_distance(text1,text2))
        return True
    else:
        return False

def search_query(query,df,col="Party",thres = 0.9):

    df_new = pd.DataFrame(columns = df.columns)
    row_added = 0
    for i,r in df.iterrows():
        t1 = r[col]
        if is_similar(query,t1,thres ):
            print "[search]- Got match {} -- {}".format(query,t1)
            df_new.loc[row_added] = df.ix[i] 
            row_added += 1


    return df_new

