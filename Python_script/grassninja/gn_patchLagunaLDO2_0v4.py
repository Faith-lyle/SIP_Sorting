#PYTHON3
#HWTE Yan Li
#Modified based on Calvin Ryan's patchLagunaLDO2.py script
#Add 1s delay for Laguna to enter test mode
import serial
import time
import argparse
from grassninja import grassNinjaHost


####################
# Globals
####################
LAGUNA_DEVICE = 0x75
LAGUNA_TESTMODE_ENTRY_REG = 0x3100
LAGUNA_TESTMODE_STATUS_REG = 0x3105
LAGUNA_OTP_MSB_POINTER = 0xc009
LAGUNA_OTP_LSB_POINTER = 0xc008
LAGUNA_OTP_DATA_REG = 0xc010
LAGUNA_OTP_CMD_REG = 0xc020
LAGUNA_OTP_CRC_REG = 0xc022
LAGUNA_OTP_REV_REG = 0x1405
LAGUNA_CRC_FAULT_REG = 0x1801

LAGUNA_OTP_DEBUG1 = 0xc029
LAGUNA_OTP_DEBUG2 = 0xc02c

def laguna_otp_dump():
    ADDRL = 0x0600
    ADDRH = 0x07ff
    ADDRList = [0x0600, 0x06BF, 0x06C0, 0x07FF, 0x07FE]

#    for address in range(0x0600,0x07ff+1,1):
    for address in ADDRList:
        otpaddr_msb = (address >> 8) & 0xff
        otpaddr_lsb = (address) & 0xff
        data = laguna_read_otp_word(otpaddr_msb,otpaddr_lsb)
        dbg1 = gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_MSB_POINTER)[0] 
        dbg2 = gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_LSB_POINTER)[0] 
        hexdata = []
        for i in data:
            hexdata.append(hex(i))
        print('Address:', hex(address), 'data:', hexdata, 'debug1:',hex(dbg1),'debug2:',hex(dbg2))
    
    print('Laguna OTP dump commpleted')


def laguna_read_otp_word(otpaddr_msb: int, otpaddr_lsb: int):
    ########################################
    # Function: laguna_read_otp_word
    # Description: read a single 4-byte OTP word from the otpaddr given in the argument
    # Usage: laguna_read_otp_word(shell, 0x06, 0xBE)
    ########################################

    while gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_CMD_REG)[0] != 0: # KP added in order to prevent new commands from being issued while a previous command is happening
        pass
    gnTest.locustB2P.writeLagunaReg(LAGUNA_OTP_MSB_POINTER,data = otpaddr_msb)
    gnTest.locustB2P.writeLagunaReg(LAGUNA_OTP_LSB_POINTER,data = otpaddr_lsb)
    gnTest.locustB2P.writeLagunaReg(LAGUNA_OTP_CMD_REG,data = 0x04)

    while gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_CMD_REG)[0] != 0: # KP added in order to prevent new commands from being issued while a previous command is happening
        pass
    debug_data = []
    for i in range(4):
        data = gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_DATA_REG + i)[0]
        debug_data.append(data)
   
    debug_data_str = ''.join(hex(x)[2:].rjust(2, '0') for x in debug_data)

#    print('Data: 0x{data_str}'.format(data_str=debug_data_str))
    return debug_data

def laguna_write_otp_word(otpaddr_msb: int, otpaddr_lsb: int, data0_3: list):
    ########################################
    # Function: laguna_write_otp_word
    # Description: write a single 4-byte OTP word to the otpaddr given in the argument.  Note for data, the order is [data0,data1,data2,data3]
    # Usage: laguna_write_otp_word(shell, 0x06, 0xBE, 0xFFFFFFFF)
    ########################################
    while gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_CMD_REG)[0] != 0: # KP added in order to prevent new commands from being issued while a previous command is happening
        pass
    gnTest.locustB2P.writeLagunaReg(LAGUNA_OTP_MSB_POINTER,data = otpaddr_msb)
    gnTest.locustB2P.writeLagunaReg(LAGUNA_OTP_LSB_POINTER,data = otpaddr_lsb)

    REG = LAGUNA_OTP_DATA_REG
    for data in data0_3:
        gnTest.locustB2P.writeLagunaReg(REG,data = data)
        REG += 1

    ### debug print statements -- print register values prior to actual write ###
    debug_msb = gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_MSB_POINTER)[0]
    debug_lsb = gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_LSB_POINTER)[0]
    debug_data = []
    for i in range(4):
        data = gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_DATA_REG + i)[0]
        debug_data.append(data)
   
    debug_data_str = ''.join(hex(x)[2:].rjust(2, '0') for x in debug_data)

    print('Attempting to write OTP')
    print('MSB: {msb:x}'.format(msb=debug_msb))
    print('LSB: {lsb:x}'.format(lsb=debug_lsb))
    print('Write Data: {data_str}'.format(data_str=debug_data_str))


    gnTest.locustB2P.writeLagunaReg(LAGUNA_OTP_CMD_REG,data = 0x02)

def laguna_update_crc():
    ########################################
    # Function: laguna_update_crc
    # Description: Runs crc calculation and updates CRC byte after an OTP re-program sequence
    # Usage: laguna_update_crc(shell)
    ########################################

    # calculate new crc pointer
    old_crc_ptr_list = laguna_read_otp_word(0x06,0x00)
    print('laguna_read_otp_word(0x06,0x00): ', old_crc_ptr_list)
    old_crc_ptr = old_crc_ptr_list[0]
    new_crc_ptr = (old_crc_ptr * 2) + 1

    if new_crc_ptr > 0xFF:
        raise ValueError('Specified CRC value: {crc} is outside the allowed range'.format(crc=new_crc_ptr))

    # update crc pointer
    laguna_write_otp_word(0x06,0x00,[new_crc_ptr])

    # do crc calculation
    cmd = gnTest.locustB2P.writeLagunaReg(LAGUNA_OTP_CMD_REG,0x40)
    print('crc calculation: ',LAGUNA_OTP_CMD_REG,cmd)

    while gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_CMD_REG)[0] != 0: # KP added in order to prevent new commands from being issued while a previous command is happening
        pass
    cmd = gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_CRC_REG)
    print('crc calculation: ',LAGUNA_OTP_CRC_REG,cmd)
    new_crc = cmd[0]

    # write new crc
    # generate new last byte of OTP space
    new_crc_ind = new_crc_ptr.bit_length() - 1
    new_crc_data0_3 = []

    if new_crc_ind < 4:
        for i in range(4):
            if i == new_crc_ind:
                new_crc_data0_3.insert(0, new_crc)
            else:
                new_crc_data0_3.insert(0, 0x00)

        laguna_write_otp_word(0x07,0xFF,new_crc_data0_3)
        print('new_crc_ind < 4','crc: ',new_crc_data0_3)
        old_crc_ptr_list = laguna_read_otp_word(0x07,0xFF)
        # assert(new_crc_data0_3 == old_crc_ptr_list)
        print('laguna_read_otp_word(0x07,0xFF): ', old_crc_ptr_list)        

    elif new_crc_ind < 8:
        for i in range(4):
            if i == (new_crc_ind-4):
                new_crc_data0_3.insert(0, new_crc)
            else:
                new_crc_data0_3.insert(0, 0x00)

        laguna_write_otp_word(0x07,0xFE,new_crc_data0_3)
        print('new_crc_ind < 8','crc: ',new_crc_data0_3)
        old_crc_ptr_list = laguna_read_otp_word(0x07,0xFE)
        # assert(new_crc_data0_3 == old_crc_ptr_list)
        print('laguna_read_otp_word(0x07,0xFE): ', old_crc_ptr_list)
    else:
        raise ValueError('Specified CRC index: {crc} is outside the allowed range'.format(crc=new_crc_ind))

#def laguna_write_otp_patch(shell, otpaddr: int, otpbyte: int, addr_msb: List[int], addr_lsb: List[int], data: List[int]):
    ########################################
    # Function: laguna_write_OTP_byte
    # Arguments: shell (SentinelShell_Mini object), otpaddr (int, address of 4-byte OTP word), otpbyte (int, 0-indexed byte where payload will be written, valid range 0-3), addr_msb (int, patch address MSB), addr_lsb (int, patch address LSB), data (int, patch data)
    # Description: Burns a single 3-byte OTP patch to the otpaddr/otpbyte given in the arguments
    # Usage: laguna_write_OTP_byte(shell, otpaddr, otpbyte, [addr_msb], [addr_lsb], [data])
    ########################################

    # todo -- implement this function, which will burn a single 3-byte otp patch to the given start address

def laguna_verify_otp_patch():
    ########################################
    # Function: laguna_verify_otp_patch
    # Description: Checks Laguna OTP version has been updated successfully and that there is no CRC error.
    # Usage: laguna_verify_otp_patch()
    ########################################

    new_otp_rev = gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_REV_REG)[0]
    if new_otp_rev != 0x24:
        print('OTP rev: {rev} does not equal expected value 0x24, patch not applied'.format(rev=hex(new_otp_rev)))
        patched = False
    else: patched = True

    fault2_reg = gnTest.locustB2P.readLagunaReg(LAGUNA_CRC_FAULT_REG)[0]

    if fault2_reg != 0x0:
        raise ValueError('Fault2 Reg is not 0x0: Reg 0x1801 = {fault2}'.format(fault2=fault2_reg))

    return patched


if __name__ == '__main__': 
    print('====== Laguna OTP programmer with GrassNinjaHost : P1 ======')
    parser = argparse.ArgumentParser(description='GrassNinja Host Application, ver 1.0')
    parser.add_argument('-p', '--serialport', help='Serial port name.', type=str, default=False, required=True)
    parser.add_argument('-s', '--switch', help='Switch on/off.', type=str, default='on', required=False)

    args = parser.parse_args()
    onoff = args.switch

    GNH_UART ={ 
            'portname': args.serialport,
            'baudrate': 905600, # DON'T TOUCH BAUDRATE!
            'timeout':0.2
            }
    FTDISerialNumber = GNH_UART['portname'].split('-')[1][:-1]
    i2cPortName = 'ftdi://ftdi:2232:'+FTDISerialNumber+'/2'
    b2pUart = serial.Serial(GNH_UART['portname'],baudrate=GNH_UART['baudrate'],timeout=GNH_UART['timeout']) 
    gnTest = grassNinjaHost(b2pUart,i2cPortName)

    # Apply 7.5V to PP7V5 before programming

    gnTest.resetAll()
    gnTest.enableLink()
    time.sleep(1)
    gnTest.enterLagunaTestMode()
    print('====== Laguna OTP programmer begins here ======')
    print('GN host: Laguna found, checking Laguna OTP...')

    laguna_otp_dump()

    if laguna_verify_otp_patch() == False: 
    #    if True:
    # begin OTP writes.  Modify this section to write different OTP bytes. 
        laguna_write_otp_word(0x06,0xBF,[0xb2,0x24,0x00,0x05]) #0x24B2 -> 0x00 
        laguna_write_otp_word(0x06,0xC0,[0x14,0x24,0x00,0X00]) #0x1405 -> 0x24 
        print('GN host: Patch is 100 percent completed')

    # patch CRC -- ONLY DO THIS ONCE OTP PATCH IS VERIFIED TO BE CORRECT.  Do not need to modify for your particular test run, it does all the calculations ~automagically~ and increments CRC pointer by 1 every time it is run.
        print('GN host: OTP update finished.  Patching Laguna CRC') 
        laguna_update_crc()

        cmd = gnTest.locustB2P.writeLagunaReg(LAGUNA_CRC_FAULT_REG,0xFF) #clear CRC Fault Register

        while gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_CMD_REG)[0] != 0: # KP added in order to prevent new commands from being issued while a previous command is happening
            pass

        cmd = gnTest.locustB2P.writeLagunaReg(LAGUNA_OTP_CMD_REG,0x20) #Do a full read of OTP Values + CRC

        while gnTest.locustB2P.readLagunaReg(LAGUNA_OTP_CMD_REG)[0] != 0: # KP added in order to prevent new commands from being issued while a previous command is happening
            pass

        print('GN host: Verifying patch')
        '''
        print('GN host: Resetting Laguna and verifying patch')
        gnTest.PMUReset()
        time.sleep(0.3)
        gnTest.resetAll()
        gnTest.enableLink()
        time.sleep(1)
        '''
        gnTest.enterLagunaTestMode()
        laguna_otp_dump()
        if laguna_verify_otp_patch():
#        print('GN host: New OTP revision: {rev:#x}'.format(rev=otp_rev))
            print('GN host: Laguna OTP patch completed successfully')
        else:
            print('GN host: Laguna OTP patch failed')
    else:
        print('GN host: Laguna OTP patch ALREADY completed successfully')
    # Close the FTDI ports
    gnTest.closePorts()
