"""
Module - Verifier

flist1, flist2 - fieldname lists
filename - the csv file to read
Returns new df with verification column
"""
import pandas as pd
import sys

def verify(df,flist1,flist2):

    assert(len(flist1) == len(flist2))
    resp = ''
    resp_list=[]
    for i,r in df.iterrows():

        print "Are these entities same??"

        for i,j in zip(flist1,flist2):

            print "1: "+i+" {}".format(r[i])
            print "2: "+j+" {}".format(r[j])

        while True:
            print "yes(y) / no(n) / unsure(u) ?"
            resp = raw_input()
            if resp.strip().lower()  in ['y','yes','n','no','unsure','u']:
                break
            print "Can't get you..."

        print "Your response - {} ....".format(resp)

        resp_list.append(resp)

    df['verification'] = pd.Series(resp_list)

    return df

if __name__=="__main__":

    filename = sys.argv[1]
    #inp_file = pr.resource_filename('')
    df = pd.read_csv(filename)
    flist1 = ['name_x','cid_x']
    flist2 = ['name_y','cid_y']
    df_new = verify(df,flist1,flist2)

    df_new.to_csv("verified_"+filename)

