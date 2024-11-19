# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/17/24 00:58
# @Author  : lzg
# @Site    : 
# @File    : test_ensure_excel_file_with_headers.py
# @Software: PyCharm
import pytest
import os
import pandas as pd
from findReviewer.useDerison.runFindReviewer import ensure_excel_file_with_headers  # 替换为实际的模块名称

import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory

# 被测试函数
# ensure_excel_file_with_headers 定义同上

def test_ensure_excel_file_with_headers_creation():
    """
    测试文件不存在时是否正确创建。
    """
    with TemporaryDirectory() as temp_dir:
        temp_file = "test_file_creation"
        full_path = os.path.join(temp_dir, temp_file + ".xlsx")

        # 测试文件创建
        ensure_excel_file_with_headers(temp_dir, temp_file)
        assert os.path.exists(full_path), "The file should be created if it doesn't exist."

        # 检查文件内容
        df = pd.read_excel(full_path)
        assert list(df.columns) == ["Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"], \
            "The file should contain the correct headers."

def test_ensure_excel_file_with_headers_update():
    """
    测试文件存在但标题错误时是否正确更新。
    """
    with TemporaryDirectory() as temp_dir:
        temp_file = "test_file_update"
        full_path = os.path.join(temp_dir, temp_file + ".xlsx")

        # 创建文件但设置错误标题
        pd.DataFrame(columns=["InvalidColumn"]).to_excel(full_path, index=False)

        # 测试文件更新
        ensure_excel_file_with_headers(temp_dir, temp_file)

        # 检查文件内容是否更新
        df = pd.read_excel(full_path)
        assert list(df.columns) == ["Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"], \
            "The file should update headers if they are incorrect."

def test_ensure_excel_file_with_headers_existing_correct_file():
    """
    测试文件已存在且标题正确时是否保持不变。
    """
    with TemporaryDirectory() as temp_dir:
        temp_file = "test_file_existing"
        full_path = os.path.join(temp_dir, temp_file + ".xlsx")

        # 创建正确的文件
        pd.DataFrame(columns=["Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"]).to_excel(full_path, index=False)

        # 测试文件存在且正确
        ensure_excel_file_with_headers(temp_dir, temp_file)

        # 检查文件内容
        df = pd.read_excel(full_path)
        assert list(df.columns) == ["Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"], \
            "The file should retain headers if they are correct."