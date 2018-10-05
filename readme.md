## 说明
运用Flask写的个人博客

这是一个博客，带有前端展示和后台编写

## Ecosystem

| Project | Status | Description                |
| ------- | ------ | -------------------------- |
| python  | 3.6.0  | 在这个版本以及以上都课可以 |
| Flask   | 1.0.2  | 1.x版本都可以              |

## 运行方式

- 下载源码:

```
https://github.com/tianjinqiujie/my_blog.git

或者直接到https://github.com/tianjinqiujie/my_blog 下载zip文件
```

- 安装依赖:

```
pip install -r requirements.txt
```

- 配置setting.py:

```python
# setting.py 为项目配置文件
# 配置DB
    POOL = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host='127.0.0.1',
        port=3306,
        user='root',	# 数据库账号
        password='*',	# 数据库密码
        database='blog',
        charset='utf8'
    )
```

- 启动:

```
# 如果你的依赖已经安全完成并且具备运行条件,可以直接在Run下运行manage.py
# 到Run目录下:
>>>python manage.py
```

## 个人博客地址

https://www.mypy3.cn/

## Bug修复
1. 修复了分页显示问题
2. 修复了详情页搜索问题
3. 删除过多的代码
4. 调整静态目录结构
5. 更新bootstrap-3.3.7以及font-awesome-4.7.0

## 修改

1. 增加了图片上传
2. 编辑器改为markdown编辑器
3. 增加了代码高亮

## 展示

![Alt text](https://github.com/tianjinqiujie/my_blog/blob/master/Screenshots/1.png)

![Alt text](https://github.com/tianjinqiujie/my_blog/blob/master/Screenshots/2.png)

![Alt text](https://github.com/tianjinqiujie/my_blog/blob/master/Screenshots/3.png)

![Alt text](https://github.com/tianjinqiujie/my_blog/blob/master/Screenshots/4.png)