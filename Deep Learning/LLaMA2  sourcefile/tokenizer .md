# Tokenizer 核心学习笔记

![image-20260311201422569](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260311201422569.png)

## 一、Tokenizer 在 LLM 体系中的核心定位

Tokenizer（分词器）是**连接人类文本世界与模型数字世界的唯一、不可拆分的双向桥梁**，贯穿 LLM 全生命周期。

### 1. 全链路固定位置

- **预训练**：原始语料 → Tokenizer 编码 → Token ID 序列 → 模型训练
- **微调**：任务指令 → Tokenizer 标准化编码 → 模型微调
- **推理**：用户输入 → Tokenizer 编码 → 模型生成 ID → Tokenizer 解码 → 输出文本

### 2. 对模型的决定性影响

1. **参数量与成本**：词表大小（`vocab_size`）直接决定 Embedding 层参数量（`dim × vocab_size`）。
2. **上下文利用率**：分词压缩率决定相同文本的序列长度，压缩率越低越浪费窗口。
3. **泛化能力**：OOV（未登录词）率、语义完整性决定模型对新词 / 低资源语言的理解能力。
4. **全流程一致性**：预训练规则一旦确定，微调 / 推理不可修改，否则分布偏移导致效果崩溃。

------

## 二、核心设计目标与三代方案演进

### 1. 设计的核心矛盾

所有 Tokenizer 都是在三大矛盾中找平衡：

- **词表大小** vs **OOV 率** vs **序列压缩率**

### 2. 三代主流方案的实现思路

表格







|           方案类型           |                 核心思路                 |                             优势                             |                           致命缺陷                           |            现状             |
| :--------------------------: | :--------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :-------------------------: |
|    **词级 (Word-based)**     |         按空格 / 标点切分完整词          |                粒度最粗，压缩率最高，符合直觉                | 1. 词表爆炸（英文需百万级）；2. OOV 严重（新词 / 生僻字）；3. 形态学割裂（`run`/`running`） |      已被主流 LLM 淘汰      |
| **字符级 (Character-based)** |          每个字符作为一个 Token          |                     词表极小，完全无 OOV                     | 1. 序列长度爆炸，严重浪费上下文；2. 字符无语义，训练难度陡增 |     仅用于极低资源语言      |
|  **子词级 (Subword-based)**  | **常用词不拆分，罕见词拆分为有意义子词** | 1. 词表可控（32k-128k）；2. 几乎零 OOV；3. 保留语义，兼顾压缩率；4. 可学习词根词缀 |                 实现复杂度较高，需预训练词表                 | **所有主流 LLM 的唯一选择** |

------

## 三、子词级三大主流算法核心逻辑

### 1. BPE (Byte-Pair Encoding) —— LLaMA/GPT 首选

**实现思路**：

1. **初始状态**：从最基础的字符 / 字节（UTF-8）开始，初始词表仅 256 个字节。
2. **迭代合并**：统计语料中相邻字符对的频率，合并频率最高的一对为新子词。
3. **终止条件**：重复合并，直到词表达到预设大小（如 6144、32000）。

**核心优势**：逻辑极简、可控性强、词表大小精准、工业界最成熟。

### 2. WordPiece —— BERT/T5 采用

**实现思路**：基于 BPE，但合并规则从 “频率最高” 改为 “合并后能最大化语言模型联合概率”，优先合并有强语义关联的子词。

### 3. Unigram —— 多语言模型采用

**实现思路**：从一个超大初始词表开始，迭代计算每个子词对模型概率的影响，删除影响最小的冗余子词，直到达到目标大小。

------

## 四、落地中的核心问题与工业界优化方案

### 1. 问题一：未登录词 (OOV) 导致语义丢失

**优化方案**：

- **字节级 BPE (Byte-level BPE)**：LLaMA2 标准方案。先将所有文本转 UTF-8 字节（0-255），再做 BPE。从根源实现**零 OOV**，完美覆盖所有语言、emoji、生僻字。
- **领域自适应预训练**：在通用词表基础上，用目标领域语料（中文、代码）继续训练，合并领域高频子词。

### 2. 问题二：分词粒度不合理（过拆 / 过合）

**优化方案**：

- **规模匹配原则**：轻量小模型（<7B）用 4k-32k 词表，大模型用 32k-128k 词表。
- **最小频率阈值**：训练时设置 `min_frequency`，避免合并极低频次子词，减少词表冗余。
- **压缩率验证**：训练后用目标语料验证，确保相同文本的序列长度在合理范围内。

### 3. 问题三：预训练与下游任务分布偏移

**优化方案**：

- **全流程锁定**：预训练完成后，词表、分词规则、特殊 Token 定义全程锁定，不做任何修改。
- **标准化预处理**：预训练 / 微调 / 推理三阶段，使用完全一致的文本清洗、空格归一化、全角半角转换规则。

### 4. 问题四：推理效率低

**优化方案**：

- **底层高性能实现**：采用 C++/Rust 内核（如 Hugging Face `tokenizers` 库），速度比 Python 快 10-100 倍。
- **高频内容预编码缓存**：对系统提示词等固定内容，提前编码并缓存。

------

## 五、极简实现流程概括（参考开源项目思路）

### 目标

训练一个适配类 LLaMA2 轻量模型（Tiny-K）的 Tokenizer。

### 核心步骤

1. **语料准备**：

   

   - 收集 / 清洗目标语料（≥100MB），去重、过滤低质量文本。
   - 保存为纯文本格式（`.txt`，每行一个段落）。

   

2. **配置训练参数**：

   

   - 设定目标词表大小（如 `vocab_size=6144`）。
   - 设定子词最小频率（如 `min_frequency=2`）。
   - 预留特殊 Token：`<s>`（句首）、`</s>`（句尾）、`<pad>`（填充）、`<unk>`（未知）。

   

3. **训练（Byte-level BPE）**：

   

   - 初始化：从 UTF-8 字节（256 个）开始。
   - 迭代：统计字节对频率 → 合并最高频 → 更新词表。
   - 终止：达到目标词表大小。

   

4. **验证与后处理**：

   

   - 测试典型文本（中文、英文、生僻词、emoji），确保常用词不拆分。
   - 添加后处理模板：自动在句首加 `<s>`，句尾加 `</s>`。

   

5. **保存与对接**：

   

   - 保存为 Hugging Face 标准格式（`tokenizer.json`）。
   - 锁定规则，后续全流程复用，不做修改。





## 整体逻辑总览

这是典型的**模块化、流水线设计**，和我们之前讲的 “代码书写思路” 完全一致：

<svg aria-roledescription="flowchart-v2" role="graphics-document document" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/2000/svg" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ev="http://www.w3.org/2001/xml-events"><g transform="matrix(0.6941391941391941,0,0,0.6941391941391941,319.71082303113553,0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><marker orient="auto" markerHeight="8" markerWidth="8" markerUnits="userSpaceOnUse" refY="5" refX="5" viewBox="0 0 10 10" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 0 0 L 10 5 L 0 10 z"></path></marker><marker orient="auto" markerHeight="8" markerWidth="8" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 0 5 L 10 10 L 10 0 z"></path></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><circle style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" r="5" cy="5" cx="5"></circle></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><circle style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" r="5" cy="5" cx="5"></circle></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 1,1 l 9,9 M 10,1 l -9,9"></path></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 1,1 l 9,9 M 10,1 l -9,9"></path></marker><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path marker-end="url(#svg-mermaid-diagram-4ksj3rf_flowchart-v2-pointEnd)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M103.422,74L103.422,78.167C103.422,82.333,103.422,90.667,103.422,98.333C103.422,106,103.422,113,103.422,116.5L103.422,120"></path><path marker-end="url(#svg-mermaid-diagram-4ksj3rf_flowchart-v2-pointEnd)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M103.422,190L103.422,194.167C103.422,198.333,103.422,206.667,103.422,214.333C103.422,222,103.422,229,103.422,232.5L103.422,236"></path><path marker-end="url(#svg-mermaid-diagram-4ksj3rf_flowchart-v2-pointEnd)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M103.422,306L103.422,310.167C103.422,314.333,103.422,322.667,103.422,330.333C103.422,338,103.422,345,103.422,348.5L103.422,352"></path><path marker-end="url(#svg-mermaid-diagram-4ksj3rf_flowchart-v2-pointEnd)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M103.422,422L103.422,426.167C103.422,430.333,103.422,438.667,103.422,446.333C103.422,454,103.422,461,103.422,464.5L103.422,468"></path></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(103.421875, 41)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="181.30208587646484" y="-33" x="-90.65104293823242" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-60.65104293823242, -18)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="121.30208587646484" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">1. 数据读取<br style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">read_texts_from_jsonl</span></div></foreignObject></g></g><g transform="translate(103.421875, 157)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="142.67708587646484" y="-33" x="-71.33854293823242" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-41.33854293823242, -18)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="82.67708587646484" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">2. 核心训练<br style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">train_tokenizer</span></div></foreignObject></g></g><g transform="translate(103.421875, 273)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="190.84375" y="-33" x="-95.421875" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-65.421875, -18)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="130.84375" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">3. 配置生成<br style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">create_tokenizer_config</span></div></foreignObject></g></g><g transform="translate(103.421875, 389)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="139.23958587646484" y="-33" x="-69.61979293823242" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-39.61979293823242, -18)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="79.23958587646484" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">4. 效果验证<br style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">eval_tokenizer</span></div></foreignObject></g></g><g transform="translate(103.421875, 505)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="134.3229217529297" y="-33" x="-67.16146087646484" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-37.161460876464844, -18)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="74.32292175292969" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">5. 主流程串联<br style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">main</span></div></foreignObject></g></g></g></g></g></g></svg>

```
graph TD
    A[1. 数据读取<br>read_texts_from_jsonl] --> B[2. 核心训练<br>train_tokenizer]
    B --> C[3. 配置生成<br>create_tokenizer_config]
    C --> D[4. 效果验证<br>eval_tokenizer]
    D --> E[5. 主流程串联<br>main]
```

<svg aria-roledescription="flowchart-v2" role="graphics-document document" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/2000/svg" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ev="http://www.w3.org/2001/xml-events"><g transform="matrix(1.7124542124542124,0,0,1.7124542124542124,672.394774496337,0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><marker orient="auto" markerHeight="8" markerWidth="8" markerUnits="userSpaceOnUse" refY="5" refX="5" viewBox="0 0 10 10" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 0 0 L 10 5 L 0 10 z"></path></marker><marker orient="auto" markerHeight="8" markerWidth="8" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 0 5 L 10 10 L 10 0 z"></path></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><circle style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" r="5" cy="5" cx="5"></circle></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><circle style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" r="5" cy="5" cx="5"></circle></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 1,1 l 9,9 M 10,1 l -9,9"></path></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 1,1 l 9,9 M 10,1 l -9,9"></path></marker><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path marker-end="url(#svg-mermaid-diagram-huzvjbg_flowchart-v2-pointEnd)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M103.422,74L103.422,78.167C103.422,82.333,103.422,90.667,103.422,98.333C103.422,106,103.422,113,103.422,116.5L103.422,120"></path><path marker-end="url(#svg-mermaid-diagram-huzvjbg_flowchart-v2-pointEnd)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M103.422,190L103.422,194.167C103.422,198.333,103.422,206.667,103.422,214.333C103.422,222,103.422,229,103.422,232.5L103.422,236"></path><path marker-end="url(#svg-mermaid-diagram-huzvjbg_flowchart-v2-pointEnd)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M103.422,306L103.422,310.167C103.422,314.333,103.422,322.667,103.422,330.333C103.422,338,103.422,345,103.422,348.5L103.422,352"></path><path marker-end="url(#svg-mermaid-diagram-huzvjbg_flowchart-v2-pointEnd)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M103.422,422L103.422,426.167C103.422,430.333,103.422,438.667,103.422,446.333C103.422,454,103.422,461,103.422,464.5L103.422,468"></path></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(103.421875, 41)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="181.30208587646484" y="-33" x="-90.65104293823242" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-60.65104293823242, -18)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="121.30208587646484" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">1. 数据读取<br style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">read_texts_from_jsonl</span></div></foreignObject></g></g><g transform="translate(103.421875, 157)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="142.67708587646484" y="-33" x="-71.33854293823242" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-41.33854293823242, -18)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="82.67708587646484" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">2. 核心训练<br style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">train_tokenizer</span></div></foreignObject></g></g><g transform="translate(103.421875, 273)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="190.84375" y="-33" x="-95.421875" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-65.421875, -18)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="130.84375" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">3. 配置生成<br style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">create_tokenizer_config</span></div></foreignObject></g></g><g transform="translate(103.421875, 389)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="139.23958587646484" y="-33" x="-69.61979293823242" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-39.61979293823242, -18)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="79.23958587646484" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">4. 效果验证<br style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">eval_tokenizer</span></div></foreignObject></g></g><g transform="translate(103.421875, 505)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="134.3229217529297" y="-33" x="-67.16146087646484" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-37.161460876464844, -18)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="74.32292175292969" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">5. 主流程串联<br style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">main</span></div></foreignObject></g></g></g></g></g></g></svg>

分模块详细逻辑拆解

### 模块 1：数据读取 `read_texts_from_jsonl` —— 解决大语料爆内存的问题

**核心逻辑**：用 Python **生成器（Generator）** 实现懒加载，每次只从磁盘读取一条文本，绝不把整个语料全量加载进内存。

#### 关键细节

1. `Generator[str, None, None]`

   ：

   - 这是类型提示，说明这是一个生成器，每次 `yield` 一个字符串（单条文本）。
   - **对应笔记知识点**：解决 “大语料无法全量加载进内存” 的痛点，内存占用仅和单条文本有关，和语料总大小无关。

   

2. 异常处理

   ：

   - `try-except` 捕获 JSON 解码错误、缺 `text` 字段的错误，打印警告后直接 `continue` 跳过，不会让整个程序因为一条坏数据崩溃。
   - **工程化意义**：真实语料里一定有脏数据，这是必须的鲁棒性设计。

   

3. `enumerate(f, 1)`

   ：

   - 行号从 1 开始计数，报错时能精准定位是哪一行出了问题，方便调试。

   

------

### 模块 2：核心训练 `train_tokenizer` —— Byte-level BPE 的完整落地

这是代码的核心，完全对应学习笔记里的 “子词级 BPE 训练流程”。

#### 逻辑拆解

##### （1）初始化 Tokenizer：Byte-level BPE 配置





```
tokenizer = Tokenizer(models.BPE(unk_token="<unk>"))
tokenizer.normalizer = NFKC()  # Unicode 规范化
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
tokenizer.decoder = decoders.ByteLevel()
```

- **`models.BPE`**：核心算法选 BPE，对应 LLaMA/GPT 方案。

- `NFKC()`

  ：

  Unicode 规范化

  ，把全角字符转半角、把带重音的字符拆成 “字符 + 重音符号”，确保相同语义的不同写法被分成同一个 Token。

  - **对应笔记知识点**：“全流程文本预处理一致性”，预训练 / 微调 / 推理必须用相同的规范化规则。

  

- `pre_tokenizers.ByteLevel` + `decoders.ByteLevel`

  ：

  - 这是 **Byte-level BPE 的核心**：先把所有文本转成 UTF-8 字节（0-255），再做 BPE。
  - **对应笔记知识点**：从根源实现 “零 OOV”，完美覆盖所有语言、emoji、生僻字。

  

##### （2）配置 Trainer：控制词表大小与质量



```
trainer = trainers.BpeTrainer(
    vocab_size=vocab_size,  # 6144，对应你的 Tiny-K 模型
    special_tokens=special_tokens,
    min_frequency=2,  # 过滤低频子词
    show_progress=True,
    initial_alphabet=pre_tokenizers.ByteLevel.alphabet()  # 初始词表是 UTF-8 字节
)
```

- `vocab_size=6144`

  ：词表大小和你的模型规模匹配（轻量模型用 4k-16k）。

  - **对应笔记知识点**：“规模匹配原则”。

  

- `min_frequency=2`

  ：只合并出现频率≥2 的字节对，避免把极低频次的随机组合加入词表，减少词表冗余。

  - **对应笔记知识点**：“最小频率阈值控制”。

  

- `initial_alphabet=pre_tokenizers.ByteLevel.alphabet()`

  ：

  - 强制初始词表是完整的 UTF-8 字节（256 个），这是 Byte-level BPE 能零 OOV 的前提。

  

##### （3）训练：用生成器喂数据



```
texts = read_texts_from_jsonl(data_path)
tokenizer.train_from_iterator(texts, trainer=trainer, length=os.path.getsize(data_path))
```

- **`train_from_iterator`**：接收生成器 `texts`，边读边训练，绝不把整个语料加载进内存。
- **`length=os.path.getsize(data_path)`**：传入文件大小，让进度条（`show_progress=True`）能准确显示训练进度。

##### （4）验证特殊 Token 映射：全流程一致性的关键



```
assert tokenizer.token_to_id("<unk>") == 0
assert tokenizer.token_to_id("<s>") == 1
# ... 其他特殊 Token
```

- 强制固定特殊 Token 的 ID

  ：比如 

  ```
  <unk>
  ```

   必须是 0，

  ```
  <s>
  ```

   必须是 1。

  - **对应笔记知识点**：“全流程锁定”—— 预训练时的 ID 和微调 / 推理时必须完全一致，否则会出现分布偏移，模型效果直接崩溃。

  

------

### 模块 3：配置生成 `create_tokenizer_config` —— 完美对接 Hugging Face 生态

这个函数生成两个 Hugging Face 标准的配置文件，让你训练的 Tokenizer 能直接用 `AutoTokenizer.from_pretrained` 加载，和所有开源模型兼容。

#### 关键配置解读

##### （1）`tokenizer_config.json`：对话模型的核心适配



```
{
    "bos_token": "<|im_start|>",
    "eos_token": "<|im_end|>",
    "pad_token": "<|im_end|>",  // 复用 eos_token，节省词表空间
    "chat_template": "{% for message in messages %}...{% endfor %}"  // Jinja2 对话模板
}
```

- ChatML 格式特殊 Token

  ：

  ```
  <|im_start|>
  ```

  （对话开始）、

  ```
  <|im_end|>
  ```

  （对话结束），这是现在 GPT、Claude 等对话模型通用的格式。

  - **对应笔记知识点**：“预留特殊 Token”。

  

- `chat_template`

  ：Jinja2 模板，用来把多轮对话历史（

  ```
  [{"role": "user", "content": "..."}, ...]
  ```

  ）自动格式化成模型能接受的输入字符串。

  - **工程化意义**：这是对话模型微调 / 推理的核心，不用自己手写字符串拼接逻辑，避免出错。

  

- **`model_max_length` 设得极大**：`1000000000000000019884624838656`，这是一个 trick，避免 Tokenizer 在预处理时自动截断文本，把截断的控制权完全交给用户。

##### （2）`special_tokens_map.json`：特殊 Token 的映射表

这个文件是 `AutoTokenizer` 加载时的辅助文件，确保特殊 Token 能被正确识别。

------

### 模块 4：效果验证 `eval_tokenizer` —— 确保全流程一致性

训练完必须验证，这是避免后续踩坑的关键，对应学习笔记里的 “训练后验证分词效果”。

#### 验证逻辑拆解

1. **加载测试**：用 `AutoTokenizer.from_pretrained` 加载，确保配置文件是对的，能完美对接 Hugging Face 生态。

2. **基本信息测试**：打印词表大小、特殊 Token 列表，确认和训练时一致。

3. 聊天模板测试

   ：

   - 用 `apply_chat_template` 把多轮对话转成格式化的 prompt，这是对话模型的核心功能。
   - 验证生成的 prompt 是否符合 ChatML 格式。

   

4. 编码解码 Round-trip 测试

   ：

   - 把文本编码成 Token ID，再解码回文本，确认和原文完全一致（`decoded == prompt`）。
   - **对应笔记知识点**：确保没有信息丢失，分词规则是可逆的。

   

5. 特殊 Token 测试

   ：

   - 测试特殊 Token（`<|im_start|>`）是否能被正确识别，不会被切分成普通子词。
   - 验证解码后特殊 Token 是否被保留。

   

------

### 模块 5：主流程 `main` —— 把所有模块串起来

python



运行









```
def main():
    data_path = "your data path"
    save_dir = "tokenizer_k"
    train_tokenizer(data_path=data_path, save_dir=save_dir, vocab_size=6144)
    eval_tokenizer(save_dir)
```

- 逻辑极简：配置路径 → 训练 → 评估。

- ```
  random.seed(42)
  ```

  ：固定随机种子，确保每次训练的结果完全一致，可复现。

  - **对应笔记知识点**：“固定随机种子”。

  

------

## 这段代码的核心工程化亮点（对应学习笔记）

1. **解决大语料问题**：用生成器（Generator）+ `train_from_iterator` 实现懒加载，100GB 语料也能在 16GB 内存的机器上训练。

2. **零 OOV**：用 Byte-level BPE + UTF-8 初始字母表，完美覆盖所有语言和符号。

3. 全流程一致性

   ：

   - 固定特殊 Token ID；
   - 用 NFKC 做 Unicode 规范化；
   - 验证 Round-trip 确保无信息丢失。

   

4. **完美对接生态**：生成 Hugging Face 标准配置文件，支持 `AutoTokenizer` 加载，支持 `chat_template` 对话模板。

5. **鲁棒性强**：有异常处理，不会因为一条坏数据崩溃；有验证环节，确保训练结果可用。