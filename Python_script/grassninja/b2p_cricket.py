#python3
# HWTE Yan Li, 2020/05/10
# This script is to try b2p with cricket
# yan.li@apple.com
# DO NOT DISTRIBUTE THE CODE TO THE 3RD PARTY

import serial
import time
import struct
import random

class b2p():
    def __init__(self,Portname,Baudrate=921600,Timeout=5): 
        try:
            self.port = serial.Serial(Portname,baudrate=Baudrate,timeout=Timeout)
            self.port.flush()
        except:
            raise RuntimeError("Open serial port error: %s", Portname)

        self.debug = False
        self.sequence = 1 # B2P squence
        self.tx = bytearray(b'')
        self.rx = bytearray(b'')
        self.port.flush()
        self.crc32tab=[ 
            0x00000000, 0x04c11db7, 0x09823b6e, 0x0d4326d9, 0x130476dc, 
            0x17c56b6b, 0x1a864db2, 0x1e475005, 0x2608edb8, 0x22c9f00f, 
            0x2f8ad6d6, 0x2b4bcb61, 0x350c9b64, 0x31cd86d3, 0x3c8ea00a, 
            0x384fbdbd, 0x4c11db70, 0x48d0c6c7, 0x4593e01e, 0x4152fda9, 
            0x5f15adac, 0x5bd4b01b, 0x569796c2, 0x52568b75, 0x6a1936c8, 
            0x6ed82b7f, 0x639b0da6, 0x675a1011, 0x791d4014, 0x7ddc5da3, 
            0x709f7b7a, 0x745e66cd, 0x9823b6e0, 0x9ce2ab57, 0x91a18d8e, 
            0x95609039, 0x8b27c03c, 0x8fe6dd8b, 0x82a5fb52, 0x8664e6e5, 
            0xbe2b5b58, 0xbaea46ef, 0xb7a96036, 0xb3687d81, 0xad2f2d84, 
            0xa9ee3033, 0xa4ad16ea, 0xa06c0b5d, 0xd4326d90, 0xd0f37027, 
            0xddb056fe, 0xd9714b49, 0xc7361b4c, 0xc3f706fb, 0xceb42022, 
            0xca753d95, 0xf23a8028, 0xf6fb9d9f, 0xfbb8bb46, 0xff79a6f1, 
            0xe13ef6f4, 0xe5ffeb43, 0xe8bccd9a, 0xec7dd02d, 0x34867077, 
            0x30476dc0, 0x3d044b19, 0x39c556ae, 0x278206ab, 0x23431b1c, 
            0x2e003dc5, 0x2ac12072, 0x128e9dcf, 0x164f8078, 0x1b0ca6a1, 
            0x1fcdbb16, 0x018aeb13, 0x054bf6a4, 0x0808d07d, 0x0cc9cdca, 
            0x7897ab07, 0x7c56b6b0, 0x71159069, 0x75d48dde, 0x6b93dddb, 
            0x6f52c06c, 0x6211e6b5, 0x66d0fb02, 0x5e9f46bf, 0x5a5e5b08, 
            0x571d7dd1, 0x53dc6066, 0x4d9b3063, 0x495a2dd4, 0x44190b0d, 
            0x40d816ba, 0xaca5c697, 0xa864db20, 0xa527fdf9, 0xa1e6e04e, 
            0xbfa1b04b, 0xbb60adfc, 0xb6238b25, 0xb2e29692, 0x8aad2b2f, 
            0x8e6c3698, 0x832f1041, 0x87ee0df6, 0x99a95df3, 0x9d684044, 
            0x902b669d, 0x94ea7b2a, 0xe0b41de7, 0xe4750050, 0xe9362689, 
            0xedf73b3e, 0xf3b06b3b, 0xf771768c, 0xfa325055, 0xfef34de2, 
            0xc6bcf05f, 0xc27dede8, 0xcf3ecb31, 0xcbffd686, 0xd5b88683, 
            0xd1799b34, 0xdc3abded, 0xd8fba05a, 0x690ce0ee, 0x6dcdfd59, 
            0x608edb80, 0x644fc637, 0x7a089632, 0x7ec98b85, 0x738aad5c, 
            0x774bb0eb, 0x4f040d56, 0x4bc510e1, 0x46863638, 0x42472b8f, 
            0x5c007b8a, 0x58c1663d, 0x558240e4, 0x51435d53, 0x251d3b9e, 
            0x21dc2629, 0x2c9f00f0, 0x285e1d47, 0x36194d42, 0x32d850f5, 
            0x3f9b762c, 0x3b5a6b9b, 0x0315d626, 0x07d4cb91, 0x0a97ed48, 
            0x0e56f0ff, 0x1011a0fa, 0x14d0bd4d, 0x19939b94, 0x1d528623, 
            0xf12f560e, 0xf5ee4bb9, 0xf8ad6d60, 0xfc6c70d7, 0xe22b20d2, 
            0xe6ea3d65, 0xeba91bbc, 0xef68060b, 0xd727bbb6, 0xd3e6a601, 
            0xdea580d8, 0xda649d6f, 0xc423cd6a, 0xc0e2d0dd, 0xcda1f604, 
            0xc960ebb3, 0xbd3e8d7e, 0xb9ff90c9, 0xb4bcb610, 0xb07daba7, 
            0xae3afba2, 0xaafbe615, 0xa7b8c0cc, 0xa379dd7b, 0x9b3660c6, 
            0x9ff77d71, 0x92b45ba8, 0x9675461f, 0x8832161a, 0x8cf30bad, 
            0x81b02d74, 0x857130c3, 0x5d8a9099, 0x594b8d2e, 0x5408abf7, 
            0x50c9b640, 0x4e8ee645, 0x4a4ffbf2, 0x470cdd2b, 0x43cdc09c, 
            0x7b827d21, 0x7f436096, 0x7200464f, 0x76c15bf8, 0x68860bfd, 
            0x6c47164a, 0x61043093, 0x65c52d24, 0x119b4be9, 0x155a565e, 
            0x18197087, 0x1cd86d30, 0x029f3d35, 0x065e2082, 0x0b1d065b, 
            0x0fdc1bec, 0x3793a651, 0x3352bbe6, 0x3e119d3f, 0x3ad08088, 
            0x2497d08d, 0x2056cd3a, 0x2d15ebe3, 0x29d4f654, 0xc5a92679, 
            0xc1683bce, 0xcc2b1d17, 0xc8ea00a0, 0xd6ad50a5, 0xd26c4d12, 
            0xdf2f6bcb, 0xdbee767c, 0xe3a1cbc1, 0xe760d676, 0xea23f0af, 
            0xeee2ed18, 0xf0a5bd1d, 0xf464a0aa, 0xf9278673, 0xfde69bc4, 
            0x89b8fd09, 0x8d79e0be, 0x803ac667, 0x84fbdbd0, 0x9abc8bd5, 
            0x9e7d9662, 0x933eb0bb, 0x97ffad0c, 0xafb010b1, 0xab710d06, 
            0xa6322bdf, 0xa2f33668, 0xbcb4666d, 0xb8757bda, 0xb5365d03, 0xb1f740b4]

    def close(self):
        self.port.flush()
        self.port.close()

    def sendCommand(self,seq,cmd,payload): #payload is an array []
        if self.port.is_open:
            txdata = [0xff,0xb2]
            data_len= len(payload)+11
            txdata.append((data_len&0xff)) #append ls byte, big endian
            txdata.append((data_len&0xff00)>>8) #append ms byte, big endian
            txdata.append(seq)
            txdata.append((cmd&0xff)) #append ls byte, big endian
            txdata.append((cmd&0xff00)>>8) #append ms byte, big endian
            for i in range(len(payload)): 
                txdata.append(payload[i])
            crc_pkt = self.crc32_calc_done(test.crc32_calc(txdata)) 
            txdata.append(crc_pkt&0xff)
            txdata.append((crc_pkt>>8)&0xff)
            txdata.append((crc_pkt>>16)&0xff)
            txdata.append((crc_pkt>>24)&0xff)
            self.tx =  bytearray(txdata)
            if self.debug: print(self.tx)
            self.port.write(self.tx)
        else:
            raise RuntimeError("Open serial port error: %s", self.port.name)

    def sendStop(self): #payload is an array [], this will stop Hearst + cricket from running in a dead loop for some b2p commands like ping
        if self.port.is_open:
            txdata = []
            for i in range(1028):
                txdata.append(0x00)
            txdata =  bytearray(txdata)
            self.port.write(txdata)
            rxdata = self.port.read_all()
            print(txdata)
            print(rxdata)
        else:
            raise RuntimeError("Open serial port error: %s", self.port.name)

    def sendCMD(self, CMD): #payload is a byte, manual command to MCU
        if self.port.is_open:
            txdata =  bytearray(CMD)
            self.port.write(txdata)
#            time.sleep(1)
            rxdata = self.port.read_all()
            print(txdata)
            print(rxdata)
        else:
            raise RuntimeError("Open serial port error: %s", self.port.name)
    
    def readResponse(self,seq,cmd,timeout): # timeout in seconds
        if self.port.is_open:
            self.rx = bytearray(b'')
            TimeBegin = time.time()
            rxdata_Length = 65535
            while ((time.time()-TimeBegin) < timeout):
                data = self.port.read_all()
                if data: 
                    self.rx +=bytearray(data) 
#                    if (len(self.rx) >= 2*self.rx[2]+1) and (self.rx[2]>12): 
                    if (len(self.rx) >= self.rx[2]) and (self.rx[2]>12): 
                        break
            if self.debug: print(self.rx)
#            self.removeCricketEcho()
        return self.rx[8:-4]

    def SendRead(self,seq,cmd,payload,timeout):
        self.sendCommand(seq,cmd,payload) #payload is an array []
        response = self.readResponse(seq,cmd,timeout)
        return response
    
    def removeCricketEcho(self):
        packetLength = self.tx[2]
        self.rx = self.rx[packetLength:]

    def TunnelOpen(self,timeout):
        response = self.SendRead(self.sequence,0x10,[0,1],timeout)
        self.sequence += 1
        return response

    def TunnelClose(self,timeout):
        response = self.SendRead(self.sequence,0x10,[0,0],timeout)
        self.sequence += 1
        return response

    def TunnelCmd(self,cmd,timeout):
        full_response=""
        payload = [0,1]+list(cmd.encode('utf-8'))+[0x0d,0x0a]
        response = self.SendRead(self.sequence,0x12,payload,timeout)
        full_response = response.decode('utf-8')
        if self.debug: 
            print(response.decode('utf-8')) 
        self.sequence += 1
        EOF = False
        while not EOF: 
            payload = [0,1] 
            response = self.SendRead(self.sequence,0x12,payload,timeout) 
            full_response += response.decode('latin-1')
            if self.debug:
                print(response.decode('utf-8')) 
            self.sequence += 1
            EOF = (response[-1] == 0x20) and (response[-2] == 0x5d)
        
        print(full_response)
        return full_response 

    def GetDeviceInfo(self): # DFU mode is required
        print('\n' + "**** Getting Device Info Payload *** ")
        RSP = self.SendRead(self.sequence,0x02,[0],0.2)
        print(list(RSP))
        [stat, chipidLow, chipidHigh, boardidLow, boardidHigh, securityEpoch, prodStatus, securityMode, securityDomain, ecid, nonce1, nonce2, nonce3, nonce4, chipRev] = struct.unpack('>BBBBBBBBBQ4QB', RSP)
        chipid = (chipidHigh << 8 | chipidLow)
        boardid = (boardidHigh << 8 | boardidLow)
        temp = 0
        while ecid != 0:
            temp = (temp << 8) + (ecid & 0xFF)
            ecid = ecid >> 8
        ecid = temp
        print('\n' + "ChipId = 0x%x, BoardID = 0x%x, Epoch = %d, Prod = %s, SecMode = %s, SecDom = %d, ECID = 0x%x, Nonce1 = 0x%x, Nonce2 = 0x%x, Nonce3 = 0x%x, Nonce4 = 0x%x, CRev = %d" % (chipid, boardid, securityEpoch, prodStatus, securityMode, securityDomain, ecid, nonce1, nonce2, nonce3, nonce4, chipRev))
        self.sequence +=1

    def ping(self,timeout): # b2p ping device in DFU mode
        print("\n*** Pinging Device ***") 
        rsp = self.SendRead(self.sequence,0x00,[0, 2],timeout)
        print(list(rsp)) 
        if (rsp[0] ==2):
            print("B2P device found\n")
        self.sequence +=1


# clock is used to check the frequency of a locust chip
# total number of bits sent = 10 x (number of data + 13), 13 is due to header and CRC

    def Clock(self):
        rsp = self.SendRead(self.sequence,0x10, [4,1], 0.2)
        payload=[]
        for i in range(100): 
            payload.append(0x55)
        rsp = self.SendRead(self.sequence,0x12, [4,1]+payload, 0.2)
        rsp = self.SendRead(self.sequence,0x10, [4,0], 0.2)

    def Reset(self):
        rsp = self.SendRead(self.sequence,0x08,[0,255,255],0.2)
        self.sequence = 1

    def blq(self,N,timeout): #buddy link quality check
        tx = bytearray(b'')
        rx = bytearray(b'')
        tx_len = 0
        rx_len = 0
        err = 0
        print("\nBLQ test\n")
        random.seed(time.time())
        payload = []
        Nloops = round(N/(250-7-4))
        Nresidue = N%(250-7-4)

        time0 = time.time()
        for i in range(Nloops):
            for j in range(250-7-4): 
                payload.append(random.randint(0,255)) 
            rx = rx + self.SendRead(0, 0x5e,payload,timeout) 
            tx = tx + self.tx[7:-4] 
            payload = []

        payload = []
        for i in range(Nresidue):
            payload.append(random.randint(0,255))

        rx = rx + self.SendRead(0, 0x5e,payload,timeout) 
        time1 = time.time()
        tx = tx + self.tx[7:-4] 

        tx_len = len(tx)
        rx_len = len(rx)

        # comparison
        m = 0
        if (tx != rx):
            for Abyte in tx:
                if(rx[m] != Abyte):
                    err = err + 1
                    m = m + 1

        print("BLQ: TX bytes %d, RX bytes %d, Error %d\n" %(tx_len, rx_len, err))
        print('Test finished in %f s\n' %(time1-time0))

# Buddy Test Packet uses the ping command and has 12 additional bytes of payload.
# The first 8 bytes of the payload has the following word 0x00FF00AA5533CC01 and could be left shifted by upto 7.
# Packet tx count is in the last 4 bytes.
#    def SendTestPacket(self,testPacketSize, i):
#        cmd = 0x5E
#        payload = [] 
#        index = 0 
#        srand(tmrGetCounter_ms())
#
#        if(testPacketSize == 8): 
#            tw = 0x00FF00AA5533CC01 << (i % 8) 
#            uint32_t * wp = (uint32_t *) &tw;
#    trgUInt32ToBigEndBuf(wp[1], &payload[0]);
#    trgUInt32ToBigEndBuf(wp[0], &payload[4]);
#    trgUInt32ToBigEndBuf(i, &payload[8]);
#
#    return buddyMasterSendPacket(bud, BUDDY_CMD_PING, testPacketSize + 1 + 3, &payload[0]);
#  }
#  else
#  {
#    for(index = 0; index < testPacketSize; index++)
#    {
#      payload[index] = rand()%256;
#    }
#    return buddyMasterSendPacket(bud, BUDDY_CMD_PING, testPacketSize + 3, &payload[0]);
#  }
#}
    # Data is a byte
    def crc32_get(self,crc, data): 
        crc = (crc << 8) ^ self.crc32tab[((crc >> 24) ^ data) & 0xFF] 
        return crc

#Calculate CRC, when running over buffer with CRC included the result should be 0 for good CRC */
#Data is a byte array, data=[0x00,0x23,0xff]
    def crc32_calc(self,data): 
        crc = 0 
        i=0 
        N=len(data)
        while (N>0): 
            crc = self.crc32_get(crc, data[i]) 
            i=i+1 
            N=N-1 
        return crc

#data is a byte array, continue the CRC calculation
    def crc32_calc_cont(self,crc, data): 
        i=0 
        N=len(data)
        while (N>0): 
            crc = self.crc32_get(crc, data[i]) 
            i=i+1 
            N=N-1 
        return crc

    def crc32_calc_done(self,crc): 
        return ~crc & 0xFFFFFFFF

if __name__ == '__main__': 
    Debug_UART ={ 
#            'portname': '/dev/cu.usbserial-HLK26010',
            'portname': '/dev/cu.usbserial-142300',
#            'portname': '/dev/cu.usbserial-HLK12210',
            'baudrate': 921600,
            'timeout':10
            }
    test= b2p(Debug_UART['portname'],Baudrate=Debug_UART['baudrate'],Timeout=Debug_UART['timeout'])
    test.debug = True 
#   test.sendStop()
    test.sendCMD([0x02,0x00, 0x00, 0x0D,0x0A]) #disable 5V charger
    time.sleep(0.4)
    test.sendCMD([0x12,0x00, 0x00, 0x0D,0x0A]) #Enable 5V charger
    time.sleep(0.2)
    test.sendCMD([0x01,0xa8, 0x58, 0x0D,0x0A]) #force DFU mode RESETCODE, the mode can't be recovered by hard reset or crabs reset
#    test.sendCMD([0x01,0x80, 0x80, 0x0D,0x0A]) #force reset RESETCODE, exit from the force dfu mode
#    time.sleep(1)
#    test.ping(0.1)
#    test.sendCMD([0x04,0x00, 0x00, 0x0D,0x0A]) #disable 5V charger

#    for i in range(300):
#       test.ping(0.1)
#        test.sendStop()
#       time.sleep(0.1)

#    for i in range(125,250,25):
#        test.sendCMD([0x50,i,0x00,0x0D,0x0A])
#        time.sleep(0.05)
#    test.sendCMD([0x3,0x0D,0x0A])
#    time.sleep(0.2)
#    test.sendCMD([0x04,0x0D,0x0A])
#    time.sleep(5)
#    test.sendCMD([0x03,0x0D,0x0A])
#    test.sendStop()
#    test.GetDeviceInfo()
#    test.blq(9096,0.3)
#    rsp = test.TunnelOpen(0.1)
#    rsp = test.TunnelCmd('ft version',0.1)
#    rsp = test.TunnelCmd('help',0.1)
#    rsp = test.TunnelCmd('gpio help',0.1)
#    rsp = test.TunnelCmd('ft help',0.1)
#    rsp = test.TunnelCmd('ft reset',0.1) # After reset command, there will be no response from DUT
#    rsp = test.TunnelClose(0.1)
#    rsp = test.Clock() # for frequency measurment
#    rsp = test.Reset()