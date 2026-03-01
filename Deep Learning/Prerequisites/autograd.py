import torch

x = torch.arange(4.0)
"""
重要的是，我们不会在每次对一个参数求导时都分配新的内存。 因为我们经常会成千上万次地更新相同的参数，
每次都分配新的内存可能很快就会将内存耗尽。
x.requires_grad_(True)  # 等价于x=torch.arange(4.0,requires_grad=True)
x.grad  # 默认值是None
y.backward()
反向传播函数，计算y关于x的梯度
注意，一个标量函数关于向量x的梯度是向量，并且与x具有相同的形状。
x.grad
# 在默认情况下，PyTorch会累积梯度，我们需要清除之前的值
x.grad.zero_()
y = x.sum()
y.backward()
x.grad
"""

"""
在 PyTorch 中，对一个非标量张量 y直接调用 .backward()会报错，
必须提供一个与 y同形状的 gradient参数，这个参数就是上游梯度 dL/dy。
import torch
x = torch.arange(4.0, requires_grad=True)
y = x * x  # y 是一个向量 [x0^2, x1^2, x2^2, x3^2]
方法一：提供一个全为1的gradient，等价于对y的所有元素求和后再反向传播
y.backward(torch.ones_like(y))
print(x.grad) # 输出: tensor([0., 2., 4., 6.])
方法二：更常见的写法，先求和得到标量，再反向传播
x.grad.zero_() # 清零之前计算的梯度
y.sum().backward()
print(x.grad) # 输出: tensor([0., 2., 4., 6.])
这两种写法在数学上是等价的，都实现了对向量 y的所有元素求和（即 dL/dy = [1, 1, 1, 1]），然后通过 VJP 计算出 dL/dx = 2x
"""

"""
有时，我们希望将某些计算移动到记录的计算图之外。 例如，假设y是作为x的函数计算的，而z则是作为y和x的函数计算的。
我们想计算z关于x的梯度，但由于某种原因，希望将y视为一个常数， 并且只考虑到x在y被计算后发挥的作用。
这里可以分离y来返回一个新变量u，该变量与y具有相同的值， 但丢弃计算图中如何计算y的任何信息。 
换句话说，梯度不会向后流经u到x。 因此，下面的反向传播函数计算z=u*x关于x的偏导数，
同时将u作为常数处理， 而不是z=x*x*x关于x的偏导数。
u=y.detach()
"""
"""
 在下面的代码中，while循环的迭代次数和if语句的结果都取决于输入a的值。
def f(a):
    b = a * 2
    while b.norm() < 1000:
        b = b * 2
    if b.sum() > 0:
        c = b
    else:
        c = 100 * b
    return c
a = torch.randn(size=(), requires_grad=True)
d = f(a)
d.backward()
"""