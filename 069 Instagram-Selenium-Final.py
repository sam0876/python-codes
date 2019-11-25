from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook
import os
import requests
import shutil


class App:
    def __init__(self, email='sam.nitrr@gmail.com', password='recovered@69', target_email='sam.nitrr@gmail.com',
                 path='C:/Users/samni/Downloads/reviewsamazon'): #Change this to your Instagram details and desired images path
        self.email = email
        self.password = password
        self.target_email = target_email
        self.path = path
        self.driver = webdriver.Chrome('C:/Users/samni/Downloads/chromedriver/chromedriver.exe') #Change this to your ChromeDriver path.
        self.error = False
        self.main_url = 'https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2FAll-New-Amazon-Echo-Dot-Add-Alexa-To-Any-Room%2Fdp%2FB01DFKC2SO%2Fref%3Dnav_signin%3Fie%3DUTF8&switch_account='
        self.driver.get(self.main_url)
        self.sign_in()
        sleep(20)
        #self.driver.close()
        
        
    def sign_in(self,):
        email_input=self.driver.find_element_by_xpath('//*[@id="ap_email"]')
        email_input.send_keys(self.email)
        password_input=self.driver.find_element_by_xpath('//*[@id="ap_password"]')
        password_input.send_keys(self.password)
        sign_in_button= self.driver.find_element_by_xpath('//*[@id="signInSubmit"]')
        sign_in_button.click()
        #deliver_continue=self.driver.find_element_by_xpath('//*[@id="nav-main"]/div[1]/div[2]/div/div[3]/span[1]/span/input')
        #deliver_continue.click()
        reviews_link=self.driver.find_element_by_xpath('//*[@id="reviews-medley-footer"]/div[2]/a')
        reviews_link.click()
        #no_reviews=self.driver.find_element_by_xpath('//*[@id="customer_review-R3W2AFY4JQ2SVA"]/div[4]/span')
        #no_reviews=str(no_reviews.text).replace(',','')
        #print(no_reviews)
        #len(no_reviews)
    
    
    def review_in(self,):   
        maxNumOfPages = 11848; # for example
        for pageId in range(1,maxNumOfPages+1):
            for review in self.driver.find_elements_by_class_name('a-section a-spacing-none review-views celwidget'):
                title  = review.find_elements_by_css_selector('span.a-size-base.review-text').text
                review = review.find_element_by_xpath('//*[@id="customer_review-R3W2AFY4JQ2SVA"]/div[4]/span').get_attribute('title')
                print(title,review)
            try:
                self.driver.find_element_by_link_text(str(pageId)).click()
            except:
                break   

# Result: the browser is opened t the given url, no download occur
         
  
if __name__ == '__main__':
    app = App()            
