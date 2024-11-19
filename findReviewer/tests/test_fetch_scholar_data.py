# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/24 13:30
# @Author  : lzg
# @Site    : 
# @File    : test_fetch_scholar_data.py
# @Software: PyCharm
import pytest
import sqlite3
from findReviewer.useDerison.databaseHandler import initialize_database, insert_data, fetch_scholar_data, DB_FILE, TABLE_NAME  # 替换 `your_module` 为实际模块名

import sqlite3
import pytest


@pytest.fixture
def temp_db_file(tmp_path):
    """
    创建一个临时 SQLite 数据库文件并初始化表结构。
    """
    db_file = tmp_path / "test_scholar_data.db"
    initialize_database(db_file=str(db_file))
    return db_file


@pytest.fixture
def sample_data():
    """
    提供测试用的样本数据。
    """
    return [
        {
            'googlescholar_id': '1dh5WWUAAAAJ',
            'name': 'G Han',
            'href': 'https://scholar.google.com/citations?user=1dh5WWUAAAAJ&hl=zh-CN&oi=sra',
            'full_name': 'Guangxing Han',
            'position': 'Google DeepMind',
            'affiliation': 'Google',
            'affiliation_link': '/citations?view_op=view_org&hl=zh-CN&org=6518679690484165796',
            'homepage': {'href': 'https://guangxinghan.github.io/'},
            'keywords': [
                {'name': 'Computer Vision'},
                {'name': 'Deep Learning'},
                {'name': 'Multimedia'},
                {'name': 'Few-Shot Learning'},
                {'name': 'Large Language Model'}
            ]
        }
    ]


def test_fetch_scholar_data_existing_entry(temp_db_file, sample_data):
    """
    测试 fetch_scholar_data 函数是否正确返回已存在的数据。
    """
    # 插入测试数据
    insert_data(sample_data, db_file=str(temp_db_file))

    # 查询插入的数据
    result = fetch_scholar_data('1dh5WWUAAAAJ', db_file=str(temp_db_file))

    # 验证返回的数据结构
    assert result['googlescholar_id'] == '1dh5WWUAAAAJ'
    assert result['name'] == 'G Han'
    assert result['href'] == 'https://scholar.google.com/citations?user=1dh5WWUAAAAJ&hl=zh-CN&oi=sra'
    assert result['full_name'] == 'Guangxing Han'
    assert result['position'] == 'Google DeepMind'
    assert result['affiliation'] == 'Google'
    assert result['affiliation_link'] == '/citations?view_op=view_org&hl=zh-CN&org=6518679690484165796'
    assert result['homepage']['href'] == 'https://guangxinghan.github.io/'
    assert result['homepage']['text'] == 'N/A'
    expected_keywords = [
        {'name': 'computer_vision',
         'href': '/citations?view_op=search_authors&hl=zh-CN&mauthors=label:computer_vision'},
        {'name': 'deep_learning', 'href': '/citations?view_op=search_authors&hl=zh-CN&mauthors=label:deep_learning'},
        {'name': 'multimedia', 'href': '/citations?view_op=search_authors&hl=zh-CN&mauthors=label:multimedia'},
        {'name': 'few-shot_learning',
         'href': '/citations?view_op=search_authors&hl=zh-CN&mauthors=label:few-shot_learning'},
        {'name': 'large_language_model',
         'href': '/citations?view_op=search_authors&hl=zh-CN&mauthors=label:large_language_model'}
    ]
    assert result['keywords'] == expected_keywords


def test_fetch_scholar_data_nonexistent_entry(temp_db_file):
    """
    测试 fetch_scholar_data 函数在查询不存在的 ID 时返回默认值。
    """
    # 查询一个不存在的 ID
    result = fetch_scholar_data('nonexistent_id', db_file=str(temp_db_file))

    # 验证返回的默认值
    assert result['googlescholar_id'] == 'nonexistent_id'
    assert result['href'] == ''
    assert result['name'] == ''
    assert result['full_name'] == ''
    assert result['position'] == ''
    assert result['affiliation'] == ''
    assert result['affiliation_link'] == ''
    assert result['homepage']['href'] == ''
    assert result['homepage']['text'] == 'N/A'
    assert result['keywords'] == []
