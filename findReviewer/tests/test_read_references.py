# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/24 10:56
# @Author  : lzg
# @Site    : 
# @File    : test_read_references.py
# @Software: PyCharm
import pytest
from findReviewer.useDerison.justtest import read_references
@pytest.fixture
def create_sample_file(tmp_path):
    """
    使用 pytest 的 tmp_path fixture 创建一个临时文件
    """
    file = tmp_path / "target.txt"
    content = """Reference 1
Reference 2
Reference 3

Reference 4
    """
    file.write_text(content, encoding='utf-8')
    return file

def test_read_references_success(create_sample_file):
    """
    测试正常读取文件的情况
    """
    file_path = str(create_sample_file)
    expected = ["Reference 1", "Reference 2", "Reference 3", "Reference 4"]
    assert read_references(file_path) == expected

def test_read_references_file_not_found():
    """
    测试文件不存在的情况
    """
    file_path = "non_existent_file.txt"
    assert read_references(file_path) == []

def test_read_references_empty_file(tmp_path):
    """
    测试文件为空的情况
    """
    file = tmp_path / "empty.txt"
    file.write_text("", encoding='utf-8')
    assert read_references(str(file)) == []
