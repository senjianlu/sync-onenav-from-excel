#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/OneNavSite.py
# @DATE: 2024/10/12
# @TIME: 19:38:05
#
# @DESCRIPTION: OneNav 网址类


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
                 wechat_qr_pic_url: str):
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

    def select(self, session):
        """
        函数说明: 查询网址
        :param session: 数据库会话
        """
        pass

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