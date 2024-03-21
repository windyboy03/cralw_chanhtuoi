# -*- encoding: utf-8 -*-

import pymongo
from decouple import config
from tqdm import tqdm
from clean_html_chanhtuoi import extract_html 
import random
import traceback
import time
url = config('url')
client = pymongo.MongoClient(url)
db = client["chanhtuoi"]


articles = list(db.article_details_clean.find({}, {"raw_id": 1, "url": 1}))
cleaned_raw_ids = [item["raw_id"] for item in articles]
cleaned_raw_urls = [item["url"] for item in articles]
jo = db.article_details_raw.find({"_id": {"$nin": cleaned_raw_ids}, "url": {"$nin": cleaned_raw_urls}})

# idx = random.randint(0, 3400)
# jo = db.article_details_raw.find({'url': 'https://chanhtuoi.com/top-10-quat-cay-dep-ban-chay-nhat-p4301.html' })
# jo = db.article_details_raw.find().skip(idx).limit(1)
# jo = db.article_details_raw.find()


data = []
id_set = set()
print('====================================================================================')
for html in tqdm(jo):
    print(html)
    try:
        print(len(data))
        print('-----------Start------------')
        to = extract_html(html['tab_details'], html['url'], html['title'], "")
        # time.sleep(2)

        title = to['title']
        body = to['body']
        # des = to['description']


        if len(title) > 0 and len(body) > 300:
            print(html['tab_details'])
            print(html['url'])
            print(html['title'])
            print('=====')
            print('---', to)
            # print('====des====',html['description'])
            clean_data = {
                "url": to['url'],
                "title": title,
                "body": body,
                "raw_id": html['_id']
            }
            
            if html['url'] not in id_set:
                data.append(clean_data)
                id_set.add(html['url'])
                
        if len(data) == 1:
            try:
                print('Saved 1')
                db.article_details_clean.insert_many(data)
                
                data = []
            except Exception as e:
                data = []
                print('Error: db.article_details_clean.insert_many', e)
                print(traceback.format_exc())
    except Exception as e:
        print(traceback.format_exc())


