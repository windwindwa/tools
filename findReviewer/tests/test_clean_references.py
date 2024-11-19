# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/24 11:29
# @Author  : lzg
# @Site    : 
# @File    : test_clean_references.py
# @Software: PyCharm
import os
import pytest
from findReviewer.useDerison.citaionHandler import clean_references

@pytest.fixture
def sample_input_file(tmp_path):
    """
    创建一个临时输入文件，用于测试。
    """
    input_file = tmp_path / "raw_references.txt"
    input_file.write_text(
        """
         G. Han, J. Ma, S. Huang, L. Chen, and S.-F. Chang, “Few-shot object detection with fully cross-transformer,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 5321–5330, June 2022.
        [2] A. Liu, J. Guo, J. Wang, S. Liang, R. Tao, W. Zhou, C. Liu, X. Liu, and D. Tao, “X-adv: Physical adversarial object attacks against x-ray prohibited item detection,” in 32st USENIX Security Symposium (USENIX Security 23), 2023.
        [3] Z. Hu, S. Huang, X. Zhu, F. Sun, B. Zhang, and X. Hu, “Adversarial texture for fooling person detectors in the physical world,” in Proceedings of CVPR, 2022.
        """,
        encoding="utf-8",
    )
    return input_file


def test_clean_references_with_output_file(sample_input_file, tmp_path):
    """
    测试 clean_references 函数，当提供输出文件时。
    """
    output_file = tmp_path / "cleaned_references.txt"
    clean_references(input_file=str(sample_input_file), output_file=str(output_file))

    # 验证输出文件是否存在
    assert output_file.exists()

    # 验证输出内容是否正确
    expected_content = (
        "G. Han, J. Ma, S. Huang, L. Chen, and S.-F. Chang, “Few-shot object detection with fully cross-transformer,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 5321–5330, June 2022.\n"
        "A. Liu, J. Guo, J. Wang, S. Liang, R. Tao, W. Zhou, C. Liu, X. Liu, and D. Tao, “X-adv: Physical adversarial object attacks against x-ray prohibited item detection,” in 32st USENIX Security Symposium (USENIX Security 23), 2023.\n"
        "Z. Hu, S. Huang, X. Zhu, F. Sun, B. Zhang, and X. Hu, “Adversarial texture for fooling person detectors in the physical world,” in Proceedings of CVPR, 2022.\n"
    )
    with open(output_file, "r", encoding="utf-8") as f:
        assert f.read() == expected_content


def test_clean_references_overwrite_input_file(sample_input_file):
    """
    测试 clean_references 函数，当未提供输出文件时，是否覆盖输入文件。
    """
    input_file_path = str(sample_input_file)
    clean_references(input_file=input_file_path)

    # 验证输入文件内容是否被正确覆盖
    expected_content = (
        "G. Han, J. Ma, S. Huang, L. Chen, and S.-F. Chang, “Few-shot object detection with fully cross-transformer,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 5321–5330, June 2022.\n"
        "A. Liu, J. Guo, J. Wang, S. Liang, R. Tao, W. Zhou, C. Liu, X. Liu, and D. Tao, “X-adv: Physical adversarial object attacks against x-ray prohibited item detection,” in 32st USENIX Security Symposium (USENIX Security 23), 2023.\n"
        "Z. Hu, S. Huang, X. Zhu, F. Sun, B. Zhang, and X. Hu, “Adversarial texture for fooling person detectors in the physical world,” in Proceedings of CVPR, 2022.\n"
    )
    with open(input_file_path, "r", encoding="utf-8") as f:
        assert f.read() == expected_content
