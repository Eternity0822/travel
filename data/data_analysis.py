
from collections import Counter
import jieba
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

df = pd.read_csv('C:\\Users\\lenovo\\Desktop\\智能旅游推荐系统\\travel\\data\\data_pro.csv')

# 统计评分分布
def part1():
    print("正在统计评分分布并写入数据库...")
    data = df.copy()
    data = data[data['评分'] != 0.0] # 去除评分缺失的数据

    score_counts = data['评分'].value_counts() # 统计评分分布
    # 先清空表数据，再将统计结果写入 sql
    truncate_sql = 'truncate table part1'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into part1(score, value) values(%s, %s)'

    for score, value in score_counts.items():
        cursor.execute(sql, (score, value)) # 执行 sql 语句
    conn.commit()

# 根据评论数排名
def part2():
    print("正在根据评论数排名并写入数据库...")
    top_10 = df.nlargest(10, '评论数量')[['景点名称', '评论数量']] # 根据评论数排序，取前 10 条数据
    # 先清空表数据，再将统计结果写入 sql
    truncate_sql = 'truncate table part2'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into part2(name, value) values(%s, %s)'

    for index, row in top_10.iterrows():
        cursor.execute(sql, (row['景点名称'], row['评论数量'])) # 执行 sql 语句
    conn.commit()

# 统计票价区间分布
def part3():
    print("正在统计票价区间分布并写入数据库...")
    df['价格'] = df['价格'].astype(str)
    df['价格'] = df['价格'].replace('免费', '0')

    df['价格'] = df['价格'].astype(float) # 将价格列转换为数值类型
    
    bins = [0, 1, 50, 100, 200, 500, 1000, float('inf')] # 定义价格区间
    labels = ['0', '1-50', '50-100', '100-200', '200-500', '500-1000', '1000以上'] # 定义区间标签
    price_dis = pd.cut(df['价格'], bins=bins, labels=labels, right=False) # 将价格划分到对应的区间
    price_counts = price_dis.value_counts().sort_index() # 按区间顺序排序

    # 先清空表数据，再将统计结果写入 sql
    truncate_sql = 'truncate table part3'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into part3(name, value) values(%s, %s)'

    for index, value in price_counts.items():
        cursor.execute(sql, (index, value))
    conn.commit()

# 统计区域分布
def part4():
    print("正在统计区域分布并写入数据库...")
    data = df.copy()
    area_counts = data['区域名称'].value_counts() # 统计区域分布

    truncate_sql = 'truncate table part4'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into part4(name, value) values(%s, %s)'

    for index, value in area_counts.items():
        cursor.execute(sql, (index, value))
    conn.commit()

def load_stopwords():
    stopwords = set([
        '的', '了', '和', '是', '在', '我', '有', '就', '不', '人', '都', '一个', '上', 
        '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', 
        '这', '还', '但', '我们', '他们', '她们', '它们', '吗', '呢', '吧', '啊', '哦', '嗯', '呀', '哇',
        ',', '.', '！', '？', '：', '；', '（', '）', '【', '】', '《', '》', '“', '”', '‘', '’',
        ':', '+', '-', '*', '/', '=', '<', '>', '&', '|', '^', '%', '$', '#', '@', '~', '`', '」', 
        '「', '…', '—', '～', '·', '•', '『', '』', '——', '，', '。', '?', '!', '！', '、', '(', ')', 
        '[', ']', '{', '}', '"', "'", '\\', ' ', '\n', '\t'
    ])
    return stopwords

# 词云分析
def part5():
    print("正在进行词云分析并写入数据库...")
    all_texts = df['标签列表'].fillna('').tolist() + df['景点名称'].fillna('').tolist() # 将标签列表和景点名称合并成一个文本列表

    stopwords = load_stopwords() # 加载停用词列表

    words = []
    for text in all_texts:
        seg_list = jieba.cut(text) # 使用 jieba 分词
        words.extend([word for word in seg_list if word not in stopwords and word.strip() != '']) # 去除停用词
    word_count = Counter(words) # 统计词频

    word_count_df = pd.DataFrame(word_count.items(), columns=['词语', '出现次数']) # 将词频统计结果转换为 DataFrame
    
    # 先清空表数据，再将统计结果写入 sql
    truncate_sql = 'truncate table part5'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into part5(name, value) values(%s, %s)'

    for index, row in word_count_df.iterrows():
        cursor.execute(sql, (row['词语'], row['出现次数'])) # 执行 sql 语句
    conn.commit()

# 统计省份景点数量
def part6():
    print("正在统计省份景点数量并写入数据库...")
    pro_counts = df['省份'].value_counts() # 统计省份景点数量

    truncate_sql = 'truncate table part6'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into part6(name, value) values(%s, %s)'

    for index, value in pro_counts.items():
        cursor.execute(sql, (index, value))
    conn.commit()

# 各地区热门景点排行
def part7():
    print("正在统计各地区热门景点排行并写入数据库...")
    city_travel_rank = df.sort_values(['热度评分'], ascending=False).groupby('城市名称').head(10)
    rank_data = city_travel_rank[['城市名称', '景点名称', '热度评分']] # 按热度评分排序，取每个城市前 10 条数据
    
    # 先清空表数据，再将统计结果写入 sql
    truncate_sql = 'truncate table part7'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into part7(city, name, value) values(%s, %s, %s)'

    for index, row in rank_data.iterrows():
        cursor.execute(sql, (row['城市名称'], row['景点名称'], row['热度评分'])) # 执行 sql 语句
    conn.commit()

# 各省份景点平均评分
def part8():
    print("正在统计各省份景点平均评分并写入数据库...")
    data = df.copy()
    data = data[data['评分'] != 0.0]
    data['评分'] = data['评分'].astype(float) # 将评分列转换为数值类型

    pro_ratings = data.groupby('省份')['评分'].agg(['count', 'mean']).reset_index() # 按省份分组，计算平均评分\
    pro_ratings.columns = ['省份', '景点数量', '平均评分'] # 重命名列名
    pro_ratings['平均评分'] = pro_ratings['平均评分'].round(2) # 保留两位小数

    # 先清空表数据，再将统计结果写入 sql
    truncate_sql = 'truncate table part8'
    cursor.execute(truncate_sql)
    conn.commit()

    sql = 'insert into part8(name, travel_num, avg_score) values(%s, %s, %s)'

    for index, row in pro_ratings.iterrows():
        cursor.execute(sql, (row['省份'], row['景点数量'], row['平均评分'])) # 执行 sql 语句
    conn.commit()

if __name__ == '__main__':  
    part1()
    part2()
    part3()
    part4()
    part5()
    part6()
    part7()
    part8()
    cursor.close()
    conn.close()

# 分析结果存储到数据库的part1-part8表中，用于前端可视化展示。