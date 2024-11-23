# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/22/24 20:17
# @Author  : lzg
# @Site    : 
# @File    : onlyFilteredResultExcel.py
# @Software: PyCharm
import argparse
import os
import sys

from runFindReviewer import read_excel_file, read_school_file, filter_affiliation_by_school, write_results_to_excel
file_path = '/Users/lzg/0_lzgData/2_Personal/220_othersTools/tools/findReviewer/useDerison/'
file_name = 'output_20241122_200345.xlsx'
filter_school_file = '/Users/lzg/0_lzgData/2_Personal/220_othersTools/tools/findReviewer/useDerison/qs_top_50_universities.txt'



if __name__ == "__main__":
    # 定义命令行参数
    parser = argparse.ArgumentParser(description="Filter affiliations based on school list.")
    parser.add_argument(
        "--excel_path", "-e",
        required=True,
        type=str,
        help="Path to the Excel file."
    )
    parser.add_argument(
        "--filter_school_file", "-f",
        required=True,
        type=str,
        help="Path to the filter school file."
    )


    # 解析命令行参数
    args = parser.parse_args()
    excel_path = args.excel_path
    filter_school_file = args.filter_school_file
    # 拆解为目录路径和文件名
    directory_path = os.path.dirname(excel_path)
    file_name = os.path.basename(excel_path)

    # print("目录路径:", directory_path)  # 输出: /Users/username/Documents
    # print("文件名:", file_name)  # 输出: example.txt

    # 检查文件是否存在
    if not os.path.exists(excel_path):
        print(f"Error: Excel file '{excel_path}' does not exist.")
        sys.exit(1)
    if not os.path.exists(filter_school_file):
        print(f"Error: Filter school file '{filter_school_file}' does not exist.")
        sys.exit(1)

    # 读取 Excel 和过滤文件，进行过滤
    try:
        filtered_results, excluded_results = filter_affiliation_by_school(read_excel_file(directory_path, file_name),
                                                                          read_school_file(filter_school_file))
        write_results_to_excel(directory_path, file_name, filtered_results, excluded_results)

        # 写入结果
        print("Processing completed successfully.")
    except Exception as e:
        print(f"Error during processing: {e}")
