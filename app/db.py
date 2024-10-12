#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: db.py
# @DATE: 2024/10/12
# @TIME: 16:27:09
#
# @DESCRIPTION: 数据库模块


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text


# 基类
Base = declarative_base()


def get_db_engine(mysql_host, mysql_port, mysql_username, mysql_password, mysql_database):
    """
    获取数据库引擎
    """
    # 1. 创建数据库引擎
    db_url = "mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}".format(
        mysql_host=mysql_host,
        mysql_port=mysql_port,
        mysql_username=mysql_username,
        mysql_password=mysql_password,
        mysql_database=mysql_database
    )
    engine = create_engine(db_url)
    # 2. 不更改表结构
    # Base.metadata.create_all(engine)
    # 3. 返回
    return engine

def get_db_session(engine):
    """
    获取数据库会话
    注：使用 session.close() 关闭会话
    """
    # 1. 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()
    # 2. 查看数据库版本
    db_version = session.execute(text("SELECT VERSION()")).fetchall()[0][0]
    print("MySQL 数据库连接成功，版本为 {}\n".format(db_version) + "="*50)
    # 3. 返回
    return session