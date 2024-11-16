# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/15/24 00:21
# @Author  : lzg
# @Site    : 
# @File    : test_exact_author_info.py
# @Software: PyCharm
# ---

import pytest
from findReviewer.lzgcode.findArticleAutherInfo import extract_authors_info
def test_extract_authors_info_normal_case():
    """
    测试正常情况下的函数行为
    """
    paper = {
        'bib': {
            'author': ['T Sharma', 'Y Potter', 'K Pongmala']
        },
        'author_id': ['U_iQbMIAAAAJ', 'ZDG9RD8AAAAJ', 'I2fhMnQAAAAJ']
    }
    expected_output = [
        {"name": "T Sharma", "google_scholar_id": "U_iQbMIAAAAJ"},
        {"name": "Y Potter", "google_scholar_id": "ZDG9RD8AAAAJ"},
        {"name": "K Pongmala", "google_scholar_id": "I2fhMnQAAAAJ"}
    ]
    assert extract_authors_info(paper) == expected_output

def test_extract_authors_info_mismatched_authors_and_ids():
    """
    测试作者数量与 author_id 数量不匹配的情况
    """
    paper = {
        'bib': {
            'author': ['T Sharma', 'Y Potter']
        },
        'author_id': ['U_iQbMIAAAAJ']
    }
    expected_output = "Mismatch between authors and author IDs. Please verify the input data."
    assert extract_authors_info(paper) == expected_output

def test_extract_authors_info_missing_author_field():
    """
    测试作者字段缺失的情况
    """
    paper = {
        'bib': {},  # 没有作者字段
        'author_id': ['U_iQbMIAAAAJ']
    }
    expected_output = "Mismatch between authors and author IDs. Please verify the input data."
    assert extract_authors_info(paper) == expected_output

def test_extract_authors_info_empty_input():
    """
    测试空输入的情况
    """
    paper = {}
    expected_output = "Mismatch between authors and author IDs. Please verify the input data."
    assert extract_authors_info(paper) == expected_output

def test_extract_authors_info_no_ids():
    """
    测试 author_id 字段缺失的情况
    """
    paper = {
        'bib': {
            'author': ['T Sharma', 'Y Potter', 'K Pongmala']
        }
    }
    expected_output = "Mismatch between authors and author IDs. Please verify the input data."
    assert extract_authors_info(paper) == expected_output