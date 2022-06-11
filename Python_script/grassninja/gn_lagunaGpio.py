#python3
# GrassNinja python driver
# HWTE Yan Li, 2020/10/10
# yan.li@apple.com
# DO NOT DISTRIBUTE THE CODE TO THE 3RD PART

import serial
import time
import argparse
from grassninja import grassNinjaHost


LAGUNA_I2C_7BIT_ADDR = 0x11
DEBUG_FLAG = True


if __name__ == '__main__': 
    print('GrassNinjaHost test: P1')
#    parser = argparse.ArgumentParser(description='GrassNinja Host test')
#    parser.add_argument('-p', '--serialport', help='Serial port name.', type=str, default=False, required=True)
#    parser.add_argument('-b', '--baudrate', help='BaudRate.', type=int, default=921600)
#
#    args = parser.parse_args()

    Debug_UART ={ 
            'portname': '/dev/cu.usbserial-146200',
            'baudrate': 905600,
            'timeout':0.2
            }

    b2pUart = serial.Serial(Debug_UART['portname'],baudrate=Debug_UART['baudrate'],timeout=Debug_UART['timeout']) 
    gnTest = grassNinjaHost(b2pUart)
    gnTest.dumpGPIOConfigures()
    gnTest.gpioStatus()
