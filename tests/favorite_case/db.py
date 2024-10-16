#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: favorite_case/db.py
# @DATE: 2024/10/15
# @TIME: 17:30:15
#
# @DESCRIPTION: 数据库交互的测试用例


from models.OneNavFavorite import OneNavFavorite
from onenav import favorite


def test_select(session):
    """
    测试数据库查询
    """
    # 1. 建立数据库连接
    assert session is not None
    # 2. 查询网址分类
    favorite_id = 2
    favorite_obj = favorite.select(favorite_id, session)
    assert favorite_obj is not None
    # 3. 判断网站分类值是否正确
    # print(favorite_obj.__dict__)
    assert favorite_obj.name == "测试分类"
    assert favorite_obj.slug == "test_favorite"
    assert favorite_obj.parent == 0
    assert favorite_obj.description == "测试分类的描述"
    assert favorite_obj.order == "99"
    assert favorite_obj.seo_title == "SEO 标题"
    assert favorite_obj.seo_metakey == "SEO 关键词一、关键词2"
    assert favorite_obj.seo_desc == "SEO 描述"
    assert favorite_obj.card_mode == "null"
    assert favorite_obj.columns_type == "global"
    assert favorite_obj.columns == 'a:5:{s:2:"sm";s:1:"2";s:2:"md";s:1:"2";s:2:"lg";s:1:"3";s:2:"xl";s:1:"5";s:3:"xxl";s:1:"6";}'