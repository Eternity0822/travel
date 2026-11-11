-- 统计分析结果表（part1 ~ part8）参考建表语句
-- 数据来源：data/data_analysis.py
-- 注意：home_travelinfo / user_userinfo 由 Django 迁移自动创建，无需手动建表

USE db_travel;

-- 景点评分分布（data_analysis.py -> part1）
CREATE TABLE IF NOT EXISTS part1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    score DECIMAL(4, 1) NOT NULL COMMENT '评分',
    value INT NOT NULL COMMENT '数量'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '评分分布';

-- 评论数 TOP10 景点（part2）
CREATE TABLE IF NOT EXISTS part2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT '景点名称',
    value INT NOT NULL COMMENT '评论数量'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '评论数 TOP10';

-- 票价区间分布（part3）
CREATE TABLE IF NOT EXISTS part3 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '价格区间',
    value INT NOT NULL COMMENT '数量'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '票价区间分布';

-- 景点区域分布（part4）
CREATE TABLE IF NOT EXISTS part4 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT '区域名称',
    value INT NOT NULL COMMENT '数量'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '区域分布';

-- 词云词频（part5）
CREATE TABLE IF NOT EXISTS part5 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT '词语',
    value INT NOT NULL COMMENT '出现次数'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '词云词频';

-- 省份景点数量（part6）
CREATE TABLE IF NOT EXISTS part6 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '省份',
    value INT NOT NULL COMMENT '景点数量'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '省份景点数量';

-- 各地区热门景点排行（part7，每城市按热度 TOP10）
CREATE TABLE IF NOT EXISTS part7 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50) NOT NULL COMMENT '城市',
    name VARCHAR(255) NOT NULL COMMENT '景点名称',
    value DECIMAL(10, 2) NOT NULL COMMENT '热度评分'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '地区热门景点排行';

-- 各省份景点数量与平均评分（part8）
CREATE TABLE IF NOT EXISTS part8 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '省份',
    travel_num INT NOT NULL COMMENT '景点数量',
    avg_score DECIMAL(4, 2) NOT NULL COMMENT '平均评分'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '省份平均评分';