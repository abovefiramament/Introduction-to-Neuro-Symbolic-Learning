import torch
import torch.nn.functional as F
@torch.inference_mode()
def generate(self, idx, stop_id=None, max_new_tokens=256, temperature=1.0, top_k=None):
    """
    给定输入序列 idx（形状为 (bz,seq_len) 的长整型张量），通过多次生成新 token 来完成序列。
    在 model.eval() 模式下运行。效率较低的采样版本，没有使用键k/v cache。
    """
    index = idx.shape[1]
    for _ in range(max_new_tokens):
        # 如果序列上下文过长，截断它到最大长度
        idx_cond = idx if idx.size(1) <= self.args.max_seq_len else idx[:, -self.args.max_seq_len:]

        # 前向传播获取序列中最后一个位置的 logits
        logits = self(idx_cond).logits
        logits = logits[:, -1, :]  # 只保留最后一个时间步的输出

        if temperature == 0.0:
            # 选择最有可能的索引
            _, idx_next = torch.topk(logits, k=1, dim=-1)
        else:
            # 缩放 logits 并应用 softmax
            logits = logits / temperature
            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = -float('Inf')
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)

        if idx_next == stop_id:
            break

        # 将采样的索引添加到序列中并继续
        idx = torch.cat((idx, idx_next), dim=1)

    return idx[:, index:]  # 只返回生成的token
