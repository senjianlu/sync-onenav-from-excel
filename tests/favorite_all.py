#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: favorite_all.py
# @DATE: 2024/10/16
# @TIME: 10:08:30
#
# @DESCRIPTION: 网址分类相关的测试用例集合


import sys
sys.path.append("../app")

from config import CONFIG
from db import get_db_engine, get_db_session
from favorite_case import db as favorite_db


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


def test_db_select():
    """
    测试数据库查询
    """
    # 1. 连接数据库
    session = _connect_db()
    # 2. 测试
    try:
        favorite_db.test_select(session)
    except Exception as e:
        raise e
    finally:
        # 3. 关闭数据库
        session.close()