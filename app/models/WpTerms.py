#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/WpTerms.py
# @DATE: 2024/10/13
# @TIME: 20:31:55
#
# @DESCRIPTION: wp_terms 表模型


from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, DECIMAL, text, Text

from db import Base


class WpTerms(Base):
    """
    类说明: wp_terms 表模型
    """
    __tablename__ = "wp_terms"

    term_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False)
    term_group = Column(Integer, nullable=False)

    def __init__(self, name, slug, term_group):
        self.name = name
        self.slug = slug
        self.term_group = term_group

    def __repr__(self):
        return "<WpTerms %r>" % self.term_id

    def to_json(self):
        return {
            "term_id": self.term_id,
            "name": self.name,
            "slug": self.slug,
            "term_group": self.term_group
        }