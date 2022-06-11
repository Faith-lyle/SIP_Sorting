#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:Long.Hou
@file: demo2.py 
@time: 2022/04/02 
@email:long.hou2@luxshare-ict.com
"""
# print(0x3b500+hex(1000))
print(hex(0x3b500+1000)[2:])
print(hex(0x3c3e48+1000))

import time


print(str(time.time()).split('.')[0])

print(time.localtime(time.time()))
