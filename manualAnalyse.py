# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 02:41:34 2018

@author: Shashank
"""



import os
os.getcwd()
os.chdir("D:\\vishnoi\\M Tech Course\\Research_paper\\Nilesh\\Code")
import pandas as pd
import json
import regex as re
import mysql.connector
from gensim.summarization.summarizer import summarize
from gensim.summarization.textcleaner import split_sentences
from nltk.tokenize import RegexpTokenizer
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
with open('config.json', 'r') as json_data_file:
    config = json.load(json_data_file)
    
from sklearn.model_selection import train_test_split as tts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
custom=set(stopwords.words('english')+list(punctuation)+[',', '”', '’', '“', '``', '‘', '=', ':',  '``', '���','“','”','--','said','percent','per cent',"''",'time','per','cent','would','also','stock','year','could','company','month','Rs','crore','market','India','one','growth'])    


class ManualAnalse:
    
    def wordCloud(self):
        try:
            manual_arrwc=[]
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM news_project.news_manual where return_label=manual_label and manual_label='negative';")
            positiveNews=""
            positiveNews1=""
            for row in cursor:
                manualObjwc = dict()
                manualObjwc['news_id'] = row[0]
                manualObjwc['comp_symbol'] = row[1]
                manualObjwc['news_url'] = row[2]
                manualObjwc['news_heading'] = row[3]
                manualObjwc['news_desc'] = " ".join([word for word in word_tokenize(row[4]) if word not in custom])
                
                positiveNews=positiveNews+' '+manualObjwc['news_desc']
                #positiveNews=positiveNews+' '
                manual_arrwc.append(manualObjwc)
                sent_arr=[]
                
                for sent in re.split("[.]\s*(?=\D)", row[4]):
                    #sent = " ".join(tokenizer.tokenize(sent))
                    sent_arr.append(sent)
                para = ". ".join([sent for sent in sent_arr])
                
                if len(sent_arr) > 50:
                    manualObjwc['news_summ'] = summarize(para, ratio=0.20)
                else:
                    manualObjwc['news_summ'] = para
                positiveNews1=positiveNews1+' '+manualObjwc['news_summ']
            
            #print(positiveNews)
            
                
            #positiveNews=" ".join([news_desc for news_desc in manual_arrwc['news_desc']])
             ########WordCloud
            wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = custom, 
                min_font_size = 10).generate(positiveNews1) 
             
            # plot the WordCloud image                        
            plt.figure(figsize = (8, 8), facecolor = None) 
            plt.imshow(wordcloud) 
            plt.axis("off") 
            plt.tight_layout(pad = 0) 
  
            plt.show()
        
        except Exception as ex:
            print(ex)
        
        finally:
            cursor.close()
            cnx.close()

    def manualCheck(self):
        try:
            manual_arr=[]
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            cursor.execute("select * from news_manual where return_label='positive';")
                            
            #tokenizer = RegexpTokenizer(r'\w+')
            for row in cursor:
                manualObj = dict()
                manualObj['news_id'] = row[0]
                manualObj['comp_symbol'] = row[1]
                manualObj['news_url'] = row[2]
                manualObj['news_heading'] = row[3]
                manualObj['news_desc'] = " ".join([word for word in word_tokenize(row[4]) if word not in custom])
                
                sent_arr=[]
                
                for sent in re.split("[.]\s*(?=\D)", row[4]):
                    #sent = " ".join(tokenizer.tokenize(sent))
                    sent_arr.append(sent)
                para = ". ".join([sent for sent in sent_arr])
                
                if len(sent_arr) > 50:
                    manualObj['news_summ'] = summarize(para, ratio=0.20)
                else:
                    manualObj['news_summ'] = para
                
                
                manualObj['manual_label'] = row[5]
                
                manual_arr.append(manualObj)
                
                
               
            manualNews = pd.DataFrame(manual_arr)
            #print(manualNews.head(5))
                        
            news_dmmy = manualNews.loc[:, ('news_summ', 'manual_label')]
            #print(news_dmmy.head(5))
            y = news_dmmy['manual_label'].replace({'positive':0, 'negative':1})
            #print(y)
            x_train, x_test, y_train, y_test = tts(news_dmmy['news_summ'], y, test_size=0.20, random_state=53)
            tfidf_vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_train = tfidf_vectorizer.fit_transform(x_train)
            tfidf_test = tfidf_vectorizer.transform(x_test)
            nb_classifier = MultinomialNB()
            nb_classifier.fit(tfidf_train, y_train)
            preds = nb_classifier.predict(tfidf_test)
            acc = metrics.accuracy_score(y_test, preds)
            print(acc)
            cm = metrics.confusion_matrix(y_test, preds, labels=[0,1])
            print(cm)
            self.predNews(tfidf_vectorizer, nb_classifier)
            
            
            
            
        except Exception as ex:
            print(ex)
        
        finally:
            cursor.close()
            cnx.close()
            
           
    def predNews(self, tfidf_vectorizer, nb_classifier):
        try:
            restNews_arr=[]
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            cursor.execute("select * from news where news_url not in (select news_url from news_manual) and return_label!='none';")
            for row in cursor:
                restNewsObj = dict()
                restNewsObj['news_id'] = row[0]
                restNewsObj['comp_symbol'] = row[1]
                restNewsObj['news_time'] = row[2]
                restNewsObj['news_url'] = row[3]
                restNewsObj['news_title'] = row[4]
                restNewsObj['news_heading'] = row[5]
                restNewsObj['news_desc'] = row[6]
                restNewsObj['return_label'] = row[7]
                
                
                
                sent_arr=[]
                
                for sent in re.split("[.]\s*(?=\D)", row[6]):
                    #sent = " ".join(tokenizer.tokenize(sent))
                    sent_arr.append(sent)
                para = ". ".join([sent for sent in sent_arr])
                
                if len(sent_arr) > 50:
                    restNewsObj['news_summ'] = summarize(para, ratio=0.20)
                else:
                    restNewsObj['news_summ'] = para
                
                
                
                
                restNews_arr.append(restNewsObj)
                
            restNews_df = pd.DataFrame(restNews_arr)
            #print(restNews_df.head(5))
            restNews_dmmy = restNews_df.loc[:, ('news_summ', 'return_label')]
            y_returnLabel = restNews_dmmy['return_label'].replace({'positive':0, 'negative':1})
            
            #print("y_returnLabel===========")
            #print(y_returnLabel.unique())
            #print(type(y_returnLabel))
            tfidf_restNews = tfidf_vectorizer.transform(restNews_dmmy['news_summ'])
            #print(tfidf_restNews)
            y_pred = nb_classifier.predict(tfidf_restNews)
            #print("y_pred==============")
            #print(y_pred.unique())
            
            acc = metrics.accuracy_score(y_returnLabel, y_pred)
            print(acc)
            cm = metrics.confusion_matrix(y_returnLabel, y_pred, labels=[0,1])
            print(cm)
            
            
        except Exception as ex:
            print("Error from prediction of rest news")
            print(ex)
        finally:
            cursor.close()
            cnx.close()

        
        
        
        
manualNews = ManualAnalse()
#manualNews.manualCheck()
manualNews.wordCloud()       
        
        