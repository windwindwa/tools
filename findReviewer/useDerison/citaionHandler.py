import re


def process_file(input_file, output_file):
    """
    从输入文件中读取内容，去掉所有换行符，并在每个 "[数字]" 前面添加换行符，然后写入到输出文件中。
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 去掉所有换行符
    content = content.replace('\n', '')

    # 在每个 "[数字]" 前面添加换行符
    import re
    content = re.sub(r'(\[\d+\])', r'\n\1', content)

    # 写入到输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)


def clean_references(input_file, output_file=None):
    """
    从输入文件中读取参考文献，去掉编号并写入到输出文件中。

    参数:
        input_file (str): 输入文件路径，包含原始参考文献。
        output_file (str): 输出文件路径，用于保存清理后的参考文献。
                          如果未提供，则覆盖输入文件。
    """
    try:
        # 如果没有提供 output_file，默认覆盖 input_file
        if output_file is None:
            output_file = input_file
        clean_references(input_file, output_file)
        # 从文件读取原始内容
        with open(input_file, "r", encoding="utf-8") as file:
            raw_references = file.readlines()

        # 去掉编号并清理空格
        cleaned_references = [re.sub(r"^\[\d+\]\s*", "", ref.strip()) for ref in raw_references if ref.strip()]

        # 写入清理后的内容到输出文件
        with open(output_file, "w", encoding="utf-8") as file:
            for ref in cleaned_references:
                file.write(ref + "\n")

        print(f"清理后的参考文献已保存到 {output_file}")
    except Exception as e:
        print(f"处理文件时出错: {e}")


# 示例使用
# input_path = "/mnt/data/raw_references.txt"
# clean_references(input_path)  # 默认覆盖输入文件
