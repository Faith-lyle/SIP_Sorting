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
    parser.add_argument('-ch', '--channel', help='AMUXOUT channel', type=str, default='VDD_MAIN_SNS', required=True)
    parser.add_argument('-xy', '--pin', help='AMUXOUT select pin', type=str, default='ay', required=True)
    args = parser.parse_args()
    ch = args.channel
    pin = args.pin

    GNH_UART ={ 
            'portname': args.serialport,
            'baudrate': 905600, # DON'T TOUCH BAUDRATE!
            'timeout':0.2
            }
    FTDISerialNumber = GNH_UART['portname'].split('-')[1][:-1]
    i2cPortName = 'ftdi://ftdi:2232:'+FTDISerialNumber+'/2'

    b2pUart = serial.Serial(GNH_UART['portname'],baudrate=GNH_UART['baudrate'],timeout=GNH_UART['timeout']) 
    gnTest = grassNinjaHost(b2pUart,i2cPortName)

    '''
        channel_List= {
                'disabled',
                'AMUX0',
                'AMUX1',
                'AMUX2',
                'AMUX3',
                'AMUX4',
                'AMUX5',
                'AMUX6',
                'AMUX7',
                'VDD_MAIN_SNS', 
                'VBAT_SNS_CHG', 
                'NTC_BAT_P', 
                'BUCK0_FB', 
                'BUCK1_FB', 
                'BUCK2_FB', 
                'BUCK3_FB', 
                'BUCK4_FB', 
                'BUCK5_FB', 
                'PMU_1V5', 
                'LDO1_VOUT', 
                'LDO2_VOUT', 
                'LDO3_VOUT', 
                'LSA_VOUT0', 
                'LSB_VOUT0', 
                'LSB_VOUT1',
                'LSC_VOUT0', 
                'LSC_VOUT1',
                'LSC_VOUT2',
                'LS_HPA_VOUT', 
                'VSS_REF', 
                'GPADC_LVMUX', 
                'GPADC_HVMUX', 
                'VSS'
                }

        pin_list = {'ax','ay'}
    '''


    gnTest.enterLagunaTestMode()
    if 'ax' in pin: gnTest.lagunaIsink(current=0x5,target='amuxout_ax') # disable sink current on axmout_ax
    gnTest.lagunaAmuxSel(src='disabled',target=pin)
    gnTest.lagunaAmuxSel(src=ch,target=pin)
    print("GN host: %s is now on AMUXOUT_%s" %(ch, pin))

    # Close the FTDI ports
    gnTest.closePorts()
