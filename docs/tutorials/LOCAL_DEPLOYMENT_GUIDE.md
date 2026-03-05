# HelloAgents 本地部署指南

## 🏠 本地部署概述

HelloAgents现在全面支持本地LLM部署方案, 包括Ollama、vLLM和其他OpenAI兼容的本地服务. 

## 🚀 支持的本地部署方案

### 1. Ollama 部署

#### 安装Ollama
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# 从 https://ollama.ai/download 下载安装包
```

#### 启动模型
```bash
# 下载并运行Llama 3.2
ollama run llama3.2

# 或其他模型
ollama run qwen2.5:7b
ollama run codellama:7b
```

#### HelloAgents配置
```env
# 方式1: 使用专用环境变量
OLLAMA_API_KEY=ollama
OLLAMA_HOST=http://localhost:11434/v1

# 方式2: 使用统一配置
LLM_MODEL_ID=llama3.2
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434/v1
```

```python
from hello_agents import HelloAgentsLLM, SimpleAgent

# 自动检测为ollama
llm = HelloAgentsLLM()
agent = SimpleAgent("Llama助手", llm)
response = agent.run("你好! ")
```

### 2. vLLM 部署

#### 安装vLLM
```bash
pip install vllm
```

#### 启动vLLM服务
```bash
# 启动Llama-2-7B模型
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-7b-chat-hf \
    --port 8000

# 或启动Qwen模型
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --port 8000
```

#### HelloAgents配置
```env
# 方式1: 使用专用环境变量
VLLM_API_KEY=vllm
VLLM_HOST=http://localhost:8000/v1

# 方式2: 使用统一配置
LLM_MODEL_ID=meta-llama/Llama-2-7b-chat-hf
LLM_API_KEY=vllm
LLM_BASE_URL=http://localhost:8000/v1
```

```python
from hello_agents import HelloAgentsLLM, SimpleAgent

# 自动检测为vllm
llm = HelloAgentsLLM()
agent = SimpleAgent("vLLM助手", llm)
response = agent.run("你好! ")
```

### 3. FastChat 部署

#### 安装FastChat
```bash
pip install fschat
```

#### 启动FastChat服务
```bash
# 启动控制器
python -m fastchat.serve.controller

# 启动模型worker
python -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.5

# 启动OpenAI兼容API服务器
python -m fastchat.serve.openai_api_server --host localhost --port 8000
```

#### HelloAgents配置
```env
LLM_MODEL_ID=vicuna-7b-v1.5
LLM_API_KEY=local
LLM_BASE_URL=http://localhost:8000/v1
```

### 4. Text Generation WebUI

#### 安装Text Generation WebUI
```bash
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui
pip install -r requirements.txt
```

#### 启动服务
```bash
python server.py --api --listen --port 7860
```

#### HelloAgents配置
```env
LLM_MODEL_ID=your-model-name
LLM_API_KEY=local
LLM_BASE_URL=http://localhost:7860/v1
```

### 5. 其他本地部署

对于任何提供OpenAI兼容API的本地服务: 

```env
LLM_MODEL_ID=your-custom-model
LLM_API_KEY=local
LLM_BASE_URL=http://localhost:PORT/v1
```

## 🔍 自动检测逻辑

HelloAgents会根据以下规则自动检测本地部署: 

### 1. 特定服务检测
- `OLLAMA_API_KEY` 或 `OLLAMA_HOST` → ollama
- `VLLM_API_KEY` 或 `VLLM_HOST` → vllm

### 2. URL模式检测
- `localhost:11434` 或包含 `ollama` → ollama
- `localhost:8000` 且包含 `vllm` → vllm
- `localhost:8080`、`localhost:7860` → local
- 其他localhost端口 → local

### 3. API密钥检测
- `LLM_API_KEY=ollama` → ollama
- `LLM_API_KEY=vllm` → vllm
- `LLM_API_KEY=local` → local

## 📋 配置示例

### 完整的本地部署配置文件
```env
# ============================================================================
# HelloAgents 本地部署配置
# ============================================================================

# Ollama配置
# LLM_MODEL_ID=llama3.2
# LLM_API_KEY=ollama
# LLM_BASE_URL=http://localhost:11434/v1

# vLLM配置
# LLM_MODEL_ID=meta-llama/Llama-2-7b-chat-hf
# LLM_API_KEY=vllm
# LLM_BASE_URL=http://localhost:8000/v1

# FastChat配置
# LLM_MODEL_ID=vicuna-7b-v1.5
# LLM_API_KEY=local
# LLM_BASE_URL=http://localhost:8000/v1

# Text Generation WebUI配置
# LLM_MODEL_ID=your-model
# LLM_API_KEY=local
# LLM_BASE_URL=http://localhost:7860/v1

# 通用本地部署配置
LLM_MODEL_ID=your-local-model
LLM_API_KEY=local
LLM_BASE_URL=http://localhost:8080/v1
LLM_TIMEOUT=120  # 本地部署可能需要更长超时时间
```

### Python使用示例
```python
from hello_agents import HelloAgentsLLM, SimpleAgent, ReActAgent, ToolRegistry

# 1. 基础对话
llm = HelloAgentsLLM()  # 自动检测本地部署
agent = SimpleAgent("本地助手", llm)
response = agent.run("介绍一下你自己")

# 2. 工具调用(本地模型也支持)
from hello_agents.tools.builtin import calculate

tool_registry = ToolRegistry()
tool_registry.register_function("calculate", "数学计算", calculate)

react_agent = ReActAgent("本地工具助手", llm, tool_registry)
result = react_agent.run("计算 123 * 456 的结果")

# 3. 检查配置
print(f"Provider: {llm.provider}")
print(f"Model: {llm.model}")
print(f"Base URL: {llm.base_url}")
```

## 🔧 故障排除

### 常见问题

1. **连接失败**
   ```python
   # 检查服务是否启动
   import requests
   response = requests.get("http://localhost:11434/v1/models")
   print(response.status_code)
   ```

2. **模型未找到**
   ```bash
   # Ollama: 检查可用模型
   ollama list
   
   # vLLM: 确保模型路径正确
   ls ~/.cache/huggingface/transformers/
   ```

3. **超时问题**
   ```env
   # 增加超时时间
   LLM_TIMEOUT=300
   ```

### 性能优化

1. **GPU加速**
   ```bash
   # Ollama GPU支持
   ollama run llama3.2  # 自动使用GPU
   
   # vLLM GPU支持
   python -m vllm.entrypoints.openai.api_server \
       --model meta-llama/Llama-2-7b-chat-hf \
       --tensor-parallel-size 2
   ```

2. **内存优化**
   ```bash
   # 使用量化模型
   ollama run llama3.2:7b-instruct-q4_0
   ```

## 🎯 最佳实践

1. **选择合适的部署方案**
   - **Ollama**: 简单易用, 适合快速体验
   - **vLLM**: 高性能, 适合生产环境
   - **FastChat**: 功能丰富, 支持多种模型
   - **Text Generation WebUI**: 图形界面, 适合研究

2. **模型选择建议**
   - **7B模型**: 适合16GB内存
   - **13B模型**: 适合32GB内存
   - **70B模型**: 需要多GPU或量化

3. **配置建议**
   - 本地部署建议增加超时时间
   - 使用合适的模型大小
   - 考虑使用量化模型节省内存

现在HelloAgents完全支持本地LLM部署, 让您可以在本地环境中享受AI助手的强大功能! 🚀
