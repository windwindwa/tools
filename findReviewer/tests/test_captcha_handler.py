import pytest
from unittest.mock import MagicMock
from findReviewer.useDerison.captchaHandler import CaptchaHandler


@pytest.fixture
def mock_chromium():
    """创建模拟的 Chromium 对象"""
    mock_chromium = MagicMock()
    mock_tab = MagicMock()
    mock_chromium.latest_tab = mock_tab
    return mock_chromium


def test_check_captcha_both_tags_exist(mock_chromium):
    """测试 check_captcha 方法，两个验证码标签同时存在的情况"""
    # 模拟页面同时存在两个验证码标签
    mock_chromium.latest_tab.ele.side_effect = lambda x: True if x in ['#gs_captcha_f', '#captcha-form'] else None

    handler = CaptchaHandler(mock_chromium)
    assert handler.check_captcha() is True

    # 验证每个标签的检查
    mock_chromium.latest_tab.ele.assert_any_call('#gs_captcha_f')
    mock_chromium.latest_tab.ele.assert_any_call('#captcha-form')


def test_check_captcha_no_tags(mock_chromium):
    """测试 check_captcha 方法，不存在任何验证码标签的情况"""
    # 模拟页面不存在任何验证码标签
    mock_chromium.latest_tab.ele.return_value = None

    handler = CaptchaHandler(mock_chromium)
    assert handler.check_captcha() is False

    # 验证每个标签的检查
    mock_chromium.latest_tab.ele.assert_any_call('#gs_captcha_f')
    mock_chromium.latest_tab.ele.assert_any_call('#captcha-form')