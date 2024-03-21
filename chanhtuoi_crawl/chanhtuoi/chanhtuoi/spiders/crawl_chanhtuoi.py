## 1 -> 480
import traceback
import pymongo
import requests
import time
import os
import schedule
from time import gmtime, strftime
import scrapy
from bs4 import BeautifulSoup
from decouple import config
url = config('url')
client = pymongo.MongoClient(url)
db = client["chanhtuoi"]

def cleanText(p_texts):
    txt = ''
    for p_t in p_texts:
        clean_p_t = p_t.strip()
        if clean_p_t and len(clean_p_t) >= 2:
            txt += "{}\n".format(clean_p_t)
    return txt

REMOVE_ATTRIBUTES = ['style']

class JobSpider(scrapy.Spider):
    name = 'chanhtuoi'
    url1=['https://chanhtuoi.com/kinh-nghiem/tay-trang?pagePost={}'.format(i) for i in range(15)]
  
    start_urls = url1
    # start_urls = urls1
    
    def parse(self, response):
        links = response.css('div.item a::attr("href")').getall()
        for link in links:
            if 'http' in link:
                yield scrapy.Request(url=link, callback=self.parse_job_info)
                
        
        
    def parse_job_info(self, response):
        url = response.request.url
        html = response.text
        soup = BeautifulSoup(html, features="lxml")
        tab_details = soup.find_all("div", {"class": "ck-content"})[0]
        title = soup.find_all("h1", {"class": "reviews-title"})[0]
        
        # Remove attributes
        for tag in tab_details.recursiveChildGenerator():
            if hasattr(tag, 'attrs'):
                tag.attrs = {key:value for key,value in tag.attrs.items()
                            if key not in REMOVE_ATTRIBUTES}
        
        yield {
            "url": url,
            "tab_details": str(tab_details),
            "title": str(title)
        }
