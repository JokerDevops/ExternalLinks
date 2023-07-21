class Queue(object):
    # 初始化队列
    def __init__(self):
        self.items = []

    # 入队
    def enqueue(self, item):
        self.items.append(item)

    # 出队
    def dequeue(self):
        if self.is_Empty():
            print("当前队列为空！！")
        else:
            return self.items.pop(0)

    # 判断是否为空
    def is_Empty(self):
        return self.items == []

    # 队列长度
    def size(self):
        return len(self.items)

    # 返回队头元素，如果队列为空的话，返回None
    def front(self):
        if self.is_Empty():
            print("当前队列为空！！")
        else:
            return self.items[len(self.items) - 1]


# 导入库
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import re
import urllib.parse
import time
import random

queueInt = Queue()  # 存储内链的队列
queueExt = Queue()  # 存储外链的队列

externalLinks = []
externalDomain = []
internalLinks = []
internalDomain = []

# 获取页面中所有外链的列表
def getExterLinksAndDomain(bs, exterurl):
    # 找出所有以www或http开头且不包含当前URL的链接
    for link in bs.find_all('a', href=re.compile
        ('^(http|www)((?!' + urlparse(exterurl).netloc + ').)*$')):
        # 按照标准，URL只允许一部分ASCII字符，其他字符（如汉字）是不符合标准的，
        # 我们的链接网址可能存在汉字的情况，此时就要进行编码。
        link.attrs['href'] = urllib.parse.quote(link.attrs['href'], safe='?=&:/')
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                queueExt.enqueue(link.attrs['href'])
                externalLinks.append(link.attrs['href'])
                externalDomain.append(urlparse(link.attrs['href']).hostname)

    return externalDomain, externalLinks


# 获取页面中所以内链的列表
def getInterLinks(bs, interurl):
    interurl = '{}://{}'.format(urlparse(interurl).scheme,
                                urlparse(interurl).netloc)

    # 找出所有以“/”开头的内部链接
    for link in bs.find_all('a', href=re.compile
        ('^(/|.*' + urlparse(interurl).netloc + ')')):
        link.attrs['href'] = urllib.parse.quote(link.attrs['href'], safe='?=&:/')


        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                # startsWith()方法用来判断当前字符串是否是以另外一个给定的子字符串“开头”的
                if (link.attrs['href'].startswith('//')):
                    if interurl + link.attrs['href'] not in internalLinks:
                        queueInt.enqueue(interurl + link.attrs['href'])
                        internalLinks.append(interurl + link.attrs['href'])
                elif (link.attrs['href'].startswith('/')):
                    if interurl + link.attrs['href'] not in internalLinks:
                        queueInt.enqueue(interurl + link.attrs['href'])
                        internalLinks.append(interurl + link.attrs['href'])
                else:
                    queueInt.enqueue(link.attrs['href'])
                    internalLinks.append(link.attrs['href'])


#     return internalLinks

def deepLinks():
    num = queueInt.size()
    while num > 1:
        i = queueInt.dequeue()
        if i is None:
            break
        else:
            print('访问的内链')
            print(i)
            print('找到的新外链')
            #         html = urlopen(i)
            headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'}

            html = requests.get(i, headers=headers_)
            time.sleep(random.random() * 3)
            domain1 = '{}://{}'.format(urlparse(i).scheme, urlparse(i).netloc)
            bs = BeautifulSoup(html.content, 'html.parser')
            getExterLinksAndDomain(bs, domain1)
            getInterLinks(bs, domain1)


def getAllLinks(url):
    global num
    #     html = urlopen(url)
    headers_ = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'}
    html = requests.get(url, headers=headers_)
    time.sleep(random.random() * 3)  # 模拟人类行为，间隔随机的时间
    domain = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)
    bs = BeautifulSoup(html.content, 'html.parser')

    getInterLinks(bs, domain)

    getExterLinksAndDomain(bs,domain)
    deepLinks()


getAllLinks('https://image.baidu.com/')

print(len(externalDomain))

for d in externalDomain:
    print(d)