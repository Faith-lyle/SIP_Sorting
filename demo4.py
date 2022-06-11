from Python_script import logDriver, serialPort
import time

start = (time.time())
log = logDriver.LogDriver("log.txt")
port = '/dev/cu.kis-14210000-ch-2'
term = serialPort.SerialPort(port, log_driver=log)
mic1_cmd = ['siggen clear all\n',
            'audio config mic1 memory record 48kHz 3MHz 10\n',
            'audio leap apply_cal unity_gain\n',
            'audio start 0\n',
            'audio stop\n',
            'audio dump\n']

mic2_cmd = ['siggen clear all\n',
            'audio config mic2 memory record 48kHz 3MHz 10\n',
            'audio leap apply_cal unity_gain\n',
            'audio start 0\n',
            'audio stop\n',
            'audio dump\n']


def mic_test(cmd_list):
    content = ''
    result = 0
    for cmd in cmd_list:
        text = term.send_and_read_until(cmd,timeout=2)
        if cmd == 'audio dump\n':
            results = text.split(":")
            for res in results[-41:-1]:
                for a in range(3):
                    ok1 = res[a * 16 : (a + 1) * 16]
                    ok2 = res[(a + 1) * 16:(a + 2) * 16]
                    if ok1 == ok2:
                        result += 1
        content += text
        time.sleep(0.5)
    if result < 80:
        return True
    else:
        return False


print(mic_test(mic1_cmd))
time.sleep(1)
print(mic_test(mic2_cmd))
print(time.time() - start)
