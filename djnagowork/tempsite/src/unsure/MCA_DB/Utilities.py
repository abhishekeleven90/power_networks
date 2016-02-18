# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from bs4 import BeautifulSoup
import pandas as pd
import requests as rq
import re
import hashlib
import time

# <codecell>

#a basic method that can be used to extract state name long from any address, just pass in the address
#see the usgae below

ipaddress = ''
dbnm = ''
user = ''
password = ''
logfilename = ''

def setParamsDB(ip, dbname, name, passw):
    global ipaddress
    global dbnm
    global user
    global password 
    ipaddress = ip
    dbnm = dbname
    user = name
    password = passw

#setParamsDB('localhost','powernetworks2','root','yoyo')

def setLogFileName(filename):
    global logfilename
    logfilename = filename

def log(towrite):
    now = time.strftime("%c")
    with open(logfilename, "a") as myfile:
            myfile.write(time.strftime("%c")+" -- "+towrite+"\n")

def getCityStateName(address):
    url='http://maps.googleapis.com/maps/api/geocode/xml?address=\"' + address + '\"&sensor=true'
    r = rq.get(url)
    print r.url
    data = r.text
    soup = BeautifulSoup(data)
    address_components = soup.find_all('address_component')
    l = len(address_components)
    if l <= 1:
        print 'No results for url ='+url
        return ""
    else:
        return (address_components[-3].find('long_name').text, address_components[-2].find('long_name').text)
#getCityStateName('''18 A Indl Development Area,  Patancheru,  Medak,  502319,  Andhra Pradesh''')

# <codecell>

def sqlQuerytoDF(query):
    global ipaddress
    global dbnm
    global user
    global password
    import MySQLdb as db
    from pandas.io.sql import frame_query
    #print user
    #print password
    database = db.connect(ipaddress, user, password, dbnm)
    dirframe = frame_query(query, database)
    #dirframe
    return dirframe
##Usage: sqlQuerytoDF("select id,name,office from company;","localhost","himanshu","root","yoyo")

# <codecell>

def sqlUpdateQuery(query):
    global ipaddress
    global dbnm
    global user
    global password
    import MySQLdb as db
    from pandas.io.sql import frame_query
    database = db.connect(ipaddress, user, password, dbnm)
    cur = database.cursor()
    value=False
    try:
        cur.execute(query)
        database.commit()
        value = True
    except Exception, e:
	#print(str(e))
        log(str(e))
        database.rollback()
    database.close()
    return value
    #dirframe

# <codecell>

#sqlUpdateQuery("insert into covered_dirs values('1');",'localhost','powernetworks2','root','yoyo')

