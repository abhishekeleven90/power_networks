"""
Module - Political corporate ER
Resolves political - corporate by dedupe library
"""

from collections import defaultdict
import os
import re
import logging
import optparse
import numpy
import sys
import dedupe
from unidecode import unidecode
from src.cleaner.preprocess import name_preprocess
from src.cleaner.preprocess import preprocess
import pandas as pd
import pkg_resources as pr

#common file names

output_file = 'data_matching_output.csv'
settings_file = 'data_matching_learned_settings'
training_file = 'data_matching_training.json'

def setLogging():

    # ## Logging

    # dedupe uses Python logging to show or suppress verbose output. Added for convenience.
    # To enable verbose logging, run `python examples/csv_example/csv_example.py -v`
    optp = optparse.OptionParser()
    optp.add_option('-v', '--verbose', dest='verbose', action='count',
                    help='Increase verbosity (specify multiple times for more)'
                     )
    (opts, args) = optp.parse_args()
    log_level = logging.WARNING 
    if opts.verbose :
        if opts.verbose == 1:
            log_level = logging.INFO
        elif opts.verbose >= 2:
            log_level = logging.DEBUG
    logging.getLogger().setLevel(log_level)

    return


def readDataPD(filename):
    #put to a pandas dataframe, process data and give dictionary of records

    inp_file = pr.resource_filename('src.input',filename)
    df = pd.read_csv(inp_file)
    
    data_d = defaultdict(dict)
    #File specific code - remove later
    reverse = False
#    if filename == "Alphabeticallist.csv":
#        reverse =True

    df[u'name'] = df.apply(lambda r: name_preprocess(r[u'name'],reverse),axis = 1)
    df[u'state'] = df.apply(lambda r: preprocess(r[u'state']),axis = 1)

    for i,row in df.iterrows():

        row_dict = row.to_dict()
        data_d[filename + str(i)] =  dict(row_dict)

    return data_d


def get_resolved_df(data_1,data_2,fields):

    # Training

    if os.path.exists(settings_file):
        print ('reading from', settings_file)
        with open(settings_file, 'rb') as sf :
            linker = dedupe.StaticRecordLink(sf)

    else:
        # Create a new linker object and pass our data model to it.
        linker = dedupe.RecordLink(fields)
        # To train the linker, we feed it a sample of records.
        linker.sample(data_1, data_2, 15000)

        # If we have training data saved from a previous run of linker,
        # look for it an load it in.
        if os.path.exists(training_file):
            print('reading labeled examples from ', training_file)
            with open(training_file) as tf :
                linker.readTraining(tf)

        # ## Active learning
        print('starting active labeling...')
        dedupe.consoleLabel(linker)

        linker.train()

        # When finished, save our training away to disk
        with open(training_file, 'w') as tf :
            linker.writeTraining(tf)

		# Save our weights and predicates to disk.  If the settings file
        # exists, we will skip all the training and learning next time we run
        # this file.
        with open(settings_file, 'wb') as sf :
    	    linker.writeSettings(sf)

    # ## Clustering

    print('clustering...')
    linked_records = linker.match(data_1, data_2, 0)

    print('# duplicate sets', len(linked_records))
    print (linked_records)

    # ## Writing Results

    df_list = []

    for cluster, score in linked_records:

        #obtain filename + record no clusters
        cluster1 = cluster[0]
        cluster2 = cluster[1]
        match = re.match(r"(\w+)\.csv(\d+)",cluster1)
        filename,idx = match.groups()
        filename +='.csv'
        filename = pr.resource_filename('src.input',filename)
        idx = int(idx)
        print filename
        print idx

        #dataframe for cluster - 1
        df1 = pd.DataFrame(columns=pd.read_csv(filename).columns)
        df1.loc[0] = pd.read_csv(filename).ix[idx]

        #for cluster 2
        match = re.match(r"(\w+)\.csv(\d+)",cluster2)
        filename,idx = match.groups()
        filename += '.csv'
        filename = pr.resource_filename('src.input',filename)
        idx = int(idx)
        print filename
        print idx

        #dataframe for cluster 2
        df2 = pd.DataFrame(columns=pd.read_csv(filename).columns)
        df2.loc[0] = pd.read_csv(filename).ix[idx]

        #common attribute
        df2['score'] = [score]
        df1['score'] = [score]

        df = pd.merge(df1,df2,on = 'score')
        df_list.append(df)

    results_df = pd.concat(df_list,ignore_index = True)
    return results_df

if __name__== '__main__':

    setLogging()

    #resolve file name

    # Define the fields the linker will pay attention to
    fields = [{'field' : 'name', 'type': 'String'},{'field':'state','type':'String'}]
    #get data in format taken by dedupe library
    print 'importing data ...'
    data_1 = readDataPD(sys.argv[1])
    data_2 = readDataPD(sys.argv[2])
    results_df = get_resolved_df(data_1,data_2,fields)
    print "creating output csv file - "+output_file
    results_df.to_csv(output_file)

