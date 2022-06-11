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
    parser = argparse.ArgumentParser(description='GrassNinja Host Application, ver 1.0')
    parser.add_argument('-p', '--serialport', help='Serial port name.', type=str, default=False, required=True)
    parser.add_argument('-s', '--switch', help='Switch GN power path [on|off].', type=str, default='on', required=False)

    args = parser.parse_args()
    state = args.switch

    GNH_UART ={ 
            'portname': args.serialport,
            'baudrate': 905600, # DON'T TOUCH BAUDRATE!
            'timeout':0.2
            }
    FTDISerialNumber = GNH_UART['portname'].split('-')[1][:-1]
    i2cPortName = 'ftdi://ftdi:2232:'+FTDISerialNumber+'/2'
    b2pUart = serial.Serial(GNH_UART['portname'],baudrate=GNH_UART['baudrate'],timeout=GNH_UART['timeout']) 
    gnTest = grassNinjaHost(b2pUart,i2cPortName)


    if 'off' in state: gnTest.insecureMode(False)
    else: gnTest.insecureMode(True)


    # Close the FTDI ports
    gnTest.closePorts()
