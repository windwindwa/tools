# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/24 13:39
# @Author  : lzg
# @Site    : 
# @File    : test_read_school_file.py
# @Software: PyCharm
import pytest
from pathlib import Path
from findReviewer.useDerison.filterHandler import read_school_file  # 替换 `your_module_name` 为实际模块名


# 测试数据生成器
@pytest.fixture
def create_test_file(tmp_path):
    def _create_file(content):
        test_file_path = tmp_path / "test_file.txt"
        test_file_path.write_text(content, encoding="utf-8")
        return test_file_path
    return _create_file

# 测试函数
def test_read_school_file_valid_data(create_test_file):
    # 测试正常数据
    content = """Georgia State University,GSU
Changchun University of Technology,CCUT
Tsinghua University,THU
Peking University,PKU"""
    file_path = create_test_file(content)

    expected_result = {
        "full_name": [
            "Georgia State University",
            "Changchun University of Technology",
            "Tsinghua University",
            "Peking University",
        ],
        "short_name": ["GSU", "CCUT", "THU", "PKU"],
    }

    result = read_school_file(file_path)
    assert result == expected_result


def test_read_school_file_empty_file(create_test_file):
    # 测试空文件
    file_path = create_test_file("")

    expected_result = {"full_name": [], "short_name": []}

    result = read_school_file(file_path)
    assert result == expected_result


def test_read_school_file_partial_invalid_data(create_test_file):
    # 测试部分数据格式错误
    content = """Georgia State University,GSU
Changchun University of Technology
Tsinghua University,THU
,PKU"""
    file_path = create_test_file(content)

    expected_result = {
        "full_name": ["Georgia State University", "Tsinghua University"],
        "short_name": ["GSU", "THU"],
    }

    result = read_school_file(file_path)
    assert result == expected_result


def test_read_school_file_invalid_file_path():
    # 测试无效文件路径
    invalid_path = Path("/non/existent/path.txt")

    result = read_school_file(invalid_path)

    # 结果应为空字典
    assert result == {"full_name": [], "short_name": []}


def test_read_school_file_special_characters(create_test_file):
    # 测试包含特殊字符的数据
    content = """乔治亚州立大学,GSU
长春工业大学,CCUT
清华大学,THU
北京大学,PKU"""
    file_path = create_test_file(content)

    expected_result = {
        "full_name": ["乔治亚州立大学", "长春工业大学", "清华大学", "北京大学"],
        "short_name": ["GSU", "CCUT", "THU", "PKU"],
    }

    result = read_school_file(file_path)
    assert result == expected_result