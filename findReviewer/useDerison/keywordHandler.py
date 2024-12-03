# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/24 12:20
# @Author  : lzg
# @Site    : 
# @File    : keywordHandler.py
# @Software: PyCharm

def process_keywords(input_file, output_file):
    """
    处理关键词文件，将每个关键词的每个词之间使用"_"连接。

    参数:
    input_file (str): 输入文件路径，包含以逗号分割的关键词。
    output_file (str): 输出文件路径，用于保存处理后的关键词。
    """
    try:
        # 打开输入文件读取内容
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()

        # 按逗号分割关键词
        keywords = content.split(",")

        # 将每个关键词的空格替换为下划线
        processed_keywords = ["_".join(keyword.split()) for keyword in keywords]

        # 将处理后的关键词用逗号重新连接
        result = ",".join(processed_keywords)

        # 将结果写入输出文件
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(result)

        print(f"处理完成，结果已保存到 {output_file}")

    except Exception as e:
        print(f"处理过程中出错: {e}")


def get_keywords_as_list(input_file):
    """
    从文件中读取关键词并返回一个列表。

    参数:
    input_file (str): 输入文件路径，文件内容以逗号分隔关键词。

    返回:
    list: 包含所有关键词的列表。
    """
    try:
        # 打开文件并读取内容
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read().strip()  # 读取并去除首尾空白字符

        # 如果内容为空，直接返回空列表
        if not content:
            return []

        # 分割关键词并返回列表
        keywords = content.split(",")
        return [keyword.strip() for keyword in keywords]  # 去除每个关键词的首尾空格

    except FileNotFoundError:
        print(f"文件 {input_file} 未找到！")
        return []
    except Exception as e:
        print(f"处理文件时发生错误: {e}")
        return []

# # 使用示例
# input_file = "keyword.txt"
# output_file = "processed_keyword.txt"
# process_keywords(input_file, output_file)
