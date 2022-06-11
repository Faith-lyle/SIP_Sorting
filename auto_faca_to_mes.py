#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:Long.Hou
@file: auto_faca_to_mes.py 
@time: 2022/03/15 
@email:long.hou2@luxshare-ict.com
"""
import openpyxl
import pyautogui
import pyperclip
import time

x= 715
x1 = 921
y1= 602
y = 343
def read_content(file_path):
    work_book = openpyxl.open(file_path)
    sheet = work_book.active
    data = []
    i = 0
    for rows in sheet:
        row_data = []
        for cell in rows:
            if i>5:
                break
            if cell.value is None:
                row_data.append('')
                i +=1
            else:
                row_data.append(str(cell.value).replace("\n",''))

        data.append(row_data)

    return data[1:]


def auto_update(date):
    pyautogui.doubleClick()
    pyautogui.press('delete')
    pyautogui.write(date[0])
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(0.6)
    pyperclip.copy(date[1])
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.press("enter")

def get_x_y():
    # time.sleep(5)
    pyautogui.mouseInfo()
    # print(x,y)
    return



if __name__ == '__main__':

    # get_x_y()
    print("run script start!\n")
    dates = read_content("date.csv")
    time.sleep(6)
    for date in dates:
        try:
            auto_update(date)
            # print("SN:{} ;CA: {}update successful!\n".format(date[0], date[1]))
        except:
            pass
        time.sleep(1)
    print("update successful!\n")

