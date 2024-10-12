#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/WpPosts.py
# @DATE: 2024/10/12
# @TIME: 16:26:33
#
# @DESCRIPTION: wp_posts 表模型


from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, DECIMAL, text, Text

from db import Base


class WpPosts(Base):
    """
    类说明: wp_posts 表模型
    """

    __tablename__ = "wp_posts"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    post_author = Column(Integer, nullable=False)
    post_date = Column(DateTime, nullable=False)
    post_date_gmt = Column(DateTime, nullable=False)
    post_content = Column(Text, nullable=False)
    post_title = Column(String(255), nullable=False)
    post_excerpt = Column(Text)
    post_status = Column(String(20), nullable=False)
    comment_status = Column(String(20), nullable=False)
    ping_status = Column(String(20), nullable=False)
    post_password = Column(String(255), nullable=False)
    post_name = Column(String(200), nullable=False)
    to_ping = Column(Text)
    pinged = Column(Text)
    post_modified = Column(DateTime, nullable=False)
    post_modified_gmt = Column(DateTime, nullable=False)
    post_content_filtered = Column(Text)
    post_parent = Column(Integer, nullable=False)
    guid = Column(String(255), nullable=False)
    menu_order = Column(Integer, nullable=False)
    post_type = Column(String(20), nullable=False)
    post_mime_type = Column(String(100), nullable=False)
    comment_count = Column(Integer, nullable=False)

    def __init__(self, post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged, post_modified, post_modified_gmt, post_content_filtered, post_parent, guid, menu_order, post_type, post_mime_type, comment_count):
        self.post_author = post_author
        self.post_date = post_date
        self.post_date_gmt = post_date_gmt
        self.post_content = post_content
        self.post_title = post_title
        self.post_excerpt = post_excerpt
        self.post_status = post_status
        self.comment_status = comment_status
        self.ping_status = ping_status
        self.post_password = post_password
        self.post_name = post_name
        self.to_ping = to_ping
        self.pinged = pinged
        self.post_modified = post_modified
        self.post_modified_gmt = post_modified_gmt
        self.post_content_filtered = post_content_filtered
        self.post_parent = post_parent
        self.guid = guid
        self.menu_order = menu_order
        self.post_type = post_type
        self.post_mime_type = post_mime_type
        self.comment_count = comment_count
    
    def __repr__(self):
        return "<WpPosts %r>" % self.ID
    
    def to_json(self):
        return {
            "ID": self.ID,
            "post_author": self.post_author,
            "post_date": self.post_date,
            "post_date_gmt": self.post_date_gmt,
            "post_content": self.post_content,
            "post_title": self.post_title,
            "post_excerpt": self.post_excerpt,
            "post_status": self.post_status,
            "comment_status": self.comment_status,
            "ping_status": self.ping_status,
            "post_password": self.post_password,
            "post_name": self.post_name,
            "to_ping": self.to_ping,
            "pinged": self.pinged,
            "post_modified": self.post_modified,
            "post_modified_gmt": self.post_modified_gmt,
            "post_content_filtered": self.post_content_filtered,
            "post_parent": self.post_parent,
            "guid": self.guid,
            "menu_order": self.menu_order,
            "post_type": self.post_type,
            "post_mime_type": self.post_mime_type,
            "comment_count": self.comment_count
        }