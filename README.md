# 智能旅游推荐系统（Travel）

> 基于 **Django + MySQL + DeepSeek** 的旅行数据平台：集景点数据采集、数据清洗与分析、ECharts 可视化展示、用户管理和 AI 智能旅游路线推荐于一体。

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![MySQL](https://img.shields.io/badge/MySQL-5.7%2F8.0-orange)

## ✨ 功能特性

| 模块 | 说明 |
| --- | --- |
| 🔐 用户系统 | 注册 / 登录 / 编辑个人信息 / 头像上传，基于 Session 认证 |
| 🗺️ 景点总览 | 数据汇总统计、全国景点分布地图（ECharts）、热度排行、用户新增分布 |
| 📋 景点列表 | 景点名称搜索、按省份筛选、分页展示、按热度评分排序 |
| 📊 数据可视化 | 评分分布、评论数 TOP10、票价区间分布、区域分布、标签词云（jieba 分词）、省份景点数量、地区热门景点排行、省份平均评分 |
| 🤖 AI 路线推荐 | 基于 DeepSeek 大模型，根据「城市 + 季节 + 天数 + 预算」生成结构化路线表格（景点 / 游玩时间 / 特点 / 经纬度 / 预计花费） |
| 🧰 数据管道 | 爬虫采集 → 数据清洗 → 写入数据库 → 统计分析，全流程脚本化 |
| ⚙️ 后台管理 | Django Admin + [simpleui](https://github.com/newpanjing/simpleui) 主题，管理景点与用户数据 |

## 🛠 技术栈

- **后端**：Python 3.10、Django 5.2
- **数据库**：MySQL（PyMySQL 驱动，通过 `pymysql.install_as_MySQLdb()` 适配 Django）
- **数据处理**：pandas、jieba（中文分词）
- **AI**：DeepSeek API（OpenAI 兼容 SDK）
- **前端**：Bootstrap、jQuery、ECharts（含中国地图）

## 📂 项目结构

```
travel/
├── AI/
│   └── Get_Message.py          # DeepSeek AI 路线生成（API Key 读环境变量）
├── data/
│   ├── spider.py               # 景点数据爬虫（携程接口）
│   ├── data_pro.py             # 数据清洗：去重、缺失值、标签格式处理
│   ├── csv_to_sql.py           # 将清洗后数据写入 home_travelinfo 表
│   ├── data_analysis.py        # 统计分析，结果写入 part1 ~ part8 表
│   ├── data.csv                # 原始爬取数据（示例数据已附）
│   └── data_pro.csv            # 清洗后的数据（示例数据已附）
├── home/                       # 景点展示 + AI 路线推荐应用
├── user/                       # 用户系统应用（注册/登录/资料/头像）
├── ksh/                        # 数据可视化应用（part1 ~ part5 页面）
├── sql/
│   └── init_part_tables.sql    # part1 ~ part8 统计表参考建表语句
├── templates/                  # Django 模板
├── static/                     # 静态资源（Bootstrap / ECharts / jQuery 等）
├── media/                      # 用户上传文件（头像），不入库
├── utils/
│   └── util.py                 # MySQL 连接 / 查询工具函数
├── config.py                   # 数据库连接配置
├── manage.py
└── travel/                     # Django 项目配置
    ├── __init__.py             # 注册 PyMySQL 为 MySQL 驱动
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- MySQL 5.7 / 8.0
- （可选）DeepSeek API Key，仅 AI 路线推荐功能需要

### 1. 安装依赖

```bash
git clone <仓库地址>
cd travel

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. 配置数据库

修改根目录 [config.py](config.py)，填入你的 MySQL 连接信息：

```python
class Config:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = '你的数据库密码'
    DATABASE = 'db_travel'
    PORT = 3306
```

创建数据库并初始化统计表：

```bash
mysql -u root -p -e "CREATE DATABASE db_travel DEFAULT CHARSET utf8mb4;"
mysql -u root -p db_travel < sql/init_part_tables.sql
```

> `home_travelinfo`（景点）和 `user_userinfo`（用户）两张表由 Django 迁移自动创建；
> `part1` ~ `part8` 为统计分析结果表，建表参考 [sql/init_part_tables.sql](sql/init_part_tables.sql)。

### 3. 初始化数据（可选）

数据流如下：

```
spider.py（爬虫）→ data.csv → data_pro.py（清洗）→ data_pro.csv
                                              ├→ csv_to_sql.py    → home_travelinfo（景点明细）
                                              └→ data_analysis.py → part1 ~ part8（可视化统计数据）
```

仓库已附带 `data.csv` / `data_pro.csv` 示例数据，可直接运行：

```bash
python data/data_pro.py
python data/csv_to_sql.py
python data/data_analysis.py
```

> ⚠️ `spider.py` 中的请求头 / Cookie 是抓包时保存的**临时会话数据**，可能已失效；
> 如需自行爬取请替换为自己的 Cookie，并注意控制频率、遵守目标网站条款。

### 4. 数据库迁移并启动

```bash
python manage.py migrate
python manage.py createsuperuser   # 创建后台管理账号
python manage.py runserver
```

启动后访问：

- 首页（重定向到登录页）：<http://127.0.0.1:8000/>
- 后台管理：<http://127.0.0.1:8000/admin/>

### 5. 配置 DeepSeek API Key（AI 路线推荐）

API Key **不再硬编码在代码中**，统一从环境变量 `DEEPSEEK_API_KEY` 读取：

```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-你的key"
# Windows cmd
set DEEPSEEK_API_KEY=sk-你的key
# macOS / Linux
export DEEPSEEK_API_KEY="sk-你的key"
```

未配置时访问 AI 路线推荐会返回明确的错误提示，不影响其他功能。

> 🔒 安全提示：旧版代码中曾硬编码过一把 DeepSeek API Key（已在本次提交中移除）。
> 该 key 仍存在于本地历史记录中，建议在 [DeepSeek 开放平台](https://platform.deepseek.com) **删除旧 key 并重新申请**。

## 📡 路由说明

| 路由 | 说明 |
| --- | --- |
| `/` | 重定向到 `/user/` |
| `/user/login/` | 登录 |
| `/user/register/` | 注册 |
| `/user/changeinfo/` | 编辑个人信息 |
| `/user/upload_avatar/` | 上传头像（≤2MB，jpg/png/gif/webp） |
| `/user/logout/` | 退出登录 |
| `/travel/` | 首页：数据总览 + 全国分布地图 + 热度排行 |
| `/travel/travel_list` | 景点列表（搜索 / 省份筛选 / 分页） |
| `/travel/get_ai_travelRoute` | AI 旅游路线推荐（POST JSON：`city`、`season`、`days`、`budget`） |
| `/ksh/part1` | 景点评分分布 + 省份平均评分 |
| `/ksh/part2` | 景点评论数 TOP10 + 地区热门景点 |
| `/ksh/part3` | 票价区间分布 |
| `/ksh/part4` | 景点区域分布 |
| `/ksh/part5` | 景点省份分布（中国地图） |
| `/ksh/get_cityData` | 按城市查询热门景点（AJAX） |
| `/admin/` | 后台管理（simpleui 主题） |

## 🗄 数据库表说明

| 表名 | 说明 |
| --- | --- |
| `user_userinfo` | 用户信息（Django 迁移创建） |
| `home_travelinfo` | 景点明细：名称、城市/省份、评分、评论数、价格、经纬度、热度等（由 CSV 写入） |
| `part1` | 景点评分分布 |
| `part2` | 评论数 TOP10 景点 |
| `part3` | 票价区间分布 |
| `part4` | 景点区域分布 |
| `part5` | 标签 + 名称词云词频 |
| `part6` | 省份景点数量 |
| `part7` | 各地区热门景点排行（每城市 TOP10） |
| `part8` | 各省份景点数量与平均评分 |

## 🔒 安全与改进说明

本次已处理：

- ✅ 移除了硬编码在 `AI/Get_Message.py` 中的 DeepSeek API Key，改为从环境变量 `DEEPSEEK_API_KEY` 读取；
- ✅ 添加 `.gitignore`，`__pycache__`、`media/`、`.env` 等不再入库；
- ✅ 添加 `requirements.txt`，锁定依赖版本。

仍建议后续改进：

- [ ] 旧版泄露的 API Key 已在历史版本中出现，**务必到 DeepSeek 控制台吊销并换发**；
- [ ] `config.py` 中的数据库密码为明文，建议同样迁移到环境变量，且不要把真实凭证提交到仓库；
- [ ] 用户密码目前为明文存储，建议改用 Django 自带 `User` 模型或至少做哈希存储；
- [ ] `DEBUG = True`、`ALLOWED_HOSTS = []`、CSRF 中间件被注释均为开发态配置，上线前需要调整；
- [ ] `data/spider.py` 中存在抓包 Cookie 与固定路径，建议参数化并清理。

## 📄 License

本项目仅供学习参考。数据来源于公开网络爬取，版权归原作者所有；如需商用请遵守相关法律规定与目标网站服务条款。