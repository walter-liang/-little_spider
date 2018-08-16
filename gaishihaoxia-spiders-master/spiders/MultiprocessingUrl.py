# -*- coding: utf-8 -*-
import requests
from multiprocessing import Process, Manager ,Value, Lock
import os
import time
import re
from sendmail import fa_mail
from selenium import webdriver
try:
    import urlparse as parse
except:
    from urllib import parse


f1 = open("all_urls.txt", 'a+')

# 获取html完整源码===================================================
def urlmonitor(base_urls, url_nums, addre, errorurl, lock):
    

    d = webdriver.PhantomJS()
    d.get(base_urls)
    d.implicitly_wait(10) 
    html = d.page_source.encode("utf-8")
    d.quit()

    
    addre.append(base_urls)

    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    img_regex = re.compile('<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
    link_regex = re.compile('<link.*?href=["\'](.*?)["\']', re.IGNORECASE)
    script_regex = re.compile('<script.*?src=["\'](.*?)["\']', re.IGNORECASE)

    url_list = webpage_regex.findall(html)
    img_list = img_regex.findall(html)
    link_list = link_regex.findall(html)
    script_list = script_regex.findall(html)

    urls = url_list+img_list+link_list+script_list


    urls = [url for url in urls if "javascript" not in url]
    print(len(urls))
    
    
    
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Connection": "close"
        }

    s = requests.Session()

    
    for url in urls:
        url = parse.urljoin(base_urls, url)
        with lock: 
            url_nums.value += 1
        try:
            r_code = s.get(url, timeout=10, headers=headers).status_code
            if r_code > 400:
                errorurl[r_code] = url
            else:
                errorurl["error_url"] = 0
            f1.write(url + "===" + str(r_code) + "\n")

        except Exception as e:
            print(e)
            f1.write("发现一个有异常的URL:"+url+"\n")
            errorurl["exception_url"] = url      

        print"write a link "

    f1.close()


if __name__ == "__main__":
    
    os.remove("all_urls.txt")
    url_nums = Value('i', 0)
    lock = Lock()
    manager = Manager()
    errorurl = manager.dict()
    addre = manager.list()

    p1 = Process(target = urlmonitor, args=("https://www.baidu.com",url_nums, addre, errorurl,lock,))

    p2 = Process(target = urlmonitor, args=("http://m.baidu.com",url_nums, addre, errorurl,lock,))

    p1.start()
    p2.start()
    p2.join()

    scan_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    fa_mail(url_nums.value, scan_time, addre, errorurl)
    print '*************scan  over****************'





# server = multiprocessing.Manager()
# x    = server.Value('d', 0.0)
# arr  = server.Array('i', range(10))
# l    = server.list()
