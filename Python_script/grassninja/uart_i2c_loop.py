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

class i2cTest():
    def __init__(self,portname):
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
        data = i2cDevice.read_from(reg,N)
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

    def i2cLoopTest(self,addr, reg, N):
        Nread = 0
        Nwrite = 0
        err = 0
        time0 = time.time()
        for i in range(N+1):
            data = self.i2cRead(addr,reg,1)
            data = (random.randint(0,255))&0xff
            self.i2cWrite(addr, reg , data) 
            data2 = self.i2cRead(addr, reg ,1)
            Nread += 2
            Nwrite += 1
            if (data2 != data):
                err += 1
                print("\nError found: write = 0x%x\n, readback = 0x%x\n\n" %(data, data2))
        print("\n\nTotal runs: %d, i2c read %d, i2c write %d, Error %d\n" %(i, Nread, Nwrite, err))
        time1 = time.time()
        print('I2C loop test finished in %f s\n' %(time1-time0))


class uartloopTest():
    def __init__(self,Portname,Baudrate=921600,Timeout=5): 
        try:
            self.port = serial.Serial(Portname,baudrate=Baudrate,timeout=Timeout)
        except:
            raise RuntimeError("Open serial port error: %s", Portname)
        self.debug = False
        self.tx =[]
        self.rx =[]

    def close(self):
        self.port.flush()
        self.port.close()

    def sendData(self, len): #len is the length of the packet to send once
        self.tx =[]
        if self.port.is_open:
            for i in range(len):
                data = random.randint(0,255)
                self.tx.append(data)
            self.tx.append(0x0A)
            self.tx.append(0x32)
            self.tx =  bytearray(self.tx)
            self.port.write(self.tx)
            if self.debug: print(self.tx)
        else:
            raise RuntimeError("Open serial port error: %s", self.port.name)
    
    def receiveData(self,timeout): # timeout in seconds
        self.rx =[]
        if self.port.is_open:
            self.rx = bytearray(b'')
            TimeBegin = time.time()
            rxdata_Length = 65535
            while ((time.time()-TimeBegin) < timeout):
                data = self.port.read_all()
                if data: 
                    self.rx +=bytearray(data) 
                    if ((self.rx[-1]==0x32) and (self.rx[-2]==0x0A)): 
                        break
            if self.debug: print(self.rx)
        return

    def runTest(self,pkt_len,N): # pkt_len -- length of the packet, N -- number of transmit
        tx_len = 0
        rx_len = 0
        err = 0
        time0 = time.time()
        for i in range(N+1):
            self.sendData(pkt_len)
            self.receiveData(0.5)
            tx_len +=len(self.tx)
            rx_len +=len(self.rx)
            if (self.tx != self.rx):
                err += 1
                print("\nError found: tx = %s\n rx = %s\n\n" %(self.tx, self.rx))
        
        print("\n\nTotal runs: %d, TX bytes %d, RX bytes %d, Error %d\n" %(i, tx_len, rx_len, err))
        time1 = time.time()
        print('Uart loop test finished in %f s\n' %(time1-time0))

if __name__ == '__main__': 
    DFU_UART ={ 
            'portname': '/dev/cu.usbserial-14100',
            'baudrate': 921600,
            'timeout':0.2
            }
    Debug_UART ={ 
            'portname': '/dev/cu.usbserial-14401',
            'baudrate': 921600,
            'timeout':0.2
            }
    i2cMaster = 'ftdi://ftdi:2232:14:5/2'

#    loop = uartloopTest(Debug_UART['portname'],Baudrate=Debug_UART['baudrate'],Timeout=Debug_UART['timeout'])
    Uartloop = uartloopTest(DFU_UART['portname'],Baudrate=DFU_UART['baudrate'],Timeout=DFU_UART['timeout'])
    Uartloop.debug = False
    i2cloop = i2cTest(i2cMaster)
    i2cloop.debug = False

    t1 = threading.Thread(target=Uartloop.runTest,args=(200,1000))
    t2 = threading.Thread(target=i2cloop.i2cLoopTest, args=(0x34,0x5F, 300))

#    t2 = threading.Thread(target=loop2.runTest,args=(200,1000))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Loop test completed\n")
