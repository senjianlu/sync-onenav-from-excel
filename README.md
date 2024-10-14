<div align="center">
    <img src=https://raw.githubusercontent.com/senjianlu/sync-onenav-from-excel/master/logo.png width=20%/>
</div>

# sync-onenav-from-excel
将 Excel 中的网址同步到 OneNav 一为导航中。  

## 事前提醒
### 一、该脚本只对来源是 Excel 的网址进行同步
我实现区分来源的方法是：首次将 Excel 表格中的网址导入 OneNav 时，会在 `wp_postmeta` 表中添加 `meta_key` 为 `_sync_site_id` 的记录，而它的值 `meta_value` 为 Excel 表格中设定的 `自定义 ID`。  
这些数据后续就会被判断为来源于 Excel 表格。  
**任何你手动添加的、不存在 `_sync_site_id` 数据的网址，因此都不会被修改到**。  

### 二、⭐ 请在执行脚本备份整站
虽然我已经尽量缩小了影响范围，脚本仅会操作 `wp_posts`、`wp_postmeta`、`wp_term_taxonomy` 和 `wp_term_relationships` 表，但是仍然无法保证 100% 不会损坏你的站点数据。  
**你可以在 `工具` -> `导出` 处执行下载备份的操作**。  

### 三、有问题和建议请提交 Issue
我在维护自己的导航站点：[steam.cash](https://steam.cash)，所以我会优先根据自己的需求更新脚本。  
如果你有好的想法，可以提交 [Issue](https://github.com/senjianlu/sync-onenav-from-excel/issues)，我会考虑添加到脚本中。  
**但如果你发现了 Bug，请不要有顾虑直接提交 Issue 或是在线联系我，我会尽快修复**。

## 使用方法

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


## 更多文章
你可以在我的[博客](https://senjianlu.com)中找到数篇与 [OneNav 相关的文章](https://senjianlu.com/tags/steam-cash/)，如果你想二开，它们应该会对你有所帮助。
- [使用 Docker 部署 MySQL + WordPress 并安装 OneNav 一为导航](https://senjianlu.com/2024/10/10/docker_mysql_wordpress_onenav/)
- [OneNav 一为导航新建目录与导航网址](https://senjianlu.com/2024/10/11/wordpress_onenav_add_link/)
- ⭐ [WordPress 表结构描述与 OneNav 一为导航新建网址实际生成的表数据](https://senjianlu.com/2024/10/12/wordpress_data_modeler_onenav/)
- [OneNav 一为导航通过 Python3 脚本实现网址的增删改查](https://senjianlu.com/2024/10/12/onenav_python3_site_crud/)