# -*- coding: utf-8 -*-
# @Time    : 11/15/24
# @Author  : lzg
# @Site    :
# @File    : scholar_search.py
# @Software: PyCharm

import json
import sys
import argparse
import time

from DrissionPage import Chromium
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import os
from captchaHandler import CaptchaHandler
from citaionHandler import clean_references
from databaseHandler import initialize_database, insert_data,fetch_scholar_data
from pyfiglet import figlet_format
from filterHandler import write_results_to_excel,filter_affiliation_by_school,read_school_file,read_excel_file


def read_unique_names_from_excel(file_path, file_name, sheet_name=0):
    """
    从目标 Excel 文件中读取 `Name` 列的所有数据并去重。

    参数:
        file_path (str): 文件夹路径。
        file_name (str): 文件名。
        sheet_name (int or str): 要读取的工作表名或索引，默认为第一个工作表。

    返回:
        list: 去重后的 Name 列数据列表。
    """
    try:
        # 如果文件名没有后缀，自动添加 .xlsx
        if not file_name.endswith('.xlsx'):
            file_name += '.xlsx'

        # 合并文件路径
        full_path = os.path.join(file_path, file_name)

        # 读取 Excel 文件
        df = pd.read_excel(full_path, sheet_name=sheet_name)

        # 检查是否存在 `Name` 列
        if 'Name' not in df.columns:
            raise ValueError("Excel 文件中未找到 `Name` 列。")

        # 获取 `Name` 列并去重
        unique_names = df['Name'].dropna().unique()

        # 转为列表返回
        return unique_names.tolist()
    except Exception as e:
        print(f"读取 Excel 文件时发生错误: {e}")
        return []

def print_logo():
    """
    打印程序的 Logo
    """
    print("--------------------\n")
    print(figlet_format("L Z G", font="doh"))
    print("--------------------\n")


def read_references(file_path):
    """
    读取文件中的每行内容，并将其存储为列表返回。

    :param file_path: str, 文件路径
    :return: list, 每行作为一个列表元素
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            references = [line.strip() for line in file if line.strip()]
        return references
    except FileNotFoundError:
        print(f"错误: 文件 '{os.path.abspath(file_path)}' 未找到！")
        return []
    except Exception as e:
        print(f"发生错误: {e}")
        return []



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
        name = item.get('profile_info', {}).get('full_name', '')
        affiliation = item.get('profile_info', {}).get('affiliation', '')
        choice_reason = item.get('profile_info', {}).get('position', '')
        href = item.get('href', '')
        new_data.append({
            "googlescholar_id": googlescholar_id,
            "Name": name,
            "Affiliation": affiliation,
            "Email": "",
            "Choice Reason": choice_reason,
            "Google Scholar Home Page": href,
        })

    # 将新数据转换为 DataFrame 并追加到现有数据
    new_data_df = pd.DataFrame(new_data, columns=required_columns)
    updated_data = pd.concat([existing_data, new_data_df], ignore_index=True)

    # 保存更新后的数据到文件
    updated_data.to_excel(full_path, index=False)
    return full_path
# 筛选函数
def filter_professors(data):
    """
    过滤出满足特定职位条件的人员数据。

    此函数遍历输入的人员数据列表，根据每个人的 `profile_info` 中的 `position` 字段内容，
    筛选出职位包含 "Assistant Professor" 或 "Associate Professor" 或"Postdoctoral"（大小写不敏感匹配）的人，
    并将这些人员的数据保存在新的列表中返回。

    参数:
        data (list): 一个包含人员数据的列表，每个元素是一个字典，
                     必须包含 `profile_info` 键，且其值是一个字典，
                     包含 `position` 键描述职位信息。

    返回:
        list: 一个包含符合条件的人员数据的新列表，保留原数据结构。

    示例:
        输入:
            data = [
                {'name': 'T Sharma', 'profile_info': {'position': 'Assistant Professor, Penn State University'}},
                {'name': 'Y Potter', 'profile_info': {'position': 'UC Berkeley'}},
                {'name': 'K Pongmala', 'profile_info': {'position': 'Associate Professor, UC Berkeley'}}
            ]
        调用:
            result = filter_professors(data)
        输出:
            [
                {'name': 'T Sharma', 'profile_info': {'position': 'Assistant Professor, Penn State University'}},
                {'name': 'K Pongmala', 'profile_info': {'position': 'Associate Professor, UC Berkeley'}}
            ]
    """
    filtered_list = []
    for item in data:
        # 安全获取每个人的 profile_info 信息
        profile_info = item.get('profile_info', {})

        # 安全获取职位信息并转换为小写以支持大小写不敏感匹配
        position = profile_info.get('position', '').lower()

        # 检查职位中是否包含目标关键词
        # if 'assistant professor' in position or 'associate professor'  in position or 'postdoctoral' in position:
        if 'assistant professor' in position or 'postdoctoral' in position:
            # 如果匹配成功，将整个数据项添加到结果列表中
            filtered_list.append(item)

    # 返回筛选后的列表
    return filtered_list


def extract_profile_info(html_str):
    """
    从HTML字符串中提取Google Scholar个人档案的相关信息。

    参数:
        html_str (str): HTML字符串。

    返回:
        dict: 包含以下信息的字典：
            - full_name: 全名
            - position: 职位
            - googlescholar_id: Google Scholar ID
            - affiliation: 隶属单位（文字）
            - affiliation_link: 隶属单位的链接（如果存在）
            - homepage: 首页链接及文字（如果存在），格式为 {"href": 链接, "text": "首页"}
            - keywords: 包含关键字及其链接的列表，每个关键字为字典，格式如下：
                {"name": 关键字, "href": 关键字链接}
    """

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_str, 'html.parser')

    # 初始化结果字典
    profile_info = {
        "full_name": None,
        "position": None,
        "googlescholar_id": None,
        "affiliation": None,
        "affiliation_link": None,
        "homepage": None,
        "keywords": []
    }

    # 提取全名
    full_name_div = soup.find("div", id="gsc_prf_in")
    if full_name_div:
        profile_info["full_name"] = full_name_div.text.strip()



    # 提取职位
    position_div = soup.find("div", class_="gsc_prf_il")
    if position_div and position_div.get("id") != "gsc_prf_ivh":
        profile_info["position"] = position_div.text.strip()

    # 提取隶属单位及链接
    affiliation_div = soup.find("div", id="gsc_prf_i")
    if affiliation_div:
        affiliation_a = affiliation_div.find("a", class_="gsc_prf_ila")
        if affiliation_a:
            profile_info["affiliation"] = affiliation_a.text.strip()
            profile_info["affiliation_link"] = affiliation_a["href"]

    # 提取首页链接及文字
    verification_div = soup.find("div", id="gsc_prf_ivh")
    if verification_div:
        homepage_a = verification_div.find("a", class_="gsc_prf_ila", text="首页")
        if homepage_a:
            profile_info["homepage"] = {
                "href": homepage_a["href"],
                "text": "首页"
            }

    # 提取关键字及链接
    keywords_div = soup.find("div", id="gsc_prf_int")
    if keywords_div:
        for a_tag in keywords_div.find_all("a", href=True):
            keyword_name = a_tag.text.strip()
            keyword_href = a_tag["href"]
            profile_info["keywords"].append({"name": keyword_name, "href": keyword_href})

    return profile_info

def extract_first_gs_ri_names_ids_hrefs(html_str):
    """
    从提供的HTML字符串中提取第一个 class="gs_ri" 块中的第一个 class="gs_a gs_fma_s" 内的所有name, href 和 Google Scholar ID。

    参数:
        html_str (str): HTML字符串

    返回:
        list: 包含字典的列表，每个字典包含 `name`, `href`, 和 `googlescholar_id`
    """
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_str, 'html.parser')

    # 找到第一个 class="gs_ri" 的div
    gs_ri_div = soup.find("div", class_="gs_ri")

    # 初始化结果列表
    result = []

    if gs_ri_div:
        # 找到第一个 class="gs_a gs_fma_s"
        gs_a_fma_s_div = gs_ri_div.find("div", class_="gs_a gs_fma_s")

        if gs_a_fma_s_div:
            # 在找到的块中查找所有的 a 标签
            for a_tag in gs_a_fma_s_div.find_all("a", href=True):
                name = a_tag.text.strip()
                href = a_tag["href"]
                # 尝试提取 Google Scholar ID
                id_param = None
                if "user=" in href:
                    # 提取ID参数
                    href_parts = href.split("user=")
                    id_param = href_parts[1].split("&")[0] if len(href_parts) > 1 else None

                result.append({"name": name, "href": href, "googlescholar_id": id_param})

    return result

def extract_authors_info(tab):
    """提取作者的名称、链接和 Google Scholar ID"""
    authors_info = []

    # 定位到 gs_a gs_fma_s 类的元素
    author_elements = tab.eles('.gs_a.gs_fma_s a')  # 使用 CSS 选择器获取 gs_a 类下的所有 <a> 标签
    print(author_elements)
    for author in author_elements:
        # 提取作者的名称
        name = author.text

        # 提取作者的链接
        href = author.attr('href')

        # 提取 Google Scholar ID
        scholar_id = href.split('user=')[1].split('&')[0] if 'user=' in href else None

        authors_info.append({
            'name': name,
            'href': href,
            'scholar_id': scholar_id
        })

    return authors_info




def scholar_search(tab, query: str):
    """
    在已打开的Google Scholar页面中更改搜索框的值并执行搜索。

    :param tab: Chromium 浏览器的标签页对象
    :param query: 要搜索的关键词
    :return tab: 更新后的标签页对象
    """
    # 使用JavaScript修改搜索框的值并触发事件
    escaped_value = json.dumps(query)  # 转义特殊字符
    js_script = f'''
        let input = document.getElementById("gs_hdr_tsi");
        input.value = {escaped_value};  // 修改值
        input.dispatchEvent(new Event("input"));  // 触发 input 事件
        input.dispatchEvent(new Event("change"));  // 触发 change 事件
    '''
    tab.run_js(js_script)

    # 定位搜索按钮并点击
    search_button = tab.ele('#gs_hdr_tsb')  # 使用CSS选择器定位搜索按钮
    search_button.click()
    return tab


def main(citations_file,filter_school_file, output_path=None, output_file=None, sleep_time=500, max_reviewers=12):
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
    print(chromium)
    captcha_handler = CaptchaHandler(chromium)

    # 清理引用文件
    print(f">>> 清理引用文件: {citations_file}")
    clean_references(citations_file)

    # 读取引用文件
    print(f">>> 从引用文件 {citations_file} 中加载引用列表...")
    citations = read_references(citations_file)
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
                author_info_from_database['href'] = author_url
                full_result[author_idx - 1]['profile_info'] = author_info_from_database
                continue
            else:
                print(f">>> 未在数据库中找到作者信息，继续提取...")
                print(f">>> 访问第 {author_idx} 位作者页面: {author['href']}")
                author_url = google_scholar_author_url_prefix + author['href']
                author['href'] = author_url
                tab.get(author_url)
                captcha_handler.handle_captcha()
                tab.wait(sleep_time/1000)
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
            current_excel_names = read_unique_names_from_excel(file_path, file_name)
            for target_author in target_authors:
                if target_author['name'] in current_excel_names:
                    print(f"发现重复作者: {target_author['name']}，跳过...")
                    field_target_authors.remove(target_author)

            # 保存到 Excel 文件
            print(f">>> 将结果保存到 Excel 文件: {file_name}")
            append_to_excel(field_target_authors, file_path, file_name)
            if max_reviewers == 0:
                print(f"当前查看到第 {idx} 条引用，程序结束！")
                print(f"已经找到{len(field_target_authors)} 位符合条件的作者，程序结束！")
                # print(f">>> 任务完成---》已经写入到excel文件： {os.path.abspath(path=file_name)}")
                print(">>> 目标人数达到，处理完成，程序结束！")
                break
            else:
                max_reviewers -= 1


    print(f"执行学校过滤...")
    filtered_results, excluded_results = filter_affiliation_by_school(read_excel_file(file_path, file_name), read_school_file(filter_school_file))
    write_results_to_excel(file_path,file_name,filtered_results,excluded_results)
    print(f">>> 任务完成---》已经写入到excel文件： {os.path.abspath(path=file_path)}")
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
        help="Sleep time in milliseconds seconds between requests (default: 500 milliseconds seconds （0.5s))."
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
        main(args.citations_file, args.output_path, args.output_file, args.sleep_time)
    else:
        # 如果没有命令行参数，使用默认路径和文件名，适合直接在 PyCharm 点击运行
        print("未检测到命令行参数，使用默认设置运行...")
        default_citations_file = "citations.txt"  # 默认引用文件路径
        default_school_file = "qs_top_50_universities.txt"  # 默认学校过滤文件路径
        default_output_path = os.getcwd()        # 默认输出路径
        main(default_citations_file,default_school_file, default_output_path)
