#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:Long.Hou
@file: main.py.py 
@time: 2022/03/04 
@email:long.hou2@luxshare-ict.com
"""
import tkinter as tk
import os, csv, socket, json
import subprocess
import threading
import time
from tkinter import ttk, messagebox
from threading import Timer


class TestItem:
    def __init__(self, **args):
        if "TestName" in args.keys():
            self._TestName = args['TestName']
        else:
            self._TestName = None
        if "TestResult" in args.keys():
            self._TestResult = args['TestResult']
        else:
            self._TestResult = None
        if "TestLower" in args.keys():
            self._TestLower = args['TestLower']
        else:
            self._TestLower = None
        if "TestUpper" in args.keys():
            self._TestUpper = args['TestUpper']
        else:
            self._TestUpper = None
        if "TestEnabled" in args.keys():
            if args["TestEnabled"].lower() == "true":
                self._IsEnabled = True
            else:
                self._IsEnabled = False
        else:
            self._IsEnabled = False
        if 'TestCmd' in args.keys():
            self._TestCmd = args["TestCmd"]
        else:
            self._TestCmd = None
        if "ReMarket" in args.keys():
            self._ReMarket = args["ReMarket"]
        else:
            self._ReMarket = None
        if "DecisionMode" in args.keys():
            self._DecisionMode = args["DecisionMode"]
        else:
            self._DecisionMode = None
        if "TestMode" in args.keys():
            self._TestMode = args["TestMode"]
        else:
            self._TestMode = None
        if "TestValue" in args.keys():
            self._TestValue = args["TestValue"]
        else:
            self._TestValue = None
        if "ReTestTime" in args.keys():
            self._ReTestTime = args["ReTestTime"]
        else:
            self._ReTestTime = None

    @property
    def ReTestTime(self):
        return self._ReTestTime

    @property
    def TestResult(self):
        return self._TestResult

    @property
    def TestMode(self):
        return self._TestMode

    @TestResult.setter
    def TestValue(self, value):
        self._TestResult = value

    @property
    def DecisionMode(self):
        return self._DecisionMode

    @property
    def ReMarket(self):
        return self._ReMarket

    @ReMarket.setter
    def ReMarket(self, value):
        self._ReMarket = value

    @property
    def TestValue(self):
        return self._TestValue

    @TestValue.setter
    def TestValue(self, value):
        self._TestValue = value

    @property
    def TestName(self):
        return self._TestName

    @TestName.setter
    def TestName(self, name):
        self._TestName = name

    @property
    def TestLower(self):
        return self._TestLower

    @TestLower.setter
    def TestLower(self, Lower):
        self._TestLower = Lower

    @property
    def TestUpper(self):
        return self._TestUpper

    @TestUpper.setter
    def TestUpper(self, upper):
        self._TestUpper = upper

    @property
    def isEnabled(self):
        return self._IsEnabled

    @isEnabled.setter
    def isEnabled(self, enabled):
        self._IsEnabled = enabled

    @property
    def TestCmd(self):
        return self._TestCmd


# 读取json文件
def read_json(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f, encoding='utf-8')
        return data


def read_test_plant(file_path):
    test_items = []
    if not os.path.exists(file_path):
        messagebox.showerror("错误", "未找到测试文档，请检查配置文件", messagebox.OK)
        exit()
    with open(file_path, "r") as f:
        reader = list(csv.reader(f))
        for text in reader[1:]:
            map1 = dict(zip(reader[0], text))
            item = TestItem(**map1)
            test_items.append(item)
    return test_items

    '''
    格式
    正常测试
    [INFO]::[DadaTime]::[slot]::[row]::[TestItem]::[value]::[result]::[upper]::[lower]
    结束 
    [EXIT]::[DadaTime]::[slot]::[result]
    错误
    [ERROR]::[DadaTime]::[slot]::[row]::[TestItem]::[result]::[error_info]
    '''


def analysis_data(data):
    result = {}
    try:
        data_list = data.split('::[')
        # print data_list
        result['slot'] = int(data_list[1][:-1])
        result['value'] = data_list[3][:-1]
        temp = hex(int(data_list[2][:-1])).upper()
        # print temp
        if len(temp) < 4:
            result['row'] = 'I00{}'.format(temp[-1:])
        else:
            result['row'] = 'I0{}'.format(temp[-2:])
    except Exception as e:
        print(e)

    return result


class TunnelFrame(tk.Frame):
    def __init__(self, master, slot=1, *args, **kwargs):
        tk.Frame.__init__(self, master=master, *args, **kwargs)
        self.IsEnabled = True
        self.title = tk.StringVar(self)
        self.title.set("SLOT{}".format(slot))
        self.slot = slot
        self.value = tk.StringVar(self)
        self.sn = tk.StringVar(self)
        self.sn.set("")
        self.slot_enabled = tk.BooleanVar(self)
        self.slot_enabled.set(True)
        self.value.set("PASS")
        self.config(width=200, height=250, bg="LightCyan")
        self.setup_ui()
        # self.set_test_value("TEST")

    def setup_ui(self):
        self.lb_title = tk.Label(self, textvariable=self.title, font=('Arial', 20), fg='black', bg='LightCyan')
        self.lb_title.pack(fill=tk.X)
        f = tk.Frame(self, width=200, height=160, bg='LightCyan')
        self.lb_value = tk.Label(f, textvariable=self.value, font=('Arial', 20), fg='black', bg='lime', width=16,
                                 height=1)
        self.lb_value.pack(fill=tk.X)
        self.lb_sn = tk.Label(f, textvariable=self.sn, font=('Arial', 20), fg='black', bg='white', width=16,
                              relief='solid', borderwidth=1, height=1)
        self.lb_sn.pack(fill=tk.X)
        f.pack()
        self.lb_title.bind("<Double-Button-1>", lambda x: self.enabled_slot())

    def enabled_slot(self):
        self.IsEnabled = True if self.IsEnabled == False else False
        if self.IsEnabled:
            self.lb_title.config(bg='LightCyan')
            self.lb_value.config(bg='lime')
            self.lb_sn.config(bg='white', borderwidth=1)
            # self.config(bg="LightCyan")
        else:
            self.lb_title.config(bg='LightGray')
            self.lb_value.config(bg='LightGray')
            self.lb_sn.config(bg='LightGray', borderwidth=0)
            # self.config(bg="LightGray")

    def set_title_name(self, title):
        self.title.set(value=title)

    def set_test_value(self, value):
        if value == "PASS":
            self.value.set("PASS")
            self.lb_value.config(bg="lime")
        elif value == "FAIL":
            self.value.set("FAIL")
            self.lb_value.config(bg="red")
        elif value == "TEST":
            self.value.set("TESTING")
            self.lb_value.config(bg="yellow")


class Application(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        # super(Application, self).__init__()
        tk.Frame.__init__(self, master=master, *args, **kwargs)
        self.thread_flag = 0
        self.audit_mode_string = tk.StringVar()
        self.audit_mode_string.set("PDCA")
        self.slot_list = []
        self.config(padx=0)
        self.sn = tk.StringVar()
        self.sn.set("")
        self.ct = tk.StringVar()
        self.ct.set("CT: 0 S")
        self.pack(fill=tk.BOTH)
        self.setup_ui()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("localhost", 6001))
        self.server.listen(20)
        self.th1 = threading.Thread(target=self.socket_thread)
        self.th1.setDaemon(True)
        self.th1.start()
        self.stop_flag = False

    def timer_count(self):
        i = 0
        while True:
            if self.stop_flag == self.thread_flag:
                self.thread_flag=0
                self.stop_flag = 0
                break
            if i > 250:
                break
            self.ct.set("CT: {} S".format(i))
            time.sleep(0.1)
            i += 0.1

    def socket_thread(self):
        while True:
            client, add = self.server.accept()
            thread = threading.Thread(target=self.client_read, args=(client,))
            thread.setDaemon(True)
            thread.start()

    def client_read(self, client):
        while True:
            data = client.recv(28).encode("gbk")
            # print data
            if data.startswith('[ERRO]'):
                # client.close()
                result = analysis_data(data)
                self.test_table.see(item=result['row'])
                self.test_table.set(item=result['row'], column=3 + result['slot'], value=result['value'])
                self.slot_list[result['slot'] - 1].set_test_value("FAIL")
                break
            elif data.startswith('[EXIT]'):
                self.stop_flag += 1
                result = analysis_data(data)
                self.slot_list[result['slot'] - 1].set_test_value(result['value'])
                self.bt_start.config(state='normal')  # 将按钮置为可用
                self.bt_reset.config(state='normal')  # 将按钮置为可用
                break
            elif data.startswith('[INFO]'):
                result = analysis_data(data)
                self.test_table.selection_set(result['row'])
                self.test_table.set(item=result['row'], column=3 + result['slot'], value=result['value'])

        client.close()

    def setup_ui(self):
        title_frame = tk.Frame(self)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text=data['AppTitle'], font=("Arial", 32), fg='red').grid(padx=200, row=0, column=0,
                                                                                        columnspan=2)
        tk.Label(title_frame, textvariable=self.audit_mode_string, font=("Arial", 20), fg="green").grid(ipadx=400,
                                                                                                        row=1, column=0,
                                                                                                        sticky="W")
        tk.Label(title_frame, text="Ver: {}".format(data['AppVersion']), font=("Arial", 16)).grid(ipadx=200, row=1,
                                                                                                  column=1, sticky='E')
        table_frame = tk.Frame(self, relief='groove', borderwidth=1)
        table_frame.pack(fill=tk.X)
        items = read_test_plant(data['TestPlant'])
        self.table_window_init(table_frame, items)
        fuc_frame = tk.Frame(self)
        self.func_window_init(fuc_frame)
        fuc_frame.pack(fill=tk.X, pady=3, padx=3)
        log_frame = tk.Frame(self)
        self.LogUi(master=log_frame)
        log_frame.pack(fill=tk.X)

    def tabled_window_clear(self):
        for item in self.test_table.get_children():
            for i in range(4, 18):
                self.test_table.set(item=item, column=i, value='')

    def table_window_init(self, master, items):
        headers = ["NO", "TestItem", "TestUpper", "TestLower"]
        for i in range(data['TestSlot']):
            headers.append("Slot{}".format(i + 1))
        self.test_table = ttk.Treeview(master=master, height=20, show='headings', columns=headers, )
        for header in headers:
            if header == "NO":
                self.test_table.column(header, width=10, anchor='center')
                self.test_table.heading(header, text=header)
            elif header == 'TestItem':
                self.test_table.column(header, width=120, anchor='center')
                self.test_table.heading(header, text=header)
            else:
                self.test_table.column(header, width=50, anchor='center')
                self.test_table.heading(header, text=header)
        i = 0
        for item in items:
            if item.isEnabled:
                self.test_table.insert("", index=i, value=(str(i), item.TestName, item.TestUpper, item.TestLower))
                i += 1
        self.test_table.pack(fill=tk.BOTH)
        # 遍历表格的item
        for i, item in enumerate(self.test_table.get_children()):
            if i % 2 == 0:
                self.test_table.item(item, tags='even')
                self.test_table.tag_configure('even', background="#f0f0f0")
            else:
                self.test_table.item(item, tags="odd")
                self.test_table.tag_configure('odd', background='white')

    def func_window_init(self, master):
        master.config(height=250, relief='solid', borderwidth=0.5)
        f1 = tk.Frame(master, relief='solid', height=250, width=950, borderwidth=0.5)
        f1_1 = tk.Frame(f1)
        f1_2 = tk.Frame(f1)
        f1_1.pack(pady=5)
        f1_2.pack(pady=5)
        f1.pack(fill=tk.Y, side='left')
        # f2 = tk.Frame(master, relief='solid', height=250, width=500, borderwidth=0.5)
        # f2.pack(fill=tk.Y, side='right')
        # 绘制输入框和开始、复位按钮
        tk.Label(f1_1, text="SN:", bg='white', font=("Arial", 16)).grid(row=0, column=0, sticky='W')
        self.et_sn = tk.Entry(f1_1, width=32, textvariable=self.sn, font=("Arial", 16))
        self.et_sn.grid(row=0, column=1, columnspan=4)
        self.bt_start = tk.Button(f1_1, text='Start', width=10, font=("Arial", 16), command=self.run)
        self.bt_start.grid(row=0, column=5, padx=30)
        self.bt_reset = tk.Button(f1_1, text='Reset', width=10, font=("Arial", 16))
        self.bt_reset.grid(row=0, column=6, padx=30)
        tk.Label(f1_1, textvariable=self.ct, bg='white', font=("Arial", 16)).grid(row=0, column=7, padx=15, sticky='E')
        # 绘制通道显示
        for row in range(2):
            for column in range(int(data['TestSlot']/2)):
                tunnel = TunnelFrame(master=f1_2, slot=column + 1 + row * data['TestSlot']/2)
                tunnel.grid(row=row, column=column, padx=5, pady=5)
                self.slot_list.append(tunnel)

    def LogUi(self, master):
        master.config(bg='SkyBlue')
        tk.Label(master, text="Another: Long.Hou", heigh=1, font=('Arial', 13), bg="SkyBlue", fg='red').pack(pady=5,
                                                                                                             side='right')
        tk.Label(master, text="Luxshare-ict", heigh=1, font=('Arial', 17), bg="SkyBlue", fg='red').pack(pady=5,
                                                                                                        side='left')

    def RunShellWithTimeout(self, cmd, slot, timeout=3):
        # print cmd
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        timer = Timer(timeout, self.time_out, [p, slot])
        try:
            timer.start()
            stdout, stderr = p.communicate()
            return_code = p.returncode
            print(stdout)
            print(stderr)
            return return_code, stdout, stderr
        finally:
            timer.cancel()

    def time_out(self, p, slot):
        p.kill()
        self.slot_list[slot].set_test_value("FAIL")

    def run(self):
        sn1 = self.sn.get()
        if len(sn1) == 0:
            return
        self.tabled_window_clear()
        self.bt_start.config(state='disabled')  # 将按钮置为不可用
        self.bt_reset.config(state='disabled')  # 将按钮置为不可用
        for m, slot in enumerate(self.slot_list):
            if slot.IsEnabled:
                slot.set_test_value("TEST")
                self.thread_flag += 1
                if m < 10:
                    sn = sn1 + "0" + str(m)
                else:
                    sn = sn1 + str(m)
                slot.sn.set(sn)
                threading.Thread(target=self.RunShellWithTimeout,
                                 args=("python3 {}/run_mic_script.py -s {} -f {} -vp {} -sp {} -n {}".format(
                                     data['RunScriptCmd'], m + 1,
                                     data['LogDirPath'], data['VirtualPorts'][m], data['SerialPorts'][m], sn), m,
                                       20,)).start()
                time.sleep(0.01)
        t1 = threading.Thread(target=self.timer_count)
        t1.setDaemon(True)
        t1.start()



if __name__ == '__main__':
    data = read_json("config.json")
    # print data['TestItem']
    win = tk.Tk()
    win.title(data['AppTitle'])
    win.geometry("{}x{}".format(win.winfo_screenwidth(), win.winfo_screenheight() - 150))
    win.resizable(width=0, height=0)
    win.config(bg='SkyBlue', padx=0, pady=0)
    app = Application(master=win)
    win.mainloop()
