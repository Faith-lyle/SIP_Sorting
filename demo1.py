#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:Long.Hou
@file: demo1.py 
@time: 2022/04/01 
@email:long.hou2@luxshare-ict.com
"""
from matplotlib import pyplot as plt
import pandas as pd

# title_name :图表的标题名
title_name = 'ErrorMic3 3.072MHz_DMIC_Sensitivity@DMic1_Sensitivity'

# 要对比的文件路径
file_list = [
    '/Users/user/Documents/企业微信/WXWork Files/Caches/Files/2022-04/05d452d698461381ef09d2a635fff712/AFB-CFR_M2_After_Cal.csv',
    '/Users/user/Documents/企业微信/WXWork Files/Caches/Files/2022-04/1127ac600240a787bca92392bb923dcf/AFB-CFR_M2_Before_Cal.csv'
]

# 要对比的不良项目
item = 'ErrorMic3 3.072MHz_DMIC_Sensitivity@DMic1_Sensitivity'

# 每个图形的名称
labels = ["AFB-CFR_M2_After_Cal", "AFB-CFR_M2_Before_Cal"]

# 删除误差值，lower：下限，upper：上限
lower = -100
upper = 100
# 读取多少行数据
row = 100000


def read_data(file_path):
    data2 = pd.read_csv(file_path)
    new_data = data2[3:]
    print(new_data.index.stop)
    # print(data['ErrorMic3 3.072MHz_DMIC_Sensitivity@DMic1_Sensitivity'])
    data1 = new_data[new_data[item] != '#NAME?']
    # new_data = new_data[new]
    data3 = pd.DataFrame(data1[item], dtype=float)
    data3 = data3[data3[item] > lower]
    data3 = data3[data3[item] < upper]
    return data3

def xticks():
    for x in range(len(group())):
        mx=int(group()[x].describe()['max'])
        mi=int(group()[x].describe()['min'])
        a=int(group()[x].describe()['25%'])
        b=int(group()[x].describe()['50%'])
        c=int(group()[x].describe()['75%'])
        up=int(a-1.5*(c-a))
        down=int(c+1.5*(c-a))
        xtext=[mi,up,a,b,c,mx,down]
        for y in xtext:
            plt.text(y-500,x+1.25,y,fontsize=11.1)


if __name__ == '__main__':
    colors = ["#7B68EE", '#747388', '#772388', '#7534BB', "#7EDD28", "#837211", "#89776B", "#94F32D", "#687729",
              "8D3254"]
    data = pd.DataFrame(None, dtype=float)
    positions = []
    for i, file in enumerate(file_list):
        data['NO{}'.format(i)] = read_data(file)
        positions.append((i+1)*2)
    plt.title(title_name)
    p = plt.boxplot(data, positions=positions, widths=1.5, patch_artist=True,
                    showmeans=False, showfliers=False,
                    medianprops={"color": "white", "linewidth": 0.5},
                    boxprops={"edgecolor": "white",
                              "linewidth": 0.5},
                    whiskerprops={"color": "C0", "linewidth": 1.5},
                    capprops={"color": "LightGray", "linewidth": 1.5},
                    labels=labels)

    for i, plot in enumerate(p['boxes']):
        plot.set(facecolor=colors[i])
        # plot.set(position=i)
        plt.text(positions[i], -34, -34, fontsize=11.1)
    plt.savefig("a.png")
    plt.show()

