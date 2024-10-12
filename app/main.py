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
        file_name = CONFIG["excel"]["file_name"]
        if file_name == "":
            raise Exception("Excel 文件名为空！")
    except Exception as e:
        print("Excel 文件名读取失败，请检查配置文件！")
        return False
    # 3. 检查同步模式
    try:
        mode = CONFIG["sync"]["mode"]
        if mode not in ["incremental", "full"]:
            raise Exception("同步模式错误！")
    except Exception as e:
        print("同步模式读取失败，请检查配置文件！")
        return False
    # 4. 返回
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
    data = load_data(file_path)
    # 7. 使用 Excel 表中的数据创建 ORM 对象
    sites = generate_sites_from_excel_data(data)
    # 8. 获取同步模式
    sync_mode = CONFIG["sync"]["mode"]
    # 9. 同步到数据库中
    # todo...
    # 10. 关闭数据库连接
    # session.close()
        

if __name__ == "__main__":
    main()