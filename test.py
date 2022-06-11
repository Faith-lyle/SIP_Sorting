#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:Long.Hou
@file: test.py
@time: 2022/03/07
@email:long.hou2@luxshare-ict.com
"""
import socket
import time
import logging
import argparse

Parser = argparse.ArgumentParser()
Parser.add_argument("-s","--slot",help="Slot Name")
arg = Parser.parse_args()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 6001))
start_time = time.time()
for i in range(1,20):
    client.send("[INFO]::[{}]::[{}]::[{}]::[Buddy Link Test]::[1-1-1111]::[PASS]::[1-1-1111]::[1-1-1111]\n".format(time.
        strftime("%y%y-%m-%d %H:%M:%S"),arg.slot,i))
    time.sleep(0.5)
client.send("[EXIT]:hello")

'''
格式
正常测试
[INFO]::[DadaTime]::[slot]::[row]::[TestItem]::[value]::[result]::[upper]::[lower]
结束
[EXIT]::[DadaTime]::[slot]::[result]
错误
[ERROR]::[DadaTime]::[slot]::[row]::[TestItem]::[result]::[error_info]
'''
# text = '[ERROR]::[DadaTime]::[slot]::[row]::[TestItem]::[result]::[error_info]'
# print text.split('::[')
# print hex(20).upper()[-1:]
print len('[INFO]::[1]::[1]::[PASS]')