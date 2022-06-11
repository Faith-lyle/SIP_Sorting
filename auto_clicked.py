#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:Long.Hou
@file: auto_clicked.py 
@time: 2022/05/07 
@email:long.hou2@luxshare-ict.com
"""
import sys

import pyautogui
import time


timer = sys.argv[1]
print(timer)
time.sleep(5)
for i in range(int(timer)):
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(30)
    print(i)

print("update successful!\n")