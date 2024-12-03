# -*- coding: utf-8 -*-
# @Time    : 11/15/24
# @Author  : lzg
# @Site    :
# @File    : scholar_search.py
# @Software: PyCharm
import shutil

import json
import sys
import argparse
import time

from DrissionPage import Chromium
from datetime import datetime
from bs4 import BeautifulSoup
import os
import pandas as pd
from captchaHandler import CaptchaHandler
from citaionHandler import clean_references,read_references
from databaseHandler import initialize_database, insert_data,fetch_scholar_data
from filterHandler import write_results_to_excel,filter_affiliation_by_school,read_school_file,read_excel_file
from pageHandler import scholar_search,extract_authors_info,extract_profile_info,extract_first_gs_ri_names_ids_hrefs
from logoHandler import print_logo
from excelHandler import read_unique_googlescholar_id_from_excel,ensure_excel_file_with_headers,append_to_excel
from dataHander import filter_professors

def main(citations_file,filter_school_file, output_path=None, output_file=None, sleep_time=1000, max_reviewers=12):
    """
    主函数：从引用文件中读取引用列表，使用 Google Scholar 进行搜索，提取作者信息并保存到 Excel 文件。

    参数：
        citations_file (str): 引用文件路径，文件中每行包含一个引用。
        filter_school_file (str): 学校过滤文件路径，文件中每行包含一个学校全称和简称。
        output_path (str): 输出目录路径，默认是当前工作目录。
        output_file (str): 输出 Excel 文件名，默认格式为 output_<时间戳>.xlsx。
        sleep_time (int): 每次请求之间的等待时间（单位：毫秒秒），默认值为 500 毫秒 （0.5s）。
        max_reviewers (int): 从这个列表中找最大审稿人数，默认为 12。

    流程：
    1. 初始化 Chromium 和验证码处理器。
    2. 加载引用文件并逐条处理。
    3. 在 Google Scholar 中搜索引用，提取作者信息。
    4. 根据条件筛选目标作者并保存到 Excel 文件。
    """
    # 打印程序 Logo
    print_logo()
    print(">>> 欢迎使用 Google Scholar 引用和作者信息提取程序！")
    time.sleep(3)

    print(">>> 初始化程序...")
    # 初始化数据库
    print(">>> 初始化数据库...")
    initialize_database()
    # 获取当前日期和时间
    current_time = datetime.now()
    file_path = output_path or os.getcwd()
    file_name = output_file or f"output_{current_time.strftime('%Y%m%d_%H%M%S')}.xlsx"
    print(f"当前时间: {current_time}, 新建excel文件在: {file_path}/{file_name}")
    ensure_excel_file_with_headers(file_path, file_name)

    # 初始化 Chromium 和验证码处理器
    print(">>> 初始化 Chromium 和验证码处理器...")
    chromium = Chromium()
    # print(chromium)
    captcha_handler = CaptchaHandler(chromium)
    # copy the citation to temp file

    destination_file = "temp_citaions.txt"
    # 复制文件到临时文件
    shutil.copy(citations_file, destination_file)

    print(f"文件已复制到 {os.path.abspath(destination_file)}")


    # 清理引用文件
    print(f">>> 清理引用文件: {destination_file}")
    clean_references(destination_file)

    # 读取引用文件
    print(f">>> 从引用文件 {destination_file} 中加载引用列表...")
    citations = read_references(destination_file)
    print(f"共加载 {len(citations)} 条引用。")

    # 遍历引用并处理
    for idx, citation in enumerate(citations, start=1):
        print(f">>> 处理第 {idx} 条引用: {citation}")
        # 打开 Google Scholar 并处理验证码
        print(">>> 打开 Google Scholar 并处理验证码...")
        tab = chromium.latest_tab
        tab.get('https://scholar.google.com/scholar?hl=zh-CN')
        # time.sleep(sleep_time)
        # Google Scholar 搜索
        print(">>> 在 Google Scholar 中搜索引用...")
        captcha_handler.handle_captcha()
        tab = scholar_search(tab, citation)
        # tab.wait(sleep_time)
        captcha_handler.handle_captcha()


        # 提取作者和引用信息
        print(">>> 提取搜索结果中的作者和引用信息...")
        result = extract_first_gs_ri_names_ids_hrefs(tab.html)
        full_result = result

        google_scholar_author_url_prefix = 'https://scholar.google.com'

        # 访问作者页面并提取信息
        for author_idx, author in enumerate(result, start=1):

            print(f">>> 检索现有数据库 googlescholar id: {author['googlescholar_id']}...")

            author_info_from_database = fetch_scholar_data(author['googlescholar_id'])
            if author_info_from_database['googlescholar_id'] == author['googlescholar_id']:
                print(f">>> 从数据库中提取到作者信息...")
                author_url = google_scholar_author_url_prefix + author['href']
                full_result[author_idx - 1]['href'] = author_url
                full_result[author_idx - 1]['profile_info'] = author_info_from_database
                continue
            else:
                print(f">>> 未在数据库中找到作者信息，继续提取...")
                print(f">>> 访问第 {author_idx} 位作者页面: {author['href']}")
                author_url = google_scholar_author_url_prefix + author['href']
                author['href'] = author_url
                tab.get(author_url)
                captcha_handler.handle_captcha()
                tab.wait(sleep_time/1000, sleep_time/500)
                print(f">>> 提取作者信息...")
                profile_info = extract_profile_info(tab.html)
                full_result[author_idx-1]['profile_info'] = profile_info
                print(f">>> 将作者信息插入数据库中...")
                insert_data(full_result[author_idx-1])
        # 筛选目标作者

        print(">>> 筛选符合条件的作者...")
        target_authors = filter_professors(full_result)
        field_target_authors = target_authors
        if len(target_authors) > 0:
            print(f"找到符合的作者，执行去重操作...")
            # sheet 1
            current_excel_names = read_unique_googlescholar_id_from_excel(file_path, file_name)
            # current_excel_names.append(excluded_excel_names)
            for target_author in target_authors:
                if target_author['googlescholar_id'] in current_excel_names:
                    print(f"发现重复作者: {target_author['name']}，跳过...")
                    field_target_authors.remove(target_author)
            # 保存到 Excel 文件
            print(f">>> 将结果保存到 Excel 文件: {file_name}")
            append_to_excel(field_target_authors, file_path, file_name)
            filter_reviewer =  len(read_unique_googlescholar_id_from_excel(file_path, file_name))
            if max_reviewers < filter_reviewer :
                print(f"当前查看到第 {idx} 条引用，程序结束！")
                print(f"已经找到{len(field_target_authors)} 位符合条件的作者，程序结束！")
                # print(f">>> 任务完成---》已经写入到excel文件： {os.path.abspath(path=file_name)}")
                print(">>> 目标人数达到，处理完成，程序结束！")
                break



    print(f"执行学校过滤...")
    filtered_results, excluded_results = filter_affiliation_by_school(read_excel_file(file_path, file_name), read_school_file(filter_school_file))
    write_results_to_excel(file_path,file_name,filtered_results,excluded_results)
    # print(f">>> 任务完成---》已经写入到excel文件： {os.path.abspath(path=file_path)}")
    print(">>> 所有引用处理完成，程序结束！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Scholar Citation and Author Extraction")
    parser.add_argument(
        '--citations_file', '-c',
        type=str,
        help="Path to the citations text file containing one citation per line."
    )
    parser.add_argument(
        '--filter_school_file', '-fs',
        type=str,
        help="Path to the filter school file text file containing one school  per line which is  full name , short name."
    )
    parser.add_argument(
        '--output_path', '-o',
        type=str,
        help="Path to the output directory (default: current working directory)."
    )
    parser.add_argument(
        '--output_file', '-f',
        type=str,
        help="Name of the output Excel file (default: output_<current_time>.xlsx)."
    )
    parser.add_argument(
        '--sleep_time', '-s',
        type=int,
        default=500,
        help="Sleep time in milliseconds seconds between requests (default: 1000 milliseconds seconds （1s))."
    )
    parser.add_argument(
        '--max_reviewers', '-m',
        type=int,
        help="set the max reviewers to find (default: 12)."
    )
    # 如果没有传入参数，显示帮助并退出
    # args = parser.parse_args()
    # if not any(vars(args).values()):  # 检查是否传入了任何参数
    #     parser.print_help()
    #     sys.exit(1)
    #
    # # 如果传递了参数，则运行主逻辑
    # if args.citations_file:
    #     main(args.citations_file, args.output_path, args.output_file, args.sleep_time)
    # else:
    #     # 如果没有提供 citations_file，显示帮助信息并退出
    #     print("Error: --citations_file (-c) is required.")
    #     print("------------------------------------------\n")
    #
    #     parser.print_help()
    #     sys.exit(1)

    args = parser.parse_args()

    if args.citations_file:
        # 如果命令行传递参数，使用参数运行
        main(args.citations_file,args.filter_school_file, args.output_path, args.output_file, args.sleep_time)
    else:
        # 如果没有命令行参数，使用默认路径和文件名，适合直接在 PyCharm 点击运行
        print("未检测到命令行参数，使用默认设置运行...")
        default_citations_file = "citations.txt"  # 默认引用文件路径
        default_school_file = "qs_top_50_universities.txt"  # 默认学校过滤文件路径
        default_output_path = os.getcwd()        # 默认输出路径
        main(default_citations_file,default_school_file, default_output_path)
