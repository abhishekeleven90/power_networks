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
import pkg_resources as pr
import sys
from time import time
from src.cleaner.preprocess import name_preprocess
from src.cleaner.preprocess import preprocess

def can_join(text1,text2,thres = 0.6,algo = jf.jaro_distance):

    if text1 == text2 :
        return True
    elif algo(text1,text2) >= thres :
        #print 'jaro distance -'+str(jf.jaro_distance(text1,text2))
        return True
    else:
        return False

def custom_merge_rows(df, df1_fields,df2_fields,thres = 0.6,algo = jf.jaro_distance):

    print "[custom_merge_rows]-threshold-"+str(thres)
    df_ret = df
    for f in range(len(df1_fields)):
        df_new = pd.DataFrame(columns = df_ret.columns)
        df_list = []
        row_added = 0
        for i,r in df_ret.iterrows():
            key1 = df_ret[df1_fields[f]][i]
            key2 =  df_ret[df2_fields[f]][i]
            if can_join(key1,key2,thres,algo):
                print "[custom_merge_rows]- Got match {}--{}".format(key1,key2)
                df_new.loc[row_added] = df_ret.ix[i]
                row_added += 1

        df_list.append(df_new)
        if row_added == 0:
            print "Breaking the loop"
            print "# field-iterations "+str(f)
            print "Last field checked - "+"Field 1 ="+df1_fields[f]+" Field 2="+df2_fields[f]

            break
        else:
            df_ret = pd.concat(df_list,ignore_index = True)

    return df_ret



def custom_merge(df1,df2,df1_field,df2_field,thres = 0.6,algo=jf.jaro_distance):

    #do a nested loop join on df1 df2
    print "[custom_merge]- threshold -"+str(thres)
    if df1_field not in df1.columns:
        print df1_field+" should be present in dataframe 1"
        sys.exit(1)

    if df2_field not in df2.columns:
        print df2_field+" should be present in dataframe 2"
        sys.exit(1)

    df_columns = df1.columns + df2.columns
    df = pd.DataFrame()

    df_new = pd.DataFrame()
    df1_new = pd.DataFrame(columns = df1.columns)
    df2_new = pd.DataFrame(columns = df2.columns)

    df_list = []
    row_added = 0

    for i1,row1 in df1.iterrows():
        for i2,row2 in df2.iterrows():

            key1 = df1[df1_field][i1]
            key2 = df2[df2_field][i2]

            if can_join(key1,key2,thres,algo):

                print "Got match {} -- {}".format(key1,key2)
                df1_new.loc[0] = df1.ix[i1]
                df2_new.loc[0] = df2.ix[i2]
                df1_new['dupno']=row_added
                df2_new['dupno'] = row_added
                df_new = pd.merge(df1_new,df2_new,on='dupno')
                row_added += 1
                df_list.append(df_new)

    if not df_list:
        return df
    df  = pd.concat(df_list,ignore_index=True)
    return df


def resolver(df1,df2,flist1,flist2, thres_list,algo=jf.jaro_distance):

    assert (len(flist1) == len(flist2))
    assert(len(flist1) == len(thres_list))
    assert(len(flist1) != 0)

    cols_df1 = list(df1.columns)
    cols_df2 = list(df2.columns)
   
    print "[resolver]- joining on first field"
    df=  custom_merge(df1,df2,flist1[0],flist2[0],thres=thres_list[0])
    
    if(len(df) == 0):
        return df

    print "[resolver] - resolving done on first field - rowwise join on rest fields"
    df = custom_merge_rows(df,df1_fields=flist1[1:],df2_fields=flist2[1:],thres=thres_list[1])
    print "[resolver] - complete!!"
    return df


if __name__=='__main__':

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    
    inp_file1 = pr.resource_filename('src.input',filename1)
    inp_file2 = pr.resource_filename('src.input',filename2)
    inp_df1 = pd.read_csv(inp_file1)
    inp_df2 = pd.read_csv(inp_file2)
    inp_df1['name'] = inp_df1.apply(lambda r: name_preprocess(r['name']),axis =1)
    inp_df1['state'] = inp_df1.apply(lambda r: preprocess(r['state']),axis =1)
    inp_df2['Candidate'] = inp_df2.apply(lambda r: name_preprocess(r['Candidate']),axis =1)
    inp_df2['State'] = inp_df2.apply(lambda r: preprocess(r['State']),axis =1)

    start = time()
    df = resolver(inp_df1, inp_df2,flist1=['name','state'], flist2=['Candidate','State'],thres_list = [0.85,0.9])
    end = time()
    print "[main]- Resolving complete"
    print "[main]-Time taken- " + str(end - start)
    
    print df
    print "[main] -Dumping to file"
    df.to_csv("join_df_output.csv")
    print "[main]- Complete"
