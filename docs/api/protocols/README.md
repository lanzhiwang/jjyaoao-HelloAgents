# HelloAgents 智能体通信协议 API 文档

本目录包含 HelloAgents 框架支持的三种主要智能体通信协议的完整 API 文档和实用案例.

## 📋 协议概览

HelloAgents 支持三种核心通信协议, 每种协议都有其特定的应用场景:

| 协议    | 全称                    | 主要用途           | 实现状态       | 文档链接                    |
| ------- | ----------------------- | ------------------ | -------------- | --------------------------- |
| **MCP** | Model Context Protocol  | 工具调用、资源访问 | ✅ 生产就绪     | [MCP 详解](mcp.md)          |
| **A2A** | Agent-to-Agent Protocol | 智能体间通信协作   | ✅ 基于官方 SDK | [A2A 案例](a2a_examples.md) |
| **ANP** | Agent Network Protocol  | 网络管理、服务发现 | ✅ 概念实现     | [ANP 演示](anp_examples.md) |

## 🚀 快速开始

### 环境准备

```bash
# 安装核心依赖
pip install fastmcp>=2.0.0

# 安装 A2A SDK(可选)
pip install a2a-sdk

# 验证安装
python -c "from fastmcp import FastMCP; print('FastMCP 安装成功')"
python -c "from a2a.client import A2AClient; print('A2A SDK 安装成功')"
```

### MCP - 创建自定义服务器

```python
from fastmcp import FastMCP

# 创建服务器
server = FastMCP("my-server")

@server.tool()
def greet(name: str) -> str:
    """问候工具"""
    return f"Hello, {name}! 欢迎使用 MCP 协议."

@server.tool()
def calculate(expression: str) -> float:
    """计算工具"""
    try:
        result = eval(expression)  # 注意: 生产环境需要安全处理
        return result
    except Exception as e:
        return f"计算错误: {e}"

if __name__ == "__main__":
    server.run()
```

### A2A - 使用官方 SDK

```python
from hello_agents.protocols.a2a.implementation import A2AServer

# 创建智能体
agent = A2AServer(
    name="my-agent",
    description="我的智能体",
    capabilities={"skills": ["greet", "help"]}
)

@agent.skill("greet")
def greet_user(name: str) -> str:
    """问候技能"""
    return f"你好, {name}! 我是 A2A 智能体."

@agent.skill("help")
def show_help(topic: str = "") -> str:
    """帮助技能"""
    if topic:
        return f"关于 {topic} 的帮助信息..."
    return "可用技能: greet, help"

# 测试技能
print(agent.skills["greet"]("用户"))
print(agent.skills["help"]("A2A协议"))
```

### ANP - 网络管理

```python
from hello_agents.protocols.anp.implementation import ANPNetwork, ANPDiscovery, ServiceInfo

# 创建网络管理器
network = ANPNetwork(network_id="my-network")
discovery = ANPDiscovery()

# 注册服务
service = ServiceInfo(
    service_id="calculator-service",
    service_type="calculator",
    endpoint="http://localhost:8001",
    capabilities=["add", "subtract", "multiply", "divide"],
    metadata={"version": "1.0", "region": "local"}
)

discovery.register_service(service)
network.add_agent(service.service_id, service.endpoint)

# 服务发现
calc_services = discovery.find_services_by_type("calculator")
print(f"找到 {len(calc_services)} 个计算服务")

# 网络状态
status = network.get_network_status()
print(f"网络状态: {status['health_status']}")
```

## 📚 详细文档

### 核心协议文档
- [MCP 协议详解](mcp.md) - 完整的 MCP 协议规范、传输方式和最佳实践
- [MCP 实战案例](mcp_examples.md) - 官方服务器使用和自定义服务器开发
- [A2A 实战案例](a2a_examples.md) - 基于官方 SDK 的智能体协作案例
- [ANP 概念演示](anp_examples.md) - 网络管理和服务发现的概念性实现

### 实用指南
- 协议选择指南 - 如何根据需求选择合适的协议
- 性能优化建议 - 提升协议通信效率的方法
- 安全最佳实践 - 协议使用中的安全考虑
- 故障排除指南 - 常见问题和解决方案

## 🎯 协议选择指南

### 选择 MCP 当你需要:
- ✅ 集成外部工具和服务(文件系统、数据库、API)
- ✅ 标准化的工具调用接口
- ✅ 访问结构化资源和提示词
- ✅ 与现有 MCP 生态系统兼容

典型场景: 文档处理、数据查询、代码分析、系统集成

### 选择 A2A 当你需要:
- ✅ 多个智能体协作完成复杂任务
- ✅ 实现智能体间的技能共享
- ✅ 构建工作流自动化系统
- ✅ 智能体角色分工和协调

典型场景: 内容创作团队、客服系统、代码审查流程、教学系统

### 选择 ANP 当你需要:
- ✅ 管理大规模智能体网络
- ✅ 实现服务发现和负载均衡
- ✅ 构建分布式智能体系统
- ✅ 网络拓扑管理和监控

典型场景: 企业级智能体平台、云原生智能体服务、IoT 智能体网络

## 📁 示例代码

### 完整示例文件
- `examples/weather_mcp_server.py` - 完整的天气查询 MCP 服务器
- `examples/a2a_content_team.py` - A2A 内容创作团队协作演示
- `examples/comprehensive_protocol_demo.py` - 三种协议的综合演示
- `examples/chapter10_protocols.py` - 教学示例集合

### 测试和验证
- `test_protocols.py` - 协议功能测试脚本
- `test_mcp_client.py` - MCP 客户端测试
- `final_verification_test.py` - 最终验证测试

## 🔧 开发工具

### HelloAgents 协议工具
```python
from hello_agents.tools.builtin.protocol_tools import MCPTool, A2ATool, ANPTool

# 在 Agent 中使用协议工具
from hello_agents import SimpleAgent, HelloAgentsLLM

llm = HelloAgentsLLM()
agent = SimpleAgent(name="协议演示助手", llm=llm)

# 添加 MCP 工具
mcp_tool = MCPTool(server_command=["python", "examples/weather_mcp_server.py"])
agent.add_tool(mcp_tool)

# 添加 A2A 工具
a2a_tool = A2ATool(agent_endpoint="http://localhost:8000")
agent.add_tool(a2a_tool)

# 使用智能体
response = agent.run("查询北京的天气情况")
```

### MCP 客户端
```python
from hello_agents.protocols.mcp.client import MCPClient

# 支持多种传输方式
async with MCPClient("examples/weather_mcp_server.py") as client:
    # Stdio 传输
    weather = await client.call_tool("get_weather", {"city": "北京"})

async with MCPClient("http://localhost:8000") as client:
    # HTTP 传输
    result = await client.call_tool("some_tool", {})
```

## 📦 依赖管理

### 核心依赖
```bash
# MCP 协议(必需)
pip install fastmcp>=2.0.0

# A2A 协议(可选)
pip install a2a-sdk

# 开发和测试工具
pip install pytest asyncio
```

### 官方 MCP 服务器(Node.js)
```bash
# 安装 Node.js 和 npm
# 然后安装官方服务器
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-memory
```

## 🌐 参考资源

### 官方文档
- [MCP 官方规范](https://modelcontextprotocol.io/) - Model Context Protocol 官方文档
- [FastMCP 文档](https://fastmcp.wiki/) - FastMCP 库的详细文档
- [A2A 项目](https://github.com/a2aproject/A2A) - Agent-to-Agent Protocol 官方项目

### 社区资源
- [MCP 服务器集合](https://github.com/modelcontextprotocol) - 官方 MCP 服务器仓库
- [HelloAgents 示例](https://github.com/HelloAgents/examples) - 更多实用示例
- [协议讨论区](https://github.com/HelloAgents/HelloAgents/discussions) - 技术讨论和问答

## 🤝 贡献指南

欢迎为协议文档和示例贡献代码:

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/new-protocol-example`)
3. 添加测试和文档
4. 提交更改 (`git commit -am 'Add new protocol example'`)
5. 推送分支 (`git push origin feature/new-protocol-example`)
6. 创建 Pull Request

### 贡献类型
- 📝 文档改进和翻译
- 🔧 新的协议示例
- 🐛 错误修复和优化
- 🧪 测试用例补充

## 📞 支持与反馈

- 📧 邮箱: support@helloagents.ai
- 💬 讨论: [GitHub Discussions](https://github.com/HelloAgents/HelloAgents/discussions)
- 🐛 问题报告: [GitHub Issues](https://github.com/HelloAgents/HelloAgents/issues)
- 📚 在线文档: https://docs.helloagents.ai

---

*最后更新: 2024年12月 | HelloAgents 团队*
