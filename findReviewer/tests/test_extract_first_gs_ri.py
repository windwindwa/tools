# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/16/24 00:52
# @Author  : lzg
# @Site    : 
# @File    : test_extract_first_gs_ri.py.py
# @Software: PyCharm
import pytest
from bs4 import BeautifulSoup
from findReviewer.useDerison.runFindReviewer import extract_first_gs_ri_names_ids_hrefs  # 替换为实际的模块名

def test_extract_first_gs_ri_names_ids_hrefs():
    # 示例HTML输入
    html_str = """
    <div class="gs_ri">
        <h3 class="gs_rt"><a href="https://example.com/paper" id="paper123">Example Paper Title</a></h3>
        <div class="gs_a">
            <a href="/citations?user=abc123&amp;hl=zh-CN">Author One</a>,
            <a href="/citations?user=def456&amp;hl=zh-CN">Author Two</a>
        </div>
    </div>
    """
    # 调用函数
    result = extract_first_gs_ri_names_ids_hrefs(html_str)

    # 期望输出
    expected_result = [
        {"name": "Example Paper Title", "href": "https://example.com/paper", "googlescholar_id": None},
        {"name": "Author One", "href": "/citations?user=abc123&hl=zh-CN", "googlescholar_id": "abc123"},
        {"name": "Author Two", "href": "/citations?user=def456&hl=zh-CN", "googlescholar_id": "def456"},
    ]

    # 验证结果
    assert result == expected_result

def test_extract_first_gs_ri_names_ids_hrefs_no_gs_ri():
    # HTML输入没有gs_ri
    html_str = "<div>No relevant content here</div>"

    # 调用函数
    result = extract_first_gs_ri_names_ids_hrefs(html_str)

    # 验证结果为空
    assert result == []

def test_extract_first_gs_ri_names_ids_hrefs_partial_data():
    # HTML输入有部分字段缺失
    html_str = """
    <div class="gs_ri">
        <h3 class="gs_rt"><a href="https://example.com/paper2">Another Paper Title</a></h3>
        <div class="gs_a">
            <a href="/citations?user=xyz789&amp;hl=zh-CN">Author Three</a>
        </div>
    </div>
    """
    # 调用函数
    result = extract_first_gs_ri_names_ids_hrefs(html_str)

    # 期望输出
    expected_result = [
        {"name": "Another Paper Title", "href": "https://example.com/paper2", "googlescholar_id": None},
        {"name": "Author Three", "href": "/citations?user=xyz789&hl=zh-CN", "googlescholar_id": "xyz789"},
    ]

    # 验证结果
    assert result == expected_result


def test_extract_first_gs_ri_names_ids_hrefs_multiple_divs():
    # 示例HTML输入包含多个符合条件的 gs_ri
    html_str = """
    <div class="gs_ri">
        <h3 class="gs_rt"><a href="https://example.com/paper1" id="paper123">Paper Title One</a></h3>
        <div class="gs_a">
            <a href="/citations?user=abc123&amp;hl=zh-CN">Author One</a>,
            <a href="/citations?user=def456&amp;hl=zh-CN">Author Two</a>
        </div>
    </div>
    <div class="gs_ri">
        <h3 class="gs_rt"><a href="https://example.com/paper2" id="paper456">Paper Title Two</a></h3>
        <div class="gs_a">
            <a href="/citations?user=ghi789&amp;hl=zh-CN">Author Three</a>
        </div>
    </div>
    """
    # 调用函数
    result = extract_first_gs_ri_names_ids_hrefs(html_str)

    # 期望输出（仅匹配第一个 gs_ri）
    expected_result = [
        {"name": "Paper Title One", "href": "https://example.com/paper1", "googlescholar_id": None},
        {"name": "Author One", "href": "/citations?user=abc123&hl=zh-CN", "googlescholar_id": "abc123"},
        {"name": "Author Two", "href": "/citations?user=def456&hl=zh-CN", "googlescholar_id": "def456"},
    ]

    # 验证结果
    assert result == expected_result


# 测试用例
def test_extract_multiple_gs_ri():
    html_str = """
    <div class="gs_ri">
        <h3 class="gs_rt"><a href="https://example.com/paper1" id="paper1">Paper 1</a></h3>
        <div class="gs_a gs_fma_s">
            <a href="/citations?user=abc123&hl=en">Author A1</a>
            <a href="/citations?user=def456&hl=en">Author A2</a>
        </div>
        <div class="gs_a gs_fma_s">
            <a href="/citations?user=ghi789&hl=en">Author A3</a>
        </div>
    </div>
    <div class="gs_ri">
        <h3 class="gs_rt"><a href="https://example.com/paper2" id="paper2">Paper 2</a></h3>
        <div class="gs_a gs_fma_s">
            <a href="/citations?user=jkl012&hl=en">Author B1</a>
        </div>
    </div>
    """
    result = extract_first_gs_ri_names_ids_hrefs(html_str)

    # 预期结果
    expected = [
        {"name": "Author A1", "href": "/citations?user=abc123&hl=en", "googlescholar_id": "abc123"},
        {"name": "Author A2", "href": "/citations?user=def456&hl=en", "googlescholar_id": "def456"}
    ]

    # 验证
    assert result == expected


# 执行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])