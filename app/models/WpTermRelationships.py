#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/WpTermRelationships.py
# @DATE: 2024/10/12
# @TIME: 16:26:33
#
# @DESCRIPTION: wp_term_relationships 表模型


from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, DECIMAL, text, Text


class WpTermRelationships(Base):
    """
    类说明: wp_term_relationships 表模型
    """
    __tablename__ = "wp_term_relationships"

    object_id = Column(Integer, primary_key=True)
    term_taxonomy_id = Column(Integer, primary_key=True)
    term_order = Column(Integer)

    def __init__(self, object_id, term_taxonomy_id, term_order):
        self.object_id = object_id
        self.term_taxonomy_id = term_taxonomy_id
        self.term_order = term_order

    def __repr__(self):
        return "<WpTermRelationships %r>" % self.object_id

    def to_json(self):
        return {
            "object_id": self.object_id,
            "term_taxonomy_id": self.term_taxonomy_id,
            "term_order": self.term_order
        }


