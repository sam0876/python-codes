from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import requests 
import re
from fake_useragent import UserAgent
ua = UserAgent()
import lxml
import ssl
from urllib.request import urlretrieve

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
driver = webdriver.Chrome('C:/Users/samni/Downloads/chromedriver/chromedriver.exe')
driver.maximize_window()
driver.implicitly_wait(30)
driver.get('https://www.amazon.com/All-New-Amazon-Echo-Dot-Add-Alexa-To-Any-Room/product-reviews/B01DFKC2SO/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=2')
soup = BeautifulSoup(driver.page_source, 'lxml')
print(soup.prettify())
base_url= 'https://www.amazon.com'

#search_chrome=driver.find_element_by_id('twotabsearchtextbox')
#search_chrome.send_keys('a-row a-spacing-small review-data')
elements = driver.find_elements_by_css_selector('span.a-size-base.review-text')
elements[2].text
len(elements)
#find_elements_by_id('acrCustomerReviewText')

#search_bar.send_keys('Echo Dot (2nd Generation)')

#search_bar.submit()
sleep(20)
driver.close()


import asyncio


async def getReviews(url):
    
    print("get review urls: {0}".format(url))



async def fetchUrls():
    try:
        print("In fetchUrls")
        urlst=[]
        tasks=[]
        baselink="https://www.amazon.com/All-New-Amazon-Echo-Dot-Add-Alexa-To-Any-Room/product-reviews/B01DFKC2SO/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews"
        for i in range(11848):
            pgNo=i+1
            url=baselink+"&pageNumber="+str(pgNo)
            urlst.append(url)
            
        tasks+=[asyncio.ensure_future(getReviews(url)) for url in urlst]	
        responses = await asyncio.gather(*tasks)
        return responses
    except Exception as ex:
        print("Exception occurred in fetchUrls")
        print(ex)


async def main(loop):
    try:
        print("In main")
        t1 = loop.create_task(fetchUrls())
        await t1
    except Exception as ex:
        print("Exception occurred in main")
        print(ex)


if __name__ == "__main__":        
    
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()