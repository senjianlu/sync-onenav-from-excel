#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: config.py
# @DATE: 2024/10/12
# @TIME: 16:22:51
#
# @DESCRIPTION: 配置文件读取模块


import toml


# 项目根目录下的配置文件
CONFIG = {}
CONFIG_FILE_PATH = ""
try:
    CONFIG = toml.load("../config.toml")
    CONFIG_FILE_PATH = "../config.toml"
except Exception as e:
    CONFIG = toml.load("config.toml")
    CONFIG_FILE_PATH = "config.toml"