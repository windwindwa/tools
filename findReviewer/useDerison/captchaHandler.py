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

    def contains_captcha_verification(slef, html_content):
        """
        检查 HTML 字符串中是否包含关键字 "进行人机身份验证"。

        :param html_content: HTML 字符串
        :return: 如果找到关键字返回 True，否则返回 False
        """

        keyword = "进行人机身份验证"
        return keyword in html_content
    def check_captcha(self) -> bool:
        """检查页面是否包含验证码
        """
        try:
            # import time
            # start_time = time.time()

            # 要测试的代码
            # bool(self.tab.ele('#gs_captcha_f')) or bool(self.tab.ele('#captcha-form'))
            self.tab.wait(2.4, 3.6)
            return self.contains_captcha_verification(self.tab.html)

            # end_time = time.time()
            # print(f"代码执行时间: {end_time - start_time:.2f} 秒")
            # 同时检查两个可能的验证码标签
            # 下面验证要20秒，太慢了
            # return bool(self.tab.ele('#gs_captcha_f')) or bool(self.tab.ele('#captcha-form'))
        except Exception as e:
            print(f"检查验证码时出错: {e}")
            return False
    def handle_captcha(self):
        """处理验证码"""
        while self.check_captcha():
            pyautogui.alert(title='验证码提示', text='请手动完成人机验证后，点击“已完成”', button='已完成')
            self.tab.refresh()
            time.sleep(5)