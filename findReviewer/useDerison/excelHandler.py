# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/24 13:14
# @Author  : lzg
# @Site    : 
# @File    : excelHandler.py
# @Software: PyCharm
import os
import pandas as pd
def ensure_excel_file_with_headers(file_path, file_name):
    """
    检测 Excel 文件是否存在，如果不存在则创建一个包含指定标题的空文件。

    参数:
        file_path (str): 文件存放的路径。
        file_name (str): Excel 文件的文件名，可以不包括后缀。
    """
    # 定义所需的标题
    required_columns = ["googlescholar_id","Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"]

    # 如果文件名不包括后缀，自动添加 .xlsx
    if not file_name.endswith('.xlsx'):
        file_name += '.xlsx'

    # 构建完整的文件路径
    full_path = os.path.join(file_path, file_name)

    # 检测文件是否存在
    if not os.path.exists(full_path):
        # 如果文件不存在，创建一个空的 DataFrame 并保存为 Excel 文件
        df = pd.DataFrame(columns=required_columns)
        os.makedirs(file_path, exist_ok=True)  # 确保目录存在
        df.to_excel(full_path, index=False)
        print(f"File created: {full_path}")
    else:
        # 如果文件存在，检查标题是否正确
        try:
            existing_data = pd.read_excel(full_path)
            if list(existing_data.columns) != required_columns:
                # 标题不匹配时，覆盖文件以确保标题正确
                df = pd.DataFrame(columns=required_columns)
                df.to_excel(full_path, index=False)
                print(f"File updated with correct headers: {full_path}")
            else:
                print(f"File already exists and headers are correct: {full_path}")
        except Exception as e:
            # 如果读取文件失败，重新创建文件
            print(f"Error reading the file. Re-creating: {full_path}. Error: {e}")
            df = pd.DataFrame(columns=required_columns)
            df.to_excel(full_path, index=False)


def append_to_excel(target_result, file_path, file_name):
    """
    将目标列表数据续写到已存在的 Excel 文件中。

    参数:
        target_result (list): 要追加的数据列表。
        file_path (str): 文件存放的路径。
        file_name (str): Excel 文件的文件名，可以不包括后缀。
    """
    # 如果文件名没有后缀，自动添加 .xlsx
    if not file_name.endswith('.xlsx'):
        file_name += '.xlsx'

    # 构建完整的文件路径
    full_path = os.path.join(file_path, file_name)
    print(os.path.abspath(full_path))
    # 如果文件不存在，则调用 ensure_excel_file_with_headers 创建文件
    if not os.path.exists(full_path):
        ensure_excel_file_with_headers(file_path, file_name)

    # 定义标准的列标题
    required_columns = ["googlescholar_id","Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"]

    # 读取现有的 Excel 文件
    try:
        existing_data = pd.read_excel(full_path)
        # 确保列标题一致
        if list(existing_data.columns) != required_columns:
            existing_data = pd.DataFrame(columns=required_columns)
    except Exception as e:
        # 如果读取失败，重新初始化 DataFrame
        print(f"Error reading the file. Resetting: {full_path}. Error: {e}")
        existing_data = pd.DataFrame(columns=required_columns)

    # 准备要追加的新数据
    new_data = []
    for item in target_result:
        googlescholar_id = item.get('googlescholar_id', '')
        name = item.get('profile_info', {}).get('full_name', '') or item.get('name', '')
        affiliation = item.get('profile_info', {}).get('affiliation', '') or item.get('affiliation', '')
        choice_reason = item.get('profile_info', {}).get('position', '') or item.get('position', '')
        email = item.get('email', '') or ''
        href = item.get('href', '')
        new_data.append({
            "googlescholar_id": googlescholar_id,
            "Name": name,
            "Affiliation": affiliation,
            "Email": email,
            "Choice Reason": choice_reason,
            "Google Scholar Home Page": href,
        })

    # 将新数据转换为 DataFrame 并追加到现有数据
    new_data_df = pd.DataFrame(new_data, columns=required_columns)
    updated_data = pd.concat([existing_data, new_data_df], ignore_index=True)

    # 保存更新后的数据到文件
    updated_data.to_excel(full_path, index=False)
    return full_path

def read_unique_googlescholar_id_from_excel(file_path, file_name, sheet_name=None):
    """
    从目标 Excel 文件中读取 'googlescholar_id' 列的所有数据并去重。

    参数:
        file_path (str): 文件夹路径。
        file_name (str): 文件名。
        sheet_name (int or str): 要读取的工作表名或索引，默认为第一个工作表。

    返回:
        list: 去重后的 'googlescholar_id' 列数据列表。
    """
    try:
        # 如果文件名没有后缀，自动添加 .xlsx
        if not file_name.endswith('.xlsx'):
            file_name += '.xlsx'

        # 合并文件路径
        full_path = os.path.join(file_path, file_name)

        # 读取 Excel 文件
        df = pd.read_excel(full_path, sheet_name=sheet_name)
        unique_names =[]

        for sheet in df:
            # 检查是否存在 `Name` 列
            if 'googlescholar_id' not in df[sheet].columns:
                raise ValueError("Excel 文件中未找到 `googlescholar_id` 列。")

            unique_names.extend(df[sheet]['googlescholar_id'].dropna().unique())

        # 转为列表返回
        return unique_names
    except Exception as e:
        print(f"读取 Excel 文件时发生错误: {e}")
        return []

