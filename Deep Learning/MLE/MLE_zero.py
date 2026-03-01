import torch
import math
from torch import nn
from d2l import torch as d2l
from IPython import display
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

batch_size = 256

# 手动实现MNIST数据集加载
transform = transforms.Compose([transforms.ToTensor()])

train_dataset = datasets.MNIST(
    root='./data',
    train=True,
    transform=transform,
    download=True
)

test_dataset = datasets.MNIST(
    root='./data',
    train=False,
    transform=transform,
    download=True
)

train_iter = DataLoader(
    dataset=train_dataset,
    batch_size=batch_size,
    shuffle=True,
    num_workers=0
)

test_iter = DataLoader(
    dataset=test_dataset,
    batch_size=batch_size,
    shuffle=False,
    num_workers=0
)

num_inputs, num_outputs, num_hiddens = 784, 10, 256

# 使用Xavier初始化改进权重初始化
W1 = nn.Parameter(torch.randn(
    num_inputs, num_hiddens, requires_grad=True) * math.sqrt(1/num_inputs))
b1 = nn.Parameter(torch.zeros(num_hiddens, requires_grad=True))
W2 = nn.Parameter(torch.randn(
    num_hiddens, num_outputs, requires_grad=True) * math.sqrt(1/num_hiddens))
b2 = nn.Parameter(torch.zeros(num_outputs, requires_grad=True))

params = [W1, b1, W2, b2]

def relu(X):
    a = torch.zeros_like(X)
    return torch.max(X, a)
def net(X):
    X = X.reshape((-1, num_inputs))
    H = relu(X@W1 + b1)  # 这里“@”代表矩阵乘法
    return (H@W2 + b2)

def evaluate_accuracy(net, data_iter): #@save
    if isinstance(net, torch.nn.Module):
        net.eval() # 将模型设置为评估模式
    metric = d2l.Accumulator(2) # 正确预测数、预测总数
    with torch.no_grad():
        for X, y in data_iter:
            metric.add(d2l.accuracy(net(X), y), y.numel())
    return metric[0] / metric[1]

def train_epoch_ch3(net, train_iter, loss, updater): #@save
    # 将模型设置为训练模式
    if isinstance(net, torch.nn.Module):
        net.train()
    # 训练损失总和、训练准确度总和、样本数
    metric = d2l.Accumulator(3)
    for X, y in train_iter:
        # 计算梯度并更新参数
        y_hat = net(X)
        l = loss(y_hat, y)
        if isinstance(updater, torch.optim.Optimizer):
            # 使用PyTorch内置的优化器和损失函数
            updater.zero_grad()
            l.mean().backward()
            updater.step()
        else:
            # 使用定制的优化器和损失函数
            l.sum().backward()
            updater(X.shape[0])
        metric.add(float(l.sum().detach()), d2l.accuracy(y_hat, y), y.numel())
    # 返回训练损失和训练精度
    return metric[0] / metric[2], metric[1] / metric[2]

def train_ch3(net, train_iter, test_iter, loss, num_epochs, updater): #@save
    # 初始化训练数据存储
    train_history = {
        'train_loss': [],
        'train_acc': [],
        'test_acc': []
    }
    
    animator = d2l.Animator(xlabel='epoch', xlim=[1, num_epochs], ylim=[0.3, 0.9],
                            legend=['train loss', 'train acc', 'test acc'])
    
    for epoch in range(num_epochs):
        train_metrics = train_epoch_ch3(net, train_iter, loss, updater)
        test_acc = evaluate_accuracy(net, test_iter)
        animator.add(epoch + 1, train_metrics + (test_acc,))
        train_loss, train_acc = train_metrics
        
        # 保存训练数据
        train_history['train_loss'].append(train_loss)
        train_history['train_acc'].append(train_acc)
        train_history['test_acc'].append(test_acc)
        
        # 打印当前 epoch 的训练结果
        print(f'Epoch {epoch+1}/{num_epochs}:')
        print(f'  Train Loss: {train_loss:.4f}')
        print(f'  Train Acc: {train_acc:.4f}')
        print(f'  Test Acc: {test_acc:.4f}')

    # 将训练数据保存到文件
    torch.save(train_history, 'MLE_zero_data/train_history.pth')
    print('\n训练数据已保存到 MLE_zero_data/train_history.pth')
    
    # 保存训练曲线图表
    d2l.plt.savefig('MLE_zero_data/training_curve.png', dpi=300, bbox_inches='tight')
    print('训练曲线图表已保存到 MLE_zero_data/training_curve.png')

    assert train_loss < 0.5, train_loss
    assert train_acc <= 1 and train_acc > 0.7, train_acc
    assert test_acc <= 1 and test_acc > 0.7, test_acc
    
    return train_history

loss = nn.CrossEntropyLoss(reduction='none')
num_epochs, lr = 10, 0.5
updater = torch.optim.SGD(params, lr=lr)
train_ch3(net, train_iter, test_iter, loss, num_epochs, updater)

# 预测和图片保存函数
def predict_ch3(net, test_iter, n=6):
    """预测并显示前n个样本的结果，同时保存图片和准确率"""
    # 计算测试集准确率
    test_acc = evaluate_accuracy(net, test_iter)
    print(f'测试集准确率: {test_acc:.4f}')
    
    # 获取前n个测试样本并进行预测
    for X, y in test_iter:
        break
    
    # 进行预测
    y_hat = net(X)
    _, predicted = torch.max(y_hat, 1)
    
    # 准备标签（MNIST是数字0-9）
    trues = [f'{label}' for label in y[:n].tolist()]
    preds = [f'{label}' for label in predicted[:n].tolist()]
    titles = [f'True: {true}\nPred: {pred}' for true, pred in zip(trues, preds)]
    
    # 显示和保存预测图片
    d2l.show_images(X[:n].reshape((n, 28, 28)), 1, n, titles=titles)
    
    # 保存组合图片
    d2l.plt.savefig('MLE_zero_data/test_predictions.png', dpi=300, bbox_inches='tight')
    print('预测图片已保存到 MLE_zero_data/test_predictions.png')
    
    # 保存单张图片
    for i in range(n):
        img = X[i].reshape(28, 28)
        true_label = trues[i]
        pred_label = preds[i]
        # 创建包含真实标签和预测标签的文件名
        filename = f'MLE_zero_data/test_{i+1}_true_{true_label}_pred_{pred_label}.png'
        # 保存图片
        d2l.plt.figure(figsize=(2, 2))
        d2l.plt.imshow(img, cmap='gray')
        d2l.plt.axis('off')
        d2l.plt.savefig(filename, dpi=300, bbox_inches='tight')
        d2l.plt.close()
    
    d2l.plt.show()

# 调用预测函数
predict_ch3(net, test_iter)