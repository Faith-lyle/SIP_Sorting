#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:Long.Hou
@file: test.py 
@time: 2022/03/07 
@email:long.hou2@luxshare-ict.com
"""

import socket
import time,csv,os
import logging
import argparse
import serial

client = None


class TestItem:
    def __init__(self, **args):
        if "TestName" in args.keys():
            self._TestName = args['TestName']
        else:
            self._TestName = None
        if "TestResult" in args.keys():
            self._TestResult = args['TestResult']
        else:
            self._TestResult = None
        if "TestLower" in args.keys():
            self._TestLower = args['TestLower']
        else:
            self._TestLower = None
        if "TestUpper" in args.keys():
            self._TestUpper = args['TestUpper']
        else:
            self._TestUpper = None
        if "TestEnabled" in args.keys():
            if args["TestEnabled"].lower() == "true":
                self._IsEnabled = True
            else:
                self._IsEnabled = False
        else:
            self._IsEnabled = False
        if 'TestCmd' in args.keys():
            self._TestCmd = args["TestCmd"]
        else:
            self._TestCmd = None
        if "ReMarket" in args.keys():
            self._ReMarket = args["ReMarket"]
        else:
            self._ReMarket = None
        if "DecisionMode" in args.keys():
            self._DecisionMode = args["DecisionMode"]
        else:
            self._DecisionMode = None
        if "TestMode" in args.keys():
            self._TestMode = args["TestMode"]
        else:
            self._TestMode = None
        if "TestValue" in args.keys():
            self._TestValue = args["TestValue"]
        else:
            self._TestValue = None
        if "ReTestTime" in args.keys():
            self._ReTestTime = args["ReTestTime"]
        else:
            self._ReTestTime = None

    @property
    def ReTestTime(self):
        return self._ReTestTime

    @property
    def TestResult(self):
        return self._TestResult

    @property
    def TestMode(self):
        return self._TestMode

    @TestResult.setter
    def TestValue(self, value):
        self._TestResult = value

    @property
    def DecisionMode(self):
        return self._DecisionMode

    @property
    def ReMarket(self):
        return self._ReMarket

    @ReMarket.setter
    def ReMarket(self, value):
        self._ReMarket = value

    @property
    def TestValue(self):
        return self._TestValue

    @TestValue.setter
    def TestValue(self, value):
        self._TestValue = value

    @property
    def TestName(self):
        return self._TestName

    @TestName.setter
    def TestName(self, name):
        self._TestName = name

    @property
    def TestLower(self):
        return self._TestLower

    @TestLower.setter
    def TestLower(self, Lower):
        self._TestLower = Lower

    @property
    def TestUpper(self):
        return self._TestUpper

    @TestUpper.setter
    def TestUpper(self, upper):
        self._TestUpper = upper

    @property
    def isEnabled(self):
        return self._IsEnabled

    @isEnabled.setter
    def isEnabled(self, enabled):
        self._IsEnabled = enabled

    @property
    def TestCmd(self):
        return self._TestCmd


def read_test_plant(file_path):
    test_items = []
    if not os.path.exists(file_path):
        return
    with open(file_path, "r") as f:
        reader = list(csv.reader(f))
        for text in reader[1:]:
            map1 = dict(zip(reader[0], text))
            item = TestItem(**map1)
            test_items.append(item)
    return test_items


def get_argparse():
    args = argparse.ArgumentParser()
    args.add_argument("-s", "--slot", help="Slot Name")
    args.add_argument("-p", "--port", help="Port Name")
    args.add_argument("-f", "--file", help="Test Plant path")
    result = args.parse_args()
    return result


def open_socter_client():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 6001))


if __name__ == '__main__':
    '''
    格式
    正常测试
    [INFO]::[DadaTime]::[slot]::[row]::[TestItem]::[value]::[result]::[upper]::[lower]
    结束 
    [EXIT]::[DadaTime]::[slot]::[result]
    错误
    [ERROR]::[DadaTime]::[slot]::[row]::[TestItem]::[result]::[error_info]
    '''
    args = get_argparse()
    open_socter_client()
    if len(args) != 3:
        client.send("[EXIT]::[{}]::[{}]::[FAIL]\n".format(time.strftime("%y%y-%m-%d %H:%M:%S"), args.slot))
        exit()
    items = read_test_plant(args.file)
    if not items:
        client.send("[EXIT]::[{}]::[{}]::[FAIL]\n".format(time.strftime("%y%y-%m-%d %H:%M:%S"), args.slot))
        exit()
    term = serial.Serial(port=args.port,baudrate=9600,timeout=1)
    for i,item in enumerate(items):
        client.send("[INFO]::[{}]::[{}]::[{}]::[Buddy Link Test]::[1-1-1111]::[PASS]::[1-1-1111]::[1-1-1111]\n".format(time.
                    strftime("%y%y-%m-%d %H:%M:%S"), args.slot, i))
        time.sleep(0.5)

