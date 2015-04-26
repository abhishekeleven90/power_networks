
# coding: utf-8

# Motive is to match from ADR datasets , business personnel to their companies

# In[5]:

#sudo apt-get install python-bs4
#sudo apt-get install python-requests
from bs4 import BeautifulSoup
import pandas as pd
import requests as rq
import re
from first.models import QcBod,QcCompany,QcDirector,QTrack,QQuery
import hashlib


# In[6]:

def searchDirector(url):
    r = rq.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    base_link = 'https://www.quickcompany.in'
    company_names = soup.find_all('h3',attrs={'class':'companyname'})
    df = []
    l = len(company_names)
    print 'no. of names in html - '+str(l/2) #/2 added by abhishek
    
    if l == 0:
        print 'No results for url ='+url
        return pd.DataFrame()
    
    for i in range(l/2):
        c = company_names[i]
        link = c.find('a')
        din = c.parent.find('div',attrs = {'class':'lighter'})
        dlink = base_link + link['href']
        #print 'Name=https://www.quickcompany.in'+link.text
        #print 'DIN='+din.text
        #print 'url='+dlink
        df.append({'Director':c.text.strip(),'DIN':din.text.strip(),'URL':dlink.strip()})
    
    df = pd.DataFrame(df)
    return df


# In[3]:

#Usage:
#url = 'https://www.quickcompany.in/company/director?name=Amartya'
#searchDirector(url)


# In[7]:

def scrapeDirectorsPageQuickCompany(url):
    r = rq.get(url)
    data = r.text
    
    df = pd.DataFrame()
    
    soup = BeautifulSoup(data)
    
    tablediv = soup.find('div', attrs={'class':"table-responsive"})
    
    if tablediv is None:
        return pd.DataFrame() #https://www.quickcompany.in/director/418957-rohit-s.jain
    
    #print tablediv
    table = tablediv.find('table')
    
    
    
    #print table    
    rows = table.find_all('tr') 
    
    
    data2 = []
    for row in rows:
        cols = row.find_all('td') 
        if len(cols) > 0:
            dict2 = {'CompanyName':cols[0].text,'Link':'http://www.quickcompany.in'+cols[0].find('a').get('href')}
            data2.append(dict2)
    
    df  = pd.DataFrame(data2)

    
    
    return df


# In[6]:

#Usage:
#url = "https://www.quickcompany.in/director/1072151-abu-hasem-khanchowdhury"
#scrapeDirectorsPageQuickCompany(url)


# In[8]:

def prettyTitleForDF(text):
    text = text.replace(" ","")
    text = text.replace("(","")
    text = text.replace(")","")
    text = text.replace("-","")
    return text


# In[9]:

def getDirectorDf(maindiv, cin):
    #get director's table details
    table = maindiv.find('table')
    rows = table.find_all('tr') 
    
    data2 = []
    for row in rows:
        cols = row.find_all('td') 
        if len(cols) > 0 and cols[0].text.strip() != '0': #a bug in company wiki for the name of Nitin Hariyantlal Datanwala
            dict2 = {'DIN':cols[0].text,
                     'CIN':cin,
                     'Name':cols[1].text, 
                     'Link':'http://www.quickcompany.in'+cols[1].find('a').get('href'),                  
                     'Address':cols[2].text,
                     'Designation':cols[3].text,
                     'DOA':cols[4].text,
                     'DSC_Status':cols[5].text}
            data2.append(dict2)
    
    dirdf  = pd.DataFrame(data2)
    return dirdf


# In[10]:

def getCompanyDf(maindiv, curl,cname):
    cintext = maindiv.find('h3',attrs={'class':"lighter truncate"})
    cin  = cintext.text[5:] #TODO: parse
    maindict ={}
    maindict['CIN'] = cin
    maindict['Name'] = cname
    maindict['q_url'] = curl
    #get all other details
    allrows = maindiv.find_all('div', attrs={'class':'row'})
    for row in allrows:
        onlyrow_details = row.find_all('div', attrs={'class':'col-xs-6'})
        if len(onlyrow_details) == 2:
            maindict[prettyTitleForDF(onlyrow_details[0].text)] = onlyrow_details[1].text     
    cmpnydf = pd.DataFrame([maindict])
    return cmpnydf


# In[11]:

def scrapeCompanyPageQuickCompany(url, c_name):
    
    r = rq.get(url)
    data = r.text
    
    df = pd.DataFrame()
    
    soup = BeautifulSoup(data)
    
    maindiv = soup.find('div', attrs={'class':"col-md-9"})
    
    
    cintext = maindiv.find('h3',attrs={'class':"lighter truncate"})
    cin  = cintext.text[5:]
    
    
    cmpnydf=getCompanyDf(maindiv, url, c_name)
    dirdf=getDirectorDf(maindiv,cin)
    
    ##for a company : dirdf, cmpnydf to db with appropriate checks
    print '\t\t\t### Adding company '+c_name+' details to DB'
    writeCompanyFrameToDB(cmpnydf)
    print '\t\t\t## Adding directors of '+c_name+' details to DB'
    writeDirectorDataFrameToDB(dirdf)
    print '\t\t\t## Adding bod links of '+c_name+' details to DB'
    writeQcBodToDB(dirdf,cin)
    #no need to return


# In[28]:

#url_company ='https://www.quickcompany.in/company/a-l-m-real-estates-pvt-ltd'
#companydf=scrapeCompanyPageQuickCompany(url_company, '')
#companydf


# In[12]:

##for a company call this fucntion, to enter its company_df
def writeCompanyFrameToDB(companydf):
    ##first try to enter in company table, if not already
    for x in range(0,len(companydf.index)):
        ct=QcCompany.objects.filter(cin=companydf.CIN[x])
        if not ct:
            c=QcCompany()
            c.cin=companydf.CIN[x]
            if 'AuthorizedShareCapital' in companydf.columns : c.authorizedsharecapital=companydf.AuthorizedShareCapital[x]
            if 'ClassofCompany' in companydf.columns : c.classofcompany=companydf.ClassofCompany[x]
            if 'CompanyCategory' in companydf.columns : c.companycategory=companydf.CompanyCategory[x]
            if 'CompanySubCategory' in companydf.columns : c.companysubcategory=companydf.CompanySubCategory[x]
            if 'CompanyStatusforeFiling' in companydf.columns : c.companystatusforefiling=companydf.CompanyStatusforeFiling[x]
            if 'DateofIncorporation' in companydf.columns : c.dateofincorporation=companydf.DateofIncorporation[x]
            if 'DateofLastAnnualGeneralMeeting' in companydf.columns : c.dateoflastannualgeneralmeeting=companydf.DateofLastAnnualGeneralMeeting[x]
            if 'DateofLatestBalanceSheet' in companydf.columns : c.dateoflatestbalancesheet=companydf.DateofLatestBalanceSheet[x]
            if 'EmailID' in companydf.columns : c.emailid=companydf.EmailID[x]
            if 'q_url' in companydf.columns : c.link=companydf.q_url[x]
            if 'Listingstatus' in companydf.columns : c.listingstatus=companydf.Listingstatus[x]
            if 'Name' in companydf.columns : c.name=companydf.Name[x]
            if 'NumberofMembers' in companydf.columns : c.numberofmembers=int(companydf.NumberofMembers[x])
            if 'PaidUpCapital' in companydf.columns : c.paidupcapital=companydf.PaidUpCapital[x]
            if 'RegisteredOfficeAddress' in companydf.columns : c.registeredofficeaddress=companydf.RegisteredOfficeAddress[x]
            if 'RegistrationNumber' in companydf.columns : c.registrationnumber=companydf.RegistrationNumber[x]
            if 'RegistrationState' in companydf.columns : c.registrationstate=companydf.RegistrationState[x]
            c.save()
            print '\t\t\t\t##'+companydf.CIN[x] + ' saved to qc_company table'
        else:
            print '\t\t\t\t##'+ct[0].cin + ' already exists in qc_company table'
#writeCompanyFrameToDB(companydf)


# In[13]:

##for a company call this fucntion, to enter its dir_dataframe
def writeDirectorDataFrameToDB(dirdf):
    ##first try to enter in director table, if not already
    for x in range(0,len(dirdf.index)):
        dt=QcDirector.objects.filter(din=dirdf.DIN[x])
        if not dt:
            d=QcDirector()
            d.name=dirdf.Name[x]
            d.address=dirdf.Address[x]
            d.dsc_status=dirdf.DSC_Status[x]
            d.link=dirdf.Link[x]
            d.din=dirdf.DIN[x]
            d.save()
            print '\t\t\t\t##'+dirdf.DIN[x] + ' saved to qc_director table'
        else:
            print '\t\t\t\t##'+dt[0].din + ' already exists in qc_director table'
#writeDirectorDataFrameToDB(dirdf)


# In[14]:

##for a company call this fucntion, to enter its dir_dataframe
def writeQcBodToDB(dirdf, cin_num):
    ##first try to enter in director table, if not already
    for x in range(0,len(dirdf.index)):
        dt=QcBod.objects.filter(din=dirdf.DIN[x],cin=cin_num)
        if not dt:
            d=QcBod()
            d.din_id=dirdf.DIN[x]
            d.cin_id=dirdf.CIN[x]
            d.doa=dirdf.DOA[x]
            d.designation=dirdf.Designation[x]
            d.save()
            print '\t\t\t\t##'+cin_num+':'+dirdf.DIN[x] + ' saved to qc_bod table'
        else:
            print '\t\t\t\t##'+dt[0].cin_id+':'+dt[0].din_id +' already exists in qc_bod table'
#writeQcBodToDB(dirdf,'U70101WB1984PTC037414')


# In[20]:

def main(name): #name is the query, you just append
    print ('----------------------------START for : '+name)
    url = 'https://www.quickcompany.in/company/director?name='+name
    alldirs = searchDirector(url)
    print '### Found ' + str(len(alldirs.index)) + ' matches'
    i=0
    for x in range(0,len(alldirs.index)):
        i=i+1
        print '\t### Fecthing companies of match '+str(i) + ' /'+str(len(alldirs.index))
        allcompaniesforADir = scrapeDirectorsPageQuickCompany(alldirs.URL[x])
        if allcompaniesforADir.empty:
                continue
        print '\t### Found ' + str(len(allcompaniesforADir.index)) + ' companies'
        j=0
        for y in range(0, len(allcompaniesforADir.index)):
            j=j+1
            print '\t\t### Fecthing company '+str(j)+ ' /'+str(len(allcompaniesforADir.index))
            scrapeCompanyPageQuickCompany(allcompaniesforADir.Link[y], allcompaniesforADir.CompanyName[y])
    print('-----------------------------END for : '+name)


# In[16]:

import itertools
def getListOfAllSearchQueries(name):
    name=name.replace('.',' ')
    name=name.replace('-','')
    lst = name.split()
    combs=[]
    for i in xrange(1, len(lst)+1):
        els = [list(x) for x in itertools.combinations(lst, i)]
        combs.extend(els)
    toReturn = []
    for x in combs:
        toReturn.append('+'.join(x))
    return toReturn


# In[17]:

import pandas as pd
import csv
import Levenshtein
from fuzzywuzzy import fuzz
candframe=pd.read_csv('ls2014winners.csv', index_col=False, quoting=csv.QUOTE_ALL)
candframe.Party=candframe.Party.str.lower()
candframe.Candidate=candframe.Candidate.str.lower()
candframe.rename(columns={'Self profession':'profession'}, inplace=True)
candframe.rename(columns={' PAN':'PAN'}, inplace=True)
candframe.profession = candframe.profession.str.lower()
candframe['edit'] = candframe.apply(lambda r: Levenshtein.ratio(r['profession'], 'business'), axis=1)
candframe['fuzzy'] = candframe.apply(lambda r: fuzz.token_set_ratio(r['profession'], 'business'), axis=1)
toworkframe = candframe[candframe.fuzzy>90][['Candidate','Candidate ID']]
toworkframe


# In[24]:

toworkframe = toworkframe.reset_index(drop=True)
i=0
for x in range(9,len(toworkframe.index)):
    i=i+1
    if (QTrack.objects.filter(mynetaid = toworkframe['Candidate ID'][x])):
        print '@@@@@@@@@ Already covered ID: '+str(toworkframe['Candidate ID'][x])
        continue
    else:
        print '@@@@@@@@@@@@@@@@@@@@@@ START ID: '+str(toworkframe['Candidate ID'][x]) + '  '+str(i)+'/'+str(len(toworkframe.index)-5)
        tempsearchlist = getListOfAllSearchQueries(toworkframe.Candidate[x])
        j=0
        for y in tempsearchlist:
            j=j+1
            if (QQuery.objects.filter(hashmyfield=hashlib.md5(y).hexdigest())):
                print '%Already covered search query, skipping : '+str(y)
            else:
                print '%START SEARCH QUERY : ' +y +  '  '+str(j)+'/'+str(len(tempsearchlist))
                main(y)
                print '%END SEARCH QUERY : ' +y + ' /'+str(len(tempsearchlist))
                qq=QQuery()
                qq.hashmyfield = hashlib.md5(y).hexdigest()
                qq.save()
        print '$$$$$$$$$$$$  END ID: '+str(toworkframe['Candidate ID'][x])
        qt=QTrack()
        qt.mynetaid=(toworkframe['Candidate ID'][x])
        qt.save()

