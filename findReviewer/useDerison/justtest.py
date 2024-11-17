# -*- coding: utf-8 -*-
# @Time    : 11/15/24
# @Author  : lzg
# @Site    :
# @File    : scholar_search.py
# @Software: PyCharm

import json
import time

from DrissionPage import Chromium
from datetime import datetime

from bs4 import BeautifulSoup

import pandas as pd
import os
from captchaHandler import CaptchaHandler


def ensure_excel_file_with_headers(file_path, file_name):
    """
    检测 Excel 文件是否存在，如果不存在则创建一个包含指定标题的空文件。

    参数:
        file_path (str): 文件存放的路径。
        file_name (str): Excel 文件的文件名，可以不包括后缀。
    """
    # 定义所需的标题
    required_columns = ["Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"]

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
    required_columns = ["Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"]

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
        name = item.get('profile_info', {}).get('full_name', '')
        affiliation = item.get('profile_info', {}).get('affiliation', '')
        choice_reason = item.get('profile_info', {}).get('position', '')
        href = item.get('href', '')
        new_data.append({
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
    筛选出职位包含 "Assistant Professor" 或 "Associate Professor"（大小写不敏感匹配）的人，
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
        if 'assistant professor' in position or 'associate professor' in position:
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


if __name__ == "__main__":
    # 所有操作都在latest_tab上进行


    # 获取当前日期和时间
    current_time = datetime.now()
    file_path = os.getcwd()
    file_name = "output_" + str(current_time) + ".xlsx"

    chromium = Chromium()
    # 验证码处理器
    captcha_handler = CaptchaHandler(chromium)
    # 调用 handle_captcha 方法

    tab = chromium.latest_tab
    tab.get('https://scholar.google.com/scholar?hl=zh-CN')
    # 在每一个获取页面后，调用 handle_captcha 方法
    captcha_handler.handle_captcha()

    #todo: 接下来的任务是变为从文件中读取引用列表， 计划包含三个文件，作者txt，引用txt，关键词txt，一行一个。使用chatgpt完成数据读取，然后手动写入的这些txt中。
    # 但我目前想，只需要一个引用txt就可以了，是否需要自动处理关键词和作者，待定。我想的是作者手动处理，然后引用不够，必须使用关键词，也是手动处理。这样就可以了。反正找email也必须手动处理。
    # 我有考虑是否使用steamlit写一个web页面，然后做个交互，不过如果只是我自己使用的话，我想无所谓了。
    citations = ["T. Sharma, Y. Kwon, K. Pongmala, H. Wang, A. Miller, D. Song, and Y. Wang, “Unpacking how decentralized autonomous organizations (daos) work in practice,” arXiv preprint arXiv:2304.09822, 2023."] # 初始化 citations 引用列表

    for citation in citations:
        tab = scholar_search(tab,citation )
        tab.wait(5)
        # 拿到目标结果，提取作者信息
        result = extract_first_gs_ri_names_ids_hrefs(tab.html)
        full_result = result  # 初始化 full_result
        # print(result)
        google_scholar_author_url_prefix = 'https://scholar.google.com'

        for author in full_result:  # 遍历 full_result，而不是 result
            author_url = google_scholar_author_url_prefix + author['href']
            author['href'] = author_url
            tab.get(author_url)
            captcha_handler.handle_captcha()
            tab.wait(5)
            profile_info = extract_profile_info(tab.html)
            author['profile_info'] = profile_info  # 将 profile_info 添加到 author 字典中
            # print(profile_info)

        # print(full_result)  # 最终包含 profile_info 的结果
        # 下一步应该访问作者的 Google Scholar 页面，获取作者的信息，如果符合条件，就是找到目标了嘛。

        target_authors = filter_professors(full_result)
        append_to_excel(target_authors, file_path, file_name)

