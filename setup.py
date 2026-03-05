"""
HelloAgents 安装配置

这个文件主要用于向后兼容, 现代 Python 项目推荐使用 pyproject.toml
"""

from setuptools import setup, find_packages

# 从 pyproject.toml 读取配置, 这里提供一个简化版本
setup(
    name="hello-agents",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(include=["hello_agents*"]),
    python_requires=">=3.10",
)
