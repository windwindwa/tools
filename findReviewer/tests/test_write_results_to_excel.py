# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/24 14:09
# @Author  : lzg
# @Site    : 
# @File    : test_write_results_to_excel.py
# @Software: PyCharm
import pytest
import pandas as pd
from pathlib import Path
from findReviewer.useDerison.filterHandler import write_results_to_excel  # 替换为实际模块名

@pytest.fixture
def create_test_excel_file(tmp_path):
    def _create_file(data, filename="test_scholars.xlsx"):
        file_path = tmp_path / filename
        pd.DataFrame(data).to_excel(file_path, index=False)
        return file_path
    return _create_file

def test_write_results_to_excel(create_test_excel_file, tmp_path):
    # 测试数据
    original_data = [
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

    filtered_results = [
        {
            "googlescholar_id": "scholar123",
            "Name": "Alice Wang",
            "Affiliation": "Georgia State University, Computer Science Department",
            "Email": "alice@gsu.edu",
            "Choice": "Yes",
            "Reason": "Good Research",
            "Google Scholar Home Page": "http://scholar.google.com",
        },
    ]

    excluded_results = [
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

    # 创建原始Excel文件
    original_excel_path = create_test_excel_file(original_data)

    # 调用函数
    write_results_to_excel(original_excel_path, filtered_results, excluded_results)

    # 验证结果
    written_excel_path = Path(original_excel_path)

    # 读取写入的Excel文件
    with pd.ExcelFile(written_excel_path) as xls:
        # 验证过滤后的结果写入 "Filtered Results"
        filtered_df = pd.read_excel(xls, sheet_name="Filtered Results")
        assert filtered_df.to_dict(orient="records") == filtered_results

        # 验证被过滤的信息写入 "Excluded Results"
        excluded_df = pd.read_excel(xls, sheet_name="Excluded Results")
        assert excluded_df.to_dict(orient="records") == excluded_results