
# 将 csv 文件中的数据写入 sql

import pandas as pd
import pymysql
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import Config

# 建立连接
conn = pymysql.connect( 
    host = Config.HOST,
    user = Config.USER,
    password = Config.PASSWORD,
    database = Config.DATABASE,
)

cursor = conn.cursor()

# 先清空表数据，再将 csv 文件中的数据写入 sql
truncate_sql = 'truncate table home_travelinfo'
cursor.execute(truncate_sql)
conn.commit()

sql = 'insert into home_travelinfo(unique_id, area, name, review_count, rating, is_ad, is_recommended, city, image_url, distance_from_center, tags, ' \
      'detail_link, market_price, discount_price, discount_description, actual_price, price_type, price_type_description, is_free, latitude, longitude, popularity_score, province)' \
      'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

df = pd.read_csv('C:\\Users\\lenovo\\Desktop\\智能旅游推荐系统\\travel\\data\\data_pro.csv')
df = df.fillna('暂无') # 填补缺失值

for index, row in df.iterrows():
    cursor.execute(sql, (tuple(row))) # 执行 sql 语句

conn.commit()
cursor.close()
conn.close()
