# Dataset 核心学习笔记

## 一、Dataset 在 LLM 体系中的核心定位

Dataset 是**大语言模型训练流水线的「数据核心载体」**，它的本质是一套标准化的**数据读写、预处理、分发接口**，解决「如何把原始非结构化文本，高效、稳定地转换成模型可训练的张量批次」这个核心问题，是连接原始语料与模型训练的不可缺失的中间层。

### 1. 全链路中的固定位置

- **上游**：原始文本语料（txt/json/parquet）
- **Dataset 层**：数据加载 → 清洗 → Tokenizer 批量编码 → 标准化样本
- **下游**：DataLoader 批次生成 → 模型训练 / 验证

### 2. 对训练的决定性影响

1. **内存瓶颈突破**：决定能否处理上百 GB 的大语料而不爆内存。
2. **训练效率**：决定数据加载速度，避免 GPU 因等待数据而闲置（“GPU 饥饿” 是新手最常见的性能瓶颈）。
3. **数据质量**：决定预处理逻辑（去重、过滤、分词）的标准化程度，直接影响模型收敛效果。
4. **分布式适配**：决定多卡 / 多机训练时，数据能否正确分配到每张卡，避免重复训练。

------

## 二、核心设计目标与架构

### 1. 设计的核心目标（解决的三大痛点）

所有 Dataset 设计都是围绕解决以下痛点展开的：

- **痛点 1**：大语料无法全量加载进内存 → 目标：懒加载、内存映射。
- **痛点 2**：数据预处理与训练逻辑耦合 → 目标：解耦预处理，支持缓存、复用。
- **痛点 3**：单条处理效率低 → 目标：批量处理、多进程加速。

### 2. 两层核心架构

Dataset 分为**底层规范层**和**工程化实现层**，前者是强制接口标准，后者是面向 LLM 的优化实现。

#### （1）底层规范：PyTorch 原生 `torch.utils.data.Dataset`

这是所有 Dataset 的 “根规范”，核心是**强制统一两个接口**，只要实现这两个方法，就能被 PyTorch 生态完美支持。

表格







|          核心方法          |        输入        |             输出              | 强制要求 |                        核心作用                         |
| :------------------------: | :----------------: | :---------------------------: | :------: | :-----------------------------------------------------: |
|      `__len__(self)`       |         无         |       整数（总样本数）        | 必须实现 |    告诉 DataLoader 数据集大小，计算总步数、划分批次     |
| `__getitem__(self, index)` | 样本索引（0 开始） | 单个标准化样本（字典 / 张量） | 必须实现 | 根据索引读取 / 预处理单条数据，返回模型可直接使用的样本 |

**配套协作：DataLoader**

Dataset 只负责 “单样本读取”，批次生成、打乱、多进程加载全由 `DataLoader` 完成：

1. 调用 `__len__` 拿到总样本数。
2. 生成索引，传给 `__getitem__` 拿单样本。
3. 拼接成批次（batch），喂给模型。
4. 支持 `num_workers>0` 多进程并行加载，避免 GPU 闲置。

#### （2）工程化实现：Hugging Face `datasets.Dataset`（LLM 训练首选）

这不是对原生 Dataset 的简单封装，而是**基于 Apache Arrow 列式存储 + 内存映射的高性能架构**，是现在 GPT、LLaMA 训练的行业标准。

表格







|            核心特性            |      解决的问题       |                       针对 LLM 的优势                        |
| :----------------------------: | :-------------------: | :----------------------------------------------------------: |
|   **Apache Arrow 列式存储**    |     大语料读取慢      |          比 txt/json 读取快 100 倍，支持零拷贝读取           |
| **内存映射（Memory Mapping）** |     大语料爆内存      |  直接从磁盘映射数据，不用全量加载，100GB 语料内存占用 < 1GB  |
|      **`map` 批量预处理**      |      单条处理慢       | 批量执行分词 / 清洗，支持多进程、自动缓存，第二次训练不用重新跑 |
|       **`DatasetDict`**        | 训练 / 验证集管理混乱 | 原生支持 `{"train": Dataset, "val": Dataset}` 结构，清晰易管理 |
|        **`set_format`**        |     格式转换麻烦      |       一键转 PyTorch/TensorFlow 张量，不用手动处理维度       |

------

## 三、落地中的核心问题与工业界优化方案

### 1. 问题一：大语料（>10GB）全量加载爆内存

**优化方案**：

- **懒加载 + 内存映射**：优先用 Hugging Face `datasets.load_dataset`，它默认用内存映射，只在需要时从磁盘读取单条数据，内存占用仅和批次大小有关。
- **流式加载（Streaming）**：如果语料超过 100GB 或本地放不下，用 `load_dataset(..., streaming=True)` 边读边训练，不用下载到本地。

### 2. 问题二：预处理（分词）速度慢，拖慢训练

**优化方案**：

- **批量 `map` 处理**：绝对不要用循环单条处理，用 `map(..., batched=True, batch_size=1000, num_proc=4)` 批量分词，多进程并行，速度快 10 倍以上。
- **开启自动缓存**：`map` 默认开启缓存，预处理结果自动保存，第二次训练直接加载，节省 90% 时间。
- **Tokenizer 底层加速**：用 C++ 实现的 `tokenizers` 库，不要用 Python 原生实现，分词速度快 10-100 倍。

### 3. 问题三：GPU 饥饿（GPU 利用率低，等待数据）

**优化方案**：

- **多进程 DataLoader**：设置 `num_workers=4~8`（根据 CPU 核心数），多个进程并行预处理 / 加载数据，提前准备好下一批。
- **预取数据**：设置 `DataLoader(..., pin_memory=True, prefetch_factor=2)`，把数据预取到 GPU 显存，减少 CPU 到 GPU 的传输延迟。
- **简化预处理**：把复杂的清洗逻辑提前离线完成，训练时只做分词和转张量，减少单步预处理时间。

### 4. 问题四：训练 / 验证分布偏移，验证效果不可信

**优化方案**：

- **全流程数据一致性**：训练集和验证集必须用**完全相同的预处理逻辑**（分词规则、截断长度、填充方式）。
- **固定随机种子**：数据打乱、划分时固定随机种子，确保每次训练的验证集一致，结果可复现。
- **分层抽样划分**：划分训练 / 验证集时，确保两者的文本长度分布、领域分布一致，避免验证集偏科。

### 5. 问题五：分布式训练时数据重复或分配不均

**优化方案**：

- **用 `Accelerate`/`Deepspeed` 自动处理**：这些框架会自动给每张卡分配唯一的样本索引，避免重复训练。
- **`DistributedSampler`**：如果手动写分布式，用 `torch.utils.data.distributed.DistributedSampler` 包装 Dataset，确保数据正确分配。

------

## 四、极简实现流程概括（参考开源项目思路，适配 Tiny-K）

### 目标

构建一个适配类 LLaMA2 轻量模型（Tiny-K）的标准化 Dataset，支持大语料、批量预处理、自动缓存。

### 核心步骤

1. **语料准备**：

   

   - 收集 / 清洗目标语料（≥100MB），去重、过滤短文本 / 低质量文本。
   - 保存为纯文本格式（`.txt`，每行一个段落）或 JSONL。

   

2. **标准化加载**：

   

   - 用 `datasets.load_dataset("text", data_files={"train": "train.txt", "val": "val.txt"})` 一键加载。
   - 自动转为 Apache Arrow 格式，支持内存映射。

   

3. **批量预处理函数定义**：

   

   - 输入：批量文本 `examples`。
   - 逻辑：用预训练好的 Tokenizer 批量编码，截断到 `max_seq_len=512`，填充到 `max_seq_len`，添加 `labels`（自回归模型中 `labels = input_ids`）。
   - 返回：`input_ids`、`attention_mask`、`labels`。

   

4. **执行批量预处理**：

   

   - 用 `dataset.map(..., batched=True, batch_size=1000, num_proc=4, remove_columns=["text"])` 执行。
   - 开启缓存，删除原始文本节省内存。

   

5. **格式转换与 DataLoader 封装**：

   

   - 用 `dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])` 转 PyTorch 张量。
   - 封装成 `DataLoader(dataset, batch_size=2, shuffle=True, num_workers=4, pin_memory=True)`。

   

6. **全流程锁定**：

   

   - 预处理逻辑、随机种子全程锁定，微调 / 验证时完全复用，确保分布一致。



## 整体逻辑总览

这是一个继承自 PyTorch 原生 `Dataset` 的类，核心设计亮点是**预计算字节偏移量实现 O (1) 随机访问**，配合懒加载，完美处理上百 GB 的 JSONL 大语料，同时手动构造自回归模型需要的训练样本（`X`/`Y` 右移）和损失掩码。

------

## 分模块详细逻辑拆解

### 模块 1：`__init__` —— 预计算字节偏移量，解决大语料随机访问慢的核心痛点

这是这段代码**最精妙的工程化设计**，没有之一。

#### 核心逻辑

python



运行









```
# 预计算每行的起始字节偏移量
self._offsets = []
with open(data_path, 'rb') as f:
    self._offsets.append(0)
    while f.readline():
        self._offsets.append(f.tell())
self._total_lines = len(self._offsets) - 1
```

#### 逐行解读

1. `'rb'` 模式打开文件

   ：

   - 以二进制只读模式打开，避免文本编码问题，同时 `f.tell()` 返回的是字节偏移量，精准定位。

   

2. `self._offsets` 列表

   ：

   - 存储 JSONL 文件中**每一行的起始字节位置**。
   - 比如 `self._offsets[0] = 0`（第一行从文件开头开始），`self._offsets[1] = 123`（第二行从第 123 个字节开始），以此类推。

   

3. `while f.readline()` + `f.tell()`

   ：

   - 循环读取每一行，读完一行后，用 `f.tell()` 获取当前文件指针的位置（也就是下一行的起始字节位置），存入 `self._offsets`。

   

4. `self._total_lines = len(self._offsets) - 1`

   ：

   - 最后一次 `f.tell()` 返回的是文件末尾（EOF）的位置，所以总样本数是列表长度减 1。

   

#### 为什么这么做？（解决的核心痛点）

如果不预计算偏移量，每次 `__getitem__` 要访问第 `index` 行时，都得从文件开头一行一行读，直到读到第 `index` 行，时间复杂度是 **O(n)**，大语料里随机访问会慢到无法忍受。

预计算偏移量后，访问第 `index` 行时，直接用 `f.seek(self._offsets[index])` 跳到那一行的起始位置，时间复杂度是 **O(1)**，随机访问速度提升 100 倍以上。

**对应学习笔记知识点**：解决 “大语料读取慢” 的问题，优化数据加载速度，避免 GPU 饥饿。

------

### 模块 2：`__len__` —— 返回总样本数

python



运行









```
def __len__(self):
    return self._total_lines
```

- 逻辑极简：直接返回预计算好的总样本数。
- **对应学习笔记知识点**：PyTorch 原生 `Dataset` 必须实现的两个核心方法之一，告诉 `DataLoader` 数据集大小，计算总步数、划分批次。

------

### 模块 3：`__getitem__` —— 核心逻辑：随机访问 + 分词 + 自回归样本构造

这是代码的核心，负责把单条文本转换成模型可训练的样本（`X`/`Y`/`loss_mask`）。

#### 逻辑拆解

##### （1）O (1) 随机访问单条文本

python



运行









```
with open(self.data_path, 'rb') as f:
    f.seek(self._offsets[index])  # 直接跳到第 index 行的起始字节
    line = f.readline().decode('utf-8')  # 读取一行，解码成 UTF-8 文本
sample = json.loads(line)  # 解析 JSONL
text = f"{self.tokenizer.bos_token}{sample['text']}"  # 加上句首标记 <s>
```

- **懒加载**：每次只读取一条文本，绝不把整个语料加载进内存，内存占用仅和单条文本有关。
- **加 `bos_token`**：在文本开头加上句首标记（比如 `<s>`），这是 LLaMA2 等自回归模型的标准做法，帮助模型理解句子的起始。

##### （2）分词、截断、填充

python



运行









```
input_id = self.tokenizer(text).data['input_ids'][:self.max_length]  # 分词，截断到 max_length
text_len = len(input_id)
padding_len = self.max_length - text_len
input_id = input_id + [self.padding] * padding_len  # 填充到 max_length
```

- **分词**：用预训练好的 Tokenizer 把文本转成 Token ID。
- **截断**：如果文本太长，直接截断到 `max_length`（对应你的 ModelConfig 里的 `max_seq_len=512`）。
- **填充**：如果文本太短，用 `pad_token_id` 填充到 `max_length`，确保所有样本长度一致，才能拼成批次。

##### （3）构造损失掩码（loss_mask）

python



运行









```
loss_mask = [1] * text_len + [0] * padding_len
```

- **核心逻辑**：`loss_mask` 是一个和 `input_id` 长度相同的列表，**真实文本部分是 1，填充部分是 0**。

- 为什么这么做

  ：

  - 填充部分（`[pad]`）是无意义的，计算损失时应该忽略，否则会浪费算力，还会误导模型学习无意义的填充 token。
  - 训练时，把 `loss_mask` 和模型计算的损失相乘，填充部分的损失会被乘以 0，直接忽略。

  

**对应学习笔记知识点**：解决 “填充部分浪费算力” 的问题，优化训练效率。

##### （4）构造自回归模型的训练样本（X/Y 右移）

python



运行









```
input_id = np.array(input_id)
X = np.array(input_id[:-1]).astype(np.int64)  # 输入：去掉最后一个 token
Y = np.array(input_id[1:]).astype(np.int64)   # 标签：去掉第一个 token（右移）
loss_mask = np.array(loss_mask[1:]).astype(np.int64)  # 损失掩码也右移
return torch.from_numpy(X), torch.from_numpy(Y), torch.from_numpy(loss_mask)
```

- 这是自回归语言模型（LLaMA2/GPT）的核心训练逻辑

  ：

  - **自回归模型的本质**：给定前面的 token，预测下一个 token。
  - **`X`（输入）**：`input_id[:-1]`，比如 `[<s>, 我, 在, 学, 习]`。
  - **`Y`（标签）**：`input_id[1:]`，比如 `[我, 在, 学, 习, LLaMA]`。
  - 训练时，模型输入 `X`，预测 `Y`，也就是 “用 `<s>` 预测 `我`，用 `<s> 我` 预测 `在`，以此类推”。

  

- **损失掩码也右移**：因为 `Y` 是右移后的，所以 `loss_mask` 也要对应右移，确保填充部分的损失被正确忽略。

- **转成 PyTorch 张量**：最后用 `torch.from_numpy` 把 numpy 数组转成 PyTorch 张量，模型可以直接接收。

**对应学习笔记知识点**：自回归模型的样本构造逻辑，这是 LLM 预训练的核心。

------

## 这段代码的核心工程化亮点（对应学习笔记）

1. **O (1) 随机访问**：预计算字节偏移量，解决大语料随机访问慢的问题，速度提升 100 倍以上。
2. **懒加载**：每次只读取一条文本，100GB 语料也能在 16GB 内存的机器上训练，不爆内存。
3. **自回归样本构造**：手动实现 `X`/`Y` 右移，完美适配 LLaMA2 等自回归模型的训练逻辑。
4. **损失掩码**：忽略填充部分的损失，优化训练效率，避免误导模型。
5. **鲁棒性强**：用二进制模式打开文件，避免编码问题；预计算偏移量，确保随机访问稳定。

------

## 适配你的 Tiny-K 模型的使用示例

python



运行









```
from torch.utils.data import DataLoader
from transformers import AutoTokenizer

# 1. 加载你之前训练好的 Tokenizer
tokenizer = AutoTokenizer.from_pretrained("tokenizer_k")
tokenizer.pad_token = "<|im_end|>"  # 确保 pad_token 已设置

# 2. 初始化 Dataset
dataset = PretrainDataset(
    data_path="your_train_data.jsonl",
    tokenizer=tokenizer,
    max_length=512  # 对应你的 ModelConfig 里的 max_seq_len
)

# 3. 封装成 DataLoader
dataloader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True,
    num_workers=4,
    pin_memory=True
)

# 4. 遍历批次，喂给模型训练
for X, Y, loss_mask in dataloader:
    print("输入 X 形状：", X.shape)  # torch.Size([2, 511])
    print("标签 Y 形状：", Y.shape)  # torch.Size([2, 511])
    # 这里就可以喂给你的 Tiny-K 模型了：
    # outputs = model(X, labels=Y)
    # loss = outputs.loss * loss_mask
    # loss = loss.mean()
    # loss.backward()
```



这段代码是一个**专门用于对话模型有监督微调（SFT, Supervised Fine-Tuning）的高性能 Dataset 实现**，它在之前 `PretrainDataset` 的基础上，做了两个核心升级：

1. **用 `apply_chat_template` 自动格式化多轮对话**；
2. **用 `generate_loss_mask` 精准标记损失计算区域 —— 只对 `assistant` 的回复部分计算损失，忽略 `user`/`system` 的输入部分**。

这是把预训练模型（Tiny-K/LLaMA2）变成对话模型的**核心数据层代码**。

------

## 整体逻辑总览

和 `PretrainDataset` 一样继承自 PyTorch 原生 `Dataset`，保留了「预计算字节偏移量实现 O (1) 随机访问」的工程化亮点，核心变化是**输入从单条文本变成多轮对话**，**损失从全量计算变成仅计算 assistant 回复部分**。

------

## 分模块详细逻辑拆解

### 模块 1：`__init__` / `__len__` —— 和预训练完全一致，高效懒加载

python



运行









```
def __init__(self, data_path, tokenizer, max_length=512):
    # ... 和 PretrainDataset 完全相同 ...
    # 预计算字节偏移量，O(1) 随机访问
    # 懒加载，不爆内存
```

- 逻辑完全复用 `PretrainDataset` 的工程化设计：预计算 JSONL 每行的字节偏移量，实现 O (1) 随机访问；懒加载，100GB 大语料也能流畅运行。
- **对应学习笔记知识点**：解决 “大语料读取慢”“爆内存” 的问题。

------

### 模块 2：`__getitem__` —— 核心变化：多轮对话格式化

这是和预训练 Dataset 的第一个核心区别：输入不再是单条文本，而是多轮对话历史。

#### 逻辑拆解

python



运行









```
sample = json.loads(line)  # sample 是多轮对话列表，比如：
# [{"role": "system", "content": "你是AI助手"},
#  {"role": "user", "content": "你好"},
#  {"role": "assistant", "content": "你好！有什么可以帮你？"}]

text = self.tokenizer.apply_chat_template(
    sample, 
    tokenize=False, 
    add_generation_prompt=False
)
# 自动格式化成 ChatML 标准对话格式：
# <|im_start|>system
# 你是AI助手<|im_end|>
# <|im_start|>user
# 你好<|im_end|>
# <|im_start|>assistant
# 你好！有什么可以帮你？<|im_end|>
```

#### 关键细节

1. `sample` 的格式

   ：

   - 必须是多轮对话列表，每个元素是 `{"role": "...", "content": "..."}`，`role` 只能是 `system`/`user`/`assistant`。
   - 这是现在 Hugging Face、OpenAI 通用的对话数据格式。

   

2. `apply_chat_template`

   ：

   - 直接调用 Tokenizer 里预定义的 Jinja2 对话模板（就是你之前在 `create_tokenizer_config` 里写的 `chat_template`），自动把多轮对话转成 ChatML 格式的文本。
   - **工程化意义**：避免手动拼接字符串出错，确保预训练 / 微调 / 推理三阶段的对话格式完全一致。
   - **对应学习笔记知识点**：“全流程一致性”。

   

后续的分词、截断、填充逻辑和预训练完全一致，不再赘述。

------

### 模块 3：`generate_loss_mask` —— SFT 的核心：只对 assistant 回复计算损失

这是这段代码**最核心、最关键的逻辑**，也是 SFT 和预训练的本质区别。

#### 为什么需要这个方法？

- **预训练**：目标是 “通用语言建模”，给定前面的 token，预测下一个 token，所以对**所有 token** 都计算损失。

- SFT

  ：目标是 “让模型学会根据 user 的问题生成 assistant 的回复”，所以：

  - `system`/`user` 的部分是**输入提示**，不需要模型预测，不计算损失；
  - 只有 `assistant` 的回复部分是**目标输出**，需要计算损失。

  

如果不对损失做掩码，模型会浪费算力学习 `user` 的问题，甚至会被误导，学会 “预测 user 说什么” 而不是 “生成 assistant 的回复”。

#### 逐行逻辑拆解

python



运行









```
def generate_loss_mask(self, input_ids):
    # 1. 初始化全 0 的 mask：默认所有位置都不计算损失
    mask = [0] * len(input_ids)
    
    # 2. 定义 assistant 回复的起始标记：<|im_start|>assistant\n 的 token 序列
    a_sequence = self.tokenizer("<|im_start|>assistant\n")['input_ids']
    a_length = len(a_sequence)
    n = len(input_ids)
    i = 0
    
    # 3. 遍历 input_ids，找所有 assistant 起始标记的位置
    while i <= n - a_length:
        # 3.1 检查当前位置是否匹配 assistant 起始标记
        match = True
        for k in range(a_length):
            if input_ids[i + k] != a_sequence[k]:
                match = False
                break
        
        if match:
            # 3.2 找到起始标记后，往后找 eos_token_id（<|im_end|>，ID=4）
            # 这是 assistant 回复的结束位置
            j = None
            for idx in range(i + a_length, n):
                if input_ids[idx] == self.tokenizer.eos_token_id:
                    j = idx
                    break
            
            # 3.3 把 assistant 回复部分的 mask 设为 1（计算损失）
            if j is not None:
                start = i + a_length  # assistant 回复的起始位置
                end = j                # assistant 回复的结束位置（包含 eos_token）
                if start <= end:
                    for pos in range(start, end + 1):
                        if pos < len(mask):
                            mask[pos] = 1
            
            # 3.4 跳过当前匹配的子序列，避免重叠匹配
            i += a_length
        else:
            i += 1
    
    return mask
```

#### 直观示例

假设 `input_ids` 对应的文本是：

plaintext











```
<|im_start|>system\n你是AI助手<|im_end|>\n<|im_start|>user\n你好<|im_end|>\n<|im_start|>assistant\n你好！有什么可以帮你？<|im_end|>
```

那么生成的 `loss_mask` 是：

plaintext











```
[0, 0, ..., 0, 1, 1, ..., 1, 0, 0, ...]
# system/user 部分全是 0（不计算损失）
# assistant 回复部分全是 1（计算损失）
```

------

### 模块 4：最后一步：构造自回归样本

python



运行









```
input_id = np.array(input_id)
X = np.array(input_id[:-1]).astype(np.int64)
Y = np.array(input_id[1:]).astype(np.int64)
loss_mask = np.array(loss_mask[1:]).astype(np.int64)
return torch.from_numpy(X), torch.from_numpy(Y), torch.from_numpy(loss_mask)
```

- 和预训练完全一致：`X` 是去掉最后一个 token 的输入，`Y` 是去掉第一个 token 的标签（右移），`loss_mask` 也对应右移。
- 训练时，把模型计算的损失和 `loss_mask` 相乘，只保留 assistant 回复部分的损失，其余部分损失为 0。

------

## 这段代码的核心工程化亮点（针对 SFT）

1. **O (1) 随机访问 + 懒加载**：复用预训练的高效设计，大语料也能流畅运行。
2. **`apply_chat_template` 自动格式化**：确保预训练 / 微调 / 推理三阶段对话格式完全一致，避免手动拼接出错。
3. **精准的 `loss_mask`**：只对 assistant 回复部分计算损失，节省算力，避免误导模型，让模型专注于学习 “生成正确的回复”。
4. **鲁棒性强**：有重叠匹配避免逻辑，有边界检查（`pos < len(mask)`），不会因为边界问题崩溃。

------

## 适配你的 Tiny-K 模型的使用示例

python



运行









```
from torch.utils.data import DataLoader
from transformers import AutoTokenizer

# 1. 加载你之前训练好的 Tokenizer（带 chat_template）
tokenizer = AutoTokenizer.from_pretrained("tokenizer_k")
tokenizer.pad_token = "<|im_end|>"

# 2. 初始化 SFT Dataset
# 你的 sft_data.jsonl 每行应该是一个多轮对话列表，比如：
# [{"role": "user", "content": "你好"}, {"role": "assistant", "content": "你好！"}]
dataset = SFTDataset(
    data_path="sft_data.jsonl",
    tokenizer=tokenizer,
    max_length=512
)

# 3. 封装成 DataLoader
dataloader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True,
    num_workers=4,
    pin_memory=True
)

# 4. 遍历批次，喂给模型微调
for X, Y, loss_mask in dataloader:
    print("输入 X 形状：", X.shape)  # torch.Size([2, 511])
    print("标签 Y 形状：", Y.shape)  # torch.Size([2, 511])
    print("损失掩码形状：", loss_mask.shape)  # torch.Size([2, 511])
    
    # 喂给模型微调：
    # outputs = model(X, labels=Y)
    # loss = outputs.loss * loss_mask  # 只保留 assistant 部分的损失
    # loss = loss.sum() / loss_mask.sum()  # 对有效损失取平均
    # loss.backward()
```