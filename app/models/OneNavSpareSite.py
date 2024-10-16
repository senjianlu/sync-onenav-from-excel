#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: models/OneNavSpareSite.py
# @DATE: 2024/10/12
# @TIME: 19:38:05
#
# @DESCRIPTION: OneNav 备用网址类


import phpserialize


class OneNavSpareSite():
    """
    类说明: OneNav 备用网址类
    """
    def __init__(self,
                 name: str,
                 url: str,
                 note: str):
        """
        函数说明: 初始化
        :param name: 站点名称
        :param url: 站点链接
        :param note: 备注
        """
        self.name = name
        self.url = url
        self.note = note

    @staticmethod
    def convert_to_str(spare_sites: list) -> str:
        """
        函数说明: 将备用网址列表转换为 PHP 数组格式的字符串
        :param spare_sites: 备用网址列表
        """
        # 结果按照 PHP 数组的格式
        # a:3:{
        #     i:0;a:3:{s:10:"spare_name";s:4:"Bing";s:9:"spare_url";s:16:"https://bing.com";s:10:"spare_note";s:30:"这是 Bing 的跳转链接。";}
        #     i:1;a:3:{s:10:"spare_name";s:6:"Google";s:9:"spare_url";s:18:"https://google.com";s:10:"spare_note";s:32:"这是 Google 的跳转链接。";}
        #     i:2;a:3:{s:10:"spare_name";s:5:"Baidu";s:9:"spare_url";s:17:"https://baidu.com";s:10:"spare_note";s:31:"这是 Baidu 的跳转链接。";}
        # }
        # 拼接字符串
        result = phpserialize.dumps({
            i: {
                "spare_name": spare_site.name,
                "spare_url": spare_site.url,
                "spare_note": spare_site.note
            } for i, spare_site in enumerate(spare_sites)
        })
        # 返回结果
        return result

    @staticmethod
    def convert_to_list(spare_sites_str: str) -> list:
        """
        函数说明: 将 PHP 数组格式的字符串转换为备用网址列表
        :param spare_sites_str: PHP 数组格式的字符串
        """
        # 结果按照 PHP 数组的格式
        # a:3:{
        #     i:0;a:3:{s:10:"spare_name";s:4:"Bing";s:9:"spare_url";s:16:"https://bing.com";s:10:"spare_note";s:30:"这是 Bing 的跳转链接。";}
        #     i:1;a:3:{s:10:"spare_name";s:6:"Google";s:9:"spare_url";s:18:"https://google.com";s:10:"spare_note";s:32:"这是 Google 的跳转链接。";}
        #     i:2;a:3:{s:10:"spare_name";s:5:"Baidu";s:9:"spare_url";s:17:"https://baidu.com";s:10:"spare_note";s:31:"这是 Baidu 的跳转链接。";}
        # }
        # 1. 将 PHP 数组格式的字符串转为 Python3 字典
        try:
            spare_sites_str_bytes = spare_sites_str.encode("utf-8")
            temp_dict_with_byte = phpserialize.loads(spare_sites_str_bytes)
            # 将 sitetag_meta_dict 的所有 Byte 键值对转为字符串类型
            temp_dict = {}
            for key, value in temp_dict_with_byte.items():
                new_key = key.decode("utf-8") if isinstance(key, bytes) else key
                temp_dict[new_key] = {}
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        new_sub_key = sub_key.decode("utf-8") if isinstance(sub_key, bytes) else sub_key
                        new_sub_value = sub_value.decode("utf-8") if isinstance(sub_value, bytes) else sub_value
                        temp_dict[new_key][new_sub_key] = new_sub_value
                else:
                    temp_dict[new_key] = value.decode("utf-8") if isinstance(value, bytes) else value
        except Exception as e:
            print("备用网址字符串转换出错！")
            raise e
        # 2. 解析字典
        spare_sites = []
        for no in temp_dict:
            # 生成备用网址对象
            spare_sites.append(OneNavSpareSite(
                name=temp_dict[no]["spare_name"] if "spare_name" in temp_dict[no] else "",
                url=temp_dict[no]["spare_url"] if "spare_url" in temp_dict[no] else "",
                note=temp_dict[no]["spare_note"] if "spare_note" in temp_dict[no] else ""
            ))
        # 3. 返回结果
        return spare_sites