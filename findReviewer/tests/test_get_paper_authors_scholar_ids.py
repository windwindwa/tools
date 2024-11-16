import pytest
from unittest.mock import patch
from findReviewer.lzgcode.findArticleAutherInfo import get_paper_authors_scholar_ids, extract_authors_info  # 替换为实际模块名

def test_get_paper_authors_scholar_ids_normal_case():
    """
    测试正常情况下返回作者信息的行为
    """
    paper_title = "Sample Paper Title"
    mock_paper = {
        'bib': {
            'title': 'Sample Paper Title',
            'author': ['Author A', 'Author B']
        },
        'author_id': ['ID123', 'ID456']
    }
    expected_output = [
        {"name": "Author A", "google_scholar_id": "ID123"},
        {"name": "Author B", "google_scholar_id": "ID456"}
    ]

    with patch("findReviewer.lzgcode.findArticleAutherInfo.scholarly.search_pubs", return_value=iter([mock_paper])):
        with patch("findReviewer.lzgcode.findArticleAutherInfo.extract_authors_info", return_value=expected_output):
            result = get_paper_authors_scholar_ids(paper_title)
            assert result == expected_output

def test_get_paper_authors_scholar_ids_no_results():
    """
    测试没有找到论文的情况
    """
    paper_title = "Nonexistent Paper"
    with patch("findReviewer.lzgcode.findArticleAutherInfo.scholarly.search_pubs", return_value=iter([])):
        result = get_paper_authors_scholar_ids(paper_title)
        expected_output = f"No results found for the paper title: {paper_title}"
        assert result == expected_output

def test_get_paper_authors_scholar_ids_exception_case():
    """
    测试抛出异常的情况
    """
    paper_title = "Exception Paper"
    with patch("findReviewer.lzgcode.findArticleAutherInfo.scholarly.search_pubs", side_effect=Exception("Mocked Exception")):
        result = get_paper_authors_scholar_ids(paper_title)
        assert "Error occurred: Mocked Exception" in result