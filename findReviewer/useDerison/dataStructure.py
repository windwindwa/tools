# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/24 13:46
# @Author  : lzg
# @Site    : 
# @File    : dataStructure.py
# @Software: PyCharm


from typing import TypedDict, List

class Homepage(TypedDict):
    href: str
    text: str

class FullAuthorInfo(TypedDict):
    googlescholar_id: str
    href: str
    email: str
    name: str
    full_name: str
    position: str
    affiliation: str
    affiliation_link: str
    homepage: Homepage  # 嵌套的 TypedDict
    keywords: List[str]  # 关键词是一个字符串列表


