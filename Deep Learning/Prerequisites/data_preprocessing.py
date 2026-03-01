import os

os.makedirs(os.path.join('..', 'data'), exist_ok=True)#创建一个目录,地址为../data
data_file = os.path.join('..', 'data', 'house_tiny.csv')
#创建一个文件,地址为../data/house_tiny.csv
with open(data_file, 'w') as f:#以写模式打开文件并写入数据
    f.write('NumRooms,Alley,Price\n')  # 列名
    f.write('NA,Pave,127500\n')  # 每行表示一个数据样本
    f.write('2,NA,106000\n')
    f.write('4,NA,178100\n')
    f.write('NA,NA,140000\n')

import pandas as pd
data = pd.read_csv(data_file)
print(data)

inputs, outputs = data.iloc[:, 0:2], data.iloc[:, 2]
# ========== 关键修改1：分开处理数值列和类别列 ==========
# 1. 数值列（NumRooms）用均值填充缺失值
inputs['NumRooms'] = inputs['NumRooms'].fillna(inputs['NumRooms'].mean())
# 2. 类别列（Alley）先保留缺失值，等下用独热编码处理（dummy_na=True会把缺失值当成独立类别）
print("\n填充数值列缺失值后的输入数据：")
print(inputs)

# ========== 独热编码：把字符串类别列转数值型（包含缺失值的独立类别） ==========
"""
只接受两种类型的类别值“Pave”和“NaN”， pandas可以自动将此列转换为两列“Alley_Pave”和“Alley_nan”
这是 pandas 库中的一个函数，用于将分类变量（如字符串、类别型数据）转换为“虚拟变量”或“哑变量”（Dummy Variables）
也就是机器学习中常用的 独热编码​ 形式。
"""
inputs = pd.get_dummies(inputs, dummy_na=True)
print("\n独热编码后的输入数据：")
print(inputs)

import torch

# 转换为PyTorch张量
X = torch.tensor(inputs.to_numpy(dtype=float))
y = torch.tensor(outputs.to_numpy(dtype=float))
print("\n转换后的张量X（输入）和y（输出）：")
print(X, y)