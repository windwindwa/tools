# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/24 12:24
# @Author  : lzg
# @Site    : 
# @File    : test_process_keywords.py
# @Software: PyCharm

import os
import pytest
from findReviewer.useDerison.keywordHandler import process_keywords  # 替换为实际文件名


@pytest.fixture
def setup_files(tmp_path):
    """
    创建临时输入文件和输出文件。
    """
    # 创建临时目录中的输入文件
    input_file = tmp_path / "keyword.txt"
    output_file = tmp_path / "processed_keyword.txt"

    # 写入测试数据到输入文件
    input_file.write_text("keyword one-two,keyword two,another keyword", encoding="utf-8")

    return input_file, output_file


def test_process_keywords(setup_files):
    """
    测试 process_keywords 函数。
    """
    input_file, output_file = setup_files

    # 调用被测试方法
    process_keywords(str(input_file), str(output_file))

    # 读取输出文件内容
    result = output_file.read_text(encoding="utf-8")

    # 验证输出结果
    assert result == "keyword_one-two,keyword_two,another_keyword", "输出结果不符合预期！"
