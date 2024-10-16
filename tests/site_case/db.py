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
from models import WpTermTaxonomy
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

def test_insert(sites, session):
    """
    测试数据库插入
    """
    # 1. 遍历插入
    for site_obj in sites:
        site.insert(site_obj, "https://steam.cash", session)
    # 2. 判断插入数据的总数是否正确
    all_site_objs = site.select_all(session)
    assert all_site_objs is not None
    # 详细插入的数据：
    # 0️⃣ ✅ 默认数据
    # 1️⃣ ❌ test_link_01（数据不参与不同步）
    # 2️⃣ ✅ test_search_01 Google
    # 3️⃣ ✅ test_search_02 百度
    # 4️⃣ ✅ test_search_03 Bing
    # 5️⃣ ❌ test_search_04 360（不存在网址分类）
    # 6️⃣ ❌ test_search_05 DuckDuck（不存在网址标签）
    assert len(all_site_objs) == (1 + 3)
    # 3. 判断插入的数据是否正确
    # 3.1 test_search_01 Google
    site_obj = site.select("test_search_01", session)
    assert site_obj is not None
    # print(site_obj.__dict__)
    assert site_obj.favorite_ids == [2]
    assert site_obj.tag_ids == []
    assert site_obj.title == "Google"
    assert site_obj.content == "Google 搜索。\n由 Google 强力驱动。"
    assert site_obj.link == "https://google.com"
    assert len(site_obj.spare_links) == 1
    checked_spare_links_count = 0
    for spare_link in site_obj.spare_links:
        if spare_link.name == "Google 国内":
            assert spare_link.url == "https://google.cn"
            assert spare_link.note == "谷歌中国。"
            checked_spare_links_count += 1
    assert checked_spare_links_count == 1
    assert site_obj.sescribe == "很厉害的搜索引擎。"
    assert site_obj.language == "zh,en"
    assert site_obj.country == "中国"
    assert int(site_obj.order) == 0
    assert site_obj.thumbnail_pic_url == "https://image.senjianlu.com/blog/2024-10-14/google.png"
    assert site_obj.preview_pic_url is None
    assert site_obj.wechat_qr_pic_url is None
    assert site_obj._sync_site_id == "test_search_01"
    assert int(site_obj._post_id) == 12
    # 3.2 test_search_02 百度
    # todo
    # 3.3 test_search_03 Bing
    site_obj = site.select("test_search_03", session)
    assert site_obj is not None
    # print(site_obj.__dict__)
    assert site_obj.favorite_ids == [2]
    assert site_obj.tag_ids == [3]
    assert site_obj.title == "Bing"
    assert site_obj.content == "Bing 搜索。\n由微软强力驱动。"
    assert site_obj.link == "https://bing.com"
    assert len(site_obj.spare_links) == 0
    assert site_obj.sescribe == "厉害的搜索引擎。33"
    assert site_obj.language == "zh,en"
    assert site_obj.country == "中国"
    assert int(site_obj.order) == 0
    assert site_obj.thumbnail_pic_url == "https://image.senjianlu.com/blog/2024-10-14/bing.png"
    assert site_obj.preview_pic_url is None
    assert site_obj.wechat_qr_pic_url is None
    assert site_obj._sync_site_id == "test_search_03"
    assert int(site_obj._post_id) == 14
    # 4. 判断对应的网址分类旗下的网址数量是否正确
    favorite_wp_term_taxonomy = session.query(WpTermTaxonomy).filter(WpTermTaxonomy.term_id == 2).first()
    assert favorite_wp_term_taxonomy is not None
    # 0️⃣ ✅ 默认数据
    # 2️⃣ ✅ test_search_01 Google
    # 3️⃣ ❌ test_search_02 百度（没有分类）
    # 4️⃣ ✅ test_search_03 Bing
    assert favorite_wp_term_taxonomy.count == (1 + 2)
    # 5. 判断对应的网址标签旗下的网址数量是否正确
    tag_wp_term_taxonomy = session.query(WpTermTaxonomy).filter(WpTermTaxonomy.term_id == 3).first()
    assert tag_wp_term_taxonomy is not None
    # 2️⃣ ❌ test_search_01 Google（没有标签）
    # 3️⃣ ✅ test_search_02 百度
    # 4️⃣ ✅ test_search_03 Bing
    assert tag_wp_term_taxonomy.count == 2
    
def test_update(session):
    """
    测试数据库更新
    """
    assert 1 == 1

def test_delete(session):
    """
    测试数据库删除
    """
    assert 1 == 1        
