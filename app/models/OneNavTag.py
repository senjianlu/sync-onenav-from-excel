#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/OneNavTag.py
# @DATE: 2024/10/14
# @TIME: 13:48:22
#
# @DESCRIPTION: 网址标签模型


import copy
import phpserialize
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
    # 3. 描述
    description = wp_term_taxonomy_row.description
    # 4. SEO 自定义信息
    sitetag_meta = None
    for wp_termmeta_row in wp_termmeta_rows:
        if wp_termmeta_row.meta_key == "sitetag_meta":
            sitetag_meta = wp_termmeta_row.meta_value
            break
    if sitetag_meta:
        # 将 PHP 数组转换为 Python 字典
        # a:3:{s:9:"seo_title";s:19:"SEO 自定义标题";s:11:"seo_metakey";s:25:"关键词一、关键词2";s:8:"seo_desc";s:15:"自定义描述";}
        sitetag_meta_dict_with_byte = phpserialize.loads(sitetag_meta.encode("utf-8"))
        # 将 sitetag_meta_dict 的所有 Byte 键值对转为字符串类型
        sitetag_meta_dict = {}
        for key, value in sitetag_meta_dict_with_byte.items():
            sitetag_meta_dict[key.decode("utf-8")] = value.decode("utf-8")
        # 获取 SEO 自定义信息
        seo_title = sitetag_meta_dict.get("seo_title")
        seo_metakey = sitetag_meta_dict.get("seo_metakey")
        seo_desc = sitetag_meta_dict.get("seo_desc")
    else:
        seo_title, seo_metakey, seo_desc = None, None, None
    # 5. 生成对象
    return OneNavTag(
        name=name,
        slug=slug,
        description=description,
        seo_title=seo_title,
        seo_metakey=seo_metakey,
        seo_desc=seo_desc
    )


class OneNavTag():
    """
    类说明: OneNav 网址标签
    """
    def __init__(self,
                 name: str,
                 slug: str,
                 description: str,
                 seo_title: str,
                 seo_metakey: str,
                 seo_desc: str,
                 _term_id: int = None,
                 _term_taxonomy_id: int = None):
        """
        函数说明: 初始化
        :param name: 名称
        :param slug: 别名
        :param description: 描述
        :param seo_title: SEO 自定义标题
        :param seo_metakey: SEO 设置关键词
        :param seo_desc: SEO 自定义描述
        """
        self.name = name
        self.slug = slug
        self.description = description
        self.seo_title = seo_title
        self.seo_metakey = seo_metakey
        self.seo_desc = seo_desc

    @staticmethod
    def check_all(tag_ids: list, session):
        """
        函数说明: 查询分类是否存在
        :param tag_ids: 分类 ID 列表
        :param session: 数据库会话
        """
        # 1. 查询 wp_term_taxonomy 表中数量是否一致
        temp_tag_ids = copy.deepcopy(tag_ids)
        wp_term_taxonomy_rows = session.query(WpTermTaxonomy).filter(
            and_(
                WpTermTaxonomy.term_id.in_(tag_ids),
                WpTermTaxonomy.taxonomy == "sitetag"
            )
        ).all()
        for wp_term_taxonomy_row in wp_term_taxonomy_rows:
            temp_tag_ids.remove(wp_term_taxonomy_row.term_id)
        if temp_tag_ids:
            print("网址标签 ID {} 在 wp_term_taxonomy 表中不存在".format(temp_tag_ids))
            return False
        # 2. 查询 wp_terms 表中数量是否一致
        temp_tag_ids = copy.deepcopy(tag_ids)
        wp_terms_rows = session.query(WpTerms).filter(WpTerms.term_id.in_(tag_ids)).all()
        for wp_terms_row in wp_terms_rows:
            temp_tag_ids.remove(wp_terms_row.term_id)
        if temp_tag_ids:
            print("网址标签 ID {} 在 wp_terms 表中不存在".format(temp_tag_ids))
            return False
        # 3. 返回
        return True
    
    @staticmethod
    def select(term_id: int, session):
        """
        函数说明: 查询标签
        :param term_id: 标签 ID
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
        # 4. 生成网址标签对象
        tag = _generate_class_from_rows(
            wp_term_row=wp_term_row,
            wp_termmeta_rows=wp_termmeta_rows,
            wp_term_taxonomy_row=wp_term_taxonomy_row
        )
        # 5. 返回
        return tag