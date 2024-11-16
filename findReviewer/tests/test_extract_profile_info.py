import pytest
from bs4 import BeautifulSoup
from findReviewer.useDerison.justtest import extract_profile_info  # 替换为实际模块名


@pytest.mark.parametrize("html_str, expected", [
    # 测试完整数据
    ("""
    <div id="gsc_prf_i">
        <div id="gsc_prf_in">John Doe</div>
        <div class="gsc_prf_il">Professor of Computer Science</div>
        <a class="gsc_prf_ila" href="https://university.edu">University of Example</a>
    </div>
    <div id="gsc_prf_ivh">
        <div class="gsc_prf_il" id="gsc_prf_ivh">
            在 psu.edu 的电子邮件经过验证 - 
            <a href="https://homepage.example.com/" class="gsc_prf_ila">首页</a>
        </div>
    </div>
    <div id="gsc_prf_int">
        <a href="/scholar?q=keyword1">Artificial Intelligence</a>
        <a href="/scholar?q=keyword2">Machine Learning</a>
    </div>
    """,
     {
         "full_name": "John Doe",
         "position": "Professor of Computer Science",
         "affiliation": "University of Example",
         "affiliation_link": "https://university.edu",
         "homepage": {"href": "https://homepage.example.com/", "text": "首页"},
         "keywords": [
             {"name": "Artificial Intelligence", "href": "/scholar?q=keyword1"},
             {"name": "Machine Learning", "href": "/scholar?q=keyword2"}
         ]
     }),

    # 测试缺少首页
    ("""
    <div id="gsc_prf_i">
        <div id="gsc_prf_in">Jane Smith</div>
        <div class="gsc_prf_il">Associate Professor</div>
        <a class="gsc_prf_ila" href="https://university.edu">University of Research</a>
    </div>
    <div id="gsc_prf_int">
        <a href="/scholar?q=keyword1">Deep Learning</a>
    </div>
    """,
     {
         "full_name": "Jane Smith",
         "position": "Associate Professor",
         "affiliation": "University of Research",
         "affiliation_link": "https://university.edu",
         "homepage": None,
         "keywords": [
             {"name": "Deep Learning", "href": "/scholar?q=keyword1"}
         ]
     }),

    # 测试缺少所有关键字段
    ("<div></div>",
     {
         "full_name": None,
         "position": None,
         "affiliation": None,
         "affiliation_link": None,
         "homepage": None,
         "keywords": []
     }),

    # 测试只有关键字部分
    ("""
    <div id="gsc_prf_int">
        <a href="/scholar?q=keyword1">AI</a>
        <a href="/scholar?q=keyword2">ML</a>
    </div>
    """,
     {
         "full_name": None,
         "position": None,
         "affiliation": None,
         "affiliation_link": None,
         "homepage": None,
         "keywords": [
             {"name": "AI", "href": "/scholar?q=keyword1"},
             {"name": "ML", "href": "/scholar?q=keyword2"}
         ]
     }),

    # 测试缺少affiliation链接
    ("""
    <div id="gsc_prf_i">
        <div id="gsc_prf_in">Emily Zhang</div>
        <div class="gsc_prf_il">Research Scientist</div>
    </div>
    <div id="gsc_prf_ivh">
        <div class="gsc_prf_il" id="gsc_prf_ivh">
            <a href="https://personal.website.com/" class="gsc_prf_ila">首页</a>
        </div>
    </div>
    """,
     {
         "full_name": "Emily Zhang",
         "position": "Research Scientist",
         "affiliation": None,
         "affiliation_link": None,
         "homepage": {"href": "https://personal.website.com/", "text": "首页"},
         "keywords": []
     }),
])
def test_extract_profile_info(html_str, expected):
    result = extract_profile_info(html_str)
    assert result == expected