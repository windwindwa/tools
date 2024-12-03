# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/24 13:12
# @Author  : lzg
# @Site    : 
# @File    : pageHandler.py
# @Software: PyCharm

import json
import time

from bs4 import BeautifulSoup

from bs4 import BeautifulSoup
from typing import List
# from findReviewer.useDerison.dataStructure import FullAuthorInfo, Homepage
from dataStructure import FullAuthorInfo, Homepage
def extract_author_info_from_key_page(html_str: str) -> List[FullAuthorInfo]:
    """
    从 HTML 字符串中提取作者信息并组织到 FullAuthorInfo 数据结构中。

    参数:
    html_str (str): 输入的 HTML 字符串。

    返回:
    List[FullAuthorInfo]: 包含作者信息的列表。
    """
    soup = BeautifulSoup(html_str, 'html.parser')
    authors = []

    # 找到所有符合条件的 <div class="gs_ai gs_scl gs_ai_chpr">
    author_divs = soup.find_all('div', class_='gs_ai gs_scl gs_ai_chpr')

    for div in author_divs:
        # 获取 Google Scholar ID 和个人链接
        profile_link = div.find('a', class_='gs_ai_pho')
        href = profile_link['href'] if profile_link else ''
        googlescholar_id = href.split('user=')[-1] if 'user=' in href else ''

        # 获取作者姓名
        name_div = div.find('h3', class_='gs_ai_name')
        name_link = name_div.find('a') if name_div else None
        name = name_link.text if name_link else ''
        full_name = name  # 假设全名和姓名相同

        # 获取职位和单位
        position = div.find('div', class_='gs_ai_aff').text if div.find('div', class_='gs_ai_aff') else ''
        affiliation = div.find('div', class_='gs_ai_aff').text if div.find('div', class_='gs_ai_aff') else ''
        affiliation_link = ''  # 如果有链接可以在此添加提取逻辑

        # 获取电子邮件验证信息
        # email_div = div.find('div', class_='gs_ai_eml')
        # email = email_div.text.replace('在 ', '').replace(' 的电子邮件经过验证', '') if email_div else ''

        # 获取关键词
        keywords_div = div.find('div', class_='gs_ai_int')
        keywords = [a.text for a in keywords_div.find_all('a')] if keywords_div else []

        # 获取主页信息
        homepage = Homepage(href=href, text=name)

        # 构造 FullAuthorInfo
        author_info = FullAuthorInfo(
            googlescholar_id=googlescholar_id,
            href=href,
            # email=email,
            name=name,
            full_name=full_name,
            position=position,
            affiliation=affiliation,
            affiliation_link=affiliation_link,
            homepage=homepage,
            keywords=keywords
        )

        authors.append(author_info)

    return authors



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


def click_next_page_buttom(tab):
    """
    自动处理分页逻辑，点击“下一页”按钮并处理页面数据。
    :param tab: DrissionPage 对象
    :return: bool: 是否成功点击“下一页”按钮
    """
    # 等待页面加载完成
    tab._wait_loaded()

    # 检查是否存在“下一页”按钮
    # next_page_button = tab.ele('.gsc_pgn_pnx')  # 定位“下一页”按钮
    next_page_button = 'gsc_pgn_pnx' in tab.html
    if next_page_button:
        print("发现下一页按钮，点击...")

        # 通过 JavaScript 模拟点击事件
        js_script = 'document.querySelector(".gsc_pgn_pnx").click();'
        # time.sleep(2)
        # print("等待2s，之后点击下一页按钮")
        tab.run_js(js_script,timeout=5)
        return True
        # 或直接点击按钮（两者选其一）
        # next_page_button.click()
    else:
        print("没有更多页面了。")
        return False


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
    tab._wait_loaded()
    tab.run_js(js_script)

    # 定位搜索按钮并点击
    search_button = tab.ele('#gs_hdr_tsb')  # 使用CSS选择器定位搜索按钮
    search_button.click()
    return tab

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

