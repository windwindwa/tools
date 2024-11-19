# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/24 12:50
# @Author  : lzg
# @Site    : 
# @File    : test_insert_data.py
# @Software: PyCharm

import sqlite3
import pytest
from findReviewer.useDerison.databaseHandler import initialize_database, insert_data, TABLE_NAME  # 替换 your_module 为实际模块名


@pytest.fixture
def temp_db_file(tmp_path):
    """
    创建一个临时 SQLite 数据库文件用于测试，并初始化数据库。
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


def test_insert_data(temp_db_file, sample_data):
    """
    测试 insert_data 函数是否正确插入或更新数据。
    """
    # 调用 insert_data 插入数据
    insert_data(sample_data, db_file=str(temp_db_file))

    # 连接数据库，验证数据是否插入成功
    conn = sqlite3.connect(temp_db_file)
    cursor = conn.cursor()

    # 查询刚插入的记录
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE googlescholar_id = ?", (sample_data[0]['googlescholar_id'],))
    record = cursor.fetchone()

    # 验证记录内容
    assert record is not None
    assert record[0] == sample_data[0]['googlescholar_id']  # googlescholar_id
    assert record[1] == sample_data[0]['name']  # name
    assert record[2] == sample_data[0]['href']  # href
    assert record[3] == sample_data[0]['full_name']  # full_name
    assert record[4] == sample_data[0]['position']  # position
    assert record[5] == sample_data[0]['affiliation']  # affiliation
    assert record[6] == sample_data[0]['affiliation_link']  # affiliation_link
    assert record[7] == sample_data[0]['homepage']['href']  # homepage
    assert record[
               8] == "Computer Vision, Deep Learning, Multimedia, Few-Shot Learning, Large Language Model"  # keywords

    conn.close()