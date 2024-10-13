#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: sync.py
# @DATE: 2024/10/12
# @TIME: 23:27:37
#
# @DESCRIPTION: 同步模块


import copy

from models.OneNavSite import OneNavSite


def _print_next_step_info(sites_to_add, sites_to_delete, sites_to_update):
    """
    函数说明: 打印下一步操作信息
    :param sites_to_add: 需要新增的网址列表
    :param sites_to_delete: 需要删除的网址列表
    :param sites_to_update: 需要更新的网址列表
    """
    # 1. 需要新增的网址列表
    print("✅ 需要新增的网址共有 {} 条".format(len(sites_to_add)))
    for site in sites_to_add:
        print("{} {}: {}".format(site._sync_site_id, site.title, site.link))
    print("-"*40)
    # 2. 需要删除的网址列表
    print("❌ 需要删除的网址共有 {} 条".format(len(sites_to_delete)))
    for site in sites_to_delete:
        print("{} {}: {}".format(site._sync_site_id, site.title, site.link))
    print("-"*40)
    # 3. 需要更新的网址列表
    print("⚠️需要更新的网址共有 {} 条".format(len(sites_to_update)))
    for site in sites_to_update:
        print("{} {}: {}".format(site._sync_site_id, site.title, site.link))
    print("-"*40)

def _compare_sites(excel_sites_dict, db_sites_dict) -> (list, list, list):
    """
    函数说明: 对比网址列表
    :param excel_sites: Excel 中的网址列表
    :param db_sites: 数据库中的网址列表
    :return: 需要新增的网址列表、需要删除的网址列表、需要更新的网址列表
    """
    sites_to_add = []
    sites_to_delete = []
    sites_to_update = []
    # 1. 筛选出在 Excel 中存在但在数据库中不存在的网址
    for sync_site_id in excel_sites_dict:
        if sync_site_id not in db_sites_dict:
            sites_to_add.append(excel_sites_dict[sync_site_id])
    # 2. 筛选出在数据库中存在但在 Excel 中不存在的网址
    for sync_site_id in db_sites_dict:
        if sync_site_id not in excel_sites_dict:
            sites_to_delete.append(db_sites_dict[sync_site_id])
    # 3. 筛选出在两个列表中都存在的网址
    for sync_site_id in excel_sites_dict:
        if sync_site_id in db_sites_dict:
            excel_site = excel_sites_dict[sync_site_id]
            db_site = db_sites_dict[sync_site_id]
            if not excel_site.equals(db_site):
                sites_to_update.append(excel_site)
    # 4. 返回
    return sites_to_add, sites_to_delete, sites_to_update

def _do_full_sync(domain, session, sites):
    """
    函数说明: 全量同步
    :param domain: 导航站点域名
    :param session: 数据库会话
    :param sites: 网址列表
    """
    pass

def _do_part_sync(domain, session, sites):
    """
    函数说明: 部分同步
    :param domain: 导航站点域名
    :param session: 数据库会话
    :param sites: 网址列表
    """
    excel_sites = copy.deepcopy(sites)
    # 1. 获取 MySQL 表中带有 _sync_site_id 的网址列表
    db_sites = OneNavSite.select_all(session)
    # 2. 将两个列表整理成以 _sync_site_id 为 key 的字典
    # 理论上不会出现重复的情况
    excel_sites_dict = {}
    for site in excel_sites:
        excel_sites_dict[site._sync_site_id] = site
    db_sites_dict = {}
    for site in db_sites:
        db_sites_dict[site._sync_site_id] = site
    # 3. 对比两个字典，生成需要新增、删除、更新的网址列表
    sites_to_add, sites_to_delete, sites_to_update = _compare_sites(excel_sites_dict, db_sites_dict)
    # 4. 打印信息
    _print_next_step_info(sites_to_add, sites_to_delete, sites_to_update)
    # 5. 执行操作
    # 5.1 新增网址
    for site in sites_to_add:
        site.insert(domain, session)
    # 5.2 删除网址
    for site in sites_to_delete:
        site.delete(session)
    # 5.3 更新网址
    for site in sites_to_update:
        site.update(domain, session)
    # 6. 保险起见，提交事务
    session.commit()

def do_sync(sync_mode, domain, session, sites):
    """
    函数说明: 同步函数
    :param sync_mode: 同步模式
    :param domain: 导航站点域名
    :param session: 数据库会话
    :param sites: 网址列表
    """
    # 1. 全量同步
    if sync_mode == "full":
        print("暂不支持全量同步，程序将不执行任何操作！\n" + "="*50)
        # _do_full_sync(domain, session, sites)
    # 2. 部分同步
    elif sync_mode == "part":
        print("部分同步模式启动！\n" + "-"*40)
        _do_part_sync(domain, session, sites)
        print("部分同步完成！\n" + "="*50)
    # 3. 同步完成
    print("同步完成")
