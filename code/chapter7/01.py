# 配置好同级文件夹下 .env 中的大模型 API, 可参考 code 文件夹配套的 .env.example, 也可以拿前几章的案例的 .env 文件复用.
from hello_agents import SimpleAgent, HelloAgentsLLM
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建 LLM 实例 - 框架自动检测 provider
llm = HelloAgentsLLM()

# 或手动指定 provider(可选)
# llm = HelloAgentsLLM(provider="modelscope")

# 创建 SimpleAgent
agent = SimpleAgent(name="AI 助手", llm=llm, system_prompt="你是一个有用的 AI 助手")

# 基础对话
response = agent.run("你好！请介绍一下自己")
print(response)

# 添加工具功能(可选)
from hello_agents.tools import CalculatorTool

calculator = CalculatorTool()
# 需要实现 7.4.1 的 MySimpleAgent 进行调用, 后续章节会支持此类调用方式
# agent.add_tool(calculator)

# 现在可以使用工具了
response = agent.run("请帮我计算 2 + 3 * 4")
print(response)

# 查看对话历史
print(f"历史消息数: {len(agent.get_history())}")
