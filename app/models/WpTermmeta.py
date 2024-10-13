#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/WpTermmeta.py
# @DATE: 2024/10/13
# @TIME: 20:36:01
#
# @DESCRIPTION: wp_termmeta 表模型


from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, DECIMAL, text, Text

from db import Base


class WpTermmeta(Base):
    """
    类说明: wp_termmeta 表模型
    """
    __tablename__ = "wp_termmeta"

    meta_id = Column(Integer, primary_key=True, autoincrement=True)
    term_id = Column(Integer, nullable=False)
    meta_key = Column(String(255))
    meta_value = Column(Text)

    def __init__(self, term_id, meta_key, meta_value):
        self.term_id = term_id
        self.meta_key = meta_key
        self.meta_value = meta_value

    def __repr__(self):
        return "<WpTermmeta %r>" % self.meta_id

    def to_json(self):
        return {
            "meta_id": self.meta_id,
            "term_id": self.term_id,
            "meta_key": self.meta_key,
            "meta_value": self.meta_value
        }