import os
import sqlite3
import pytest
from findReviewer.useDerison.databaseHandler import initialize_database, DB_FILE, TABLE_NAME  # 替换 your_module 为实际模块名


@pytest.fixture
def temp_db_file(tmp_path):
    """
    创建一个临时 SQLite 数据库文件用于测试。
    """
    return tmp_path / "test_scholar_data.db"


def test_initialize_database_creates_file_and_table(temp_db_file):
    """
    测试 initialize_database 函数是否正确创建数据库文件和表。
    """
    # 确保数据库文件不存在
    assert not os.path.exists(temp_db_file)

    # 调用函数初始化数据库
    initialize_database(db_file=str(temp_db_file))

    # 检查数据库文件是否已创建
    assert os.path.exists(temp_db_file)

    # 连接数据库，检查表是否存在
    conn = sqlite3.connect(temp_db_file)
    cursor = conn.cursor()

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TABLE_NAME}';")
    table_exists = cursor.fetchone()

    # 检查表是否已成功创建
    assert table_exists is not None

    # 检查表的列是否正确
    cursor.execute(f"PRAGMA table_info({TABLE_NAME});")
    columns = cursor.fetchall()
    expected_columns = [
        ("googlescholar_id", "TEXT"),
        ("name", "TEXT"),
        ("href", "TEXT"),
        ("full_name", "TEXT"),
        ("position", "TEXT"),
        ("affiliation", "TEXT"),
        ("affiliation_link", "TEXT"),
        ("homepage", "TEXT"),
        ("keywords", "TEXT"),
    ]
    actual_columns = [(col[1], col[2]) for col in columns]
    assert actual_columns == expected_columns

    conn.close()