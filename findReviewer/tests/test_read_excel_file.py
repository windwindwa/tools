# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/24 13:56
# @Author  : lzg
# @Site    : 
# @File    : test_read_excel_file.py
# @Software: PyCharm
import pytest
import pandas as pd
from pathlib import Path
from findReviewer.useDerison.filterHandler import read_excel_file  # 替换为实际模块名

# 测试数据生成器
@pytest.fixture
def create_excel_file(tmp_path):
    def _create_file(filename, data):
        file_path = tmp_path / filename
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        return tmp_path, filename
    return _create_file

# 测试函数

def test_read_excel_file_valid_data(create_excel_file):
    # 测试正常数据
    data = [
        {
            "googlescholar_id": "scholar123",
            "Name": "Alice Wang",
            "Affiliation": "Georgia State Univ.",
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
    path, filename = create_excel_file("test_valid_data.xlsx", data)

    result = read_excel_file(path, filename)
    assert result == data


def test_read_excel_file_missing_columns(create_excel_file):
    # 测试缺少必要列
    data = [
        {
            "googlescholar_id": "scholar123",
            "Name": "Alice Wang",
        }
    ]
    path, filename = create_excel_file("test_missing_columns.xlsx", data)

    with pytest.raises(ValueError, match="缺少必要的列"):
        read_excel_file(path, filename)


def test_read_excel_file_empty_file(create_excel_file):
    # 测试空文件
    data = []
    path, filename = create_excel_file("test_empty_file.xlsx", data)

    result = read_excel_file(path, filename)
    assert result == []


def test_read_excel_file_invalid_path():
    # 测试无效路径
    path = Path("/non/existent/path")
    filename = "non_existent_file.xlsx"

    result = read_excel_file(path, filename)
    assert result == []


def test_read_excel_file_special_characters(create_excel_file):
    # 测试包含特殊字符的数据
    data = [
        {
            "googlescholar_id": "学者123",
            "Name": "张伟",
            "Affiliation": "北京大学",
            "Email": "zhangwei@pku.edu.cn",
            "Choice": "Yes",
            "Reason": "优秀研究",
            "Google Scholar Home Page": "http://scholar.google.com",
        }
    ]
    path, filename = create_excel_file("test_special_characters.xlsx", data)

    result = read_excel_file(path, filename)
    assert result == data