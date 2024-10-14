#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/OneNavFavorite.py
# @DATE: 2024/10/13
# @TIME: 20:21:55
#
# @DESCRIPTION: 网址分类模型


import copy
from sqlalchemy import and_

from models.WpTerms import WpTerms
from models.WpTermmeta import WpTermmeta
from models.WpTermTaxonomy import WpTermTaxonomy
from models.WpTermRelationships import WpTermRelationships


def _generate_class_from_rows(wp_term_row, wp_termmeta_rows, wp_term_taxonomy_row):
    """
    函数说明: 通过数据库查询结果生成对象
    :param wp_term_row: wp_terms 表查询结果
    :param wp_termmeta_rows: wp_termmeta 表查询结果
    :param wp_term_taxonomy_row: wp_term_taxonomy 表查询结果
    """
    # 1. 名称
    name = wp_term_row.name
    # 2. 别名
    slug = wp_term_row.slug
    # 3. 父级分类目录 ID
    parent = wp_term_taxonomy_row.parent
    # 4. 描述
    description = wp_term_taxonomy_row.description
    # 5. 排序
    order = None
    for wp_termmeta_row in wp_termmeta_rows:
        if wp_termmeta_row.meta_key == "_term_order":
            order = wp_termmeta_row.meta_value
            break
    # 6. SEO 自定义标题
    seo_title = None
    for wp_termmeta_row in wp_termmeta_rows:
        if wp_termmeta_row.meta_key == "seo_title":
            seo_title = wp_termmeta_row.meta_value
            break
    # 7. SEO 设置关键词
    seo_metakey = None
    for wp_termmeta_row in wp_termmeta_rows:
        if wp_termmeta_row.meta_key == "seo_metakey":
            seo_metakey = wp_termmeta_row.meta_value
            break
    # 8. SEO 自定义描述
    seo_desc = None
    for wp_termmeta_row in wp_termmeta_rows:
        if wp_termmeta_row.meta_key == "seo_desc":
            seo_desc = wp_termmeta_row.meta_value
            break
    # 9. 网址卡片样式
    card_mode = None
    for wp_termmeta_row in wp_termmeta_rows:
        if wp_termmeta_row.meta_key == "card_mode":
            card_mode = wp_termmeta_row.meta_value
            break
    # 10. 网址列数
    columns_type = None
    for wp_termmeta_row in wp_termmeta_rows:
        if wp_termmeta_row.meta_key == "columns_type":
            columns_type = wp_termmeta_row.meta_value
            break
    # 11. 列数
    columns = None
    for wp_termmeta_row in wp_termmeta_rows:
        if wp_termmeta_row.meta_key == "columns":
            columns = wp_termmeta_row.meta_value
            break
    # 12. 插入表后的 term_id
    _term_id = wp_term_row.term_id
    # 13. 插入表后的 term_taxonomy_id
    _term_taxonomy_id = wp_term_taxonomy_row.term_taxonomy_id
    # 14. 生成对象
    favorite = OneNavFavorite(
        name=name,
        slug=slug,
        parent=parent,
        description=description,
        order=order,
        seo_title=seo_title,
        seo_metakey=seo_metakey,
        seo_desc=seo_desc,
        card_mode=card_mode,
        columns_type=columns_type,
        columns=columns,
        _term_id=_term_id,
        _term_taxonomy_id=_term_taxonomy_id
    )
    # 15. 返回
    return favorite


class OneNavFavorite():
    """
    类说明: OneNav 网址分类
    """
    def __init__(self,
                 name: str,
                 slug: str,
                 parent: int,
                 description: str,
                 order: int,
                 seo_title: str,
                 seo_metakey: str,
                 seo_desc: str,
                 card_mode: str,
                 columns_type: str,
                 columns: str,
                 _term_id: int = None,
                 _term_taxonomy_id: int = None):
        """
        函数说明: 初始化
        :param name: 名称
        :param slug: 别名
        :param parent: 父级分类目录 ID
        :param description: 描述
        :param order: 排序
        :param seo_title: SEO 自定义标题
        :param seo_metakey: SEO 设置关键词
        :param seo_desc: SEO 自定义描述
        :param card_mode: 网址卡片样式
        :param columns_type: 网址列数
        :param columns: 列数
        :param _term_id: 插入表后的 term_id
        :param _term_taxonomy_id: 插入表后的 term_taxonomy_id
        """
        self.name = name
        self.slug = slug
        self.parent = parent
        self.description = description
        self.order = order
        self.seo_title = seo_title
        self.seo_metakey = seo_metakey
        self.seo_desc = seo_desc
        self.card_mode = card_mode
        self.columns_type = columns_type
        self.columns = columns
        # 插入表后的 term_id
        self._term_id = _term_id
        # 插入表后的 term_taxonomy_id
        self._term_taxonomy_id = _term_taxonomy_id
    
    @staticmethod
    def check_all(favorite_ids: list, session):
        """
        函数说明: 查询网站分类是否存在
        :param favorite_ids: 网址分类 ID 列表
        :param session: 数据库会话
        """
        # 1. 查询 wp_term_taxonomy 表中数量是否一致
        temp_favorite_ids = copy.deepcopy(favorite_ids)
        wp_term_taxonomy_rows = session.query(WpTermTaxonomy).filter(
            and_(
                WpTermTaxonomy.term_id.in_(favorite_ids),
                WpTermTaxonomy.taxonomy == "favorites"
            )
        ).all()
        for wp_term_taxonomy_row in wp_term_taxonomy_rows:
            temp_favorite_ids.remove(wp_term_taxonomy_row.term_id)
        if temp_favorite_ids:
            print("网址分类 ID {} 在 wp_term_taxonomy 表中不存在".format(temp_favorite_ids))
            return False
        # 2. 查询 wp_terms 表中数量是否一致
        temp_favorite_ids = copy.deepcopy(favorite_ids)
        wp_terms_rows = session.query(WpTerms).filter(WpTerms.term_id.in_(favorite_ids))
        for wp_terms_row in wp_terms_rows:
            temp_favorite_ids.remove(wp_terms_row.term_id)
        if temp_favorite_ids:
            print("网址分类 ID {} 在 wp_terms 表中不存在".format(temp_favorite_ids))
            return False
        # 3. 返回
        return True

    @staticmethod
    def select(term_id: int, session):
        """
        函数说明: 查询分类
        :param term_id: 分类 ID
        :param session: 数据库会话
        """
        # 1. 通过 term_id 查询 wp_terms 表
        wp_term_row = session.query(WpTerms).filter(WpTerms.term_id == term_id).first()
        if not wp_term_row:
            return None
        # 2. 通过 term_id 查询 wp_termmeta 表
        wp_termmeta_rows = session.query(WpTermmeta).filter(WpTermmeta.term_id == term_id).all()
        # 3. 通过 term_id 查询 wp_term_taxonomy 表
        wp_term_taxonomy_row = session.query(WpTermTaxonomy).filter(WpTermTaxonomy.term_id == term_id).first()
        if not wp_term_taxonomy_row:
            return None
        # 4. 生成网址分类对象
        favorite = _generate_class_from_rows(
            wp_term_row=wp_term_row,
            wp_termmeta_rows=wp_termmeta_rows,
            wp_term_taxonomy_row=wp_term_taxonomy_row
        )
        # 5. 返回
        return favorite
