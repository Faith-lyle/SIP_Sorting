#读取xlsx的内容
import xlrd
import xlwt
import os
import pandas as pd
import numpy as np

#读取xlsx，返回dataframe

def read_xlsx(file_path):
    data = pd.read_excel(file_path)
    #获取data第3列到第5列的内容
    data = data.iloc[:,2:6]
    #获取dataitem='fial'的行


    data = data[data['dataitem']=='fail']
    #获取data fail行
    data = data.loc()
    data = data['fail']
    data = data.iloc[:,3]
    return data

if __name__ == '__main__':
    print(len('61439DD8CFA8A3B87C82D9C98577C3B6B6914191'))