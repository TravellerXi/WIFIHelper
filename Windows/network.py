#!/usr/bin/env python3
# coding=utf-8
from Functions import *

if __name__=="__main__":
    开始登陆 = 执行()
    开始登陆.登陆()
    while 1:
        开始登陆.检查网络()
        time.sleep(3)