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


def check_all(tag_ids, session):
    """
    函数说明: 查询网址标签是否存在
    :param tag_ids: 标签 ID 列表
    :param session: 数据库会话
    """
    # 1. 查询网址标签是否存在
    is_pass = OneNavTag.check_all(tag_ids, session)
    # 2. 返回
    return is_pass

def select(term_id, session):
    """
    函数说明: 查询网址标签
    :param term_id: 分类 ID
    :param session: 数据库会话
    """
    # 1. 查询网址标签
    sites = OneNavTag.select(term_id, session)
    # 2. 返回
    return sites