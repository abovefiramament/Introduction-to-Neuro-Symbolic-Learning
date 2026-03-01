import torch
from torch.distributions import multinomial
from d2l import torch as d2l
fair_probs = torch.ones([6]) / 6
multinomial.Multinomial(1, fair_probs).sample()
#multinomial是一个离散分布，用于采样多个类别，
#Multinomial(1, fair_probs)表示从6个类别中采样1个类别，每个类别概率为1/6
# 将结果存储为32位浮点数以进行除法
counts = multinomial.Multinomial(1000, fair_probs).sample()
counts / 1000  # 相对频率作为估计值
