#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: onenav/site.py
# @DATE: 2024/10/12
# @TIME: 16:26:33
#
# @DESCRIPTION: 网址操作模块


from models.OneNavSite import OneNavSite
from models.OneNavSpareSite import OneNavSpareSite


def _get_temp_site_id_in_excel_2_spare_sites_str(spare_site_rows):
    """
    函数说明: 获取自定义 ID 与备用网站列表字符串的对应关系
    :param spare_site_rows: 备用网站源数据列表
    """
    # | 自定义 ID | No | 站点名称 | 站点链接 | 备注 |
    # 1. 生成自定义 ID 与备用网站源数据列表的对应关系
    temp_site_id_in_excel_2_spare_site_rows = {}
    for spare_site_row in spare_site_rows:
        temp_site_id_in_excel = spare_site_row[0]
        # 如果不存在对应关系则创建
        if temp_site_id_in_excel not in temp_site_id_in_excel_2_spare_site_rows:
            temp_site_id_in_excel_2_spare_site_rows[temp_site_id_in_excel] = []
        # 添加备用网站
        temp_site_id_in_excel_2_spare_site_rows[temp_site_id_in_excel].append(spare_site_row)
    # 2. 排序备用网站列表，同时生成自定义 ID 与备用网站对象列表的对应关系
    temp_site_id_in_excel_2_spare_sites = {}
    for temp_site_id_in_excel in temp_site_id_in_excel_2_spare_site_rows:
        temp_spare_site_rows = temp_site_id_in_excel_2_spare_site_rows[temp_site_id_in_excel]
        temp_spare_site_rows.sort(key=lambda x: x[1])
        temp_spare_sites = []
        for temp_spare_site_row in temp_spare_site_rows:
            temp_spare_sites.append(OneNavSpareSite(
                name=temp_spare_site_row[2],
                url=temp_spare_site_row[3],
                note=temp_spare_site_row[4]
            ))
        temp_site_id_in_excel_2_spare_sites[temp_site_id_in_excel] = temp_spare_sites
    # 3. 生成自定义 ID 和 PHP 数组格式的备用网站字符串的对应关系
    temp_site_id_in_excel_2_spare_sites_str = {}
    for temp_site_id_in_excel in temp_site_id_in_excel_2_spare_sites:
        temp_spare_sites = temp_site_id_in_excel_2_spare_sites[temp_site_id_in_excel]
        temp_spare_sites_str = OneNavSpareSite.convert_to_str(temp_spare_sites)
        temp_site_id_in_excel_2_spare_sites_str[temp_site_id_in_excel] = temp_spare_sites_str
    # 4. 返回
    return temp_site_id_in_excel_2_spare_sites_str

def _get_sites(site_rows, temp_site_id_in_excel_2_spare_sites_str):
    """
    函数说明: 生成网址列表
    :param site_rows: 网址源数据列表
    """
    # | 是否同步 | 自定义 ID | 文章 ID | 上次同步 | 网址分类 ID 列表 | 网址标签 ID 列表 | 标题 | 正文 | 链接 | 备用链接的个数 |
    # | 一句话描述（简介） | 站点语言 | 站点所在地 | 排序 | LOGO，标志的图片链接 | 网站预览截图的图片链接 | 公众号二维码的图片链接 | 备注 |
    # 1. 生成网址列表
    sites = []
    for site_row in site_rows:
        # 1.1 如果不需要同步则跳过
        # if not site_row[0]:
        #     continue
        # 1.2 网站分类 ID 列表
        if not site_row[4]:
            favorite_ids = []
        else:
            if "," in str(site_row[4]):
                favorite_ids = [str(favorite_id).strip() for favorite_id in site_row[4].split(",")]
            else:
                favorite_ids = [str(site_row[4])]
        # 1.3 网站标签 ID 列表
        if not site_row[5]:
            tag_ids = []
        else:
            if "," in str(site_row[5]):
                tag_ids = [str(tag_id).strip() for tag_id in site_row[5].split(",")]
            else:
                tag_ids = [str(site_row[5])]
        # 1.4 获取备用网站字符串
        temp_site_id_in_excel = site_row[1]
        spare_sites_str = temp_site_id_in_excel_2_spare_sites_str.get(temp_site_id_in_excel, "")
        # 1.5 添加网址
        sites.append(OneNavSite(
            favorite_ids=favorite_ids,
            tag_ids=tag_ids,
            title=site_row[6],
            content=site_row[7],
            link=site_row[8],
            spare_links=spare_sites_str,
            sescribe=site_row[10],
            language=site_row[11],
            country=site_row[12],
            order=site_row[13],
            thumbnail_pic_url=site_row[14],
            preview_pic_url=site_row[15],
            wechat_qr_pic_url=site_row[16]
        ))
    # 2. 返回
    return sites


def generate_sites_from_excel_data(data):
    """
    函数说明: 从 Excel 数据生成网址列表
    :param data: Excel 数据
    """
    # 1. 获取网址数据和备用网址数据
    site_rows = data["site_rows"]
    spare_site_rows = data["spare_site_rows"]
    # 2. 生成自定义 ID 与备用网站列表字符串的对应关系
    temp_site_id_in_excel_2_spare_sites_str = _get_temp_site_id_in_excel_2_spare_sites_str(spare_site_rows)
    # 3. 生成网址列表
    sites = _get_sites(site_rows, temp_site_id_in_excel_2_spare_sites_str)
    # 检查生成的网址数据
    # for site in sites:
    #     print(site.__dict__)
    # 4. 返回
    print("共生成 {} 条需要同步的网址数据\n".format(len(sites)) + "="*50)
    return sites
