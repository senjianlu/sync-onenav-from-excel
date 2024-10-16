#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: site_case/db.py
# @DATE: 2024/10/15
# @TIME: 17:30:15
#
# @DESCRIPTION: 数据库交互的测试用例


from models.OneNavSite import OneNavSite
from onenav import site


def test_select(session):
    """
    测试数据库查询
    """
    # 1. 建立数据库连接
    assert session is not None
    # 2. 查询网址
    site_id = 99
    site_obj = site.select(site_id, session)
    assert site_obj is not None
    # 3. 判断网站是否正确
    # print(site_obj.__dict__)
    assert site_obj.favorite_ids == [2]
    assert site_obj.tag_ids == []
    assert site_obj.title == "从 Excel 中同步来的链接"
    assert site_obj.content == '由 Rabbir 编写的脚本。\n仓库地址为：<a href="https://github.com/senjianlu/sync-onenav-from-excel">senjianlu/sync-onenav-from-excel</a>'
    assert site_obj.link == "https://github.com/senjianlu/sync-onenav-from-excel"
    assert len(site_obj.spare_links) == 2
    checked_spare_links_count = 0
    for spare_link in site_obj.spare_links:
        if spare_link.name == "百度":
            assert spare_link.url == "https://baidu.com"
            assert spare_link.note == "百度备注。"
            checked_spare_links_count += 1
        elif spare_link.name == "谷歌":
            assert spare_link.url == "https://google.com"
            assert spare_link.note == "谷歌"
            checked_spare_links_count += 1
    assert checked_spare_links_count == 2
    assert site_obj.sescribe == '将 Excel 中的网址同步到 OneNav 一为导航中。\n详细参考 GitHub 仓库的 README.md。'
    assert site_obj.language == "zh,en"
    assert site_obj.country == "中国"
    assert int(site_obj.order) == 0
    assert site_obj.thumbnail_pic_url == "https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png"
    assert site_obj.preview_pic_url == "https://kinsta.com/wp-content/uploads/2018/04/what-is-github-1-1.png"
    assert site_obj.wechat_qr_pic_url is None
    assert int(site_obj._sync_site_id) == 99
    assert int(site_obj._post_id) == 11

        
