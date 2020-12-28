import requests
import time
import random
import pandas as pd
from lxml import etree

f = open('./shanghai_urls/ok_urls.txt')
urls = f.readlines()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
def get_detail(url):
    time.sleep(random.uniform(0, 1))
    res = requests.get(url, headers = headers)
    html = etree.HTML(res.text)
    items = html.xpath("/html/body/div[3]/div[1]/div[2]/div[2]")
    for item in items:
        house_price=item.xpath("./div[3]/div[2]/div/span/div/text()")[0]
        house_area=item.xpath("./div[4]/div[1]/div[1]/label/text()")[0].replace('建筑面积：约','').replace('㎡（以现场勘察为准）','')
        house_id=item.xpath("./div[4]/div[1]/div[2]/label/text()")[0].replace('编号：','')
        house_type=item.xpath("./div[4]/div[1]/div[3]/label/text()")[0].replace('\n','').replace(' ','').replace('户型：','')
        house_floor=item.xpath("./div[4]/div[2]/div[3]/label/text()")[0].replace('楼层：','')
        house_postion_1=item.xpath("./div[4]/div[2]/div[4]/label/div/a[1]/text()")[0]
        house_postion_2=item.xpath("./div[4]/div[2]/div[4]/label/div/a[2]/text()")[0]
        house_postion_3=item.xpath("./div[4]/div[2]/div[4]/label/div/a[3]/text()")[0]
        house_subway=item.xpath("./div[4]/div[2]/div[5]/label/text()")[0]
    else:
        house_price = None
        house_area = None
        house_id = None
        house_type = None
        house_floor = None
        house_postion_1 = None
        house_postion_2 = None
        house_postion_3 = None
        house_subway = None
    data = [house_price, house_area, house_id, house_type, house_floor, house_postion_1, house_postion_2, house_postion_3, house_subway]
    result = pd.DataFrame(data, columns = ['价格', '面积', 'ID', '户型', '楼层', '位置1', '位置2', '小区', '地铁'])
    return result

def main():
    for url in urls:
        result = get_detail(url)
    result.to_excel('蛋壳房源信息.xlsx')

if __name__ == "__main__":
    main()