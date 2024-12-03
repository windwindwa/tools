# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/24 13:05
# @Author  : lzg
# @Site    : 
# @File    : test_get_keywords_as_list.py
# @Software: PyCharm

import pytest
from findReviewer.useDerison.keywordHandler import get_keywords_as_list  # 替换为实际的脚本文件名


@pytest.fixture
def setup_test_file(tmp_path):
    """
    创建临时输入文件。
    """
    input_file = tmp_path / "keywords.txt"
    return input_file


def test_get_keywords_as_list_valid_file(setup_test_file):
    """
    测试处理有效文件。
    """
    input_file = setup_test_file
    # 写入测试数据
    input_file.write_text("keyword one, keyword two ,  another keyword", encoding="utf-8")

    # 调用被测试函数
    result = get_keywords_as_list(str(input_file))

    # 验证结果
    expected_result = ['keyword one', 'keyword two', 'another keyword']
    assert result == expected_result, f"Expected {expected_result}, got {result}"


def test_get_keywords_as_list_empty_file(setup_test_file):
    """
    测试空文件的情况。
    """
    input_file = setup_test_file
    # 写入空内容
    input_file.write_text("", encoding="utf-8")

    # 调用被测试函数
    result = get_keywords_as_list(str(input_file))

    # 验证结果
    expected_result = []
    assert result == expected_result, f"Expected {expected_result}, got {result}"


def test_get_keywords_as_list_file_not_found():
    """
    测试文件不存在的情况。
    """
    non_existent_file = "non_existent_file.txt"

    # 调用被测试函数
    result = get_keywords_as_list(non_existent_file)

    # 验证结果
    expected_result = []
    assert result == expected_result, f"Expected {expected_result}, got {result}"


def test_get_keywords_as_list_extra_spaces(setup_test_file):
    """
    测试包含额外空格的关键词处理。
    """
    input_file = setup_test_file
    # 写入测试数据
    input_file.write_text("  keyword 1  ,  keyword 2 ,keyword 3  ", encoding="utf-8")

    # 调用被测试函数
    result = get_keywords_as_list(str(input_file))

    # 验证结果
    expected_result = ['keyword 1', 'keyword 2', 'keyword 3']
    assert result == expected_result, f"Expected {expected_result}, got {result}"
