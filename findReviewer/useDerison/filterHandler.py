# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/24 13:34
# @Author  : lzg
# @Site    : 
# @File    : filterHandler.py.py
# @Software: PyCharm
import os

import pandas as pd
from pathlib import Path



def write_results_to_excel(original_excel_path, original_excel_name, filtered_results, excluded_results):
    """
    将过滤后的结果和被过滤的信息分别写入原Excel文件的两个sheet中：
    - filtered_results 覆盖写入第一个sheet
    - excluded_results 写入第二个sheet

    :param original_excel_path: 原始Excel文件路径
    :param original_excel_name: 原始Excel文件名
    :param filtered_results: 过滤后的结果（列表）
    :param excluded_results: 被过滤的信息（列表）
    """
    try:
        # 转换结果为 DataFrame
        filtered_df = pd.DataFrame(filtered_results)
        excluded_df = pd.DataFrame(excluded_results)

        # 构造文件路径
        output_path = Path(original_excel_path, original_excel_name)

        # 写入 Excel 文件的两个 sheet
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            filtered_df.to_excel(writer, index=False, sheet_name="Filtered Results")
            excluded_df.to_excel(writer, index=False, sheet_name="Excluded Results")

        print(f"数据已成功写入 {output_path}")
    except Exception as e:
        print(f"写入Excel文件时出错: {e}")

def filter_affiliation_by_school(data, school_dict):
    """
    筛选 read_excel_file 结果中 Affiliation 包含任意学校全称或简称的记录。

    :param data: 从 read_excel_file 返回的字典列表
    :param school_dict: 从 read_school_file 返回的字典，包含全称和简称列表
    :return: (filtered_results, excluded_results)
        - filtered_results: 满足条件的记录列表
        - excluded_results: 不满足条件的记录列表
    """
    filtered_results = []
    excluded_results = []

    # 提取学校全称和简称列表
    full_names = set(school_dict.get("full_name", []))
    short_names = set(school_dict.get("short_name", []))

    # 遍历 data 进行筛选
    for record in data:
        affiliation = record.get("Affiliation", "")
        if any(school in affiliation for school in full_names | short_names):
            filtered_results.append(record)
        else:
            excluded_results.append(record)

    return filtered_results, excluded_results


def read_school_file(file_path):
    """
    读取txt文件内容，返回字典形式。
    文件内容格式为每行一个单位，第一个是学校全称，第二个是简称，使用“逗号”分割。

    :param file_path: txt文件路径
    :return: 字典 {full_name: [所有的全称], short_name: [所有的简称]}
    """
    result = {"full_name": [], "short_name": []}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 去掉每行的换行符并按逗号分割
                parts = line.strip().split(',')
                # 检查是否包含两个部分，且都不为空
                if len(parts) == 2 and parts[0].strip() and parts[1].strip():
                    result["full_name"].append(parts[0].strip())
                    result["short_name"].append(parts[1].strip())
    except Exception as e:
        print(f"读取文件时出错: {e}")

    return result


def read_excel_file(path, filename):
    """
    从路径和文件名指定的Excel文件中读取内容，文件包含以下标题：
    googlescholar_id, Name, Affiliation, Email, Choice Reason, Google Scholar Home Page

    :param path: 文件所在的目录路径
    :param filename: 文件名
    :return: 包含每行数据的字典列表 [{标题: 值, ...}, ...]
    """
    result = []
    try:
        # 拼接路径和文件名
        file_path = Path(path) / filename

        # 读取Excel文件
        df = pd.read_excel(file_path)

        # 检查文件是否为空
        if df.empty:
            print("Excel文件为空")
            return []

        # 必要列校验
        required_columns = [
            "googlescholar_id", "Name", "Affiliation",
            "Email", "Choice Reason", "Google Scholar Home Page"
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"缺少必要的列: {', '.join(missing_columns)}")

        # 转换为字典列表
        result = df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"文件路径无效: {path}/{filename}")
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        raise
    return result