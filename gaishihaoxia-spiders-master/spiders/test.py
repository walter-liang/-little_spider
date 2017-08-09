# -*- coding: utf-8 -*-
import requests
import os
import time
import re
from sendmail import fa_mail
from selenium import webdriver
try:
    import urlparse as parse
except:
    from urllib import parse



def get_html(url):
    d = webdriver.PhantomJS()
    d.get(url)
    myhtml = d.page_source.encode("utf-8")

    return myhtml
    #print myhtml



# 获取url函数===================================================
def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    img_regex = re.compile('<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
    link_regex = re.compile('<link.*?href=["\'](.*?)["\']', re.IGNORECASE)
    script_regex = re.compile('<script.*?src=["\'](.*?)["\']', re.IGNORECASE)

    url_list = webpage_regex.findall(html)
    img_list = img_regex.findall(html)
    link_list = link_regex.findall(html)
    script_list = script_regex.findall(html)

    return url_list+img_list+link_list+script_list


def parse_url(urls):
    # 筛选url并保存===================================================
    urls = [url for url in urls if "javascript" not in url]
    print(len(urls))
    url_nums = 0
    print_nums = 0
    errorurl = {}
    os.remove("all_urls.txt")
    f1 = open("all_urls.txt", 'a+')
    
    for url in urls:
        url = parse.urljoin(base_url, url)
        url_nums += 1
        try:
            r_code = s.get(url, timeout=10, headers=headers).status_code
            if r_code != 200:
                errorurl[str(r_code)] = url

            f1.write(url + "=====" + str(r_code) + "\n")
            print_nums += 1
        except Exception as e:
            print(e)
            f1.write("发现一个有异常的URL:"+url)
            errorurl["Error"] = url
        
        

        print"write a link "

    f1.close()
    print(url_nums)
    print(print_nums)
    fa_mail(errorurl, url_nums)



if __name__ == "__main__":
    # 基础配置===================================================
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Connection": "close"
        }

    base_url = "http://www.pingan.com"
    s = requests.Session()

    pa_html = get_html(base_url)
    urls = get_links(pa_html)
    parse_url(urls)









