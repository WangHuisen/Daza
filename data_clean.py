import pandas as pd
import numpy as np
import json
import requests
from pathlib import Path
import re
from sqlalchemy import create_engine
import pymysql

engine = create_engine("mysql+pymysql://root:whs666666@localhost:3306/danke?charset=utf8")
files = Path(r"X:\pyProjs\dankegonyu\北京蛋壳公寓").glob("*.csv")
dfs = [pd.read_csv(f) for f in files]
df = pd.concat(dfs)
print(df.head())


jp = df['价格'] != '价格'
df = df.loc[jp,:]
print(df.head())
df["价格"] = df["价格"].astype("float64")
df["面积"] = df["面积"].astype("float64")
df = df[df["楼层"].notnull()]
df["所在楼层"] = df["楼层"].apply(lambda x: x.split('/')[0])
df["所在楼层"] = df["所在楼层"].astype("int32")
df["总楼层"] = df["楼层"].apply(lambda x: x.split('/')[1])
df["总楼层"] = df["总楼层"].str.replace("层", "").astype("int32")

def subway_num(row):
    num = row.count('号线')
    return num

def subway_distance(row):
    distance = re.search(r'\d+(?=米)', row)
    if distance == None:
        return float(-1)
    else:
        return float(distance.group(0))

# def lng_lat(row):
#     if row == ''
# def baidu(row):
#     url = "http://api.map.baidu.com/geocoding/v3/?"
#     para = {
#         "address": row,
#         "city": "北京",
#         "output": "json",
#         "ak": "DwVB2aXCr9VxzjeD0IyfVqTfV6fpftMQ"
#     }
#     try:
#         res = requests.get(url, para)
#         result = res.json()
#         loc = result["result"]["location"]
#         position = f"{loc['lng'],loc['lat']}"
#         print(position, type(position))
#         return position
#     except:
#         return 'Error'

df["地铁数"] = df["地铁"].apply(subway_num)
df["地铁数"].astype("int32")
df["距离地铁距离"] = df["地铁"].apply(subway_distance)
print(df['价格'])
print(df['距离地铁距离'])
# print(df["距离地铁距离"])
# df["距离地铁距离区间"] = pd.cut(df['距离地铁距离'], [-100000, 100, 500, 1000, 1500, 2000, 3000, 1000000000000], labels = ['100米以内', '100-500米', '500-1000米', '1000-1500米', '1500-2000米', '2000-3000米', '3000米以上'], right = False)
df['价格区间'] = pd.cut(df['价格'], [0, 1000, 2000, 3000, 4000, 1000000000], labels = ['1000元以下', '1000-2000元', '2000-3000元', '3000-4000元', '4000元以上'], right = False)
df['完整地址'] = df['位置1'] + df['位置2'] + df['小区']
# df2 = df.astype(object).where(pd.notnull(df), None)
# print(df['距离地铁距离区间'].head(100))
# df['完整地址'].astype('object')
# df['经纬度'] = df['完整地址'].apply(baidu)
df.to_sql(name = 'danke', con = engine, if_exists = 'append', index = False)
print('Over!')