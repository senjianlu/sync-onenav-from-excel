#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/WpPostmeta.py
# @DATE: 2024/10/12
# @TIME: 16:26:33
#
# @DESCRIPTION: wp_postmeta 表模型


from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, DECIMAL, text, Text

from db import Base


class WpPostmeta(Base):
    """
    类说明: wp_postmeta 表模型
    """
    __tablename__ = "wp_postmeta"

    meta_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, nullable=False)
    meta_key = Column(String(255))
    meta_value = Column(Text)

    def __init__(self, post_id, meta_key, meta_value):
        self.post_id = post_id
        self.meta_key = meta_key
        self.meta_value = meta_value

    def __repr__(self):
        return "<WpPostmeta %r>" % self.meta_id

    def to_json(self):
        return {
            "meta_id": self.meta_id,
            "post_id": self.post_id,
            "meta_key": self.meta_key,
            "meta_value": self.meta_value
        }