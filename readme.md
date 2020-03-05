# 漂流图书：Django后端 rebuild

## 运行环境

阿里云 Ubuntu 16.04.3 LTS

Python 3.6.8

virtualenv 20.0.7

django 2.1.4

mysql  Ver 14.14 Distrib 5.7.27, for Linux (x86_64) using  EditLine wrapper

nginx version: nginx/1.10.3 (Ubuntu)

Redis server v=3.0.6 sha=00000000:0 malloc=jemalloc-3.6.0 bits=64 build=7785291a3d2152db

## 运行

```bash
# 修改settings.py中的数据库相关配置，连接数据库需要pymysql
# 如有必要，需将各个app目录下的migration历史删除
# python manage.py migratetions
# python manage.py migrate
python manage.py runserver 8000
# cd 到redis-server所在目录
./redis-server
nginx -c <绝对路径>/nginx.conf
```

## 其他依赖

```bash
# 连接mysql需要的包
pip install pymysql
# 安装阿里云短信服务所需要的包
pip install aliyun-python-sdk-core
# rsa
pip install rsa
# 由于有用到爬虫
pip install requests
pip install lxml
```

## 其他提示

```bash
# django版本过高会提示pymysql所支持的引擎版本过低
# 创建数据库时记得加 charset=utf8 ，否则可能不允许存储中文
# 如果实在是忘了设置utf8，可以逐张表设置
alter table `tablename` convert to character set utf8;
# import mysql.connector测试失败
# 如果你的 MySQL 是 8.0 版本，密码插件验证方式发生了变化，早期版本为 mysql_native_password，8.0 版本为 caching_sha2_password，所以需要做些改变：
# 登录mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourPassword';
FLUSH PRIVILEGES;

```

