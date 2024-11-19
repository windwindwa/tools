# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/17/24 00:29
# @Author  : lzg
# @Site    : 
# @File    : test_filter_professors.py.py
# @Software: PyCharm
import pytest

# 被测试的函数
from findReviewer.useDerison.runFindReviewer import filter_professors

# 测试函数
def test_filter_professors():
    # 测试数据
    test_data = [
        {'name': 'T Sharma', 'profile_info': {'position': 'Assistant Professor, Penn State University'}},
        {'name': 'Y Potter', 'profile_info': {'position': 'UC Berkeley'}},
        {'name': 'K Pongmala', 'profile_info': {'position': 'Associate Professor, UC Berkeley'}},
        {'name': 'M Allen', 'profile_info': {'position': 'Research Scientist'}},
        {'name': 'L Zhang', 'profile_info': {'position': ''}},  # 空职位信息
    ]

    # 期望结果
    expected_result = [
        {'name': 'T Sharma', 'profile_info': {'position': 'Assistant Professor, Penn State University'}},
        {'name': 'K Pongmala', 'profile_info': {'position': 'Associate Professor, UC Berkeley'}},
    ]

    # 调用被测函数
    result = filter_professors(test_data)

    # 断言结果是否与期望一致
    assert result == expected_result

def test_filter_professors_empty_list():
    # 测试空列表输入
    test_data = []
    # 期望结果
    expected_result = []
    # 调用被测函数
    result = filter_professors(test_data)
    # 断言结果是否为空
    assert result == expected_result

def test_filter_professors_no_match():
    # 测试无匹配项
    test_data = [
        {'name': 'A Green', 'profile_info': {'position': 'Postdoctoral Fellow'}},
        {'name': 'B White', 'profile_info': {'position': 'Student'}},
    ]
    # 期望结果
    expected_result = []
    # 调用被测函数
    result = filter_professors(test_data)
    # 断言结果是否为空
    assert result == expected_result

def test_filter_professors_case_insensitive():
    # 测试大小写不敏感匹配
    test_data = [
        {'name': 'C Brown', 'profile_info': {'position': 'ASSOCIATE PROFESSOR, MIT'}},
        {'name': 'D Black', 'profile_info': {'position': 'assistant professor, Harvard'}},
    ]
    # 期望结果
    expected_result = [
        {'name': 'C Brown', 'profile_info': {'position': 'ASSOCIATE PROFESSOR, MIT'}},
        {'name': 'D Black', 'profile_info': {'position': 'assistant professor, Harvard'}},
    ]
    # 调用被测函数
    result = filter_professors(test_data)
    # 断言结果是否与期望一致
    assert result == expected_result