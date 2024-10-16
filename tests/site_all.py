#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: site_all.py
# @DATE: 2024/10/15
# @TIME: 17:19:30
#
# @DESCRIPTION: 网址相关的测试用例集合


import sys
sys.path.append("../app")

from config import CONFIG
from db import get_db_engine, get_db_session
from site_case import excel as site_excel
from site_case import db as site_db


def _connect_db():
    """
    连接数据库
    """
    # 1. 连接数据库
    mysql_host, mysql_port, mysql_username, mysql_password, mysql_database = (
        CONFIG["mysql"]["host"],
        CONFIG["mysql"]["port"],
        CONFIG["mysql"]["username"],
        CONFIG["mysql"]["password"],
        CONFIG["mysql"]["database"]
    )
    # 2. 获取数据库引擎
    engine = get_db_engine(mysql_host, mysql_port, mysql_username, mysql_password, mysql_database)
    # 3. 获取数据库会话
    session = get_db_session(engine)
    # 4. 返回
    return session


def test_excel_load():
    """
    测试加载 Excel 文件
    """
    # 1. 读取配置文件
    file_name = CONFIG["test"]["file_name"]
    file_path = "../{}".format(file_name)
    sites_sheet = CONFIG["test"]["sites_sheet"]
    spare_links_sheet = CONFIG["test"]["spare_links_sheet"]
    # 2. 测试
    try:
        site_excel.test_load(file_path, sites_sheet, spare_links_sheet)
    except Exception as e:
        raise e

def test_excel_convert():
    """
    测试转换 Excel 数据
    """
    # 1. 读取配置文件
    file_name = CONFIG["test"]["file_name"]
    file_path = "../{}".format(file_name)
    sites_sheet = CONFIG["test"]["sites_sheet"]
    spare_links_sheet = CONFIG["test"]["spare_links_sheet"]
    # 2. 加载数据
    data = site_excel.test_load(file_path, sites_sheet, spare_links_sheet)
    # 3. 测试
    try:
        site_excel.test_convert(data)
    except Exception as e:
        raise e

def test_db_select():
    """
    测试数据库查询
    """
    # 1. 连接数据库
    session = _connect_db()
    # 2. 测试
    try:
        site_db.test_select(session)
    except Exception as e:
        raise e
    finally:
        # 3. 关闭数据库
        session.close()

def test_db_insert():
    """
    测试数据库插入
    """
    # 1. 连接数据库
    session = _connect_db()
    # 2. 读取 Excel 中的数据并转换为对象
    file_name = CONFIG["test"]["file_name"]
    file_path = "../{}".format(file_name)
    sites_sheet = CONFIG["test"]["sites_sheet"]
    spare_links_sheet = CONFIG["test"]["spare_links_sheet"]
    data = site_excel.test_load(file_path, sites_sheet, spare_links_sheet)
    sites = site_excel.test_convert(data)
    # 3. 测试
    try:
        site_db.test_insert(sites, session)
    except Exception as e:
        raise e
    finally:
        # 4. 关闭数据库
        session.close()

def test_db_update():
    """
    测试数据库更新
    """
    # 1. 连接数据库
    session = _connect_db()
    # 2. 测试
    try:
        site_db.test_update(session)
    except Exception as e:
        raise e
    finally:
        # 3. 关闭数据库
        session.close()

def test_db_delete():
    """
    测试数据库删除
    """
    # 1. 连接数据库
    session = _connect_db()
    # 2. 测试
    try:
        site_db.test_delete(session)
    except Exception as e:
        raise e
    finally:
        # 3. 关闭数据库
        session.close()