#ER module for finding equivalent names

import re

def preprocess(text):
#default preprocessing

    #preprocess 1 : turn text to lower case
    text = text.strip().lower()
    #preprocess 2 : turn all whitespaces (\t , multiple spaces to single space ' ')
    text = re.sub(' +|\t',' ',text)

    return text

def decompose_name(name,reverse = False):

    #removes all salutations and returns first name , second name list
    stopwords = ['sri','dr.','mr.','mrs.','prof.','','ms.','late','lt.','shri','smt.','shrimati','capt.']
    name = preprocess(name)
    name_list = re.split(' +|,|\(|\)',name)
    name_list = [x.strip() for x in name_list]# just to avoid extraneous spaces
    filter_name_list = []

    #removing stopwwords
    for s in name_list:
        if s not in stopwords:
            filter_name_list.append(s)

    if reverse:
        filter_name_list.reverse()
    
    return filter_name_list

def name_preprocess(name,reverse=False):

    name_components = decompose_name(name,reverse)
    return ' '.join(name_components)

if __name__ =="__main__":
    print name_preprocess('Adhalrao Patil,Shri Shivaji')


