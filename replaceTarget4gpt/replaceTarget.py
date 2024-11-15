import re

def replace_brackets(input_string):
    """
    将字符串中的 "\(" 和 "\)" 替换为 "$"，以及 "\[" 和 "\]" 替换为 "$$"。
    
    :param input_string: 输入的中英文字符串
    :return: 替换后的字符串
    """
    # 使用正则表达式进行替换
    replaced_string = re.sub(r'\\\(', r'$', input_string)  # 替换 "\(" 为 "$"
    replaced_string = re.sub(r'\\\)', r'$', replaced_string)  # 替换 "\)" 为 "$"
    replaced_string = re.sub(r'\\\[', r'$$', replaced_string)  # 替换 "\[" 为 "$$"
    replaced_string = re.sub(r'\\\]', r'$$', replaced_string)  # 替换 "\]" 为 "$$"
    return replaced_string

def read_from_file(filename="input.txt"):
    """
    从文件中读取输入字符串。
    
    :param filename: 输入文件名，默认值为 'input.txt'
    :return: 文件内容字符串
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"文件 '{filename}' 未找到。请确保文件存在并重试。")
        return ""

def write_to_file(output_string, filename="output.txt"):
    """
    将输出字符串写入文件。
    
    :param output_string: 替换后的字符串
    :param filename: 输出文件名，默认值为 'output.txt'
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(output_string)

# 从文件读取输入字符串
input_str = read_from_file("input.txt")

# 如果输入不为空，执行替换操作
if input_str:
    output_str = replace_brackets(input_str)
    write_to_file(output_str, "output.txt")
    print("替换后的字符串已写入 'output.txt' 文件。")
else:
    print("未执行任何替换操作。")