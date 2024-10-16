#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: site_case/excel.py
# @DATE: 2024/10/15
# @TIME: 17:30:15
#
# @DESCRIPTION: Excel 文件操作的测试用例


from excel import load_data
from onenav import site


def test_read(file_path, sites_sheet, spare_links_sheet):
    """
    测试读取 Excel 文件
    """
    # 1. 读取站点数据
    data = load_data(file_path, sites_sheet, spare_links_sheet)
    # 2. 判断站点数据是否正确
    assert data is not None
    assert len(data) == 5
    # 2.1 test_search_01 Google
    checked_sites_count = 0
    for site in data:
        if site["_sync_site_id"] == "test_search_01":
            assert site["favorite_ids"] == [1]
            assert site["tag_ids"] == []
            assert site["title"] == "Google"
            assert site["content"] == "Google 搜索。\r\n由 Google 强力驱动。"
            assert site["link"] == "https://www.google.com"
            assert len(site["spare_links"]) == 2
            checked_spare_links_count = 0
            for spare_link in spare_links:
                if spare_link["name"] == "测试备用链接 01":
                    assert spare_link["url"] == "https://www.google.com"
                    assert spare_link["note"] == "Google 站点。\r\n换行一下。"
                    checked_spare_links_count += 1
                elif spare_link["name"] == "测试备用链接 02":
                    assert spare_link["url"] == "https://www.baidu.com"
                    assert spare_link["note"] == "百度站点。\r\n换行一下。"
                    checked_spare_links_count += 1
            assert checked_spare_links_count == 2
            assert site["sescribe"] == "很厉害的搜索引擎。"
            assert site["is_hide"] == "zh,en"
            assert site["country"] == "中国"
            assert int(site["order"]) == 0
            assert site["thumbnail_pic_url"] == "https://image.senjianlu.com/blog/2024-10-14/google.png"
            assert site["preview_pic_url"] == ""
            assert site["wechat_qr_pic_url"] == ""
            checked_sites_count += 1
            break
    # 2.2 test_search_02 百度
    # 2.3 test_search_03 Bing
    # 2.4 test_search_04 360
    # 2.5 test_search_05 DuckDuck
    assert checked_sites_count == 1
    # 3. 返回数据
    return data

def test_convert(data):
    """
    测试转换 Excel 数据
    """
    pass