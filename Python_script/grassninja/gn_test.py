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
    gnTest.enableLink()
    gnTest.forceDfuMode()
    gnTest.forceAwake()
    gnTest.enterLagunaTestMode()
    gnTest.ccadcRead()
#    gnTest.exitLagunaTestMode()
#    gnTest.getDeviceInfo()
#    gnTest.b2pPingSoC()
#    gnTest.enableCharging(False)
#    gnTest.dumpGPIOConfigures()
#    gnTest.enableCharging(True)
#    gnTest.gpioStatus()
#    gnTest.hostReset()
#    gnTest.getLagunaPowerState()
#    time.sleep(3)
#    gnTest.hostReset(False)
#    gnTest.setLagunaPowerState("OFF")
#    gnTest.PMUResetL()

#    gnTest.powerFunbus(False)
#    time.sleep(1)
#    gnTest.powerFunbus()
#    gnTest.locustB2P.sendPing(destination="DeviceLocust")

#    gnTest.KIS2Locust(True)
#    gnTest.KIS2Locust(False)
#
#    gnTest.enableKIS2SoC()

#    gnTest.eUSB2Locust() 
#
#    gnTest.locustB2P.sendReset("HostLocust", reset_mode=0x01)
#    gnTest.locustB2P.sendPing("HostLocust")
#    gnTest.locustB2P.enablePowerPath("HostLocust")
#
#
#    gnTest.locustB2P.sendReset("DeviceLocust", reset_mode=0x01)
##    time.sleep(1)
#    gnTest.locustB2P.sendPing(destination="DeviceLocust")
#    gnTest.locustB2P.enablePowerPath(destination="DeviceLocust")
#
##    gnTest.setDPMCommsMode()
##    gnTest.locustB2P.setCommsMode("DPM")
#    gnTest.setDPMCommsMode()
#    gnTest.getState("DeviceLocust")
#    gnTest.enableEUSBLocust()
#    time.sleep(0.1)
#    gnTest.enableEUSBDurant()
#
#    print('Test done')
