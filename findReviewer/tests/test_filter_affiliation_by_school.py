# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/24 14:02
# @Author  : lzg
# @Site    : 
# @File    : test_filter_affiliation_by_school.py
# @Software: PyCharm
import pytest
from findReviewer.useDerison.filterHandler import filter_affiliation_by_school  # 替换为实际模块名

def test_filter_affiliation_by_school():
    # 输入数据
    excel_data = [
        {
            "googlescholar_id": "scholar123",
            "Name": "Alice Wang",
            "Affiliation": "Georgia State University, Computer Science Department",
            "Email": "alice@gsu.edu",
            "Choice": "Yes",
            "Reason": "Good Research",
            "Google Scholar Home Page": "http://scholar.google.com",
        },
        {
            "googlescholar_id": "scholar456",
            "Name": "Bob Li",
            "Affiliation": "Tsinghua University",
            "Email": "bob@tsinghua.edu",
            "Choice": "No",
            "Reason": "Not Relevant",
            "Google Scholar Home Page": "http://scholar.google.com",
        },
        {
            "googlescholar_id": "scholar789",
            "Name": "Charlie Zhang",
            "Affiliation": "Stanford University",
            "Email": "charlie@stanford.edu",
            "Choice": "Yes",
            "Reason": "Excellent Publication",
            "Google Scholar Home Page": "http://scholar.google.com",
        },
    ]

    school_data = {
        "full_name": ["Georgia State University", "Tsinghua University"],
        "short_name": ["GSU", "THU"],
    }

    # 调用函数
    filtered, excluded = filter_affiliation_by_school(excel_data, school_data)

    # 预期结果
    expected_filtered = [
        {
            "googlescholar_id": "scholar123",
            "Name": "Alice Wang",
            "Affiliation": "Georgia State University, Computer Science Department",
            "Email": "alice@gsu.edu",
            "Choice": "Yes",
            "Reason": "Good Research",
            "Google Scholar Home Page": "http://scholar.google.com",
        },
        {
            "googlescholar_id": "scholar456",
            "Name": "Bob Li",
            "Affiliation": "Tsinghua University",
            "Email": "bob@tsinghua.edu",
            "Choice": "No",
            "Reason": "Not Relevant",
            "Google Scholar Home Page": "http://scholar.google.com",
        },
    ]

    expected_excluded = [
        {
            "googlescholar_id": "scholar789",
            "Name": "Charlie Zhang",
            "Affiliation": "Stanford University",
            "Email": "charlie@stanford.edu",
            "Choice": "Yes",
            "Reason": "Excellent Publication",
            "Google Scholar Home Page": "http://scholar.google.com",
        },
    ]

    # 断言
    assert filtered == expected_filtered
    assert excluded == expected_excluded