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
from onenav import site as onenav_site


def _print_next_step_info(sites_to_add, sites_to_delete, sites_to_update, sites_need_update_fields_dict):
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
    print("🔁 需要更新的网址共有 {} 条".format(len(sites_to_update)))
    for site in sites_to_update:
        need_update_fields = sites_need_update_fields_dict[site._sync_site_id]
        print("{} {}: {} ➡️ {}".format(site._sync_site_id, site.title, site.link, str(need_update_fields)))
    print("-"*40)

def _compare_sites(excel_sites_dict, db_sites_dict) -> (list, list, list, dict):
    """
    函数说明: 对比网址列表
    :param excel_sites: Excel 中的网址列表
    :param db_sites: 数据库中的网址列表
    :return: 需要新增的网址列表、需要删除的网址列表、需要更新的网址列表
    """
    sites_to_add = []
    sites_to_delete = []
    sites_to_update = []
    sites_need_update_fields_dict = {}
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
            is_equal, need_update_fields_dict = onenav_site.compare(excel_site, db_site)
            if not is_equal:
                # 获取数据库中的 post_id
                excel_site._post_id = db_site._post_id
                sites_to_update.append(excel_site)
                sites_need_update_fields_dict[excel_site._sync_site_id] = need_update_fields_dict
    # 4. 返回
    return sites_to_add, sites_to_delete, sites_to_update, sites_need_update_fields_dict

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
    sites_to_add, sites_to_delete, sites_to_update, sites_need_update_fields_dict = _compare_sites(excel_sites_dict, db_sites_dict)
    # 4. 打印信息
    _print_next_step_info(sites_to_add, sites_to_delete, sites_to_update, sites_need_update_fields_dict)
    # 5. 手动确认
    print("检查以上操作是否正确，确认完成后请告知我是否继续？(y/n)")
    confirm = input()
    if confirm.lower() != "y":
        print("操作已取消！\n" + "-"*40)
        return
    print("-"*40)
    print("开始执行操作......")
    # 6. 执行操作
    # 6.1 新增网址
    for site in sites_to_add:
        onenav_site.insert(site, domain, session)
    # 6.2 删除网址
    for site in sites_to_delete:
        onenav_site.delete(site, session)
    # 6.3 更新网址
    for site in sites_to_update:
        onenav_site.update(site, session)
    # 7. 保险起见提交事务
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
    # 3. 其他情况
    else:
        print("同步模式错误！程序将不执行任何操作！\n" + "="*50)
        return
