# -*- coding: utf-8 -*-
# @Time    : 11/15/24
# @Author  : lzg
# @Site    :
# @File    : scholar_search.py
# @Software: PyCharm
import shutil
from typing import List
from DrissionPage import Chromium

import argparse
from dataStructure import FullAuthorInfo
import os
from captchaHandler import CaptchaHandler
from dataHandler import filter_authors_by_position
from databaseHandler import insert_data,fetch_scholar_data
from pageHandler import extract_author_info_from_key_page, click_next_page_buttom
from keywordHandler import process_keywords,get_keywords_as_list
from excelHandler import append_to_excel


def runFindReviewerFromKeyword(Chromium,keyword_file, output_path=None, output_file=None, sleep_time=1000,debug=False):
    """
    主函数：从keyword文件中读取关键字列表，使用 Google Scholar 进行搜索，提取作者信息并保存到 Excel 文件。

    参数：

        output_path (str): 输出目录路径，默认是当前工作目录。
        output_file (str): 输出 Excel 文件名，默认格式为 output_<时间戳>.xlsx。
        sleep_time (int): 每次请求之间的等待时间（单位：毫秒秒），默认值为 500 毫秒 （0.5s）。

    流程：
    1. 初始化 Chromium 和验证码处理器。
    2. 加载引用文件并逐条处理。
    3. 在 Google Scholar 中搜索引用，提取作者信息。
    4. 根据条件筛选目标作者并保存到 Excel 文件。
    """
    print(os.path.abspath(output_file))

    # 初始化 Chromium 和验证码处理器
    print(">>> 初始化 Chromium 和验证码处理器...")
    chromium = Chromium
    # print(chromium)
    captcha_handler = CaptchaHandler(chromium)
    # copy the citation to temp file

    temp_keyword_file = "temp_keyword.txt"
    # 复制文件到临时文件
    shutil.copy(keyword_file, temp_keyword_file)

    print(f"文件已复制到 {os.path.abspath(temp_keyword_file)}")


    # 清理keyword文件
    print(f">>> 清理keyword文件: {os.path.abspath(temp_keyword_file)}")
    process_keywords(keyword_file,temp_keyword_file)

    # 读取keyword文件
    print(f">>> 从keyword文件 {temp_keyword_file} 中加载keyword列表...")
    keyword_list = get_keywords_as_list(temp_keyword_file)
    print(f"共加载 {len(keyword_list)} 条keyword。")

    # 处理，一页，遍历引用并处理，最后有就翻页，没有就换下一个keyword
    for idx, keyword in enumerate(keyword_list, start=1):
        print(f">>> 处理第 {idx} 条keyword: {keyword}")
        net_url= f"https://scholar.google.com/citations?hl=zh-CN&view_op=search_authors&mauthors=label:{keyword}"
        # 打开 Google Scholar 并处理验证码
        print(">>> 打开 Google Scholar 并处理验证码...")
        tab = chromium.latest_tab
        tab.get(net_url)
        # time.sleep(sleep_time)
        # Google Scholar 搜索
        # print(">>> 在 Google Scholar 中搜索引用...")
        captcha_handler.handle_captcha()
        have_next_page = True
        while have_next_page:
            # ----新逻辑了
            fullAuthorInfo_list: List[FullAuthorInfo]= extract_author_info_from_key_page(tab.html)
            fullAuthorInfo_list_after_db_result_list = []
            # todo: 根据googlescholar_id 更新或新增插入数据库
            # 根据googlescholar_id 更新或新增插入数据库
            # 处理这一页的author
            for fullAuthorInfo in fullAuthorInfo_list:
                print(f">>> 检索现有数据库 googlescholar id: {fullAuthorInfo['googlescholar_id']}...")
                author_info_from_database = fetch_scholar_data(fullAuthorInfo['googlescholar_id'])
                if author_info_from_database['googlescholar_id'] == fullAuthorInfo['googlescholar_id']:
                    print(f">>> 数据库中提取到作者信息...")
                    # 使用数据库信息
                    fullAuthorInfo_list_after_db_result_list.append(author_info_from_database)
                    continue
                else:
                    print(f">>> 未在数据库中找到作者信息，插入数据...")
                    fullAuthorInfo_list_after_db_result_list.append(fullAuthorInfo)
                    insert_data(fullAuthorInfo)


            # 有符合的就写入excel文件
            find_reviewer_list = filter_authors_by_position(fullAuthorInfo_list_after_db_result_list)
            for find_one in find_reviewer_list:
                google_scholar_author_url_prefix = 'https://scholar.google.com'
                find_one['href'] = google_scholar_author_url_prefix + find_one['href']
            if find_reviewer_list:
                print(f">>> 存在符合，保存到 Excel 文件: {os.path.abspath(output_path)}")
                append_to_excel(find_reviewer_list, output_path, output_file)
            # 翻页
            print(">>> 翻页...")
            # 点击下一页
            last_tab_url = tab.url
            have_next_page = click_next_page_buttom(tab) and last_tab_url != tab.url


        if debug:
            print(">>> 调试模式：保留temp文件")
            # chromium.quit()
        else:
            print(">>> 删除temp文件")
            os.remove(temp_keyword_file)
            print(">>> 结束keyword处理。")

            # chromium.quit()

def main():
    # 初始化 ArgumentParser
    parser = argparse.ArgumentParser(description="Google Scholar Citation and Author Extraction")

    # 添加命令行参数
    parser.add_argument(
         '-k','--keyword_file',
        type=str,
        required=True,
        help="包含关键字的文件路径，关键字之间逗号分割。"
    )
    parser.add_argument(
        '-o','--output_path' ,
        type=str,
        default=os.getcwd(),
        help="输出目录路径，默认是当前工作目录。"
    )
    parser.add_argument(
        '-f','--output_file',
        type=str,
        default=None,
        help="输出 Excel 文件名，默认格式为 output_<时间戳>.xlsx。"
    )
    parser.add_argument(
        '-st','--sleep_time',
        type=int,
        default=1000,
        help="每次请求之间的等待时间（单位：毫秒），默认值为 1000 毫秒（1 秒）。"
    )
    parser.add_argument(
        '-d','--debug',
        action='store_true',
        help="启用调试模式，显示更多日志信息。"
    )

    # 解析命令行参数
    args = parser.parse_args()

    # 确保关键字文件存在
    if not os.path.exists(args.keyword_file):
        print(f"错误：关键字文件 {args.keyword_file} 不存在！")
        return

    # 打印参数信息
    print(">>> 启动程序，参数如下：")
    print(f"关键字文件: {args.keyword_file}")
    print(f"输出路径: {args.output_path}")
    print(f"输出文件名: {args.output_file}")
    print(f"请求间隔: {args.sleep_time} 毫秒")
    print(f"调试模式: {'启用' if args.debug else '禁用'}")

    # 初始化 Chromium 对象
    print(">>> 初始化 Chromium...")
    chromium = Chromium()

    # 调用主函数
    runFindReviewerFromKeyword(
        Chromium=chromium,
        keyword_file=args.keyword_file,
        output_path=args.output_path,
        output_file=args.output_file,
        sleep_time=args.sleep_time,
        debug=args.debug
    )


if __name__ == "__main__":
    main()
