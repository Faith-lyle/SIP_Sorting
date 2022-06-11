#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:Long.Hou
@file: DoCPK.py 
@time: 2022/05/07 
@email:long.hou2@luxshare-ict.com
"""
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

item = 'ANALOG_AMP_OUT_N'
file_path = "/Users/user/Desktop/H28工装/data/data.xlsx"
lower = 2.177
upper = 2.381


item2= None
items = []


def read_csv(file_path):
    sheet = pd.read_excel(file_path, sheet_name="data")
    if item2:
        return sheet[[item,item2]]
    else:
        return sheet[[item,]]
def dispose_data(data):
    global items
    length_list = []
    datas = pd.DataFrame()
    text = data[item2][0]
    items.append(text)
    for i in data[item2]:
        if i not in items:
            items.append(i)
    for n in items:
        length_list.append(len(data[(data[item2] == n)][item].values))
    for n in items:
        datas[n]= data[(data[item2] == n)][item].values[:min(length_list)]
    return datas

color = ['blue','pike','bule','yellow','lime']

# 做CPK
def do_cpk(data):
    plt.hist(data, bins=100, color = color[:len(data.columns)],range=(lower * 0.98, upper * 1.02),)
    # plt.hist(data, bins=100, color = ('red','green'),range=(1, 3))
    plt.title('ANALOG_AMP_OUT_N_L')
    plt.axvline(upper, color='red', label='upper')
    plt.axvline(lower, color='red', label='lower')
    plt.text(upper, 30, 'upper', color='red',fontdict = {'family':"Arial","size":9,'color':'red'})
    plt.text(lower, 30, 'lower', color='red',fontdict = {'family':"Arial","size":9,'color':'red'})
    # 获取y的最大值
    ymax = plt.gca().get_ylim()[1]
    # 获取y的最小值
    ymin = plt.gca().get_ylim()[0]
    # 获取x的最大值fontdict = {'family':"Arial","size":9}
    xmax = plt.gca().get_xlim()[1]
    # 获取x的最小值
    xmin = plt.gca().get_xlim()[0]
    contnt = """
    min: %s
    max: %s
    upper: %s
    lower: %s
    count: %s
    cpk: %.2f
    """ % (min(data.values)[0], max(data.values)[0], upper, lower, len(data),cpk_calc(data,upper,lower))
    plt.text(upper, ymax * 0.7, contnt, color='black',fontdict = {'family':"Arial","size":9})
    plt.show()

def cpk_calc(df_data: pd.DataFrame, usl, lsl):
    """
    :param df_data: 数据dataframe
    :param usl: 数据指标上限
    :param lsl: 数据指标下限
    :return:
    """
    sigma = 0.68
    # 若下限为0, 则使用上限反转负值替代
    if int(lsl) == 0:
        lsl = 0 - usl
 
    # 数据平均值
    u = df_data.mean()[0]
 
    # 数据标准差
    stdev = np.std(df_data.values, ddof=1)
 
    # 生成横轴数据平均分布
    x1 = np.linspace(u - sigma * stdev, u + sigma * stdev, 1000)
 
    # 计算正态分布曲线
    y1 = np.exp(-(x1 - u) ** 2 / (2 * stdev ** 2)) / (math.sqrt(2 * math.pi) * stdev)
 
    cpu = (usl - u) / (sigma * stdev)
    cpl = (u - lsl) / (sigma * stdev)
    # 得出cpk
    cpk = min(cpu, cpl)
    return cpk

if __name__ == '__main__':
    data = read_csv(file_path)
    if item2:
        data = dispose_data(data)
    # print(data)
    do_cpk(data)
