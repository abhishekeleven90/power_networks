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

def deduper1(df, key_field, rest_fields):

    df_len = len(df)
    df = df.sort(columns=key_field)
    print "[deduper]- Sorted df"
    print df
    df.to_csv("test_sorted_df.csv")
    table = []
    row_added = 0
    row_added_dup =0
    df_new = pd.DataFrame()
    df1_new_dup = pd.DataFrame(columns = df.columns)
    df2_new_dup = pd.DataFrame(columns = df.columns)
    df1_new = pd.DataFrame(columns = df.columns)
    df2_new = pd.DataFrame(columns = df.columns)

    df_list =[]
    df_list_dup = []
    #Generator element to get the index
    gen = df.iterrows()
    #Adding the first element
    print "Adding first element"
    prev_index,prev_row = gen.next()
    df1_new.loc[0] = df.ix[prev_index]
    #df2_new.loc[0] = df.ix[prev_index]
    #df1_new['dupno'] = row_added
    #df2_new['dupno'] = row_added
    row_added += 1
    #df_new = pd.merge(df1_new,df2_new,on='dupno')
    #df_list.append(df_new)
    df_list.append(df1_new)

    for i in range (df_len -1 ):
        new_index, new_row = gen.next()
        key1 = df[key_field][prev_index]
        key2 = df[key_field][new_index]
    
        if (can_join(key1,key2,thres = 0.9, algo = jf.jaro_distance) ):
            print "[deduper]- Possible match {} -- {}".format(key1,key2)


            join = True
            for r in rest_fields:
                key3 = df[r][prev_index]
                key4 = df[r][new_index]
                print "Checking rest fields - {} -- {}".format(key3,key4)
                if (key3 == key4): #if rest is same then dont join it is a duplicate
                    print "[deduper] - {} matches. Possible duplicate {}--{}".format(r,key1,key2)
                    join = False
                    break

            if join:
            
                print "[deduper]- joining {} -- {}".format(key1,key2)
                df1_new_dup.loc[0] = df.ix[prev_index]
                df2_new_dup.loc[0] = df.ix[new_index]
                df1_new_dup['dupno'] = row_added_dup
                df2_new_dup['dupno'] = row_added_dup
                row_added_dup += 1
                df_new = pd.merge(df1_new_dup,df2_new_dup,on='dupno')
                df_list_dup.append(df_new)

        else:
            print "[deduper]-New name found- "+key2
            print "[deduper]- Compared with- " +key1
            df1_new.loc[row_added] = df.ix[new_index]
            #df1_new.loc[0] = df.ix[new_index]
            #df2_new.loc[0] = df.ix[new_index]
            #df1_new['dupno'] = row_added
            #df2_new['dupno'] = row_added
            row_added += 1
            #df_new = pd.merge(df1_new,df2_new,on='dupno')
            #df_list.append(df_new)
            #df_list.append(df1_new)
        prev_index = new_index


    print "[deduper] - Deduping done -forming  unique  DataFrame"
    if (row_added > 0):
        df_ret = df1_new
        #df_ret = pd.concat(df_list,axis=0,ignore_index =True)
    else:
        print "[deduper]- No unique rows"
        df_ret = pd.DataFrame()

    print "[deduper]- Forming duplicates DataFrame"
    if row_added_dup > 0:
        df_ret_dup = pd.concat(df_list_dup,axis=0,ignore_index =True)
    else:
        print "[deduper]- No duplicates"
        df_ret_dup = pd.DataFrame()

    print "[deduper] - Done!!"
    return (df_ret,df_ret_dup)

def deduper(df, key_field, rest_fields):

    df_len = len(df)
    #df = df.sort(columns=key_field)
    #print "[deduper]- Sorted df"
    #print df
    row_added = 0
    df_new = pd.DataFrame()
    df1_new = pd.DataFrame(columns = df.columns)
    df2_new = pd.DataFrame(columns = df.columns)

    df_list =[]

    for i in range (df_len ):
        for j in range(df_len):
            key1 = df[key_field][i]
            key2 = df[key_field][j]
        
            if (can_join(key1,key2,thres = 0.9, algo = jf.jaro_distance) ):
                print "[deduper]- Possible match {} -- {}".format(key1,key2)
                join = True
                for r in rest_fields:
                    key3 = df[r][i]
                    key4 = df[r][j]
                    print "Checking rest fields - {}--{}".format(key3,key4)
                    if (key3 == key4): #if rest is same then dont join it is a duplicate
                        print "[deduper] - {} matches. Possible duplicate {}--{}".format(r,key1,key2)
                        join = False
                    break

                if join:
                
                    print "[deduper]- joining {} -- {}".format(key1,key2)
                    df1_new.loc[0] = df.ix[i]
                    df2_new.loc[0] = df.ix[j]
                    df1_new['dupno'] = row_added
                    df2_new['dupno'] = row_added
                    row_added += 1
                    df_new = pd.merge(df1_new,df2_new,on='dupno')
                    df_list.append(df_new)
            
   
    print "[deduper] - Dedupling done -forming result DataFrame"
    if (row_added > 0):
        df_ret = pd.concat(df_list,axis=0,ignore_index =True)

    print "[deduper] - Done!!"
    return df_ret

def test_resolver():
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
    df.to_csv("resolver_output.csv")
    print "[main]- Complete"

    return

def test_deduper():

    filename = sys.argv[1]
    
    inp_file = pr.resource_filename('src.input',filename)
    inp_df = pd.read_csv(inp_file)
    inp_df['name'] = inp_df.apply(lambda r: name_preprocess(r['name']),axis =1)
    #inp_df['id'] = inp_df1.apply(lambda r: preprocess(r['state']),axis =1)

    start = time()
    #if passing tuple of df objs is difficult - dump to csv directly in deduper1 function
    df,df_dup = deduper1(inp_df,'name',['cid'])
    end = time()
    print "[main]- deduping complete"
    print "[main]-Time taken- " + str(end - start)
    
    print df_dup
    print "[main] -Dumping to file"
    df.to_csv("deduper_output.csv")
    df_dup.to_csv("deduper_dup_output.csv")
    print "[main]- Complete"


if __name__=='__main__':

    #test_resolver()
    test_deduper()

