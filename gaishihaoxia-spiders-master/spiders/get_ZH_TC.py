#!/usr/bin/python
# -*- coding:utf-8 -*-
import codecs
import lxml
from bs4 import BeautifulSoup
import urllib,urllib2,re
import urlparse


def download(url, user_agent='wswp', num_retries=2):

    headers = {'User-agent':user_agent}
    
    myproxy ="10.37.84.114:8080"
    proxy_support = urllib2.ProxyHandler({"https":myproxy})  
    opener = urllib2.build_opener(proxy_support)  
    urllib2.install_opener(opener)  

    print 'Downloading:', url
    request = urllib2.Request(url,headers=headers)
    
    try:
        html = urllib2.urlopen(request).read()
         
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries>0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url,user_agent,num_retries-1)
    return  html


for u in range(1,78):
    url ='https://www.zhihu.com/collection/27109279?page=%d'%u
    html = download(url)
    print 'this is page',u
    soup = BeautifulSoup(html,'lxml')
    tag = soup.find_all('div',class_='zh-summary summary clearfix')
    for t in tag:
        t['class'] = "zh-summary-summary-clearfix"
    all_list = soup.find_all(attrs={'class':["zm-item-title","zh-summary-summary-clearfix"]})
    for all in all_list:
        try:
            if all.name=='h2':
                print 'question:\n'+all.contents[0].string
            else:
                print 'anser:'+all.contents[0].string
                
        except UnicodeEncodeError,e:
            print u'编码错误'



            





#proxies=["http":"10.37.84.116:8080","http":"10.37.84.145:8080","http":"10.37.84.118:8080","http":"10.37.84.119:8080","http":"10.37.84.115:8080","http":"10.37.84.149:8080","http":"10.37.84.126:8080","http":"10.37.84.148:8080","http":"10.37.84.125:8080","http":"10.37.84.150:8080","http":"10.37.84.117:8080","http":"10.37.84.114:8080","http":"10.37.84.117:8080"]
