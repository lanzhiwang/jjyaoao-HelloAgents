# HelloAgents RL 训练指南

本指南介绍如何使用 HelloAgents 的强化学习训练功能.

## 📚 详细文档

- [数据集 API](datasets.md) - 数据集加载和处理
- [奖励函数 API](rewards.md) - 奖励函数创建和使用
- [训练器 API](trainers.md) - SFT 和 GRPO 训练器
- [RLTrainingTool](rl_training_tool.md) - 统一训练工具(推荐)

## 目录

- [安装](#安装)
- [快速开始](#快速开始)
- [训练算法](#训练算法)
- [使用示例](#使用示例)
- [高级配置](#高级配置)
- [常见问题](#常见问题)

## 安装

### 方式1: 安装完整的 RL 功能(推荐)

```bash
pip install hello-agents[rl]
```

这将安装以下依赖:

- `trl`: Transformer Reinforcement Learning 库
- `transformers`: HuggingFace Transformers
- `torch`: PyTorch
- `datasets`: HuggingFace Datasets
- `accelerate`: 分布式训练加速
- `peft`: LoRA 等参数高效微调
- `bitsandbytes`: 量化支持
- `wandb`: 训练监控(可选)
- `tensorboard`: TensorBoard 支持(可选)

### 方式2: 单独安装 TRL

```bash
pip install trl
```

### 验证安装

```python
from hello_agents.rl import TRL_AVAILABLE

if TRL_AVAILABLE:
    print("✅ TRL 已安装, 可以开始训练")
else:
    print("❌ TRL 未安装")
```

## 快速开始

### 使用工具接口

```python
from hello_agents.tools import RLTrainingTool

# 创建 RL 训练工具
rl_tool = RLTrainingTool()

# SFT 训练
result = rl_tool.run({
    "algorithm": "sft",
    "model_name": "Qwen/Qwen2-0.5B-Instruct",
    "dataset": "gsm8k",
    "max_samples": 100,
    "num_epochs": 3,
    "output_dir": "./output/sft"
})

print(result)
```

### 加载数据集

```python
# 加载 SFT 格式数据集
result = rl_tool.run({
    "action": "load_dataset",
    "format": "sft",
    "split": "train",
    "max_samples": 100
})

# 加载 RL 格式数据集
result = rl_tool.run({
    "action": "load_dataset",
    "format": "rl",
    "split": "train",
    "max_samples": 100,
    "model_name": "Qwen/Qwen3-0.6B"
})
```

### 在 Agent 中使用

```python
from hello_agents.agents import SimpleAgent
from hello_agents.tools import RLTrainingTool
from hello_agents.core import LLMConfig

# 创建 Agent
agent = SimpleAgent(
    name="TrainingAgent",
    llm_config=LLMConfig(model="gpt-4o-mini"),
    tools=[RLTrainingTool()]
)

# 让 Agent 执行训练任务
response = agent.run(
    "请用 SFT 算法训练一个 Qwen2-0.5B 模型, 使用 gsm8k 数据集, 训练 3 轮"
)
```

## 训练算法

### SFT (Supervised Fine-Tuning)

监督微调, 让模型学会遵循指令和基本的推理格式.

适用场景:

- 模型初始对齐
- 学习特定任务格式
- 作为 RL 训练的基础

示例:

```python
rl_tool.run({
    "action": "train",
    "algorithm": "sft",
    "model_name": "Qwen/Qwen3-0.6B",
    "max_samples": 1000,
    "num_epochs": 3,
    "output_dir": "./output/sft",
    "use_lora": True,
    "batch_size": 4
})
```

### GRPO (Group Relative Policy Optimization)

群体相对策略优化, 通过强化学习优化模型的推理能力.

优势:

- 不需要 Value Model, 更简单
- 内存占用更少
- 训练速度更快
- 性能接近 PPO

适用场景:

- 优化推理能力
- 提高答案准确率
- Agentic RL 训练

示例:

```python
rl_tool.run({
    "action": "train",
    "algorithm": "grpo",
    "model_name": "Qwen/Qwen3-0.6B",
    "max_samples": 500,
    "num_epochs": 3,
    "output_dir": "./output/grpo",
    "use_lora": True,
    "batch_size": 2
})
```

### PPO (Proximal Policy Optimization)

近端策略优化, 经典的强化学习算法.

状态: 🚧 开发中

说明: PPO 需要额外的 Value Model, 实现更复杂. 建议使用 GRPO 作为替代.

## 使用示例

### 示例1: 完整训练流程

推荐的训练流程: 先 SFT, 再 GRPO

```python
from hello_agents.tools import RLTrainingTool

rl_tool = RLTrainingTool()

# 步骤1: SFT 训练
print("步骤1: SFT 训练...")
sft_result = rl_tool.run({
    "action": "train",
    "algorithm": "sft",
    "model_name": "Qwen/Qwen3-0.6B",
    "max_samples": 1000,
    "num_epochs": 3,
    "output_dir": "./output/sft"
})

# 步骤2: GRPO 训练(使用 SFT 后的模型)
print("步骤2: GRPO训练...")
grpo_result = rl_tool.run({
    "action": "train",
    "algorithm": "grpo",
    "model_name": "./output/sft",  # 使用 SFT 训练后的模型
    "max_samples": 500,
    "num_epochs": 3,
    "output_dir": "./output/grpo"
})

print("训练完成! 最终模型: ./output/grpo")
```

### 示例2: 快速测试

使用少量样本快速测试训练流程:

```python
# 快速 SFT 测试(10 个样本, 1 轮)
rl_tool.run({
    "action": "train",
    "algorithm": "sft",
    "model_name": "Qwen/Qwen3-0.6B",
    "max_samples": 10,
    "num_epochs": 1,
    "output_dir": "./output/test_sft"
})
```

### 示例3: 使用 LoRA 减少显存

```python
# 使用 LoRA 进行参数高效微调
rl_tool.run({
    "action": "train",
    "algorithm": "sft",
    "model_name": "Qwen/Qwen3-0.6B",
    "use_lora": True,  # 启用 LoRA
    "batch_size": 2,  # 小批次
    "output_dir": "./output/sft_lora"
})
```

## 高级配置

### 使用底层 API

如果需要更多控制, 可以直接使用底层 API:

```python
from hello_agents.rl import (
    TrainingConfig,
    create_sft_dataset,
    SFTTrainerWrapper,
    create_rl_dataset,
    create_accuracy_reward,
    GRPOTrainerWrapper
)

# 创建配置
config = TrainingConfig(
    model_name="Qwen/Qwen2-0.5B-Instruct",
    output_dir="./output/custom",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=5e-5,
    use_lora=True,
    lora_r=16,
    lora_alpha=32
)

# SFT 训练
dataset = create_sft_dataset(max_samples=1000)
trainer = SFTTrainerWrapper(config=config, dataset=dataset)
trainer.train()
trainer.save_model()

# GRPO 训练
rl_dataset = create_rl_dataset(max_samples=500)
reward_fn = create_accuracy_reward()
grpo_trainer = GRPOTrainerWrapper(
    config=config,
    dataset=rl_dataset,
    reward_fn=reward_fn
)
grpo_trainer.train()
grpo_trainer.save_model()
```

### 自定义奖励函数

```python
from hello_agents.rl import MathRewardFunction

# 创建自定义奖励函数
class CustomReward(MathRewardFunction):
    def __call__(self, completions: List[str], **kwargs) -> List[float]:
        ground_truths = kwargs.get("ground_truth", [])
        rewards = []
        for completion, truth in zip(completions, ground_truths):
            # 自定义奖励逻辑
            pred = self.extract_answer(completion)
            if pred and self.compare_answers(pred, truth):
                reward = 1.0
            else:
                reward = 0.0
            rewards.append(reward)
        return rewards

# 使用自定义奖励函数
reward_fn = CustomReward()
```

## 常见问题

### Q1: 训练需要多少显存?

A: 取决于模型大小和配置:

- Qwen3-0.6B + LoRA: 约 4-6GB(单 GPU 可训练)
- Qwen3-0.6B 全参数: 约 8-12GB
- Qwen2-1.5B + LoRA: 约 8-12GB
- Qwen2-7B + LoRA: 约 16-24GB

建议:

- 使用 LoRA 减少显存占用
- 减小 batch_size
- 启用 gradient_checkpointing

### Q2: 训练需要多长时间?

A: 取决于数据量和硬件:

- 100 样本, 1 轮, 单 GPU: 约 5-10 分钟
- 1000 样本, 3 轮, 单 GPU: 约 30-60 分钟
- 全量 GSM8K(7.5K), 3 轮, 单 GPU: 约 3-6 小时

### Q3: SFT 和 GRPO 有什么区别?

A:

- SFT: 监督学习, 直接学习正确答案的格式
- GRPO: 强化学习, 通过奖励信号优化推理过程

推荐流程: 先 SFT 学习格式, 再 GRPO 优化能力

### Q4: 为什么推荐 GRPO 而不是 PPO?

A: GRPO 的优势:

- 不需要 Value Model, 实现更简单
- 内存占用更少
- 训练速度更快
- 性能接近 PPO(90%+)

### Q5: 如何评估训练效果?

A: 可以使用评估工具:

```python
from hello_agents.rl import evaluate_rewards, create_accuracy_reward

# 评估模型在测试集上的表现
test_dataset = create_rl_dataset(split="test", max_samples=100)
reward_fn = create_accuracy_reward()

# 生成预测并评估
# ... (需要加载训练后的模型并生成预测)
```

### Q6: 训练失败怎么办?

A: 常见问题和解决方案:

1. 显存不足:
   - 启用 LoRA: `use_lora=True`
   - 减小 batch_size
   - 使用 gradient_checkpointing

2. TRL未安装:
   ```bash
   pip install hello-agents[rl]
   ```

3. 数据集下载失败:
   - 检查网络连接
   - 使用镜像源
   - 手动下载数据集

## 参考资源

- [TRL 官方文档](https://huggingface.co/docs/trl)
- [GRPO 论文](https://arxiv.org/abs/2402.03300)
- [GSM8K 数据集](https://huggingface.co/datasets/openai/gsm8k)
- [Qwen 模型](https://huggingface.co/Qwen)

## 下一步

- 查看完整示例: `examples/rl_training_example.py`
- 了解 Agentic RL 理论: `docs/chapter11/`
- 探索更多训练算法: DPO, KTO, ORPO 等
