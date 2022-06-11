# import matplotlib as plt
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math

def cpk_calc(df_data: pd.DataFrame, usl, lsl):
    """
    :param df_data: 数据dataframe
    :param usl: 数据指标上限
    :param lsl: 数据指标下限
    :return:
    """
    sigma = 3
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
    cpl = (u - lsl) / (sigma * stdev)   #


    # 得出cpk
    cpk = min(cpu, cpl)

    # 使用matplotlib画图
    plt.xlim(x1[0] - 0.5, 210)
    plt.plot(x1, y1)
    x2= [170,170,170,170]
    y2 = [0,0.1,0.2,0.3]
    x3 = [200,200,200,200]
    y3 = [0,0.1,0.2,0.3]
    plt.plot(x2,y2,color = 'green',label = 'Lower')
    plt.plot(x3,y3,color = "red",label= "Upper")
    plt.hist(df_data.values, 15, density=True,label="de")
    plt.title("cpk={0}".format(cpk))
    plt.show()


if __name__ == '__main__':
    # data = pd.read_csv("date.csv")
    # data = pd.DataFrame(data)
    # print(data)
    # cpk_calc(data,usl=200,lsl=170)
    print(8**3)
    print(chr((65)))
    #01000|00010