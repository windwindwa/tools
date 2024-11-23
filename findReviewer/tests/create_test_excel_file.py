# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/24 21:31
# @Author  : lzg
# @Site    : 
# @File    : create_test_excel_file.py
# @Software: PyCharm
import pytest
import sqlite3
import pandas as pd
from pathlib import Path
from findReviewer.useDerison.onlyInsertEmail2database import read_excel_file, update_email_in_db


# 创建测试文件夹
@pytest.fixture(scope="module")
def tmp_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("test_data")


# fixtures.py
import pandas as pd

@pytest.fixture
def create_test_excel_file(tmp_path):
    def _create_file(data):
        file_path = tmp_path / "test_data.xlsx"
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False, sheet_name="Sheet1")
        return file_path
    return _create_file

# 创建测试 SQLite 数据库
@pytest.fixture
def create_test_db(tmp_path):
    def _create_db(table_name, data):
        db_path = tmp_path / "test_database.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # 创建表时确保包含完整的列
        cursor.execute(f"""
            CREATE TABLE {table_name} (
                googlescholar_id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        """)
        for row in data:
            cursor.execute(f"""
                INSERT INTO {table_name} (googlescholar_id, name, email)
                VALUES (?, ?, ?)
            """, (row["googlescholar_id"], row["name"], row["email"]))
        conn.commit()
        conn.close()
        return db_path
    return _create_db
# 测试读取 Excel 文件
def test_read_excel_file(create_test_excel_file):
    test_data = [
        {"googlescholar_id": "12345", "Name": "Alice Wang", "Affiliation": "University A", "Email": "alice@example.com",
         "Choice": "Yes", "Reason": "Good", "Google Scholar Home Page": "http://example.com"},
        {"googlescholar_id": "67890", "Name": "Bob Smith", "Affiliation": "University B", "Email": "bob@example.com",
         "Choice": "No", "Reason": "Not relevant", "Google Scholar Home Page": "http://example.com"}
    ]
    file_path = create_test_excel_file(test_data)

    result = read_excel_file(file_path)
    assert len(result) == 2
    assert result[0]["googlescholar_id"] == "12345"
    assert result[0]["Email"] == "alice@example.com"


# 测试更新 SQLite 数据库
def test_update_email_in_db(create_test_db):
    initial_data = [
        {"googlescholar_id": "12345", "name": "Alice", "email": None},
        {"googlescholar_id": "67890", "name": "Bob", "email": None},
    ]
    db_path = create_test_db("users", initial_data)

    # 模拟 Excel 读取的数据
    excel_data = [
        {"googlescholar_id": "12345", "Email": "alice@example.com"},
        {"googlescholar_id": "67890", "Email": "bob@example.com"}
    ]

    update_email_in_db(db_path, excel_data)

    # 验证数据库更新结果
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE googlescholar_id = '12345'")
    row = cursor.fetchone()
    assert row[2] == "alice@example.com"

    cursor.execute("SELECT * FROM users WHERE googlescholar_id = '67890'")
    row = cursor.fetchone()
    assert row[2] == "bob@example.com"

    conn.close()