#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: main.py
# @DATE: 2024/10/12
# @TIME: 16:20:11
#
# @DESCRIPTION: 主函数


from config import CONFIG
from db import get_db_engine, get_db_session
from excel import get_file_path, load_data
from onenav.site import generate_sites_from_excel_data
from sync import do_sync
from onenav.favorite import check_all as favorite_check_all
from onenav.tag import check_all as tag_check_all


def check_config():
    """
    检查配置文件
    """
    # 1. 检查 MySQL 配置
    try:
        mysql_config = CONFIG["mysql"]
        mysql_host, mysql_port, mysql_username, mysql_password, mysql_database = (
            mysql_config["host"],
            mysql_config["port"],
            mysql_config["username"],
            mysql_config["password"],
            mysql_config["database"]
        )
        if mysql_host == "" or mysql_port == "" or mysql_username == "" or mysql_password == "" or mysql_database == "":
            raise Exception("MySQL 配置信息不完整！")
    except Exception as e:
        print("MySQL 配置信息读取失败，请检查配置文件！")
        return False
    # 2. 检查 Excel 配置
    try:
        # 2.1 检查文件名
        file_name = CONFIG["excel"]["file_name"]
        if not file_name:
            raise Exception("Excel 文件名为空！")
        # 2.2 检查站点表单名
        sites_sheet = CONFIG["excel"]["sites_sheet"]
        if not sites_sheet:
            raise Exception("Excel 站点表单名 sites_sheet 为空！")
        # 2.3 检查备用链接地址表单名
        spare_links_sheet = CONFIG["excel"]["spare_links_sheet"]
        if not spare_links_sheet:
            raise Exception("Excel 备用链接地址表单名 spare_links_sheet 为空！")
    except Exception as e:
        print("Excel 文件与表单名读取失败，请检查配置文件！")
        return False
    # 3. 检查同步模式
    try:
        mode = CONFIG["sync"]["mode"]
        if mode not in ["part", "full"]:
            raise Exception("同步模式错误！")
    except Exception as e:
        print("同步模式读取失败，请检查配置文件！")
        return False
    # 4. 导航站点信息
    try:
        domain = CONFIG["onenav"]["domain"]
        if domain == "":
            raise Exception("导航站点域名为空！")
    except Exception as e:
        print("导航站点信息读取失败，请检查配置文件！")
        return False
    # 5. 返回
    print("="*50 + "\n配置文件检查通过！\n" + "="*50)
    return True


def main():
    """
    主函数
    """
    # 1. 检查配置文件
    if not check_config():
        return
    # 2. 获取数据库连接信息
    mysql_host, mysql_port, mysql_username, mysql_password, mysql_database = (
        CONFIG["mysql"]["host"],
        CONFIG["mysql"]["port"],
        CONFIG["mysql"]["username"],
        CONFIG["mysql"]["password"],
        CONFIG["mysql"]["database"]
    )
    # 3. 获取数据库引擎
    engine = get_db_engine(
        mysql_host=mysql_host,
        mysql_port=mysql_port,
        mysql_username=mysql_username,
        mysql_password=mysql_password,
        mysql_database=mysql_database
    )
    # 4. 建立数据库连接
    try:
        session = get_db_session(engine)
    except Exception as e:
        print("MySQL 数据库连接失败，请检查配置文件和数据库连接！")
        return
    # 5. 获取 Excel 文件路径
    try:
        file_name = CONFIG["excel"]["file_name"]
        file_path = get_file_path(file_name)
    except Exception as e:
        session.close()
        print("Excel 文件名读取失败，请检查配置文件和文件路径！")
        return
    # 6. 读取 Excel 数据
    sites_sheet = CONFIG["excel"]["sites_sheet"]
    spare_links_sheet = CONFIG["excel"]["spare_links_sheet"]
    try:
        data = load_data(file_path, sites_sheet, spare_links_sheet)
    except Exception as e:
        session.close()
        print("Excel 数据读取失败，请检查数据合法性！")
        return
    # 7. 使用 Excel 表中的数据创建 ORM 对象
    sites = generate_sites_from_excel_data(data)
    # 8. 检查所涉及的网址分类和网址标签是否都存在
    all_favorite_ids = []
    all_tag_ids = []
    for site in sites:
        all_favorite_ids.extend(site.favorite_ids)
        all_tag_ids.extend(site.tag_ids)
    all_favorite_ids = list(set(all_favorite_ids))
    all_tag_ids = list(set(all_tag_ids))
    if favorite_check_all(all_favorite_ids, session) and tag_check_all(all_tag_ids, session):
        print("涉及的网址分类和网址标签检查通过，都存在！\n" + "="*50)
    else:
        session.close()
        print("涉及的网址分类和网址标签检查失败，请检查站点中的网址分类和网址标签是否存在和正确！")
        return
    # 9. 获取同步模式和导航站点域名
    sync_mode = CONFIG["sync"]["mode"]
    domain = CONFIG["onenav"]["domain"].rstrip("/")
    # 10. 同步到数据库中
    do_sync(sync_mode, domain, session, sites)
    # 11. 关闭数据库连接
    session.close()


if __name__ == "__main__":
    main()