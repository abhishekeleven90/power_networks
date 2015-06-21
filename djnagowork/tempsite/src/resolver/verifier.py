"""
Module - Verifier

flist1, flist2 - fieldname lists
filename - the csv file to read
Returns new df with verification column
"""

def verify(filename,flist1,flist2):

    df = pd.read_csv(filename)

    assert(flist1 == flist2)
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
