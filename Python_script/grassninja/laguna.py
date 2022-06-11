#python3
# HWTE Yan Li, 2020/05/10
# yan.li@apple.com
# DO NOT DISTRIBUTE THE CODE TO THE 3RD PARTY

import struct
import time
from testcmds import testCmd

testCmd = testCmd() 
secureI2CAddr = 0x22 
debugI2CAddr = 0xE8

class powerState():
  def __init__(self):
    self.reg= {
    'power_state_status':0x2406,
    'power_state_target':0x2407,
    'power_state_force':0x2408,
    'buck0_onoff': 0x24ab,
    'buck1_onoff': 0x24ac,
    'buck2_onoff': 0x24ad,
    'buck3_onoff': 0x24ae,
    'buck4_onoff': 0x24af,
    'buck5_onoff': 0x24b0,
    'ldo1_onoff': 0x24b1,
    'ldo2_onoff': 0x24b2,
    'ldo3_onoff': 0x24b3,
    'ls_a0_onoff': 0x24b4,
    'ls_b0_onoff': 0x24b5,
    'ls_b1_onoff': 0x24b6,
    'ls_c0_onoff': 0x24b7,
    'ls_c1_onoff': 0x24b8,
    'ls_c2_onoff': 0x24b9,
    'ls_hp_onoff': 0x24ba,
    'reset_out_l_onoff': 0x24bb,
    'bat_iso_allow_onoff': 0x24bc,
    'bat_charging_allow_onoff': 0x24bd,
    'pmu_ldo_src_onoff':0x24be,
    'secure_i2c_onoff': 0x24bf,
    'ccadc_onoff': 0x24c0
    }
  def sleep(self):
    testCmd.i2cWriteReg16(debugI2CAddr,self.reg['power_state_target'],0x00)
  def off(self):
    testCmd.i2cWriteReg16(debugI2CAddr,self.reg['power_state_target'],0x01)
  def status(self):
    rsp = testCmd.i2cReadReg16(debugI2CAddr,self.reg['power_state_status'])
    return rsp
  
class reg:
    def __init__(self):
      self.test ={
	    'test_reg_en0': 0x3100,
	    'test_reg_en1': 0x3101,
	    'test_reg_en2': 0x3102,
	    'test_reg_en3': 0x3103,
	    'test_reg_en_clr': 0x3104
      } 
      self.clk32k = {
      'clk32k_ext_ctrl':0x3003, #bit 0 select source
      'clk32k_ext_en':0x3004 # bit 0 turn on/off
      }
      self.i2c = {
      'i2c_addr1': 0x1420,
      'i2c_addr2': 0x1421,
      'sec_i2c_cfg': 0x1422,
      'dbg_i2c_cfg': 0x1423,
      'dbg_i2c_ctrl_dis': 0x1424,
      'i2c_misc': 0x1425,
      'i2c_debug_status': 0x1439,
      'i2c_debug1_status': 0x143a,
      'i2c_gpio1': 0x1869,
      'i2c_gpio2': 0x186a,
      'i2c_gpio3': 0x186b,
      'i2c_cfg1': 0x186c,
      'i2c_cfg2': 0x186d,
      'secure_i2c_onoff': 0x24bf
      }

class gpio:
    def __init__(self):
      self.gpio = { 
      'gpio0_cfg1': 0x1814, 
      'gpio1_cfg1': 0x1815,
      'gpio2_cfg1': 0x1816,
      'gpio3_cfg1': 0x1817,
      'gpio4_cfg1': 0x1818,
      'gpio5_cfg1': 0x1819,
      'gpio6_cfg1': 0x181a,
      'gpio7_cfg1': 0x181b,
      'gpio8_cfg1': 0x181c,
      'gpio9_cfg1': 0x181d,
      'gpio10_cfg1': 0x181e,
      'gpio11_cfg1': 0x181f,
      'gpio12_cfg1': 0x1820,
      'gpio13_cfg1': 0x1821,
      'gpio14_cfg1': 0x1822, #AMUXOUT_AX
      'gpio15_cfg1': 0x1823, #AMUXOUT_AY
      'gpio16_cfg1': 0x1824, #WDOG
      'gpio17_cfg1': 0x1825, #FORCE_DFU
      'gpio18_cfg1': 0x1826, #DFU_STATUS
      'gpio19_cfg1': 0x1827, #DOCK_CONNECT
      'gpio20_cfg1': 0x1828, #USB_EN
      'gpio21_cfg1': 0x1829, #KIS_DFU_SELECT
      'gpio22_cfg1': 0x182a, #UVP_TRIG
      'gpio0_cfg2': 0x182b,
      'gpio1_cfg2': 0x182c,
      'gpio2_cfg2': 0x182d,
      'gpio3_cfg2': 0x182e,
      'gpio4_cfg2': 0x182f,
      'gpio5_cfg2': 0x1830,
      'gpio6_cfg2': 0x1831,
      'gpio7_cfg2': 0x1832,
      'gpio8_cfg2': 0x1833,
      'gpio9_cfg2': 0x1834,
      'gpio10_cfg2': 0x1835,
      'gpio11_cfg2': 0x1836,
      'gpio12_cfg2': 0x1837,
      'gpio13_cfg2': 0x1838,
      'gpio14_cfg2': 0x1839, #AMUXOUT_AX
      'gpio15_cfg2': 0x183a, #AMUXOUT_AY
      'gpio16_cfg2': 0x183b, #WDOG
      'gpio17_cfg2': 0x183c, #FORCE_DFU
      'gpio18_cfg2': 0x183d, #DFU_STATUS
      'gpio19_cfg2': 0x183e, #DOCK_CONNECT
      'gpio20_cfg2': 0x183f, #USB_EN
      'gpio21_cfg2': 0x1840, #KIS_DFU_SELECT
      'gpio22_cfg2': 0x1841, #UVP_TRIG
      'status3': 0x180a, #status of gpio 7-0
      'status4': 0x180b, #status of gpio 15-8
      'status5': 0x180c, #status of gpio 22-16
      'CLK32K_SOC_CFG1':0x1860,
      'CLK32K_SOC_CFG2':0x1861,
      }
      self.supply_cfgLV = {
      'buck3_1v2': 0x0,
      'lsb0_1v2': 0x1,
      'buck5_1v8': 0x2,
      'lsc0_1v8': 0x3 
       } 
      self.supply_cfgHV = {
      'vddmain_3v8': 0x0,
      'ldo2_2v8': 0x1,
      'buck5_1v8': 0x2,
      'lsc0_1v8': 0x3 
       } 
      self.pullup_cfg = { #bit 2-0
      'none': 0x00,
      'pullup': 0x01, #default 200k
      'pulldown': 0x2, #default 200k
      'pullup_25k': 0x05,
      'pulldown_25k': 0x6
       } 
      self.io_cfg= {
      'input':0x0, # for input
      'outputPP':0x1, # for output
      'outputOD':0x2, # for ouptut
      'disabled':0x3 # for analog input like GPADC
      } 
      return

    def read(self,ioName): # read('gpio0')
        pin = int(ioName.split('gpio',)[1])
        if (pin<8): register = self.gpio['status3']
        else:
          if (pin>15): 
            register = self.gpio['status5']
            pin -= 16
          else: 
            register = self.gpio['status4']
            pin -= 8
        data = testCmd.i2cReadReg16(debugI2CAddr,register)
        data = (data >> pin) & 0b1
        return data


    def write(self,ioName,data): # write('gpio0', 1)
        pin = int(ioName.split('gpio',)[1])
        if (pin<8): register = self.gpio['status3']
        else:
          if (pin>15): 
            register = self.gpio['status5']
            pin -= 16
          else: 
            register = self.gpio['status4']
            pin -= 8
        data = ((data & 0b1) << pin)&0xff
        testCmd.i2cWriteReg16(debugI2CAddr,register,data)
        return data

    def config(self, ioName, function, pullup, supply):  # config('gpio0', 'input', 'pullup', 'lv')
      if (self.io_cfg[ioName] == 0 ):
        function_cfg = { # for input IO
	      'gpio':0x0,
	      'button':0x1,
	      'reqestdfu':0x2, # assert before resetIn assertion to enter DFU mode
	      'resetin':0x3,
	      'shdn':0x4, # stop the whole PMU completely after assertion
	      'wdog':0x5, # trigger a reset after assertion
	      'flash_busy':0x6
        }
      else: 
        function_cfg= { # for output IO
	      'gpio':0x0,
	      'i2c':0X1, # NEED TO CONFIGURE THE I2C REGISTERS AS WELL
	      'linkstat0':0x2,
	      'linkstat1':0x3,
	      'linkstat2':0x4,
	      'linkstat3':0x5,
	      'pwrseq0':0x6,
	      'pwrseq1':0x7,
	      'pwrseq2':0x8,
	      'pwrseq3':0x9,
	      'reset_out_l':0Xa,
	      'crash_l':0Xb,
	      'awake':0Xc,
	      'sleep':0Xd,
	      'vddmain_drive_notok':0xE,
	      'bat_isolate_status':0xF,
	      'rtc_32khz':0x10,
	      'charger_ind':0x12, # 0x12 is also for special functions on gpio14-22
	      'adcseq1':0X13,
	      'adcseq2':0X14,
	      'adcseq3':0X15,
	      'adcseq4':0X16,
	      'chg_det_comp':0X17,
	      'bat_iso_comp':0X18,
	      'uvlo_comp':0X19,
	      'raw_1hz':0X1c,
	      'dmux_sel':0x1D
        }
        cfg1 = (self.supply_cfgLV[supply]<<3) + self.pullup_cfg[pullup] & 0b111 
        cfg2 = (function_cfg[function]<<6) & 0xff
        testCmd.i2cWriteReg16(debugI2CAddr,self.gpio[ioName+'_cfg1'],cfg1)
        testCmd.i2cWriteReg16(debugI2CAddr,self.gpio[ioName+'_cfg2'],cfg2)

class laguna():
    def __init__(self):
      self.reg = reg()
      self.gpio = gpio() 
      self.powerState = powerState()
      return

    def HWInfo(self):
      OTP_REV = testCmd.i2cReadReg16(self,debugI2CAddr,0x1405)
      PLATFORM_ID = testCmd.i2cReadReg16(self,debugI2CAddr,0x1406)

    def testModeEn(self):
      testCmd.i2cWriteReg16(self.debugI2CAddr,self.reg.test['test_reg_en0'],0x61)
      testCmd.i2cWriteReg16(self.debugI2CAddr,self.reg.test['test_reg_en1'],0x45)
      testCmd.i2cWriteReg16(self.debugI2CAddr,self.reg.test['test_reg_en2'],0x72)
      testCmd.i2cWriteReg16(self.debugI2CAddr,self.reg.test['test_reg_en3'],0x4F)
      return
