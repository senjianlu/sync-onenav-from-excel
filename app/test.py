#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: test.py
# @DATE: 2024/10/12
# @TIME: 22:36:05
#
# @DESCRIPTION: 测试模块


from config import CONFIG
from db import get_db_engine, get_db_session
from models.OneNavSite import OneNavSite


def main():
    """
    函数说明: 主函数
    """
    # 1. 建立数据库连接
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
    # 2. 测试
    try:
        site = OneNavSite.select("sync_test_site_id", session)
        print(site.__dict__)
    except Exception as e:
        print(e)
    finally:
        session.close()


if __name__ == "__main__":
    main()