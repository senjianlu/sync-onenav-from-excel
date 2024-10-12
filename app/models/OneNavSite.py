#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/OneNavSite.py
# @DATE: 2024/10/12
# @TIME: 19:38:05
#
# @DESCRIPTION: OneNav 网址类


from models.WpPosts import WpPosts
from models.WpPostmeta import WpPostmeta
from models.WpTermRelationships import WpTermRelationships
from models.OneNavSpareSite import OneNavSpareSite


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
                 _sync_site_id: str):
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
        self._sync_site_id = None

    @staticmethod
    def generate_class_from_rows(sync_site_id, wp_post_row, wp_postmeta_rows, wp_term_relationships_rows):
        """
        函数说明: 生成网址对象
        :param sync_site_id: 用来将 Excel 中属于与表中数据建立关系的字段
        :param wp_post_row: wp_posts 表数据
        :param wp_postmeta_rows: wp_postmeta 表数据列表
        :param wp_term_relationships_rows: wp_term_relationships 表数据列表
        """
        # 1. 网址分类 ID 列表
        favorite_ids = [str(wp_term_relationships_row.term_taxonomy_id) for wp_term_relationships_row in wp_term_relationships_rows]
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
        # 15. 生成网址对象
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
            _sync_site_id=_sync_site_id
        )

    @staticmethod
    def select(sync_site_id: str, session):
        """
        函数说明: 查询网址
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
        return OneNavSite.generate_class_from_rows(
            sync_site_id=sync_site_id,
            wp_post_row=wp_post_row,
            wp_postmeta_rows=wp_postmeta_rows,
            wp_term_relationships_rows=wp_term_relationships_rows
        )

    def add(self, session):
        """
        函数说明: 添加网址
        :param session: 数据库会话
        """
        pass


    def update(self, session):
        """
        函数说明: 更新网址
        :param session: 数据库会话
        """
        pass

    def delete(self, session):
        """
        函数说明: 删除网址
        :param session: 数据库会话
        """
        pass