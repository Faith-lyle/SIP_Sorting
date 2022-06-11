#python3
# HWTE Yan Li, 2020/05/10
# yan.li@apple.com
# DO NOT DISTRIBUTE THE CODE TO THE 3RD PARTY

import serial
import time
import struct
import random
import threading

class loopTest():
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
        print('Loop test finished in %f s\n' %(time1-time0))

if __name__ == '__main__': 
    DFU_UART ={ 
            'portname': '/dev/cu.usbserial-14401',
            'baudrate': 921600,
            'timeout':0.2
            }
    Debug_UART ={ 
            'portname': '/dev/cu.usbserial-14400',
            'baudrate': 921600,
            'timeout':0.2
            }
    loop = loopTest(Debug_UART['portname'],Baudrate=Debug_UART['baudrate'],Timeout=Debug_UART['timeout'])
    loop2 = loopTest(DFU_UART['portname'],Baudrate=DFU_UART['baudrate'],Timeout=DFU_UART['timeout'])

    loop.debug = False

    t1 = threading.Thread(target=loop.runTest,args=(200,1000))
    t2 = threading.Thread(target=loop2.runTest,args=(200,1000))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

#    loop.runTest(200,1000)