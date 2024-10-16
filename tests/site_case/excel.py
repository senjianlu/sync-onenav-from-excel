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
from onenav.site import generate_sites_from_excel_data


def test_load(file_path, sites_sheet, spare_links_sheet):
    """
    测试读取 Excel 文件
    """
    # 1. 读取站点数据
    data = load_data(file_path, sites_sheet, spare_links_sheet)
    assert data is not None
    # 2. 判断站点数据是否正确
    assert len(data["site_rows"]) == 6
    checked_sites_count = 0
    for site_row in data["site_rows"]:
        # 2.1 test_search_01 Google
        if site_row[1] == "test_search_01":
            # (True, 'test_search_01', None, None, 1, None, 'Google', 'Google 搜索。\n由 Google 强力驱动。', 'https://google.com', '=IF(ISBLANK($B3), "", COUNTIFS(\'备用链接地址（其他站点）\'!$A$2:$A$20, "="&$B3, \'备用链接地址（其他站点）\'!$A$2:$A$20, "<>"))', '很厉害的搜索引擎。', 'zh,en', '中国', 0, 'https://image.senjianlu.com/blog/2024-10-14/google.png', None, None, None)
            assert str(site_row[4]) == "1"
            assert site_row[5] is None
            assert site_row[6] == "Google"
            assert site_row[7] == "Google 搜索。\n由 Google 强力驱动。"
            assert site_row[8] == "https://google.com"
            assert site_row[10] == "很厉害的搜索引擎。"
            assert site_row[11] == "zh,en"
            assert site_row[12] == "中国"
            assert int(site_row[13]) == 0
            assert site_row[14] == "https://image.senjianlu.com/blog/2024-10-14/google.png"
            assert site_row[15] is None
            assert site_row[16] is None
            checked_sites_count += 1
            break
        # 2.2 test_search_02 百度
        # todo
        # 2.3 test_search_03 Bing
        # todo
        # 2.4 test_search_04 360
        # todo
        # 2.5 test_search_05 DuckDuck
        # todo
    assert checked_sites_count == 1
    # 3. 判断备用链接数据是否正确
    assert len(data["spare_site_rows"]) == 3
    checked_spare_links_count = 0
    for spare_site_row in data["spare_site_rows"]:
        # 3.1 test_search_01 Google
        if spare_site_row[0] == "test_search_01":
            # ('test_search_01', 1, 'Google 国内', 'https://google.cn', '谷歌中国。')
            assert spare_site_row[1] == 1
            assert spare_site_row[2] == "Google 国内"
            assert spare_site_row[3] == "https://google.cn"
            assert spare_site_row[4] == "谷歌中国。"
            checked_spare_links_count += 1
    assert checked_spare_links_count == 1
    # 4. 返回数据
    return data

def test_convert(data):
    """
    测试转换 Excel 数据
    """
    # 1. 转换数据
    sites = generate_sites_from_excel_data(data)
    # 2. 判断转换数据是否正确
    assert sites is not None
    assert len(sites) == 5
    # 2.1 test_search_01 Google
    checked_sites_count = 0
    for site in sites:
        if site._sync_site_id == "test_search_01":
            assert site.favorite_ids == [1]
            assert site.tag_ids == []
            assert site.title == "Google"
            assert site.content == "Google 搜索。\n由 Google 强力驱动。"
            assert site.link == "https://google.com"
            assert len(site.spare_links) == 1
            for spare_link in site.spare_links:
                if spare_link.name == "Google 国内":
                    assert spare_link.url == "https://google.cn"
                    assert spare_link.note == "谷歌中国。"
            assert site.sescribe == "很厉害的搜索引擎。"
            assert site.language == "zh,en"
            assert site.country == "中国"
            assert int(site.order) == 0
            assert site.thumbnail_pic_url == "https://image.senjianlu.com/blog/2024-10-14/google.png"
            assert site.preview_pic_url is None
            assert site.wechat_qr_pic_url is None
            checked_sites_count += 1
            break
        # 2.2 test_search_02 百度
        # todo
        # 2.3 test_search_03 Bing
        # todo
        # 2.4 test_search_04 360
        # todo
        # 2.5 test_search_05 DuckDuck
        # todo
    assert checked_sites_count == 1
    # 3. 返回数据
    return sites