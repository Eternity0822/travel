
# 数据清洗

import pandas as pd

df = pd.read_csv('C:\\Users\\lenovo\\Desktop\\智能旅游推荐系统\\travel\\data\\data.csv', 
                 names = ['景点id', '区域名称', '景点名称', '评论数量', '评分', '是否为广告内容', '是否为推荐内容', '城市名称', 
                         '封面图片链接', '到市中心的距离', '标签列表', '详情页链接', '市场价', '优惠价', '优惠描述', 
                         '价格', '价格类型', '价格类型描述', '是否免费', '纬度', '经度', '热度评分', '省份'])

df = df.drop_duplicates(subset = ['景点id'])

# 处理缺失值和标签列表格式
df['评分'] = df['评分'].fillna(0)
df['评论数量'] = df['评论数量'].fillna(0)
df['热度评分'] = df['热度评分'].fillna(0)
df['标签列表'] = df['标签列表'].str.replace('[', '').str.replace(']', '').str.replace("'", '')
df.to_csv('C:\\Users\\lenovo\\Desktop\\智能旅游推荐系统\\travel\\data\\data_pro.csv', index = False)