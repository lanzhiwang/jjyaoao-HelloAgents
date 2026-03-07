# MCP (Model Context Protocol) API 详解

MCP 是一个开放标准, 用于在 AI 应用程序和外部数据源之间建立安全、可控的连接. HelloAgents 基于 FastMCP 库提供了完整的 MCP 协议支持. 

## 📋 核心概念

### 1. 工具 (Tools)
工具是 MCP 服务器可以执行的函数, 类似于 API 端点. 每个工具都有明确的输入参数和输出格式. 

### 2. 资源 (Resources)
资源是服务器可以提供的数据, 如文件、数据库记录、API 响应等. 资源通过 URI 进行标识. 

### 3. 提示词 (Prompts)
预定义的提示词模板, 可以被客户端使用来生成特定格式的请求. 

### 4. 传输层 (Transport)
MCP 支持多种传输方式: Stdio、HTTP、WebSocket、SSE 等. 

## 🚀 HelloAgents MCP 实现

### FastMCP 服务器

HelloAgents 使用 FastMCP 库来实现 MCP 服务器: 

```python
from fastmcp import FastMCP
from typing import Dict, Any

# 创建服务器实例
server = FastMCP("my-server")

@server.tool()
def calculate(expression: str) -> Dict[str, Any]:
    """
    计算数学表达式
    
    Args:
        expression: 数学表达式字符串
    
    Returns:
        包含计算结果的字典
    """
    try:
        result = eval(expression)  # 注意: 生产环境需要安全处理
        return {
            "expression": expression,
            "result": result,
            "success": True
        }
    except Exception as e:
        return {
            "expression": expression,
            "error": str(e),
            "success": False
        }

@server.tool()
def get_server_info() -> Dict[str, Any]:
    """获取服务器信息"""
    return {
        "name": "Calculator Server",
        "version": "1.0.0",
        "tools": ["calculate", "get_server_info"],
        "description": "简单的计算器 MCP 服务器"
    }

if __name__ == "__main__":
    server.run()
```

### 增强的 MCP 客户端

HelloAgents 提供了增强的 MCP 客户端, 支持多种传输方式: 

```python
from hello_agents.protocols.mcp.client import MCPClient
import asyncio

async def use_mcp_client():
    # 方式1: 连接到 Python 脚本（Stdio 传输）
    async with MCPClient("calculator_server.py") as client:
        tools = await client.list_tools()
        result = await client.call_tool("calculate", {"expression": "10 + 5"})
        print(f"计算结果: {result}")

    # 方式2: 连接到 HTTP 服务器
    async with MCPClient("http://localhost:8000") as client:
        info = await client.call_tool("get_server_info", {})
        print(f"服务器信息: {info}")

    # 方式3: 连接到 FastMCP 实例（内存传输）
    from fastmcp import FastMCP
    memory_server = FastMCP("memory-server")

    @memory_server.tool()
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    async with MCPClient(memory_server) as client:
        greeting = await client.call_tool("greet", {"name": "World"})
        print(f"问候: {greeting}")

# 运行示例
asyncio.run(use_mcp_client())
```

## 🔧 传输方式详解

### 1. Stdio 传输（默认）
通过标准输入输出进行通信, 适用于本地进程. 

```python
# 服务器端
server = FastMCP("stdio-server")
server.run()  # 默认使用 stdio

# 客户端
client = MCPClient("server_script.py")
```

### 2. HTTP 传输
通过 HTTP 协议进行通信, 适用于远程服务. 

```python
# 服务器端
server = FastMCP("http-server")
server.run(transport="http", host="0.0.0.0", port=8000)

# 客户端
client = MCPClient("http://localhost:8000")
```

### 3. SSE 传输
通过 Server-Sent Events 进行实时通信. 

```python
# 客户端
client = MCPClient(
    "http://localhost:8000",
    transport_type="sse"
)
```

### 4. 内存传输
直接在内存中通信, 适用于测试和开发. 

```python
# 直接传递 FastMCP 实例
server_instance = FastMCP("memory-server")
client = MCPClient(server_instance)
```

## 📚 实际应用案例

### 案例1: 文件系统服务器

```python
from fastmcp import FastMCP
import os
import json
from typing import List, Dict, Any

file_server = FastMCP("filesystem-server")

@file_server.tool()
def list_files(directory: str = ".") -> List[str]:
    """列出目录中的文件"""
    try:
        files = os.listdir(directory)
        return [f for f in files if os.path.isfile(os.path.join(directory, f))]
    except Exception as e:
        return [f"错误: {str(e)}"]

@file_server.tool()
def read_file(file_path: str) -> Dict[str, Any]:
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {
            "file_path": file_path,
            "content": content,
            "size": len(content),
            "success": True
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "error": str(e),
            "success": False
        }

@file_server.tool()
def write_file(file_path: str, content: str) -> Dict[str, Any]:
    """写入文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {
            "file_path": file_path,
            "bytes_written": len(content.encode('utf-8')),
            "success": True
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "error": str(e),
            "success": False
        }

if __name__ == "__main__":
    print("🗂️ 启动文件系统 MCP 服务器...")
    file_server.run()
```

### 案例2: 数据库查询服务器

```python
from fastmcp import FastMCP
import sqlite3
import json
from typing import List, Dict, Any

db_server = FastMCP("database-server")

# 初始化数据库
def init_database():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # 创建示例表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER
        )
    ''')
    
    # 插入示例数据
    cursor.execute("INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("张三", "zhangsan@example.com", 25))
    cursor.execute("INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("李四", "lisi@example.com", 30))
    
    conn.commit()
    conn.close()

@db_server.tool()
def query_users(limit: int = 10) -> Dict[str, Any]:
    """查询用户列表"""
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email, age FROM users LIMIT ?", (limit,))
        rows = cursor.fetchall()
        
        users = []
        for row in rows:
            users.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "age": row[3]
            })
        
        conn.close()
        
        return {
            "users": users,
            "count": len(users),
            "success": True
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

@db_server.tool()
def add_user(name: str, email: str, age: int) -> Dict[str, Any]:
    """添加新用户"""
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                       (name, email, age))
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return {
            "user_id": user_id,
            "name": name,
            "email": email,
            "age": age,
            "success": True
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

if __name__ == "__main__":
    print("🗄️ 初始化数据库...")
    init_database()
    print("🚀 启动数据库 MCP 服务器...")
    db_server.run()
```

## 🛠️ 在 HelloAgents 中使用 MCP

### 使用 MCPTool

```python
from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools.builtin.protocol_tools import MCPTool
from dotenv import load_dotenv

def create_mcp_agent():
    """创建使用 MCP 工具的智能体"""
    load_dotenv()
    llm = HelloAgentsLLM()
    
    # 创建智能体
    agent = SimpleAgent(name="MCP助手", llm=llm)
    
    # 添加文件系统 MCP 工具
    fs_tool = MCPTool(
        server_command=["python", "filesystem_server.py"],
        name="文件系统工具"
    )
    agent.add_tool(fs_tool)
    
    # 添加数据库 MCP 工具
    db_tool = MCPTool(
        server_command=["python", "database_server.py"],
        name="数据库工具"
    )
    agent.add_tool(db_tool)
    
    return agent

# 使用示例
agent = create_mcp_agent()

# 智能体可以自动选择合适的工具
response = agent.run("列出当前目录的所有 Python 文件")
print(response)

response = agent.run("查询数据库中的所有用户")
print(response)
```

---

*更多详细信息请参考 [MCP 实战案例](mcp_examples.md) 和 [FastMCP 官方文档](https://fastmcp.wiki/)*
