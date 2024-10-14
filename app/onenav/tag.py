#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: onenav/tag.py
# @DATE: 2024/10/12
# @TIME: 20:07:14
#
# @DESCRIPTION: 网址标签操作模块


from models.OneNavTag import OneNavTag


def select(term_id, session):
    """
    函数说明: 查询所有网址数据
    :param session: 数据库会话
    """
    # 1. 查询所有网址数据
    sites = OneNavTag.select(term_id, session)
    # 2. 返回
    return sites