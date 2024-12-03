# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/24 13:19
# @Author  : lzg
# @Site    : 
# @File    : dataHandler.py
# @Software: PyCharm


from typing import List
from dataStructure import FullAuthorInfo

def filter_authors_by_position(authors: List[FullAuthorInfo]) -> List[FullAuthorInfo]:
    """
    过滤作者列表，返回职位包含 'assistant professor' 或 'postdoctoral' 的作者。

    :param authors: 包含 FullAuthorInfo 数据的列表
    :return: 满足条件的 FullAuthorInfo 数据的列表
    """
    filtered_authors = [
        author for author in authors
        if 'assistant professor' in author.get('position', '').lower() or
           'postdoctoral' in author.get('position', '').lower()
    ]
    return filtered_authors


# 筛选函数
def filter_professors(data):
    """
    过滤出满足特定职位条件的人员数据。

    此函数遍历输入的人员数据列表，根据每个人的 `profile_info` 中的 `position` 字段内容，
    筛选出职位包含 "Assistant Professor" 或 "Associate Professor" 或"Postdoctoral"（大小写不敏感匹配）的人，
    并将这些人员的数据保存在新的列表中返回。

    参数:
        data (list): 一个包含人员数据的列表，每个元素是一个字典，
                     必须包含 `profile_info` 键，且其值是一个字典，
                     包含 `position` 键描述职位信息。

    返回:
        list: 一个包含符合条件的人员数据的新列表，保留原数据结构。

    示例:
        输入:
            data = [
                {'name': 'T Sharma', 'profile_info': {'position': 'Assistant Professor, Penn State University'}},
                {'name': 'Y Potter', 'profile_info': {'position': 'UC Berkeley'}},
                {'name': 'K Pongmala', 'profile_info': {'position': 'Associate Professor, UC Berkeley'}}
            ]
        调用:
            result = filter_professors(data)
        输出:
            [
                {'name': 'T Sharma', 'profile_info': {'position': 'Assistant Professor, Penn State University'}},
                {'name': 'K Pongmala', 'profile_info': {'position': 'Associate Professor, UC Berkeley'}}
            ]
    """
    filtered_list = []
    for item in data:
        # 安全获取每个人的 profile_info 信息
        profile_info = item.get('profile_info', {})

        # 安全获取职位信息并转换为小写以支持大小写不敏感匹配
        position = profile_info.get('position', '').lower()

        # 检查职位中是否包含目标关键词
        # if 'assistant professor' in position or 'associate professor'  in position or 'postdoctoral' in position:
        if 'assistant professor' in position or 'postdoctoral' in position:
            # 如果匹配成功，将整个数据项添加到结果列表中
            filtered_list.append(item)

    # 返回筛选后的列表
    return filtered_list


