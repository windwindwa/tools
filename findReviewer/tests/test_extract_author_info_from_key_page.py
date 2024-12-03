# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/24 13:55
# @Author  : lzg
# @Site    : 
# @File    : test_extract_author_info_from_key_page.py
# @Software: PyCharm
import pytest
from findReviewer.useDerison.pageHandler import extract_author_info_from_key_page  # 替换为实际文件名


@pytest.fixture
def sample_html():
    """
    提供一个 HTML 示例字符串供测试使用。
    """
    return """
    <div class="gs_ai gs_scl gs_ai_chpr">
        <a href="/citations?hl=zh-CN&amp;user=57BFBY0AAAAJ" class="gs_ai_pho">
            <span class="gs_rimg gs_pp_sm">
                <img alt="Matthias Minderer" sizes="56px" 
                src="https://scholar.googleusercontent.com/citations?view_op=small_photo&amp;user=57BFBY0AAAAJ&amp;citpid=1" 
                srcset="https://scholar.googleusercontent.com/citations?view_op=small_photo&amp;user=57BFBY0AAAAJ&amp;citpid=1 56w,
                        https://scholar.googleusercontent.com/citations?view_op=view_photo&amp;user=57BFBY0AAAAJ&amp;citpid=1 128w" 
                width="56" height="56">
            </span>
        </a>
        <div class="gs_ai_t">
            <h3 class="gs_ai_name">
                <a href="/citations?hl=zh-CN&amp;user=57BFBY0AAAAJ">Matthias Minderer</a>
            </h3>
            <div class="gs_ai_aff">Senior Research Scientist, Google DeepMind</div>
            <div class="gs_ai_eml">在 google.com 的电子邮件经过验证</div>
            <div class="gs_ai_cby">被引用次数：53303</div>
            <div class="gs_ai_int">
                <a class="gs_ai_one_int" href="/citations?hl=zh-CN&amp;view_op=search_authors&amp;mauthors=label:representation_learning">Representation learning</a>
                <a class="gs_ai_one_int" href="/citations?hl=zh-CN&amp;view_op=search_authors&amp;mauthors=label:unsupervised_learning">Unsupervised learning</a>
                <a class="gs_ai_one_int" href="/citations?hl=zh-CN&amp;view_op=search_authors&amp;mauthors=label:object_detection">Object detection</a>
                <a class="gs_ai_one_int" href="/citations?hl=zh-CN&amp;view_op=search_authors&amp;mauthors=label:vision_language_models">Vision-language models</a>
            </div>
        </div>
    </div>
    """


def test_extract_author_info_valid_html(sample_html):
    """
    测试从有效 HTML 中提取作者信息。
    """
    authors = extract_author_info_from_key_page(sample_html)

    # 预期结果
    expected_author = {
        'googlescholar_id': '57BFBY0AAAAJ',
        'href': '/citations?hl=zh-CN&user=57BFBY0AAAAJ',
        'email': 'google.com',
        'name': 'Matthias Minderer',
        'full_name': 'Matthias Minderer',
        'position': 'Senior Research Scientist, Google DeepMind',
        'affiliation': 'Senior Research Scientist, Google DeepMind',
        'affiliation_link': '',
        'homepage': {
            'href': '/citations?hl=zh-CN&user=57BFBY0AAAAJ',
            'text': 'Matthias Minderer'
        },
        'keywords': ['Representation learning', 'Unsupervised learning', 'Object detection', 'Vision-language models']
    }

    assert len(authors) == 1, f"Expected 1 author, got {len(authors)}"
    assert authors[0] == expected_author, f"Expected {expected_author}, got {authors[0]}"


def test_extract_author_info_empty_html():
    """
    测试输入空 HTML。
    """
    html_str = ""
    authors = extract_author_info_from_key_page(html_str)
    assert authors == [], "Expected an empty list for empty HTML input."


def test_extract_author_info_no_matching_div():
    """
    测试没有匹配的 <div> 标签时的情况。
    """
    html_str = "<div>No matching author information here.</div>"
    authors = extract_author_info_from_key_page(html_str)
    assert authors == [], "Expected an empty list when no matching div is found."




@pytest.fixture
def sample_html_multiple_authors():
    """
    提供一个包含多个作者信息的 HTML 示例字符串。
    """
    return """
    <div class="gs_ai gs_scl gs_ai_chpr">
        <a href="/citations?hl=zh-CN&amp;user=57BFBY0AAAAJ" class="gs_ai_pho">
            <span class="gs_rimg gs_pp_sm">
                <img alt="Matthias Minderer" sizes="56px" 
                src="https://scholar.googleusercontent.com/citations?view_op=small_photo&amp;user=57BFBY0AAAAJ&amp;citpid=1" 
                srcset="https://scholar.googleusercontent.com/citations?view_op=small_photo&amp;user=57BFBY0AAAAJ&amp;citpid=1 56w,
                        https://scholar.googleusercontent.com/citations?view_op=view_photo&amp;user=57BFBY0AAAAJ&amp;citpid=1 128w" 
                width="56" height="56">
            </span>
        </a>
        <div class="gs_ai_t">
            <h3 class="gs_ai_name">
                <a href="/citations?hl=zh-CN&amp;user=57BFBY0AAAAJ">Matthias Minderer</a>
            </h3>
            <div class="gs_ai_aff">Senior Research Scientist, Google DeepMind</div>
            <div class="gs_ai_eml">在 google.com 的电子邮件经过验证</div>
            <div class="gs_ai_cby">被引用次数：53303</div>
            <div class="gs_ai_int">
                <a class="gs_ai_one_int" href="/citations?hl=zh-CN&amp;view_op=search_authors&amp;mauthors=label:representation_learning">Representation learning</a>
                <a class="gs_ai_one_int" href="/citations?hl=zh-CN&amp;view_op=search_authors&amp;mauthors=label:unsupervised_learning">Unsupervised learning</a>
            </div>
        </div>
    </div>
    <div class="gs_ai gs_scl gs_ai_chpr">
        <a href="/citations?hl=zh-CN&amp;user=12A34B56CDEF" class="gs_ai_pho">
            <span class="gs_rimg gs_pp_sm">
                <img alt="Jane Doe" sizes="56px" 
                src="https://scholar.googleusercontent.com/citations?view_op=small_photo&amp;user=12A34B56CDEF&amp;citpid=1" 
                width="56" height="56">
            </span>
        </a>
        <div class="gs_ai_t">
            <h3 class="gs_ai_name">
                <a href="/citations?hl=zh-CN&amp;user=12A34B56CDEF">Jane Doe</a>
            </h3>
            <div class="gs_ai_aff">Professor, University of Example</div>
            <div class="gs_ai_eml">在 example.edu 的电子邮件经过验证</div>
            <div class="gs_ai_cby">被引用次数：10234</div>
            <div class="gs_ai_int">
                <a class="gs_ai_one_int" href="/citations?hl=zh-CN&amp;view_op=search_authors&amp;mauthors=label:data_science">Data Science</a>
                <a class="gs_ai_one_int" href="/citations?hl=zh-CN&amp;view_op=search_authors&amp;mauthors=label:machine_learning">Machine Learning</a>
            </div>
        </div>
    </div>
    """


def test_extract_author_info_multiple_authors(sample_html_multiple_authors):
    """
    测试从包含多个作者信息的 HTML 中提取所有作者。
    """
    authors = extract_author_info_from_key_page(sample_html_multiple_authors)

    # 预期结果
    expected_authors = [
        {
            'googlescholar_id': '57BFBY0AAAAJ',
            'href': '/citations?hl=zh-CN&user=57BFBY0AAAAJ',
            'email': 'google.com',
            'name': 'Matthias Minderer',
            'full_name': 'Matthias Minderer',
            'position': 'Senior Research Scientist, Google DeepMind',
            'affiliation': 'Senior Research Scientist, Google DeepMind',
            'affiliation_link': '',
            'homepage': {
                'href': '/citations?hl=zh-CN&user=57BFBY0AAAAJ',
                'text': 'Matthias Minderer'
            },
            'keywords': ['Representation learning', 'Unsupervised learning']
        },
        {
            'googlescholar_id': '12A34B56CDEF',
            'href': '/citations?hl=zh-CN&user=12A34B56CDEF',
            'email': 'example.edu',
            'name': 'Jane Doe',
            'full_name': 'Jane Doe',
            'position': 'Professor, University of Example',
            'affiliation': 'Professor, University of Example',
            'affiliation_link': '',
            'homepage': {
                'href': '/citations?hl=zh-CN&user=12A34B56CDEF',
                'text': 'Jane Doe'
            },
            'keywords': ['Data Science', 'Machine Learning']
        }
    ]

    assert len(authors) == len(expected_authors), f"Expected {len(expected_authors)} authors, got {len(authors)}"
    assert authors == expected_authors, f"Expected {expected_authors}, got {authors}"
