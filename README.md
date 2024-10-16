<div align="center">
    <img src=https://raw.githubusercontent.com/senjianlu/sync-onenav-from-excel/master/logo.png width=15%/>
</div>

# sync-onenav-from-excel
将 Excel 中的网址同步到 OneNav 一为导航中。  
**⚠️ 该脚本仅适用于 `V4.1810` 和其前后没有数据结构变化的版本**！

## 事前提醒
### 一、该脚本只对来源是 Excel 的网址进行同步
实现区分来源的方法是：首次将 Excel 表格中的网址导入 OneNav 时，会在 `wp_postmeta` 表中添加 `meta_key` 为 `_sync_site_id` 的记录，而它的值 `meta_value` 为 Excel 表格中设定的 `自定义 ID`。  
这些数据后续就会被判断为来源于 Excel 表格。  
**任何你手动添加的、不存在 `_sync_site_id` 数据的网址，都不会被修改到**。  

### 二、⭐ 请在执行脚本前备份整站
虽然我已经尽量缩小了影响范围，脚本仅会操作 `wp_posts`、`wp_postmeta`、`wp_term_taxonomy` 和 `wp_term_relationships` 表，但是仍然无法保证 100% 不会出现预想外的情况而损坏你的站点数据。  
**你可以在 `工具` -> `导出` 处执行下载备份的操作**。  

### 三、有问题和建议请提交 Issue
如果你有好的想法，可以提交 [Issue](https://github.com/senjianlu/sync-onenav-from-excel/issues)，我会考虑添加到脚本中。  
**如果你发现了 Bug，请不要有顾虑直接提交 Issue 或是在线联系我，我会尽快修复**。

## 使用方法
### 一、安装 Python3
在 [Python 官网](https://www.python.org/) 下载安装包，安装并将 Python3 添加到环境变量中。  
具体可以参考：[Python3 环境搭建](https://www.runoob.com/python3/python3-install.html)  

### 二、下载源码
如果你可以访问 GitHub，可以直接使用 `git clone` 命令下载源码：
```shell
git clone https://github.com/senjianlu/sync-onenav-from-excel.git
```
> 如果你存在网络问题，那么可以下载压缩包并解压：  
> ![下载源码压缩包](https://image.senjianlu.com/blog/2024-10-14/193912.png)

### 三、安装依赖
在项目根目录下执行以下命令安装依赖：
```shell
# 进入项目目录
cd sync-onenav-from-excel
# 安装 Python 依赖
pip3 install -r requirements.txt
# pip install -r requirements.txt
```
> 如果你存在网络问题，那么可以切换下源，具体可以参考：[pip 使用国内镜像源](https://www.runoob.com/w3cnote/pip-cn-mirror.html)

### 四、修改配置文件
在项目根目录下找到 `config.ini` 文件，修改其中的配置信息，主要是数据库连接和导航站域名：
```ini
# MySQL 连接信息
[mysql]
host = "127.0.0.1"
port = "3306"
username = "root"
password = "myPasswordForMySQL"
database = "wordpress
```
```ini
# 导航站信息
[onenav]
# 域名
domain = "https://steam.cash"
```

### 五、打开 Excel 文件填入数据
在项目根目录下找到 `OneNav 导航站数据集.xlsx` 文件，打开并填入数据。  
详细的填写方法可以参考 Excel 中「使用方法」，它总是最新的：  
![使用方法](https://image.senjianlu.com/blog/2024-10-14/194501.png)

### 六、执行脚本
进入 `app` 目录，执行 `main.py` 脚本：
```shell
cd app
# 执行脚本
python3 main.py
# python main.py
```
我尽量让脚本的输出足够丰富，以便你可以清楚地知道在发生什么：  
![运行截图](https://image.senjianlu.com/blog/2024-10-14/195105.png)

### 七、查看结果
之后回到你的导航站点，刷新页面，应该就可以看到对应的修改生效了 🎉。


## 实现流程
1. 读取 Excel 文件
2. 解析 Excel 文件获取 `网址`
3. 查询 OneNav 数据库，获取当前存在的 `网址`
4. 对比以找出需要新增、删除、修改的 `网址`
5. 执行新增、删除、修改操作

## 功能列表
- ✅ `网址` `site`  
    - ✅ 增加 (insert)  
    - ✅ 删除 (delete)  
    - ✅ 修改 (update)  
    - ✅ 查询 (select)  
- ⬜ `网址分类` `favorite`  
    - ⬜ 增加 (insert)
    - ⬜ 删除 (delete)
    - ⬜ 修改 (update)
    - ✅ 查询 (select)
    - ⬜ 展示 (show)
- ⬜ `网址标签` `tag`  
    - ⬜ 增加 (insert)
    - ⬜ 删除 (delete)
    - ⬜ 修改 (update)
    - ✅ 查询 (select)
    - ⬜ 展示 (show)
- ⬜ 将结果更新回 Excel 表中

## 测试
准备工作：
```bash
# 进入 tests 目录
cd tests
# 启动 MySQL
docker run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=myPasswordForMySQL mysql:5.7
# 创建 WordPress 数据库
docker exec -i mysql mysql -uroot -pmyPasswordForMySQL -e "CREATE DATABASE wordpress;"
# 修改下默认编码
docker exec -i mysql mysql -uroot -pmyPasswordForMySQL -e "ALTER DATABASE wordpress CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
# 导入测试所需数据
docker exec -i mysql mysql -uroot -pmyPasswordForMySQL wordpress < sql/create_tables_before_test.sql
docker exec -i mysql mysql -uroot -pmyPasswordForMySQL wordpress < sql/insert_data_before_test.sql
```

执行各个单元测试：
```bash
# 进入 tests 目录
# cd tests
# 执行测试
pytest -vs favorite_all.py
pytest -vs tag_all.py
pytest -vs site_all.py
```

结束后的清理工作：
```bash
# 删除 MySQL 容器
docker stop mysql && docker rm mysql
```

## 更多文章
你可以在我的[博客](https://senjianlu.com)中找到数篇与 [OneNav 相关的文章](https://senjianlu.com/tags/steam-cash/)，如果你想二开，它们应该会对你有所帮助。
- [使用 Docker 部署 MySQL + WordPress 并安装 OneNav 一为导航](https://senjianlu.com/2024/10/10/docker_mysql_wordpress_onenav/)
- [OneNav 一为导航新建目录与导航网址](https://senjianlu.com/2024/10/11/wordpress_onenav_add_link/)
- ⭐ [WordPress 表结构描述与 OneNav 一为导航新建网址实际生成的表数据](https://senjianlu.com/2024/10/12/wordpress_data_modeler_onenav/)
- [OneNav 一为导航通过 Python3 脚本实现网址的增删改查](https://senjianlu.com/2024/10/12/onenav_python3_site_crud/)