# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/20/24 19:41
# @Author  : lzg
# @Site    : 
# @File    : test_read_unique_names_from_excel.py
# @Software: PyCharm
import os
import pytest
import pandas as pd
from findReviewer.useDerison.testrunFindReviewer  import read_unique_names_from_excel  # 替换为实际的模块名称
tmp_path = os.path.dirname(os.path.abspath(__file__))
@pytest.fixture
def create_test_excel_file(tmp_path):
    """
    创建一个测试 Excel 文件并返回其路径。
    """
    # 创建临时目录
    file_path = tmp_path
    file_name = "test_data.xlsx"
    full_path = os.path.join(file_path, file_name)

    # 创建测试数据
    data = {
        "Name": ["Alice", "Bob", "Alice", "Charlie", None],
        "Affiliation": ["Dept A", "Dept B", "Dept A", "Dept C", "Dept D"],
        "Email": ["alice@example.com", "bob@example.com", None, "charlie@example.com", None]
    }

    # 保存为 Excel 文件
    df = pd.DataFrame(data)
    df.to_excel(full_path, index=False)

    return file_path, file_name

def test_read_unique_names_from_excel(create_test_excel_file):
    """
    测试读取 Excel 文件并去重 `Name` 列的功能。
    """
    # 获取测试文件路径
    file_path, file_name = create_test_excel_file

    # 调用函数
    unique_names = read_unique_names_from_excel(file_path, file_name)

    # 断言结果
    expected_names = ["Alice", "Bob", "Charlie"]  # 期望的去重结果
    assert set(unique_names) == set(expected_names), "去重的 Name 列数据不正确"

def test_missing_name_column(tmp_path="/Users/lzg/0_lzgData/2_Personal/220_othersTools/tools/findReviewer/tests/"):
    """
    测试当 Excel 文件中缺少 `Name` 列时的异常处理。
    """
    # 创建测试文件
    file_path = tmp_path
    file_name = "test_no_name.xlsx"
    full_path = os.path.join(file_path, file_name)

    # 创建测试数据（不包含 Name 列）
    data = {
        "Affiliation": ["Dept A", "Dept B"],
        "Email": ["alice@example.com", "bob@example.com"]
    }

    # 保存为 Excel 文件
    df = pd.DataFrame(data)
    df.to_excel(full_path, index=False)

    # 调用函数并断言抛出异常
    with pytest.raises(ValueError, match="Excel 文件中未找到 `Name` 列"):
        read_unique_names_from_excel(file_path, file_name)

def test_empty_excel_file(tmp_path):
    """
    测试空 Excel 文件的处理。
    """
    # 创建空 Excel 文件
    file_path = tmp_path
    file_name = "test_empty.xlsx"
    full_path = os.path.join(file_path, file_name)

    # 保存一个空 DataFrame
    pd.DataFrame().to_excel(full_path, index=False)

    # 调用函数并验证返回值为空列表
    result = read_unique_names_from_excel(file_path, file_name)
    assert result == [], "空 Excel 文件的返回值应该为空列表"