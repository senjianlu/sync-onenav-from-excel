#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/OneNavSite.py
# @DATE: 2024/10/12
# @TIME: 19:38:05
#
# @DESCRIPTION: OneNav 网址类


import time
import urllib.parse
from datetime import datetime, UTC

from models.WpPosts import WpPosts
from models.WpPostmeta import WpPostmeta
from models.WpTermTaxonomy import WpTermTaxonomy
from models.WpTermRelationships import WpTermRelationships
from models.OneNavSpareSite import OneNavSpareSite


def _generate_class_from_rows(sync_site_id, wp_post_row, wp_postmeta_rows, wp_term_relationships_rows):
    """
    函数说明: 生成网址对象
    :param sync_site_id: 用来将 Excel 中属于与表中数据建立关系的字段
    :param wp_post_row: wp_posts 表数据
    :param wp_postmeta_rows: wp_postmeta 表数据列表
    :param wp_term_relationships_rows: wp_term_relationships 表数据列表
    """
    # 1. 网址分类 ID 列表
    favorite_ids = [str(wp_term_relationships_row.term_taxonomy_id) for wp_term_relationships_row in
                    wp_term_relationships_rows]
    # 2. 网址标签 ID 列表
    tag_ids = []
    # 3. 标题
    title = wp_post_row.post_title
    # 4. 内容
    content = wp_post_row.post_content
    # 5. 链接
    link = None
    for wp_postmeta_row in wp_postmeta_rows:
        if wp_postmeta_row.meta_key == "_sites_link":
            link = wp_postmeta_row.meta_value
            break
    # 6. 备用链接地址（其他站点）
    spare_links_str = None
    for wp_postmeta_row in wp_postmeta_rows:
        if wp_postmeta_row.meta_key == "_spare_sites_link":
            spare_links_str = wp_postmeta_row.meta_value
            break
    if spare_links_str:
        spare_links = OneNavSpareSite.convert_to_list(spare_links_str)
    else:
        spare_links = []
    # 7. 一句话描述（简介）
    sescribe = None
    for wp_postmeta_row in wp_postmeta_rows:
        if wp_postmeta_row.meta_key == "_sites_sescribe":
            sescribe = wp_postmeta_row.meta_value
            break
    # 8. 站点语言
    language = None
    for wp_postmeta_row in wp_postmeta_rows:
        if wp_postmeta_row.meta_key == "_sites_language":
            language = wp_postmeta_row.meta_value
            break
    # 9. 站点所在国家或地区
    country = None
    for wp_postmeta_row in wp_postmeta_rows:
        if wp_postmeta_row.meta_key == "_sites_country":
            country = wp_postmeta_row.meta_value
            break
    # 10. 排序
    order = None
    for wp_postmeta_row in wp_postmeta_rows:
        if wp_postmeta_row.meta_key == "_sites_order":
            order = wp_postmeta_row.meta_value
            break
    # 11. LOGO，标志的图片链接
    thumbnail_pic_url = None
    for wp_postmeta_row in wp_postmeta_rows:
        if wp_postmeta_row.meta_key == "_thumbnail":
            thumbnail_pic_url = wp_postmeta_row.meta_value
            break
    # 12. 网站预览截图的图片链接
    preview_pic_url = None
    for wp_postmeta_row in wp_postmeta_rows:
        if wp_postmeta_row.meta_key == "_sites_preview":
            preview_pic_url = wp_postmeta_row.meta_value
            break
    # 13. 公众号二维码的图片链接
    wechat_qr_pic_url = None
    for wp_postmeta_row in wp_postmeta_rows:
        if wp_postmeta_row.meta_key == "_wechat_qr":
            wechat_qr_pic_url = wp_postmeta_row.meta_value
            break
    # 14. 用来将 Excel 中属于与表中数据建立关系的字段
    _sync_site_id = sync_site_id
    # 15. 插入表后的 post_id
    _post_id = wp_post_row.ID
    # 16. 生成网址对象
    return OneNavSite(
        favorite_ids=favorite_ids,
        tag_ids=tag_ids,
        title=title,
        content=content,
        link=link,
        spare_links=spare_links,
        sescribe=sescribe,
        language=language,
        country=country,
        order=order,
        thumbnail_pic_url=thumbnail_pic_url,
        preview_pic_url=preview_pic_url,
        wechat_qr_pic_url=wechat_qr_pic_url,
        _sync_site_id=_sync_site_id,
        _post_id=_post_id
    )

def _generate_new_wp_posts_row(site):
    """
    函数说明: 生成 wp_posts 表数据
    :param site: 网址对象
    """
    # 1. 生成 wp_posts 表数据
    new_wp_posts_row = WpPosts(
        post_author=1,
        post_date=datetime.now(),
        post_date_gmt=datetime.now(UTC),
        post_content=site.content,
        post_title=site.title,
        post_excerpt="",
        post_status="publish",
        comment_status="closed",
        ping_status="closed",
        post_password="",
        post_name=urllib.parse.quote(site.title),
        to_ping="",
        pinged="",
        post_modified=datetime.now(),
        post_modified_gmt=datetime.now(UTC),
        post_content_filtered="",
        post_parent=0,
        # 等到创建之后再更新
        guid="",
        menu_order=0,
        post_type="sites",
        post_mime_type="",
        comment_count=0
    )
    # 2. 返回
    return new_wp_posts_row

def _generate_new_wp_postmeta_rows(post_id, site):
    """
    函数说明: 生成 wp_postmeta 表数据
    :param post_id: 文章 ID
    :param site: 网址对象
    """
    new_wp_postmeta_rows = []
    # 1. 生成固定值的 wp_postmeta 表数据
    # 1.1 views
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_views",
        meta_value="0"
    ))
    # 1.2 _down_count
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_down_count",
        meta_value="0"
    ))
    # 1.3 _like_count
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_like_count",
        meta_value="0"
    ))
    # 1.4 _user_purview_level
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_user_purview_level",
        meta_value="all"
    ))
    # 1.5 _edit_last
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_edit_last",
        meta_value="1"
    ))
    # 1.6 _edit_lock
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_edit_lock",
        meta_value="{}:{}".format(str(int(time.time())), "1")
    ))
    # 1.7 _seo_title
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_seo_title",
        meta_value=""
    ))
    # 1.8 _seo_metakey
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_seo_metakey",
        meta_value=""
    ))
    # 1.9 _seo_desc
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_seo_desc",
        meta_value=""
    ))
    # 1.10 sidebar_layout
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="sidebar_layout",
        meta_value="default"
    ))
    # 1.11 _sites_type
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_sites_type",
        meta_value="sites"
    ))
    # 1.12 _goto
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_goto",
        meta_value="0"
    ))
    # 1.13 _wechat_id
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_wechat_id",
        meta_value=""
    ))
    # 1.14 _is_min_app
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_is_min_app",
        meta_value=""
    ))
    # 1.15 _down_version
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_down_version",
        meta_value=""
    ))
    # 1.16 _down_size
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_down_size",
        meta_value=""
    ))
    # 1.17 _down_url_list
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_down_url_list",
        meta_value=""
    ))
    # 1.18 _dec_password
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_dec_password",
        meta_value=""
    ))
    # 1.19 _app_platform
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_app_platform",
        meta_value=""
    ))
    # 1.20 _down_preview
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_down_preview",
        meta_value=""
    ))
    # 1.21 _down_formal
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_down_formal",
        meta_value=""
    ))
    # 1.22 _screenshot
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_screenshot",
        meta_value=""
    ))
    # 1.23 buy_option
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="buy_option",
        meta_value='a:7:{s:8:""buy_type"";s:4:""view"";s:5:""limit"";s:3:""all"";s:8:""pay_type"";s:5:""money"";' \
            + 's:10:""price_type"";s:6:""single"";s:9:""pay_title"";s:0:"""";s:9:""pay_price"";s:1:""0"";' \
            + 's:5:""price"";s:1:""0"";}'
    ))
    # 2. 生成可变值的 wp_postmeta 表数据
    # 2.1 _sites_link
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_sites_link",
        meta_value=site.link
    ))
    # 2.2 _spare_sites_link
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_spare_sites_link",
        meta_value=OneNavSpareSite.convert_to_str(site.spare_links)
    ))
    # 2.3 _sites_sescribe
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_sites_sescribe",
        meta_value=site.sescribe
    ))
    # 2.4 _sites_language
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_sites_language",
        meta_value=site.language
    ))
    # 2.5 _sites_country
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_sites_country",
        meta_value=site.country
    ))
    # 2.6 _sites_order
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_sites_order",
        meta_value=site.order
    ))
    # 2.7 _thumbnail
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_thumbnail",
        meta_value=site.thumbnail_pic_url
    ))
    # 2.8 _sites_preview
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_sites_preview",
        meta_value=site.preview_pic_url
    ))
    # 2.9 _wechat_qr
    new_wp_postmeta_rows.append(WpPostmeta(
        post_id=post_id,
        meta_key="_wechat_qr",
        meta_value=site.wechat_qr_pic_url
    ))
    # 3. 返回
    return new_wp_postmeta_rows

def _generate_new_wp_term_relationships_rows(post_id, site):
    """
    函数说明: 生成 wp_term_relationships 表数据
    :param post_id: 文章 ID
    :param site: 网址对象
    """
    new_wp_term_relationships_rows = []
    # 1. 遍历网址分类 ID 列表
    for favorite_id in site.favorite_ids:
        new_wp_term_relationships_rows.append(WpTermRelationships(
            object_id=post_id,
            term_taxonomy_id=favorite_id,
            term_order=0
        ))
    # 2. 返回
    return new_wp_term_relationships_rows


class OneNavSite():
    """
    类说明: OneNav 网址类
    """
    def __init__(self,
                 favorite_ids: list,
                 tag_ids: list,
                 title: str,
                 content: str,
                 link: str,
                 spare_links: list,
                 sescribe: str,
                 language: str,
                 country: str,
                 order: int,
                 thumbnail_pic_url: str,
                 preview_pic_url: str,
                 wechat_qr_pic_url: str,
                 _sync_site_id: str,
                 _post_id: int = None):
        """
        函数说明: 初始化
        :param favorite_ids: 网址分类 ID 列表
        :param tag_ids: 网址标签 ID 列表
        :param title: 标题
        :param content: 内容
        :param link: 链接
        :param spare_links: 备用链接地址（其他站点）
        :param sescribe: 一句话描述（简介）
        :param language: 站点语言
        :param country: 站点所在国家或地区
        :param order: 排序
        :param thumbnail_pic_url: LOGO，标志的图片链接
        :param preview_pic_url: 网站预览截图的图片链接
        :param wechat_qr_pic_url: 公众号二维码的图片链接
        :param _sync_site_id: 用来将 Excel 中属于与表中数据建立关系的字段
        """
        self.favorite_ids = favorite_ids
        self.tag_ids = tag_ids
        self.title = title
        self.content = content
        self.link = link
        self.spare_links = spare_links
        self.sescribe = sescribe
        self.language = language
        self.country = country
        self.order = order
        self.thumbnail_pic_url = thumbnail_pic_url
        self.preview_pic_url = preview_pic_url
        self.wechat_qr_pic_url = wechat_qr_pic_url
        # 用来将 Excel 中属于与表中数据建立关系的字段
        self._sync_site_id = _sync_site_id
        # 插入表后的 post_id
        self._post_id = _post_id

    @staticmethod
    def select(sync_site_id: str, session):
        """
        函数说明: 查询网址
        :param sync_site_id: 用来将 Excel 中属于与表中数据建立关系的字段
        :param session: 数据库会话
        """
        # 1. 通过 _sync_site_id 查询网址在 wp_postmeta 表中对应的 post_id
        wp_postmeta_row = session.query(WpPostmeta).filter(
            WpPostmeta.meta_key == "_sync_site_id",
            WpPostmeta.meta_value == sync_site_id
        ).first()
        if not wp_postmeta_row:
            return None
        post_id = wp_postmeta_row.post_id
        # 2. 通过 post_id 查询 wp_posts 表中的网址数据
        wp_post_row = session.query(WpPosts).filter(
            WpPosts.ID == post_id
        ).first()
        if not wp_post_row:
            return None
        # 3. 通过 post_id 查询 wp_postmeta 表中的网址数据
        wp_postmeta_rows = session.query(WpPostmeta).filter(
            WpPostmeta.post_id == post_id
        ).all()
        # 4. 通过 post_id 查询 wp_term_relationships 表中的网址数据
        wp_term_relationships_rows = session.query(WpTermRelationships).filter(
            WpTermRelationships.object_id == post_id
        ).all()
        # 5. 生成网址对象
        site = _generate_class_from_rows(
            sync_site_id=sync_site_id,
            wp_post_row=wp_post_row,
            wp_postmeta_rows=wp_postmeta_rows,
            wp_term_relationships_rows=wp_term_relationships_rows
        )
        # 6. 返回
        return site

    @staticmethod
    def select_all(session):
        """
        函数说明: 查询所有网址
        :param session: 数据库会话
        """
        # 1. 查询所有网址在 wp_postmeta 表中对应的 post_id
        wp_postmeta_rows = session.query(WpPostmeta).filter(
            WpPostmeta.meta_key == "_sync_site_id"
        ).all()
        if not wp_postmeta_rows:
            return []
        post_ids = [wp_postmeta_row.post_id for wp_postmeta_row in wp_postmeta_rows]
        sites = []
        for post_id in post_ids:
            # 2. 通过 post_id 查询 wp_posts 表中的网址数据
            wp_post_row = session.query(WpPosts).filter(
                WpPosts.ID == post_id
            ).first()
            if not wp_post_row:
                continue
            # 3. 通过 post_id 查询 wp_postmeta 表中的网址数据
            wp_postmeta_rows = session.query(WpPostmeta).filter(
                WpPostmeta.post_id == post_id
            ).all()
            # 4. 获取 sync_site_id
            sync_site_id = None
            for wp_postmeta_row in wp_postmeta_rows:
                if wp_postmeta_row.meta_key == "_sync_site_id":
                    sync_site_id = wp_postmeta_row.meta_value
                    break
            if not sync_site_id:
                continue
            # 5. 通过 post_id 查询 wp_term_relationships 表中的网址数据
            wp_term_relationships_rows = session.query(WpTermRelationships).filter(
                WpTermRelationships.object_id == post_id
            ).all()
            # 6. 生成网址对象
            site = _generate_class_from_rows(
                sync_site_id=sync_site_id,
                wp_post_row=wp_post_row,
                wp_postmeta_rows=wp_postmeta_rows,
                wp_term_relationships_rows=wp_term_relationships_rows
            )
            sites.append(site)
        # 7. 返回
        return sites

    def insert(self, domain, session):
        """
        函数说明: 添加网址
        :param domain: 导航站点域名
        :param session: 数据库会话
        """
        # 1. 生成 wp_posts 表数据
        new_wp_posts_row = _generate_new_wp_posts_row(self)
        # 2. 提交 wp_posts 表数据并获取 post_id
        session.add(new_wp_posts_row)
        session.commit()
        post_id = new_wp_posts_row.ID
        print("post_id: ", post_id)
        # 3. 更新 wp_posts 表数据中的 guid
        new_wp_posts_row.guid = "{}/sites/{}.html".format(domain, post_id)
        session.commit()
        # 2. 生成 wp_postmeta 表数据
        new_wp_postmeta_rows = _generate_new_wp_postmeta_rows(post_id, self)
        # 3. 生成 wp_term_relationships 表数据
        new_wp_term_relationships_rows = _generate_new_wp_term_relationships_rows(post_id, self)
        # 4. 添加数据
        for new_wp_postmeta_row in new_wp_postmeta_rows:
            session.add(new_wp_postmeta_row)
        for new_wp_term_relationships_row in new_wp_term_relationships_rows:
            session.add(new_wp_term_relationships_row)
        # 5. 提交
        session.commit()
        # 6. 更新 wp_term_taxonomy 表数据
        for new_wp_term_relationships_row in new_wp_term_relationships_rows:
            session.query(WpTermTaxonomy).filter(
                WpTermTaxonomy.term_taxonomy_id == new_wp_term_relationships_row.term_taxonomy_id
            ).update({
                "count": WpTermTaxonomy.count + 1
            })
        # 7. 提交
        session.commit()

    def update(self, post_id, session):
        """
        函数说明: 更新网址
        :param session: 数据库会话
        """
        # 1. 生成 wp_posts 表数据
        new_wp_posts_row = _generate_new_wp_posts_row(self)
        # 2. 生成 wp_postmeta 表数据
        new_wp_postmeta_rows = _generate_new_wp_postmeta_rows(post_id, self)
        # 3. 生成 wp_term_relationships 表数据
        new_wp_term_relationships_rows = _generate_new_wp_term_relationships_rows(post_id, self)
        # 4. 更新数据
        # 4.1 更新 wp_posts 表数据
        session.query(WpPosts).filter(WpPosts.ID == post_id).update({
            "post_title": new_wp_posts_row.post_title,
            "post_content": new_wp_posts_row.post_content,
            "post_name": new_wp_posts_row.post_name,
            "post_modified": new_wp_posts_row.post_modified,
            "post_modified_gmt": new_wp_posts_row.post_modified_gmt
        })
        # 4.2 更新 wp_postmeta 表数据
        for new_wp_postmeta_row in new_wp_postmeta_rows:
            session.query(WpPostmeta).filter(
                WpPostmeta.post_id == post_id,
                WpPostmeta.meta_key == new_wp_postmeta_row.meta_key
            ).update({
                "meta_value": new_wp_postmeta_row.meta_value
            })
        # 4.3 判断需要新增或删除的网址分类
        wp_term_relationships_rows = session.query(WpTermRelationships).filter(
            WpTermRelationships.object_id == post_id
        ).all()
        old_favorite_ids = [wp_term_relationships_row.term_id for wp_term_relationships_row in wp_term_relationships_rows]
        new_favorite_ids = self.favorite_ids
        add_favorite_ids = list(set(new_favorite_ids).difference(set(old_favorite_ids)))
        del_favorite_ids = list(set(old_favorite_ids).difference(set(new_favorite_ids)))
        # 4.4 更新 wp_term_relationships 和 wp_term_taxonomy 表数据
        for add_favorite_id in add_favorite_ids:
            new_wp_term_relationships_row = WpTermRelationships(
                object_id=post_id,
                term_taxonomy_id=add_favorite_id,
                term_order=0
            )
            session.add(new_wp_term_relationships_row)
            session.query(WpTermTaxonomy).filter(
                WpTermTaxonomy.term_taxonomy_id == add_favorite_id
            ).update({
                "count": WpTermTaxonomy.count + 1
            })
        for del_favorite_id in del_favorite_ids:
            session.query(WpTermRelationships).filter(
                WpTermRelationships.object_id == post_id,
                WpTermRelationships.term_taxonomy_id == del_favorite_id
            ).delete()
            session.query(WpTermTaxonomy).filter(
                WpTermTaxonomy.term_taxonomy_id == del_favorite_id
            ).update({
                "count": WpTermTaxonomy.count - 1
            })
        # 5. 提交
        session.commit()

    def delete(self, post_id, session):
        """
        函数说明: 删除网址
        :param session: 数据库会话
        """
        # 1. 删除 wp_posts 表数据
        session.query(WpPosts).filter(WpPosts.ID == post_id).delete()
        # 2. 删除 wp_postmeta 表数据
        session.query(WpPostmeta).filter(WpPostmeta.post_id == post_id).delete()
        # 3. 删除和更新网址分类的关联数据
        wp_term_relationships_rows = session.query(WpTermRelationships).filter(
            WpTermRelationships.object_id == post_id
        ).all()
        for wp_term_relationships_row in wp_term_relationships_rows:
            session.query(WpTermTaxonomy).filter(
                WpTermTaxonomy.term_taxonomy_id == wp_term_relationships_row.term_taxonomy_id
            ).update({
                "count": WpTermTaxonomy.count - 1
            })
        session.query(WpTermRelationships).filter(
            WpTermRelationships.object_id == post_id
        ).delete()
        # 4. 提交
        session.commit()

    def equals(self, site):
        """
        函数说明: 判断两个网址对象是否相等
        :param site: 网址对象
        """
        if (self.favorite_ids != site.favorite_ids or
            self.tag_ids != site.tag_ids or
            self.title != site.title or
            self.content != site.content or
            self.link != site.link or
            OneNavSpareSite.convert_to_str(self.spare_links) != OneNavSpareSite.convert_to_str(site.spare_links) or
            self.sescribe != site.sescribe or
            self.language != site.language or
            self.country != site.country or
            self.order != site.order or
            self.thumbnail_pic_url != site.thumbnail_pic_url or
            self.preview_pic_url != site.preview_pic_url or
            self.wechat_qr_pic_url != site.wechat_qr_pic_url):
            return False
        return True