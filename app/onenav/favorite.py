#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: onenav/favorite.py
# @DATE: 2024/10/12
# @TIME: 20:06:51
#
# @DESCRIPTION: 网址分类操作模块


from models.OneNavFavorite import OneNavFavorite


def check_all(favorite_ids, session):
    """
    函数说明: 查询网址分类是否存在
    :param favorite_ids: 分类 ID 列表
    :param session: 数据库会话
    """
    # 1. 查询网址分类是否存在
    is_pass = OneNavFavorite.check_all(favorite_ids, session)
    # 2. 返回
    return is_pass

def select(term_id, session):
    """
    函数说明: 查询网址分类
    :param term_id: 分类 ID
    :param session: 数据库会话
    """
    # 1. 查询网址分类
    sites = OneNavFavorite.select(term_id, session)
    # 2. 返回
    return sites