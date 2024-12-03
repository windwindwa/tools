# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/24 20:17
# @Author  : lzg
# @Site    : 
# @File    : onlyFilteredResultExcel.py
# @Software: PyCharm
import sqlite3
import pandas as pd
import argparse
import os

def read_excel_file(excel_path):
    """
    读取 Excel 文件的第一个 sheet，提取指定列的内容。
    :param excel_path: Excel 文件路径
    :return: 包含每行数据的列表 [{列名: 值, ...}, ...]
    """
    try:
        df = pd.read_excel(excel_path, sheet_name=0)  # 读取第一个 Sheet
        # 检查列是否完整
        required_columns = ["googlescholar_id", "Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"缺少必要列: {col}")
        # 转换为字典列表

        return df.to_dict(orient="records")
    except Exception as e:
        print(f"读取 Excel 文件失败: {e}")
        raise



def update_email_in_db(db_path, data):
    """
    根据 googlescholar_id 更新 SQLite 数据库中的 email 信息。
    :param db_path: SQLite 数据库文件路径
    :param data: 包含 Excel 数据的字典列表
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 检查表和列是否存在
        table_name = "google_scholar_profiles"  # 替换为实际的表名
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        if "googlescholar_id" not in columns or "email" not in columns:
            raise ValueError("数据库表中缺少 'googlescholar_id' 或 'email' 列")

        # 遍历数据并更新数据库
        for row in data:
            scholar_id = row.get("googlescholar_id")
            email = row.get("Email")
            if scholar_id and email:
                cursor.execute(f"""
                    UPDATE {table_name}
                    SET email = ?
                    WHERE googlescholar_id = ?
                """, (email, scholar_id))
        conn.commit()
        print("数据库更新完成")
    except Exception as e:
        print(f"更新数据库失败: {e}")
    finally:
        conn.close()

def main():
    # 定义命令行参数
    parser = argparse.ArgumentParser(description="读取 Excel 文件并更新 SQLite 数据库")
    parser.add_argument("--excel_path", "-e",  required=True, type=str, help="Excel 文件路径")
    parser.add_argument("--db_path", "-d" ,required=True, type=str, help="SQLite 数据库文件路径")
    args = parser.parse_args()
    # args.excel_path = '/Users/lzg/cli_soft/0_start_script/T-IFS-18807-2024_Proof_hi.xlsx'
    # args.db_path = '/Users/lzg/0_lzgData/2_Personal/220_othersTools/tools/findReviewer/useDerison/scholar_data1.db'
    excel_path = args.excel_path
    db_path = args.db_path

    # 检查文件是否存在
    if not os.path.exists(excel_path):
        print(f"错误: Excel 文件 '{excel_path}' 不存在")
        return
    if not os.path.exists(db_path):
        print(f"错误: SQLite 数据库文件 '{db_path}' 不存在")
        return

    # 读取 Excel 文件数据
    try:
        data = read_excel_file(excel_path)
        print(f"成功读取 Excel 文件，找到 {len(data)} 条记录")
    except Exception as e:
        print(f"读取 Excel 文件失败: {e}")
        return

    # 更新数据库
    try:
        update_email_in_db(db_path, data)
    except Exception as e:
        print(f"更新数据库失败: {e}")

if __name__ == "__main__":
    main()