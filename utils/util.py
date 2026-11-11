
import pymysql
from config import Config

# 建立数据库连接
def conn():
    connection = pymysql.connect(
        host=Config.HOST,
        port=Config.PORT,
        user=Config.USER,
        password=Config.PASSWORD,
        db=Config.DATABASE,
    )
    cur = connection.cursor()
    return connection, cur

# 关闭
def close():
    connection, cur = conn()
    cur.close()
    connection.close()

# 查询
def query(sql):
    connection, cur = conn()
    cur.execute(sql)
    result = cur.fetchall()
    close()
    return result

# 插入更新删除
def insert(sql):
    connection, cur = conn()
    cur.execute(sql)
    connection.commit()
    close()

