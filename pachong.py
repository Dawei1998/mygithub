# -*- coding:utf-8 -*-
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import re

def get_one_page(url):
    try:
        # 修改agent，应对反爬虫
        headers = {
            'Host': "sh.lianjia.com",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate, sdch",
            'Accept-Language': "zh-CN,zh;q=0.8",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            'Connection': "keep-alive",
        }
        response = requests.get(url, headers=headers)
        print(response.content.decode('utf-8'))
        if response.status_code == 200:       # 找到网页且不报错
            return response.text
        else:
            return None
    except RequestException:
        return None

def parse_one_page(html,page):
    soup = BeautifulSoup(html, 'lxml')
    prefix = 'http://sh.lianjia.com'
    id = page*30
    for item in soup.select('.content__list--item'):
        print(id)
        houseUrl = prefix + item.a["href"]
        title = item.a["title"]
        spans = item.find(class_="content__list--item--des")
        a = ''.join(str(spans))
        texta = re.sub('<[^<]+?>', '', a).replace('\n', '').strip()
        shuxing = texta.split()
        add, mianji, chaoxiang, huxing = shuxing[0], shuxing[1], shuxing[2],shuxing[4]
        if len(shuxing)>7:
            louceng = shuxing[6]+shuxing[7]
        elif len(shuxing)==7:     # 数据中不含具体楼层
            louceng = shuxing[6]
        else:
            louceng =[]
        add = add.rstrip('/')
        chaoxiang=chaoxiang.lstrip('/')
        louceng=louceng.lstrip('/')
        fabu = item.find(class_="content__list--item--time oneline").string
        temp = item.find(class_="content__list--item--bottom oneline")
        b = ''.join(str(temp))
        beizhu = re.sub('<[^<]+?>', '', b).replace('\n', '').strip()
        price = item.find(class_="content__list--item-price").find("em").string
        id = id+1
        yield {'houseUrl':houseUrl,'title': title, 'address': add,'area':mianji,'direction':chaoxiang,'huxing':huxing,'floor':louceng, 'publish':fabu,'remark': beizhu,'price': price}

if __name__ == '__main__':
    results=[]
    page = 0
    while page<100 :
        sleep(1)
        if page ==34:  #此页数据有问题，跳过
            page += 1
        url = 'http://sh.lianjia.com/zufang/pg' + str(page+1)
        html = get_one_page(url)
        for item in parse_one_page(html,page):
            results.append(item)
        page =page+1
    name = ['houseUrl', 'title', 'address','area','direction','huxing','floor', 'publish', 'remark', 'price']
    test = pd.DataFrame(columns=name,data=results)
    print(test)
    test.to_csv('result10.csv',encoding='gbk')
