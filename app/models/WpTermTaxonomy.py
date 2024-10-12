#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/WpTermTaxonomy.py
# @DATE: 2024/10/12
# @TIME: 16:26:33
#
# @DESCRIPTION: wp_term_taxonomy 表模型


from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, DECIMAL, text, Text


class WpTermTaxonomy(Base):
    """
    类说明: wp_term_taxonomy 表模型
    """
    __tablename__ = "wp_term_taxonomy"

    term_taxonomy_id = Column(Integer, primary_key=True, autoincrement=True)
    term_id = Column(Integer, nullable=False)
    taxonomy = Column(String(32), nullable=False)
    description = Column(Text)
    parent = Column(Integer)
    count = Column(Integer)

    def __init__(self, term_id, taxonomy, description, parent, count):
        self.term_id = term_id
        self.taxonomy = taxonomy
        self.description = description
        self.parent = parent
        self.count = count

    def __repr__(self):
        return "<WpTermTaxonomy %r>" % self.term_taxonomy_id

    def to_json(self):
        return {
            "term_taxonomy_id": self.term_taxonomy_id,
            "term_id": self.term_id,
            "taxonomy": self.taxonomy,
            "description": self.description,
            "parent": self.parent,
            "count": self.count
        }