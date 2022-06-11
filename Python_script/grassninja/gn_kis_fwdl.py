#python3
# GrassNinja python driver
# HWTE Yan Li, 2020/10/10
# yan.li@apple.com
# DO NOT DISTRIBUTE THE CODE TO THE 3RD PART

import serial
import time
import argparse
from grassninja import grassNinjaHost


if __name__ == '__main__': 
    print('GrassNinjaHost test: P1')
    parser = argparse.ArgumentParser(description='GrassNinja Host Application, ver 1.0')
    parser.add_argument('-p', '--serialport', help='Serial port name.', type=str, default=False, required=True)
    parser.add_argument('-s', '--switch', help='Switch KIS FWDL on or off.', type=str, default='on', required=False)

    args = parser.parse_args()
    switch = args.switch # 'on'|'off'

    GNH_UART ={ 
            'portname': args.serialport,
            'baudrate': 905600, # DON'T TOUCH BAUDRATE!
            'timeout':0.2
            }
    FTDISerialNumber = GNH_UART['portname'].split('-')[1][:-1]
    i2cPortName = 'ftdi://ftdi:2232:'+FTDISerialNumber+'/2'
    b2pUart = serial.Serial(GNH_UART['portname'],baudrate=GNH_UART['baudrate'],timeout=GNH_UART['timeout']) 
    gnTest = grassNinjaHost(b2pUart,i2cPortName)

    if 'on' == switch: 
        gnTest.resetAll()
        gnTest.enableLink(PPOn=True)
        gnTest.KIS2Locust(on=True)
        gnTest.forceDFU(on=True)
        gnTest.hostReset(on=True)
        gnTest.hostReset(on=False)
        gnTest.forceDFU(on=False)
        resp = gnTest.locustB2P.readLagunaReg(0x1868)[0]
        if 0 != gnTest.getLagunaPowerState(): # make sure PMU is awake
            raise RuntimeError("GN host: PMU power mode is incorrect")
        print('GN host: KIS FWDL path enabled; Use /dev/cu.kis-xxxxxxxx-0 for goldrestore, status = %s' %(hex(resp))) # should be 0xd0
    if 'off' == switch:
        gnTest.PMUReset()
        time.sleep(1)
        gnTest.resetAll()
        gnTest.enableLink()
        print('GN host: KIS FWDL path disabled')


    # Close the FTDI ports
    gnTest.closePorts()
