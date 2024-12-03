# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/3/24 13:14
# @Author  : lzg
# @Site    : 
# @File    : logoHandler.py
# @Software: PyCharm

from pyfiglet import figlet_format

def print_logo():

    """
    打印程序的 Logo
    """
    print("--------------------\n")
    print(figlet_format("L Z G", font="doh"))
    print("--------------------\n")
