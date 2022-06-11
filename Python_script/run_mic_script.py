# coding=utf-8
"""
@author:Long.Hou
@time: 2022/03/07
@email:long.hou2@luxshare-ict.com
"""
import socket
import argparse
import time, os, re
import logDriver, serialPort

term = None
# 脚本文件夹路径
path = '/Users/user/Desktop/Python_Project/H28_SIP_Sorting/Python_script'


def write_csv_file(csv_file, data_list):
    if not os.path.exists(csv_file):
        header = 'DUT_SN,Slot,TestTime,Result,Equipment Init,Create Serial Port,Open SerialPort,Read DUT MLB SN,' \
                 'Read DUT Version,MIC1 Init,MIC1 Test,MIC2 Init,MIC2 Test,Close SerialPort,Equipment Reset\n' \
                 'Upper Limit ----->\nLower Limit ----->\n'
        with open(csv_file, 'w') as f:
            f.write(header)
    with open(csv_file, 'a') as f:
        text = ''
        for data in data_list:
            text += '{},'.format(data)
        f.write(text+'\n')  # 将数据写入文件


def create_serial_port():
    log.item_start("Create Serial Port")
    result = False, "FAIL"
    output = ''
    # 调用终端执行cmd并获取输出内容
    try:
        output += os.popen("python3 {}/grassninja/grassninja.py -p {}".format(path, port)).read()
        time.sleep(1)
        output += os.popen("ls /dev/cu.*").read()
        print(output)
        if virtual_port in output:
            result = True, "PASS"
    except Exception as e:
        output += str(e)
    log.set_item_result(output, "PASS" if result[0] else "FAIL")
    log.item_end('Create Serial Port')
    return result


# opne serial port
def open_serial_port():
    log.item_start("Open Serial Port")
    result = False, "FAIL"
    global term
    try:
        term = serialPort.SerialPort(virtual_port, log_driver=log)
        result = True, "PASS"
        log.set_item_result("Port:{} Baudrate:921600".format(virtual_port), "PASS")
    except Exception as e:
        log.set_item_result(str(e), "FAIL")
    log.item_end("Open Serial Port")
    return result


# close serial port
def close_serial_port():
    global term
    log.item_start("Close Serial Port")
    result = False, 'FAIL'
    if term:
        try:
            term.close_port()
            result = True, 'PASS'
            log.set_item_result("Port:{} Close Successful".format(virtual_port), "PASS")
        except Exception as e:
            log.set_item_result(str(e), "FAIL")
    log.item_end("Close Serial Port")
    return result


# 读取产品MLB#
def read_product_mlb():
    log.item_start("Read Product MLB")
    result = False, "FAIL"
    output = ''
    try:
        output += term.send_and_read_until("syscfg print MLB#\n", timeout=2)
        if '> syscfg:ok' in output:
            flag = re.findall(r'syscfg:ok "(.*)?"', output)
            if len(flag) == 1:
                result = True, flag[0]
                log.set_item_result(flag[0], "PASS")
        else:
            log.set_item_result("None", "FAIL")
    except Exception as e:
        output += str(e)
        log.set_item_result(output, "FAIL")
    log.item_end("Read Product MLB")
    return result


# 读取产品FW
def read_product_fw():
    log.item_start("Read Product FW")
    result = False, "FAIL"
    output = ''
    try:
        output += term.send_and_read_until("ft version\n", timeout=2)
        if '> ft:ok' in output:
            flag = re.findall(r'ft:ok (.*)?\n', output)
            if len(flag) == 1:
                result = True, flag[0]
                log.set_item_result(flag[0], "PASS")
        else:
            log.set_item_result("None", "FAIL")
    except Exception as e:
        output += str(e)
        log.set_item_result(output, "FAIL")
    log.item_end("Read Product FW")
    return result


# MIC1 init
def mic1_init():
    log.item_start("MIC1 Init")
    result = False, "FAIL"
    output = ''
    mic1_cmd = ['siggen clear all\n',
                'audio config mic1 memory record 48kHz 3MHz 10\n',
                'audio leap apply_cal unity_gain\n',
                'audio start 0\n',
                'audio stop\n']
    try:
        for cmd in mic1_cmd:
            output += term.send_and_read_until(cmd, timeout=2)
            if 'audio:ok' in output:
                result = True, "PASS"
                log.set_item_result("PASS", "PASS")
            else:
                log.set_item_result("None", "FAIL")
    except Exception as e:
        output += str(e)
        log.set_item_result(output, "FAIL")
    log.item_end("MIC1 Init")
    return result


# MIC2 init
def mic2_init():
    log.item_start("MIC2 Init")
    result = False, "FAIL"
    output = ''
    mic2_cmd = ['siggen clear all\n',
                'audio config mic2 memory record 48kHz 3MHz 10\n',
                'audio leap apply_cal unity_gain\n',
                'audio start 1\n',
                'audio stop\n']
    try:
        for cmd in mic2_cmd:
            output += term.send_and_read_until(cmd, timeout=2)
            if 'audio:ok' in output:
                result = True, "PASS"
                log.set_item_result("PASS", "PASS")
            else:
                log.set_item_result("None", "FAIL")
    except Exception as e:
        output += str(e)
        log.set_item_result(output, "FAIL")
    log.item_end("MIC2 Init")
    return result


# MIC1 test
def mic1_test():
    log.item_start("MIC1 Test")
    result = False, "FAIL"
    output = ''
    value = 0
    try:
        output += term.send_and_read_until("audio dump\n", timeout=2)
        if 'audio:ok' in output:
            results = output.split(":")
            for res in results[-41:-1]:
                for a in range(3):
                    ok1 = res[a * 16: (a + 1) * 16]
                    ok2 = res[(a + 1) * 16:(a + 2) * 16]
                    if ok1 == ok2:
                        value += 1
            if value < 80:
                result = True, "PASS"
                log.set_item_result(str(value), "PASS")
            else:
                log.set_item_result(str(value), "FAIL")
        else:
            log.set_item_result("None", "FAIL")
    except Exception as e:
        output += str(e)
        log.set_item_result(output, "FAIL")
    log.item_end("MIC1 Test")
    return result


# MIC2 test
def mic2_test():
    log.item_start("MIC2 Test")
    result = False, "FAIL"
    output = ''
    value = 0
    try:
        output += term.send_and_read_until("audio dump\n", timeout=2)
        if 'audio:ok' in output:
            results = output.split(":")
            for res in results[-41:-1]:
                for a in range(3):
                    ok1 = res[a * 16: (a + 1) * 16]
                    ok2 = res[(a + 1) * 16:(a + 2) * 16]
                    if ok1 == ok2:
                        value += 1
            if value < 80:
                result = True, "PASS"
                log.set_item_result(str(value), "PASS")
            else:
                log.set_item_result(str(value), "FAIL")
        else:
            log.set_item_result("None", "FAIL")
    except Exception as e:
        output += str(e)
        log.set_item_result(output, "FAIL")
    log.item_end("MIC2 Test")
    return result


# 设备初始化
def device_init():
    log.item_start("Device Init")
    result = False, "FAIL"
    output = ''
    try:
        result = True, "PASS"
    except Exception as e:
        output += str(e)
        log.set_item_result(output, "FAIL")
    log.item_end("Device Init")
    return result


# 设备复位
def device_reset():
    log.item_start("Device Reset")
    result = False, "FAIL"
    output = ''
    try:
        result = True, "PASS"
    except Exception as e:
        output += str(e)
        log.set_item_result(output, "FAIL")
    log.item_end("Device Reset")
    return result


def get_argument():
    Parser = argparse.ArgumentParser()
    Parser.add_argument("-s", "--slot", help="Slot Name")
    Parser.add_argument("-sp", "--serialPort", help="serialPort")
    Parser.add_argument("-vp", "--virtualPort", help="virtualPort")
    Parser.add_argument("-f", "--logPath", help="logPath")
    Parser.add_argument("-n", "--SN", help="SN")
    arg = Parser.parse_args()
    return arg


def create_socket():
    client = None
    # 创建socket对象
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
        client.connect(("localhost", 6001))
    except socket.error as msg:
        print("Create Socket Failed. Error Code: " + str(msg[0]) + " Message: " + msg[1])
        exit()
    return client


if __name__ == '__main__':
    func_list = [device_init, create_serial_port, open_serial_port, read_product_mlb, read_product_fw, mic1_init,
                 mic1_test, mic2_init, mic2_test, close_serial_port, device_reset]
    args = get_argument()
    # 检查arg参数的长度
    if args.slot is None or args.serialPort is None or args.virtualPort is None or args.logPath is None or args.SN is None:
        print("Please input all parameters.")
        exit()
    port = args.serialPort
    virtual_port = args.virtualPort
    log_path = args.logPath + "/{}".format(time.strftime("%Y-%m-%d", time.localtime()))
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
    log = logDriver.LogDriver("{}/{}.log".format(log_path, args.SN))
    client = create_socket()  # 创建socket对象
    result = [args.SN,args.slot,time.strftime("%H:%M:%S", time.localtime())]
    result_flag = True
    time.sleep(0.5)
    for i, func in enumerate(func_list):
        content = '-FAIL-'
        try:
            result1, content = func()
            if result1:
                client.send("[INFO]::[{}]::[{}]::[-PASS-]".format(args.slot, i + 1).encode("gbk"))
            else:
                client.send("[INFO]::[{}]::[{}]::[-FAIL-]".format(args.slot, i + 1).encode("gbk"))
                result_flag = False
        except Exception as e:
            result_flag = False
            client.send("[INFO]::[{}]::[{}]::[-FAIL-]".format(args.slot, i + 1).encode("gbk"))
        time.sleep(0.5)
        result.append(content.replace(",", " "))
    if result_flag:
        result.insert(3, 'PASS')
        client.send("[EXIT]::[{}]::[1]::[PASS]".format(args.slot).encode("gbk"))
    else:
        result.insert(3, 'FAIL')
        client.send("[EXIT]::[{}]::[1]::[FAIL]".format(args.slot).encode("gbk"))
    client.close()
    write_csv_file("{}/{}.csv".format(log_path,time.strftime("%Y%m%d",time.localtime())), result)
