#python3
# GrassNinja python driver
# EE Calvin Ryan
# coyote@apple.com
# DO NOT DISTRIBUTE THE CODE TO THE 3RD PARTY

import serial
import time
import argparse
from grassninja import grassNinjaHost


if __name__ == '__main__': 
    print('GrassNinjaHost test: P1')
    parser = argparse.ArgumentParser(description='GrassNinja Host Application, ver 1.0')
    parser.add_argument('-p', '--serialport', help='Serial port name.', type=str, default=False, required=True)
    parser.add_argument('-c', '--commsmode', help='ASK or DPM.', type=str, default=False, required=True)
    parser.add_argument('-n', '--numtests', help='Number of loopback tests.', type=int, default=5000, required=False)

    args = parser.parse_args()

    GNH_UART ={ 
            'portname': args.serialport,
            'baudrate': 905600, # DON'T TOUCH BAUDRATE!
            'timeout':0.2
            }
    FTDISerialNumber = GNH_UART['portname'].split('-')[1][:-1]
    i2cPortName = 'ftdi://ftdi:2232:'+FTDISerialNumber+'/2'
    b2pUart = serial.Serial(GNH_UART['portname'],baudrate=GNH_UART['baudrate'],timeout=GNH_UART['timeout']) 
    gnTest = grassNinjaHost(b2pUart,i2cPortName)

    
    gnTest.resetAll()
    gnTest.enableLink(PPOn=True)
    gnTest.hostLocust2DeviceLocustLoopbackTest(comms_mode = args.commsmode, num = args.numtests)


    # Close the FTDI ports
    gnTest.closePorts()
