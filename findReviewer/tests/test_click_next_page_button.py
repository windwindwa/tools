# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/24 15:50
# @Author  : lzg
# @Site    : 
# @File    : test_click_next_page_button.py
# @Software: PyCharm


import pytest
from unittest.mock import MagicMock
from findReviewer.useDerison.pageHandler import click_next_page_buttom  # 替换为实际模块名

@pytest.fixture
def mock_tab():
    """
    创建一个 DrissionPage 的模拟对象。
    """
    mock_tab = MagicMock()
    # 模拟 _wait_loaded 方法
    mock_tab._wait_loaded = MagicMock()
    return mock_tab


def test_click_next_page_button_with_button(mock_tab):
    """
    测试当“下一页”按钮存在时，函数能正确点击。
    """
    # 模拟“下一页”按钮存在
    mock_tab.ele.return_value = MagicMock()

    # 调用函数
    result = click_next_page_buttom(mock_tab)

    # 验证点击了按钮
    mock_tab.run_js.assert_called_once_with('document.querySelector(".gsc_pgn_pnx").click();')
    assert result is True


def test_click_next_page_button_without_button(mock_tab):
    """
    测试当“下一页”按钮不存在时，函数能正确返回 False。
    """
    # 模拟“下一页”按钮不存在
    mock_tab.ele.return_value = None

    # 调用函数
    result = click_next_page_buttom(mock_tab)

    # 验证未调用 JS 脚本
    mock_tab.run_js.assert_not_called()
    assert result is False
