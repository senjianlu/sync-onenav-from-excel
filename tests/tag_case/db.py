#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: tag_case/db.py
# @DATE: 2024/10/15
# @TIME: 17:30:15
#
# @DESCRIPTION: 数据库交互的测试用例


from models.OneNavTag import OneNavTag
from onenav import tag


def test_select(session):
    """
    测试数据库查询
    """
    # 1. 建立数据库连接
    assert session is not None
    # 2. 查询网址标签
    tag_id = 3
    tag_obj = tag.select(tag_id, session)
    assert tag_obj is not None
    # 3. 判断网站标签值是否正确
    # print(tag_obj.__dict__)
    assert tag_obj.name == "测试标签"
    assert tag_obj.slug == "test_tag"
    assert tag_obj.description == "测试描述\r\n另起一行。"
    assert tag_obj.seo_title == "SEO 自定义标题"
    assert tag_obj.seo_metakey == "关键词一、关键词2"
    assert tag_obj.seo_desc == "自定义描述"