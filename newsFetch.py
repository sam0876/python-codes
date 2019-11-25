# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 19:50:38 2018

@author: Sanmoy
"""
import itertools
from iteration_utilities import unique_everseen
import operator
import time
import asyncio
import os
os.getcwd()
os.chdir("C:\\F\\NMIMS\\DataScience\\Sem-3\\Capstone\\Nilesh\\Code")
import urllib3
import json
import mysql.connector
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import regex as re
from datetime import datetime
import logging
import configparser
prop_config = configparser.ConfigParser()
prop_config.read('properties.ini')
logger = logging.getLogger(__name__)
if not logger.handlers:
    hdlr = logging.FileHandler('news.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)


custom=set(stopwords.words('english')+list(punctuation)+[',', '”', '’', '“', '``', '‘', '=', ':',  '``', '���','“','”','--'])
#custom=set([',', '”', '’', '“',"1,500","4,292","2,388","3,970","21,327","9,050","1,284"])
with open('config.json', 'r') as json_data_file:
    config = json.load(json_data_file)
#class NewsFetch:
#    def __init__(self, logger):
#        self.logger = logging.getLogger(__name__)
#        hdlr = logging.FileHandler('news.log')
#        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#        hdlr.setFormatter(formatter)
#        self.logger.addHandler(hdlr) 
#        self.logger.setLevel(logging.DEBUG)

  



    
    
baselink_news = "https://economictimes.indiatimes.com"
#cursor.execute('select company_name from company_name_check where detail_id =2;')
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
cursor.execute("select company_name from company_name_check;")
newsCat = []
for row in cursor:
    #print(row[0])
    newsCat.append(row[0])
cursor.close()
cnx.close()
#cursor.execute('select company_name from company_name_check where detail_id =1;')
#compCat_arr = []
#for row in cursor:
#    #print(row[0])
#    compCat_arr.append(row[0]) 
async def getHeadlines(urlObj):
    
    logger.info("get headlines and headline urls: {0}".format(urlObj['url']))
    news_task = []
    http = urllib3.PoolManager()
    response = http.request('GET', urlObj['url'])
    soup = BeautifulSoup(response.data, 'html.parser')
    headline_arr = []
    for ul_tag in soup.find_all('ul', {'class':'content'}):
        for li_tag in ul_tag.findChildren('li'):
            for href_tag in li_tag.findChildren('a'):
                headline_obj = dict()
                headline_obj['date'] = urlObj['date']
                headline_obj["headline"] = " ".join([word for word in word_tokenize(href_tag.text) if word not in custom])
                headline_obj["title"] = href_tag.get('href').split('/')[1]
                headline_obj["headline_url"] = baselink_news+href_tag.get('href')
                
                headline_arr.append(headline_obj)
                
    #uniqueHeadlineArr = list({v['headline']:v for v in headline_arr}.values())
    news_task+=[asyncio.ensure_future(getnews(obj)) for obj in headline_arr]	
    news_resp = await asyncio.gather(*news_task)
    return news_resp
    
    
async def getnews(newsObj):
    urlArr = newsObj['headline_url'].split('/')
    checkUrl = re.sub("-", " ", urlArr[len(urlArr)-3])
    check = checkHeadlinePresent(checkUrl)
    #print("Process Time: {0}".format(endTime-startTime))
    if check:
        #print('present')
        #paras=" "
        logger.info("get news url is : {0}".format(newsObj['headline_url']))
        newsObj["comp_symbol"] = check
        newsObj["news_text"] = ""                
        http = urllib3.PoolManager()
        response = http.request('GET', newsObj['headline_url'])
        soup = BeautifulSoup(response.data, 'html.parser')
        text = ". ".join([p.text for p in soup.find_all('div', {'class':'Normal'})])
        if len(text) > 0:
            newsObj["news_text"] = text
        else:
            None
             
    else:
        None
        
    
    return newsObj                   
 
def checkHeadlinePresent(text):
    #print('checkHeadlinePresent: {0}'.format(text))
    for word in newsCat:
        if re.search(r'\b' + word + r'\b', text):
            return word
        else:
            None
                               
async def fetchHeadline():
    logger.info('In fetchNewsUrl================')
    try:
        tasks = []
        
        #print(newsCat_arr)
        base_link = "https://economictimes.indiatimes.com/archivelist/"
        starttime = prop_config['starttimeSelection']['starttime']
        year_lst = list(map(int, prop_config['yearSelection']['year'].split(",")))
        
        lst_urls = []
        for year in year_lst:    
                if year == 2018:
                    mon_range = 8
                else:
                    mon_range = 12
                    
                for month in range(1):
                    mon = month+11
                    if mon in [1,3,5,7,8,10,12]:
                        nod=31
                        
                        
                    elif mon in [4,6,9,11]:
                        nod=30
                    elif year%4==0 and mon==2:
                        nod=29
                    else:
                        nod=28
                    for day in range(nod):
                        starttime = int(starttime)+1
                        date = datetime.strptime(str(year)+'_'+str(mon)+'_'+str(day+1), "%Y_%m_%d").date()
                        link_obj = dict()
                        link = base_link+"year-"+str(year)+",month-"+str(mon)+",starttime-"+str(starttime)+".cms"
                        link_obj['date'] = date
                        link_obj['url'] = link
                        lst_urls.append(link_obj)
        
        tasks+=[asyncio.ensure_future(getHeadlines(url)) for url in lst_urls]	
        responses = await asyncio.gather(*tasks)
        return responses
                       
    except Exception as ex:
        logger.error("Error occurred in newsFetch")
        logger.error(ex)
        
        #cursor.callproc('error_entry_py', args)

    
        
        
        
async def main(loop):
    #await asyncio.sleep(0)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try:
        t1 = loop.create_task(fetchHeadline())
        await t1
        finalNewsToBeStored = []
        for reslt in t1.result():
            for eachObj in reslt:
                if "news_text" in eachObj and eachObj["news_text"]!="":
                    finalNewsToBeStored.append(eachObj)
                    
                        
        storeNewsInDb(finalNewsToBeStored)
                   
    except Exception as ex:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        logger.error("Error occurred in main")
        logger.error(ex)
        err_code = "Unknown"
        args = [err_code, ex, 0]
#        cursor.callproc('error_entry_py', args)
    finally:
        cursor.close()
        cnx.commit()
        cnx.close()
    
    

def storeNewsInDb(finalNewsToBeStored):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try:
        #print("In store DB==========")
        #print(finalNewsToBeStored)
#        unique_sets = set(frozenset(d.items()) for d in finalNewsToBeStored)
#        unique_dicts = [dict(s) for s in unique_sets]
        #unique_dicts = list(unique_everseen(finalNewsToBeStored, key=operator.itemgetter('headline')))
        
        #   print("finalNewsArr===============")
#        print(unique_dicts)
        unique_dicts = list({v['headline']:v for v in finalNewsToBeStored}.values())
        for finalNewsObj in unique_dicts:
            #print(finalNewsObj)
            #cursor.execute('insert into news (comp_symbol, news_time, news_url, news_title, news_heading, news_desc) values(%s,%s,%s,%s,%s,%s)',("test", "test", "test", "test", "test", "test"))
            cursor.execute('insert into news_prev (comp_symbol, news_time, news_url, news_title, news_heading, news_desc) values(%s,%s,%s,%s,%s,%s)',(finalNewsObj['comp_symbol'], finalNewsObj['date'], finalNewsObj['headline_url'], finalNewsObj['title'], finalNewsObj['headline'], finalNewsObj['news_text']))
    
    except Exception as ex:
        print("Error occurred in main")
        print(ex)
        err_code = "Unknown"
        args = [err_code, ex, 0]
        #cursor.callproc('error_entry_py', args)
    finally:
        cursor.close()
        cnx.commit()
        cnx.close()
            
    
        
if __name__ == "__main__":        
    
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
