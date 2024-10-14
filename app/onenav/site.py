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
from models.OneNavFavorite import OneNavFavorite


def _print_operate_info(site, operate, is_success=True, detail=None):
    """
    函数说明: 打印操作信息
    :param site: 网址对象
    :param operate: 操作类型
    """
    message = "{} 网址{}成功：{}".format(
        "✅" if is_success else "❌",
        operate,
        site.title
    )
    if detail:
        message += "，{}".format(detail)
    print(message)

# def _get_site_id_in_excel_2_spare_sites_str(spare_site_rows):
#     """
#     函数说明: 获取自定义 ID 与备用网站列表字符串的对应关系
#     :param spare_site_rows: 备用网站源数据列表
#     """
#     # | 自定义 ID | No | 站点名称 | 站点链接 | 备注 |
#     # 1. 生成自定义 ID 与备用网站源数据列表的对应关系
#     site_id_in_excel_2_spare_site_rows = {}
#     for spare_site_row in spare_site_rows:
#         site_id_in_excel = spare_site_row[0]
#         # 如果不存在对应关系则创建
#         if site_id_in_excel not in site_id_in_excel_2_spare_site_rows:
#             site_id_in_excel_2_spare_site_rows[site_id_in_excel] = []
#         # 添加备用网站
#         site_id_in_excel_2_spare_site_rows[site_id_in_excel].append(spare_site_row)
#     # 2. 排序备用网站列表，同时生成自定义 ID 与备用网站对象列表的对应关系
#     site_id_in_excel_2_spare_sites = {}
#     for site_id_in_excel in site_id_in_excel_2_spare_site_rows:
#         temp_spare_site_rows = site_id_in_excel_2_spare_site_rows[site_id_in_excel]
#         temp_spare_site_rows.sort(key=lambda x: x[1])
#         temp_spare_sites = []
#         for temp_spare_site_row in temp_spare_site_rows:
#             temp_spare_sites.append(OneNavSpareSite(
#                 name=temp_spare_site_row[2],
#                 url=temp_spare_site_row[3],
#                 note=temp_spare_site_row[4]
#             ))
#         site_id_in_excel_2_spare_sites[site_id_in_excel] = temp_spare_sites
#     # 3. 生成自定义 ID 和 PHP 数组格式的备用网站字符串的对应关系
#     site_id_in_excel_2_spare_sites_str = {}
#     for site_id_in_excel in site_id_in_excel_2_spare_sites:
#         temp_spare_sites = site_id_in_excel_2_spare_sites[site_id_in_excel]
#         temp_spare_sites_str = OneNavSpareSite.convert_to_str(temp_spare_sites)
#         site_id_in_excel_2_spare_sites_str[site_id_in_excel] = temp_spare_sites_str
#     # 4. 返回
#     return site_id_in_excel_2_spare_sites_str

def _get_site_id_in_excel_2_spare_sites(spare_site_rows):
    """
    函数说明: 获取自定义 ID 与备用网站列表的对应关系
    :param spare_site_rows: 备用网站源数据列表
    """
    # | 自定义 ID | No | 站点名称 | 站点链接 | 备注 |
    # 1. 生成自定义 ID 与备用网站源数据列表的对应关系
    site_id_in_excel_2_spare_site_rows = {}
    for spare_site_row in spare_site_rows:
        site_id_in_excel = spare_site_row[0]
        # 如果不存在对应关系则创建
        if site_id_in_excel not in site_id_in_excel_2_spare_site_rows:
            site_id_in_excel_2_spare_site_rows[site_id_in_excel] = []
        # 添加备用网站
        site_id_in_excel_2_spare_site_rows[site_id_in_excel].append(spare_site_row)
    # 2. 排序备用网站列表，同时生成自定义 ID 与备用网站对象列表的对应关系
    site_id_in_excel_2_spare_sites = {}
    for site_id_in_excel in site_id_in_excel_2_spare_site_rows:
        temp_spare_site_rows = site_id_in_excel_2_spare_site_rows[site_id_in_excel]
        temp_spare_site_rows.sort(key=lambda x: x[1])
        temp_spare_sites = []
        for temp_spare_site_row in temp_spare_site_rows:
            temp_spare_sites.append(OneNavSpareSite(
                name=temp_spare_site_row[2],
                url=temp_spare_site_row[3],
                note=temp_spare_site_row[4]
            ))
        site_id_in_excel_2_spare_sites[site_id_in_excel] = temp_spare_sites
    # 3. 返回
    return site_id_in_excel_2_spare_sites

def _get_sites(site_rows, site_id_in_excel_2_spare_sites):
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
        if not site_row[0]:
            continue
        # 1.2 如果没有自定义 ID 则跳过
        if not site_row[1]:
            print('警告：网址数据中的 "{}" 未填写自定义 ID，已跳过'.format(site_row[6]))
            continue
        else:
            sync_site_id = site_row[1]
        # 1.3 网站分类 ID 列表
        if not site_row[4]:
            favorite_ids = []
        else:
            if "," in str(site_row[4]):
                favorite_ids = [int(str(favorite_id).strip()) for favorite_id in site_row[4].split(",")]
            else:
                favorite_ids = [int(str(site_row[4]))]
        # 1.4 网站标签 ID 列表
        if not site_row[5]:
            tag_ids = []
        else:
            if "," in str(site_row[5]):
                tag_ids = [int(str(tag_id).strip()) for tag_id in site_row[5].split(",")]
            else:
                tag_ids = [int(str(site_row[5]))]
        # 1.5 获取备用网站字符串
        site_id_in_excel = site_row[1]
        spare_sites = site_id_in_excel_2_spare_sites.get(site_id_in_excel, "")
        # 1.6 添加网址
        sites.append(OneNavSite(
            favorite_ids=favorite_ids,
            tag_ids=tag_ids,
            title=site_row[6],
            content=site_row[7],
            link=site_row[8],
            spare_links=spare_sites,
            sescribe=site_row[10],
            language=site_row[11],
            country=site_row[12],
            order=site_row[13],
            thumbnail_pic_url=site_row[14],
            preview_pic_url=site_row[15],
            wechat_qr_pic_url=site_row[16],
            # 用来将 Excel 中属于与表中数据建立关系的字段
            _sync_site_id=sync_site_id
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
    site_id_in_excel_2_spare_sites = _get_site_id_in_excel_2_spare_sites(spare_site_rows)
    # 3. 生成网址列表
    sites = _get_sites(site_rows, site_id_in_excel_2_spare_sites)
    # 检查生成的网址数据
    # for site in sites:
    #     print(site.__dict__)
    # 4. 返回
    print("从 Excel 的数据中筛选出 {} 条需要同步的网址\n".format(len(sites)) + "="*50)
    return sites

def select(sync_site_id, session):
    """
    函数说明: 查询网址数据
    :param sync_site_id: 网址自定义 ID
    :param session: 数据库会话
    """
    # 1. 查询网址数据
    site = OneNavSite.select(sync_site_id, session)
    # 2. 返回
    return site

def select_all(session):
    """
    函数说明: 查询所有网址数据
    :param session: 数据库会话
    """
    # 1. 查询所有网址数据
    sites = OneNavSite.select_all(session)
    # 2. 返回
    return sites

def insert(site, domain, session):
    """
    函数说明: 插入网址数据
    :param site: 网址对象
    :param session: 数据库会话
    """
    # 1. 事前检查
    # 1.1 是否有对应的网址分类
    for term_id in site.favorite_ids:
        favorite = OneNavFavorite.select(term_id, session)
        if not favorite:
            _print_operate_info(site, "插入", False, "没有对应的网址分类")
            return None
    # 1.2 是否有对应的网址标签
    # todo
    # 2. 调用对象的插入方法
    site.insert(session, domain)
    # 3. 保险起见提交事务
    session.commit()
    # 4. 打印提示信息
    _print_operate_info(site, "插入")
    # 5. 返回
    return site

def update(site, post_id, session):
    """
    函数说明: 更新网址数据
    :param site: 网址对象
    :param session: 数据库会话
    """
    # 1. 事前检查
    # 1.1 是否有对应的网址分类
    for term_id in site.favorite_ids:
        favorite = OneNavFavorite.select(term_id, session)
        if not favorite:
            _print_operate_info(site, "更新", False, "没有对应的网址分类")
            return None
    # 2. 调用对象的更新方法
    site.update(session, post_id)
    # 3. 保险起见提交事务
    session.commit()
    # 4. 打印提示信息
    _print_operate_info(site, "更新")
    # 5. 返回
    return site

def delete(site, post_id, session):
    """
    函数说明: 删除网址数据
    :param site: 网址对象
    :param session: 数据库会话
    """
    # 1. 调用对象的删除方法
    site.delete(session, post_id)
    # 2. 保险起见提交事务
    session.commit()
    # 3. 打印提示信息
    _print_operate_info(site, "删除")
    # 4. 返回
    return site