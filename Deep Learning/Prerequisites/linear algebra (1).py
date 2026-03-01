import torch

x = torch.tensor(3.0)
y = torch.tensor(2.0)

A = torch.arange(20).reshape(5, 4)

#其中张量乘法为哈德曼积，cij=aij*bij

#降维求和，可以指定按照什么方式保留维度求和

#非降维求和，将A/SUMA

#点积torch.dot(x,y)=torch.sum(x*y)一维张量且长度相同，等式成立

#向量积，torch.mv(x,y) ,列维数相同

#矩阵乘法a n*k b k* m  cij=sigma(k从0到1)aik*bkj，a行b列，torch.mm(x,y)

"""
范数是将向量映射到标量的函数，常用的范数有L1范数、L2范数、最大范数等。
L1范数：torch.norm(x,p=1)，即向量x中所有元素的绝对值之和
L2范数：torch.norm(x,p=2)，即向量x中所有元素的平方和的平方根
最大范数：torch.norm(x,p=float('inf'))，即向量x中所有元素的绝对值中的最大值
性质：
1. 非负性：||x||≥0，且||x||=0当且仅当x=0。
2. 齐次性：||αx||=|α|||x||，其中α是标量。
3. 三角不等式：||x+y||≤||x||+||y||。
"""
