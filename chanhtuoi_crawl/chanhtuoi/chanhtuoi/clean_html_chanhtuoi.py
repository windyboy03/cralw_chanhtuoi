import bs4
from bs4 import BeautifulSoup
import random
import traceback
from langdetect import detect
def removeAttributes(item):
    for tag in item.recursiveChildGenerator():
        if hasattr(tag, 'attrs'):
            tag.attrs = {} 
            tag.attrs['class'] = {} 

    return item


def extract_html(ht, url, title=None, tags=[]):
    toSave = {
        "url": url,
        "title": "",
        "body": "",
        "tags": [],
    }
    
    try:
        body = ''
        clean_title = BeautifulSoup(title, features="lxml").text
        # print('---clean_title', clean_title)
        if clean_title:
            toSave["title"] = clean_title.lower().strip()
        # print('===', url)
        # print('===ht', ht)

        soup = BeautifulSoup(ht, features="lxml")
        # boxs = soup.find_all('div', {'class': 'ck-content'})

        selects = soup.find_all("div", { "class": "posts-menu" })
        
        for match in selects:
            match.decompose()

            
        
        selects2 = soup.find_all("div", { "class": "chanh_price_trade" })

        for match in selects2:
            match.decompose() 


        selects3 = soup.find_all("div", { "class": "mce-toc" })
        

        for match in selects3:
            match.decompose()


        selects4 = soup.find_all("table", { "class": "MsoTableGrid" })


        for match in selects4:
            match.decompose()


        selects5 = soup.find_all("div", { "class": "review-top__price" })

        for match in selects5:
            match.decompose()

        items = soup.find_all()

        for idx, item in enumerate(items):
            if item.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                body += '<p>{}</p>'.format(item.text)
            elif item.name == 'p':
                body += '<p>{}</p>'.format(item.text)

        toSave["body"] = body

        return toSave
    except Exception as e:
        print(traceback.format_exc())
        print('Error', e)
        return toSave
