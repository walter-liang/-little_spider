#!/usr/bin/python
#encoding:utf-8

import requests,Queue
import urllib,urllib2,re
import urlparse
#from bs4 import BeautifulSoup


def link_crawler(seed_url, link_regex='',max_depth=3):

    crawl_queue = Queue.deque([seed_url])
    
    seen = {seed_url:0}

    while crawl_queue:

        url = crawl_queue.pop()
           #从队列取出，得到深度值
        try:
            html = download(url)
            print 'start new queue'
            depth = seen[url]
            url_list=[]
            
            if depth != max_depth:  #如果当前深度不等于最大深度
                url_list = get_links(html)
                for link  in url_list:
                    link = urlparse.urljoin(seed_url,link)
                    
                    if link not in seen and 'pingan.com'in link:
                        
                        seen[link] = depth+1
                        
                        with open('pingan_link.txt','a') as f:
                            f.write(link+'\n')
                            print 'get  a link'

                        crawl_queue.append(link)

            else:
                print 'depth is enough'
                continue
        except Exception as e:
            print  e
            #continue




# def download(url,num_retries=2):
        # headers = {"User-agent":"user_lkj"}
        # proxies={"http":"10.35.29.57:8080"}
        
        # try:
            # r = requests.get(url,headers=headers,proxies=proxies,timeout=5)
            # html = r.text
        # except requests.exceptions.RequestException as e:
            # print 'the error: ',e
            # html= None
            # if num_retries>0:
                # if hasattr(e, 'code') and 500 <= e.code < 600:
                    # return download(url,num_retries-1)
        # print html
        # return  html

        
def download(url, user_agent='wswp', num_retries=2):

    headers = {'User-agent':user_agent}
    
    #需要代理就在这里配置
    myproxy ="10.35.29.57:8080"
    proxy_support = urllib2.ProxyHandler({"http":myproxy})  
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
        

def get_links(html):

    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return  webpage_regex.findall(html)   


    
if __name__ == '__main__':
    link_crawler('http://stock.pingan.com')

