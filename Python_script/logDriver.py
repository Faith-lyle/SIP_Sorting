#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Long.Hou
@file: logDriver.py
@time: 2021/12/13
@email:long.hou2@luxshare-ict.com
"""
import datetime
import logging


class LogDriver:
    def __init__(self, file_name,level=logging.DEBUG):
        self._log = logging.Logger(name="admin", level=level)
        self.file_name = file_name
        self.setup_log()
        self.index = 1

    def setup_log(self):
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(filename=self.file_name, encoding="utf-8", mode="w")
        file_handler.setFormatter(logging.Formatter("[%(asctime)s]  %(message)s"))
        file_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(logging.Formatter("[%(threadName)s] [%(asctime)s]  %(message)s"))
        stream_handler.setLevel(logging.DEBUG)
        self._log.addHandler(file_handler)
        self._log.addHandler(stream_handler)

    def mes_log(self,func_name,url,data,response):
        self._log.debug("{}\nFunction:{}\nRequest URL:{}\nRequest Method: POST\nRequest Date:{}\n"
                        "Response Status Code:{}\nResponse Text:{}\n".format('-'*20,func_name,url,data,response.status_code,response.text))

    def mes_error_log(self,func_name,url,data,error):
        self._log.error("{}\nFunction:{}\nRequest URL:{}\nRequest Method: POST\nRequest Date:{}\nError information:{}\n".format('-'*20,func_name,url,data,error))

    def send_log(self, msg):
        self._log.debug("Send Cmd: " + msg)

    def send_error(self, msg):
        self._log.debug("Error: " + msg)

    def receive_log(self, msg):
        self._log.debug("Receive Content:\n " + msg)

    def set_item_result(self, value, result):
        self._log.debug("Get Value: {}".format(value))
        self._log.debug('Test Result: {}'.format(result))

    def item_end(self, item):
        EndTime = datetime.datetime.now().__sub__(self.stratTime)
        msg = "Elapsed Second:{}".format(EndTime.microseconds / 1000)
        self._log.info(msg)
        self._log.info('Step{}  "{}"  End   <------------------------------\n'.format(self.index, item))
        self.index += 1

    def item_start(self, item):
        self.stratTime = datetime.datetime.now()
        msg = 'Step{}  "{}" Start   ------------------------------>'.format(self.index, item)
        self._log.info(msg)

    def system_reset_start(self):
        self.stratTime = datetime.datetime.now()
        msg = 'Step{}  "System Reset" Start   ------------------------------>'.format(self.index)
        self._log.info(msg)

    def system_reset_end(self):
        EndTime = datetime.datetime.now().__sub__(self.stratTime)
        msg = "Elapsed Second:{}".format(EndTime.microseconds / 1000)
        self._log.info(msg)
        self._log.info('Step{}  "System Reset"  End   <------------------------------\n'.format(self.index))
        self.index += 1
