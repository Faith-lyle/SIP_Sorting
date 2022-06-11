#python3
# GrassNinja python driver
# HWTE Yan Li, 2020/10/10
# yan.li@apple.com
# DO NOT DISTRIBUTE THE CODE TO THE 3RD PART

import serial
import time
from grassninja import grassNinjaHost


LAGUNA_I2C_7BIT_ADDR = 0x11
DEBUG_FLAG = True


if __name__ == '__main__': 
    # dut = gn()
    # dut.parrot.interrupt()
    Debug_UART ={ 
            'portname': '/dev/cu.usbserial-141200',
            'baudrate': 921600,
            'timeout':0.2
            }

    b2pUart = serial.Serial(Debug_UART['portname'],baudrate=Debug_UART['baudrate'],timeout=Debug_UART['timeout']) 
    gnTest = grassNinjaHost(b2pUart)

    req = ''
    target = 'host'
    function = 'r'


    while req != 'q':
        req = input("target, register and function:") # target host/device/laguna, register 0x4a, function r/w

        if 'target' in req:
            target = req.split(' ')[1]
            continue

        if 'register' in req:
            register = req.split(' ')[1]
            continue

        if 'function' in req:
            function = req.split(' ')[1]
            continue

        gnTest.locustB2P.locust_b2p.writeLagunaReg(register, data)
        gnTest.locustB2P.locust_b2p.writeLocustReg(register, data, target=target)



