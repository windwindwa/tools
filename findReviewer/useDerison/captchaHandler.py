# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/15/24 23:52
# @Author  : lzg
# @Site    :
# @File    : captchaHandler.py
# @Software: PyCharm

import time

from DrissionPage import Chromium
import pyautogui


class CaptchaHandler:
    def __init__(self, chrommium: Chromium):
        """初始化验证码处理器
        :param page: DrissionPage 实例
        """
        self.tab = chrommium.latest_tab

    def check_captcha(self) -> bool:
        """检查页面是否包含验证码"""
        try:
            # 同时检查两个可能的验证码标签
            return bool(self.tab.ele('#gs_captcha_f')) or bool(self.tab.ele('#captcha-form'))
        except Exception as e:
            print(f"检查验证码时出错: {e}")
            return False
    def handle_captcha(self):
        """处理验证码"""
        while self.check_captcha():
            pyautogui.alert(title='验证码提示', text='请手动完成人机验证后，点击“已完成”', button='已完成')
            self.tab.refresh()
            time.sleep(2)