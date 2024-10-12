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


def main():
    """
    主函数
    """
    # 1. 获取数据库连接信息
    try:
        mysql_config = CONFIG["mysql"]
        mysql_host, mysql_port, mysql_username, mysql_password, mysql_database = (
            mysql_config["host"],
            mysql_config["port"],
            mysql_config["username"],
            mysql_config["password"],
            mysql_config["database"]
        )
    except Exception as e:
        print("MySQL 配置信息读取失败，请检查配置文件！")
        return
    # 2. 获取数据库引擎
    engine = get_db_engine(
        mysql_host=mysql_host,
        mysql_port=mysql_port,
        mysql_username=mysql_username,
        mysql_password=mysql_password,
        mysql_database=mysql_database
    )
    # 3. 建立数据库连接
    session = get_db_session(engine)
    # 4. 关闭数据库连接
    session.close()
        

if __name__ == "__main__":
    main()