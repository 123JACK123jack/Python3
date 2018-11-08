from typing import List
import requests
import json
import pymysql
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import ConnectionError

conn = pymysql.connect(user="root", passwd="", database="sys", charset='utf8')

def get_index(offset):
    base_url = "https://www.guokr.com/apis/minisite/article.json?retrieve_type=by_channel&channel_key=lifestyle&"
    data1 = {
       # 'retrieve_type': "by_channel",
        'limit': "20",
        'offset': offset
    }
    params = urlencode(data1)
    url = base_url + params
    try:
        resp1 = requests.get(url)
        if resp1.status_code == 200:
            return resp1.text
            print(type(resp1.text))
        return None
    except ConnectionError:
        print('Error.')
        return None

def parse_json(text):
    try:
        result = json.loads(text)
        if result:
            for i in result.get('result'):
                # print(i.get('url'))
                yield i.get('url')
    except:
        pass

def get_page(url):
    try:
        headers = {
            "Cookie":"__guid = 44876322.688890323490907100.1531097181999.909;_ga = GA1.2.69008057.1531097"
                     "232;BAIDU_SSP_lcr = https: // www.so.com / s?q = % E6 % 9E % 9C % E5 % A3 % B3 % E7 % "
                     "BD % 91 & ie = utf - 8 & src = se7_newtab_new;__utmt = 1;_32353_access_token = 36013"
                     "be2083b5682734b7c129240ceaf12a36df4390d95acebd942d9989a461f;_32353_ukey = gkg4zn;_3238"
                     "2_access_token = cb99a5c982f14a9a5c1a1834a11e1db22672eab3baa3c0d5886cacc3639a1ca4;_32382"
                     "_ukey = gkg4zn;isN = 1;monitor_count = 31;__utma = 253067679.69008057.1531097232.1531190"
                     "828.1531222724.7;__utmb = 253067679.6.10.1531222724;__utmc = 253067679;__utmz = 253067"
                     "679.1531222724.7.4.utmcsr = so.com | utmccn = (organic) | utmcmd = organic | utmctr = % "
                     "E6 % 9E % 9C % E5 % A3 % B3 % E7 % BD % 91;__utmv = 253067679. | 1 = Is % 20Registered = "
                     "Yes = 1;session = 9f5760c1 - f8f8 - 4ce8 - 8015 - 336cb92fc020",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/55.0.2883.87 Safari/537.36"
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            # print(resp.text)
            return resp.text
        return None
    except ConnectionError:
        print('Error.')
        return None

def parse_page1(resp):
    try:
        soup = BeautifulSoup(resp, 'lxml')
        content = soup.find('div', class_="main")
        title = content.find('h1').get_text()
        #author = content.find('div', class_="content-th-info").find('a').get_text()
        # print(title,'\n',author,'\n',article)
        #print(title)
        return  title
    except:
        pass

def parse_page2(resp):
    try:
        soup = BeautifulSoup(resp, 'lxml')
        content = soup.find('div', class_="main")
        #title = content.find('h1').get_text()
        way = content.find('a',class_="label label-common").get_text()
        # print(title,'\n',author,'\n',article)

        #print(title)
        return way             #,author
    except:
        pass
def save_database(title,way):
    cur = conn.cursor()
    a=str(title)
    b=str(way)
    cur.execute("insert into app2_article3(title,way) values(%s,%s)", (a,b))
    conn.commit()
    cur.close()
    return True

if __name__ == '__main__':
    offsets: List[int] = ([0] + [i * 20 + 18 for i in range(10)])
    for offset in offsets:
        text = get_index(offset)
        all_url = parse_json(text)
        for url in all_url:
            resp = get_page(url)
           # data=parse_page(resp)
            #print(data)
            title=parse_page1(resp)
            way = parse_page2(resp)
            print(title,way)
            save_database(title, way)


