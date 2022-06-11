#python3
# HWTE Yan Li, 2020/05/10
# yan.li@apple.com
# DO NOT DISTRIBUTE THE CODE TO THE 3RD PARTY

import serial
import time
import struct
import random
import threading
from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController, I2cIOError

class i2c():
    def __init__(self,portname='ftdi://ftdi:2232:14:e/2'):
        Ftdi.show_devices()
        self.i2cSlave = I2cController()
        self.debug = False
        try:
            self.i2cSlave.configure(portname)
        except:
            raise RuntimeError("Open I2C port error: %s", portname)

    def i2cRead(self,addr,reg,N):
        addr = addr >>1
        i2cDevice = self.i2cSlave.get_port(addr)
        i2cDevice.write(reg)
        data = i2cDevice.read(N,start=True)
        data = int.from_bytes(data,"little")
        if self.debug:
            print("Read from i2c addr 0x%x, reg 0x%x, data 0x%x" %(addr, reg, data))
        return data
    
    def i2cWrite(self,addr,reg,data):
        addr = addr >>1
        i2cDevice = self.i2cSlave.get_port(addr)
        i2cDevice.write_to(reg,bytes([data]))
        if self.debug: 
            print("Write to i2c addr 0x%x, reg 0x%x, data 0x%x" %(addr, reg, data))

if __name__ == '__main__': 
    i2ctest = i2c()
#    i2ctest.i2cWrite(0x78,0x14,0x00)
    i2ctest.i2cRead(0x78,0x1400,1)