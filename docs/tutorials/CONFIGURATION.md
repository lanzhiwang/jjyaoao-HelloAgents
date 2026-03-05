# HelloAgents 配置指南

> 🔧 详细的环境配置和LLM提供商设置指南

## 📋 目录

- [快速配置](#快速配置)
- [LLM提供商配置](#llm提供商配置)
- [工具配置](#工具配置)
- [高级配置](#高级配置)
- [故障排除](#故障排除)

## 🚀 快速配置

### 1. 创建环境配置文件

```bash
# 复制示例配置文件
cp .env.example .env
```

### 2. 配置LLM服务

编辑 `.env` 文件, 配置以下4个核心变量: 

```bash
# 模型名称
LLM_MODEL_ID=your-model-name

# API密钥
LLM_API_KEY=your-api-key-here

# 服务地址
LLM_BASE_URL=your-api-base-url

# 超时时间（可选, 默认60秒）
LLM_TIMEOUT=60
```

### 3. 验证配置

```bash
# 检查环境变量是否正确加载
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('🔧 环境变量检查:')
print(f'LLM_MODEL_ID: {os.getenv(\"LLM_MODEL_ID\", \"未设置\")}')
print(f'LLM_API_KEY: {\"已设置\" if os.getenv(\"LLM_API_KEY\") else \"未设置\"}')
print(f'LLM_BASE_URL: {os.getenv(\"LLM_BASE_URL\", \"未设置\")}')
"

# 测试LLM连接（需要先配置好.env文件）
python -c "
from hello_agents import HelloAgentsLLM
try:
    llm = HelloAgentsLLM()
    print(f'✅ 检测到provider: {llm.provider}')
    print(f'✅ 模型: {llm.model}')
    print('✅ 配置验证成功')
except Exception as e:
    print(f'❌ 配置验证失败: {e}')
    print('💡 请检查.env文件是否正确配置')
"
```

## 🤖 LLM提供商配置

### OpenAI官方

```bash
LLM_MODEL_ID=gpt-3.5-turbo
LLM_API_KEY=sk-your_openai_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
```

**获取API密钥**: [OpenAI Platform](https://platform.openai.com/api-keys)

### DeepSeek

```bash
LLM_MODEL_ID=deepseek-chat
LLM_API_KEY=sk-your_deepseek_api_key_here
LLM_BASE_URL=https://api.deepseek.com
```

**获取API密钥**: [DeepSeek Platform](https://platform.deepseek.com/)

### 通义千问（阿里云）

```bash
LLM_MODEL_ID=qwen-plus
LLM_API_KEY=sk-your_dashscope_api_key_here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

**获取API密钥**: [阿里云DashScope](https://dashscope.console.aliyun.com/)

### 月之暗面 Kimi

```bash
LLM_MODEL_ID=moonshot-v1-8k
LLM_API_KEY=sk-your_kimi_api_key_here
LLM_BASE_URL=https://api.moonshot.cn/v1
```

**获取API密钥**: [Kimi开放平台](https://platform.moonshot.cn/)

### 智谱AI GLM

```bash
LLM_MODEL_ID=glm-4
LLM_API_KEY=your_api_key.your_secret
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

**获取API密钥**: [智谱AI开放平台](https://open.bigmodel.cn/)

### ModelScope 魔搭社区

```bash
LLM_MODEL_ID=Qwen/Qwen2.5-72B-Instruct
LLM_API_KEY=ms-your_modelscope_api_key_here
LLM_BASE_URL=https://api-inference.modelscope.cn/v1/
```

**获取API密钥**: [ModelScope](https://modelscope.cn/my/myaccesstoken)

## 🏠 本地部署配置

### Ollama

```bash
LLM_MODEL_ID=llama3.2
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434/v1
```

**安装指南**: 参考 [本地部署指南](./LOCAL_DEPLOYMENT_GUIDE.md)

### vLLM

```bash
LLM_MODEL_ID=meta-llama/Llama-2-7b-chat-hf
LLM_API_KEY=vllm
LLM_BASE_URL=http://localhost:8000/v1
```

### 其他本地服务

```bash
LLM_MODEL_ID=your-local-model
LLM_API_KEY=local
LLM_BASE_URL=http://localhost:8080/v1
```

## 🛠️ 工具配置

### 搜索工具

#### Tavily搜索（推荐）

```bash
TAVILY_API_KEY=tvly-your_tavily_key_here
```

**获取API密钥**: [Tavily](https://tavily.com/)

#### SerpApi搜索（备选）

```bash
SERPAPI_API_KEY=your_serpapi_key_here
```

**获取API密钥**: [SerpApi](https://serpapi.com/)

## 🔄 兼容性配置

框架支持多种环境变量格式, 会自动检测: 

### OpenAI格式
```bash
OPENAI_API_KEY=sk-your_openai_api_key_here
```

### 提供商专用格式
```bash
DEEPSEEK_API_KEY=sk-your_deepseek_api_key_here
DASHSCOPE_API_KEY=sk-your_dashscope_api_key_here
MODELSCOPE_API_KEY=ms-your_modelscope_api_key_here
KIMI_API_KEY=sk-your_kimi_api_key_here
ZHIPU_API_KEY=your_zhipu_api_key.your_secret
```

## 🔍 自动检测逻辑

框架会按以下优先级自动检测LLM提供商: 

1. **API密钥格式判断**
   - `ms-` 开头 → ModelScope
   - `sk-` 开头 → OpenAI系列
   - 包含`.` → 智谱AI

2. **Base URL域名判断**
   - `api.openai.com` → OpenAI
   - `api.deepseek.com` → DeepSeek
   - `dashscope.aliyuncs.com` → 通义千问
   - `api.moonshot.cn` → Kimi
   - `localhost` → 本地部署

3. **特定环境变量检查**
   - `OPENAI_API_KEY` → OpenAI
   - `DEEPSEEK_API_KEY` → DeepSeek
   - 等等...

## 💡 使用示例

### 基础使用

```python
from hello_agents import HelloAgentsLLM, SimpleAgent

# 自动检测provider（推荐）
llm = HelloAgentsLLM()

# 创建Agent
agent = SimpleAgent("AI助手", llm)
response = agent.run("你好! ")
print(response)
```

### 手动指定Provider

```python
# 手动指定provider
llm = HelloAgentsLLM(provider="modelscope")

# 或者传入完整配置
llm = HelloAgentsLLM(
    model="gpt-3.5-turbo",
    api_key="sk-your-key",
    base_url="https://api.openai.com/v1",
    provider="openai"
)
```

## 🔧 故障排除

### 常见问题

#### 1. API密钥无效
```bash
❌ 错误: Invalid API key
```
**解决方案**: 检查API密钥是否正确, 是否有足够的配额

#### 2. 网络连接问题
```bash
❌ 错误: Connection timeout
```
**解决方案**: 检查网络连接, 或增加超时时间: 
```bash
LLM_TIMEOUT=120
```

#### 3. Provider检测错误
```bash
❌ 错误: Unknown provider
```
**解决方案**: 手动指定provider: 
```python
llm = HelloAgentsLLM(provider="your_provider")
```

#### 4. 环境变量未加载
```bash
❌ 错误: API密钥和服务地址必须被提供或在.env文件中定义
```
**解决方案**: 
1. 确保.env文件存在且配置正确
2. 检查.env文件是否在正确的目录下
3. 使用环境变量检查命令验证配置

### 调试命令

```bash
# 检查环境变量加载
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('🔧 环境变量检查:')
print(f'LLM_MODEL_ID: {os.getenv(\"LLM_MODEL_ID\", \"未设置\")}')
print(f'LLM_API_KEY: {\"已设置\" if os.getenv(\"LLM_API_KEY\") else \"未设置\"}')
print(f'LLM_BASE_URL: {os.getenv(\"LLM_BASE_URL\", \"未设置\")}')
"

# 测试连接（仅在配置正确时运行）
python -c "
from hello_agents import HelloAgentsLLM
try:
    llm = HelloAgentsLLM()
    print(f'✅ Provider: {llm.provider}')
    print(f'✅ Model: {llm.model}')
    print('✅ 连接测试成功')
except Exception as e:
    print(f'❌ 连接测试失败: {e}')
"
```

## 📚 相关文档

- [本地部署指南](./LOCAL_DEPLOYMENT_GUIDE.md) - Ollama、vLLM部署
- [API文档](../api/) - 详细的API参考
- [示例代码](../../examples/) - 完整的使用示例

## 💬 获取帮助

如果遇到配置问题, 可以: 

1. 查看 [故障排除](#故障排除) 部分
2. 运行调试命令检查配置
3. 查看项目的 Issues 页面
4. 参考示例代码中的配置
