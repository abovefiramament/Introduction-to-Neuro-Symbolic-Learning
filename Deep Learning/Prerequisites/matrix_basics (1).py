import torch
x = torch.arange(12)
print(x)
print(x.shape)
print(x.numel())

X = x.reshape(3, 4)
print(X)
print(torch.zeros((2,3, 4)))
print(torch.ones((2, 3, 4)))
print(torch.randn(3, 4))
X=torch.tensor([[2, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])
print(X)

x = torch.tensor([1.0, 2, 4, 8])
y = torch.tensor([2, 2, 2, 2])
print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x ** y)
print(torch.exp(x))

X = torch.arange(12, dtype=torch.float32).reshape((3,4))
Y = torch.tensor([[2.0, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])
torch.cat((X, Y), dim=0), torch.cat((X, Y), dim=1)
# 0表示按行拼接，1表示按列拼接

print(X == Y)# 元素相等时为True，否则为False

a = torch.arange(3).reshape((3, 1))
b = torch.arange(2).reshape((1, 2))
print(a+b)
# 广播机制,当两个张量的形状不同时,可以通过扩展维度(复制)来实现广播,
# 例如,当一个张量的形状为(3,1)时,另一个张量的形状为(1,2)时,可以将第一个张量扩展为(3,2),将第二个张量扩展为(3,2),
# 然后进行元素级别的操作,得到的结果为(3,2)的张量

x=torch.arange(12)
print(x[-1], x[1:3])
x[1, 2] = 9
print(x)

x[0:2, :] = 12
print(x)

before = id(Y)
Y = Y + X
print(Y== before)# False,因为Y是新创建的张量,而不是在原张量上进行操作

Z = torch.zeros_like(Y)
print('id(Z):', id(Z))
Z[:] = X + Y
print('id(Z):', id(Z))
""" 
执行原地操作非常简单。 我们可以使用切片表示法将操作的结果分配给先
 前分配的数组，例如Y[:] = <expression>。
"""

before = id(X)
X += Y
print(X == before)#如果在后续计算中没有重复使用X

A = X.numpy()
B = torch.tensor(A)
print(type(A), type(B))
a = torch.tensor([3.5])
print(a, a.item(), float(a), int(a))
