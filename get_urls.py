from lxml import etree
from pathlib import Path
import pandas as pd
import numpy as np
import requests
import random
import time
import math


num = int(input('你要爬取多少条数据？')) / 20
num = math.floor(num)
root_url = 'https://www.danke.com/room/sh?page={}'
url_holder = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
count = 0
def get_page_urls(url):
    time.sleep(random.uniform(0, 1))
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        res = response.content.decode('utf-8')
        html = etree.HTML(res)
        items = html.xpath("/html/body/div[3]/div/div[6]/div[2]/div[1]/div")
        
        global count
        for item in items:
            url = item.xpath('.//div[@class="r_lbx_cena"]/a/@href')
            url_holder.append(url)
            count += 1 
            print('抓取第{}条数据'.format(count))
        return url_holder
    else:
        print('请求失败！')
        return None

def get_all_urls(num):
    for i in range(1, num + 1):
        url = root_url.format(i)
        url_holder = get_page_urls(url)
        print('第{}页数据抓取完毕！'.format(i))
        time.sleep(1)
    return  url_holder

if __name__ == "__main__":
    url_holder = get_all_urls(num)
    with open("./urls_4.txt", 'w+') as f:
        f.write('北京蛋壳公寓租房信息：\n')
        for i in url_holder:
            f.write(i[0])
            f.write('\n')
    print('抓取结束！')
        