#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: site_all.py
# @DATE: 2024/10/15
# @TIME: 17:19:30
#
# @DESCRIPTION: 网址相关的测试用例集合


import sys
sys.path.append("../app")

from config import CONFIG
from site_case import excel as site_excel


def test_excel_load():
    """
    测试加载 Excel 文件
    """
    # 1. 读取配置文件
    file_name = CONFIG["test"]["file_name"]
    file_path = "../{}".format(file_name)
    sites_sheet = CONFIG["test"]["sites_sheet"]
    spare_links_sheet = CONFIG["test"]["spare_links_sheet"]
    # 2. 测试
    try:
        site_excel.test_load(file_path, sites_sheet, spare_links_sheet)
    except Exception as e:
        raise e

def test_excel_convert():
    """
    测试转换 Excel 数据
    """
    # 1. 读取配置文件
    file_name = CONFIG["test"]["file_name"]
    file_path = "../{}".format(file_name)
    sites_sheet = CONFIG["test"]["sites_sheet"]
    spare_links_sheet = CONFIG["test"]["spare_links_sheet"]
    # 2. 加载数据
    data = site_excel.test_load(file_path, sites_sheet, spare_links_sheet)
    # 3. 测试
    try:
        site_excel.test_convert(data)
    except Exception as e:
        raise e