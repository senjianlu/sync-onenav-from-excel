#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: test.py
# @DATE: 2024/10/12
# @TIME: 22:36:05
#
# @DESCRIPTION: 测试模块


import urllib.parse

from config import CONFIG
from db import get_db_engine, get_db_session
from onenav import favorite as one_nav_favorite
from onenav import site as one_nav_site
from onenav import tag as one_nav_tag
from excel import get_file_path, load_data


def test_01(session):
    """
    函数说明: 测试查询网址
    """
    site = one_nav_site.select("aaawbbbb", session)
    print(site.__dict__ if site else None)
    if site:
        for spare_link in site.spare_links:
            print(spare_link.__dict__)

def test_02(session):
    """
    函数说明: 测试查询网址分类
    """
    favorite = one_nav_favorite.select(99, session)
    print(favorite.__dict__ if favorite else None)

def test_03(session):
    """
    函数说明: 测试查询网址标签
    """
    tag = one_nav_tag.select(10, session)
    print(tag.__dict__ if tag else None)

def test_04():
    """
    函数说明: 测试从 Excel 表格中导入网址
    """
    file_path = get_file_path(CONFIG["excel"]["file_name"])
    data = load_data(file_path)
    sites = one_nav_site.generate_sites_from_excel_data(data)
    for site in sites:
        print(site.__dict__)
        if site.spare_links:
            for spare_link in site.spare_links:
                print(spare_link.__dict__)

def test_05(session):
    """
    函数说明: 测试查询网址分类是否存在
    """
    is_pass = one_nav_favorite.check_all([3], session)
    print(is_pass)

def test_06(session):
    """
    函数说明: 测试查询网址标签是否存在
    """
    is_pass = one_nav_tag.check_all([1, 10], session)
    print(is_pass)

def test_07(session):
    """
    函数说明: 测试 url encode 数字、字母和汉字
    """
    url = 360
    print(urllib.parse.quote(url))


if __name__ == "__main__":
    # 1. 建立书库库连接
    mysql_config = CONFIG["mysql"]
    mysql_host, mysql_port, mysql_username, mysql_password, mysql_database = (
        mysql_config["host"],
        mysql_config["port"],
        mysql_config["username"],
        mysql_config["password"],
        mysql_config["database"]
    )
    db_engine = get_db_engine(
        mysql_host,
        mysql_port,
        mysql_username,
        mysql_password,
        mysql_database
    )
    session = get_db_session(db_engine)
    # 2. 运行方法
    try:
        # test_01(session)
        # test_02(session)
        # test_03(session)
        # test_04()
        # test_05(session)
        # test_06(session)
        test_07(session)
    except Exception as e:
        print(e)
    finally:
        session.close()