"""演示工具模块 - 配置加载和辅助功能

提供配置管理、资源下载、性能监控等辅助功能
"""

import json
import os
import time
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import logging


@dataclass
class DemoConfig:
    """演示配置数据类"""

    name: str
    version: str
    description: str
    llm_config: Dict[str, Any]
    memory_config: Dict[str, Any]
    rag_config: Dict[str, Any]
    vision_config: Dict[str, Any]
    video_config: Dict[str, Any]
    sample_resources: Dict[str, Any]
    demo_scenarios: Dict[str, Any]
    performance_benchmarks: Dict[str, Any]
    ui_settings: Dict[str, Any]
    logging_config: Dict[str, Any]
    experimental_features: Dict[str, Any]


class ConfigLoader:
    """配置加载器"""

    def __init__(self, config_path: str = "demo_config.json"):
        self.config_path = config_path
        self.config = None

    def load_config(self) -> DemoConfig:
        """加载配置文件"""
        try:
            if not os.path.exists(self.config_path):
                print(f"⚠️ 配置文件不存在: {self.config_path}")
                return self._create_default_config()

            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

            self.config = DemoConfig(
                name=config_data["demo_settings"]["name"],
                version=config_data["demo_settings"]["version"],
                description=config_data["demo_settings"]["description"],
                llm_config=config_data["llm_config"],
                memory_config=config_data["memory_config"],
                rag_config=config_data["rag_config"],
                vision_config=config_data["vision_config"],
                video_config=config_data["video_config"],
                sample_resources=config_data["sample_resources"],
                demo_scenarios=config_data["demo_scenarios"],
                performance_benchmarks=config_data["performance_benchmarks"],
                ui_settings=config_data["ui_settings"],
                logging_config=config_data["logging"],
                experimental_features=config_data["experimental_features"],
            )

            print(f"✅ 配置加载成功: {self.config.name} v{self.config.version}")
            return self.config

        except Exception as e:
            print(f"❌ 配置加载失败: {str(e)}")
            return self._create_default_config()

    def _create_default_config(self) -> DemoConfig:
        """创建默认配置"""
        return DemoConfig(
            name="统一多模态智能体演示",
            version="1.0.0",
            description="默认配置",
            llm_config={"provider": "openai", "model": "gpt-3.5-turbo"},
            memory_config={
                "user_id": "demo_user",
                "memory_types": ["working", "episodic"],
            },
            rag_config={"knowledge_base_path": "./knowledge_base"},
            vision_config={"api_provider": "mock"},
            video_config={"supported_formats": ["mp4"]},
            sample_resources={"images": {}, "videos": {}},
            demo_scenarios={},
            performance_benchmarks={},
            ui_settings={"console_colors": {}},
            logging_config={"level": "INFO"},
            experimental_features={},
        )


class ResourceManager:
    """资源管理器"""

    def __init__(self, config: DemoConfig):
        self.config = config
        self.download_dir = Path("./downloaded_resources")
        self.download_dir.mkdir(exist_ok=True)

    def download_sample_image(self, image_type: str) -> Optional[str]:
        """下载样本图片"""
        if image_type not in self.config.sample_resources["images"]:
            print(f"❌ 未知的图片类型: {image_type}")
            return None

        image_info = self.config.sample_resources["images"][image_type]
        url = image_info["url"]
        filename = f"{image_type}.jpg"
        filepath = self.download_dir / filename

        try:
            print(f"📥 正在下载图片: {image_info['description']}")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✅ 图片下载成功: {filepath}")
            return str(filepath)

        except Exception as e:
            print(f"❌ 图片下载失败: {str(e)}")
            return None

    def get_sample_video_info(self, video_type: str) -> Optional[Dict[str, Any]]:
        """获取样本视频信息"""
        if video_type not in self.config.sample_resources["videos"]:
            print(f"❌ 未知的视频类型: {video_type}")
            return None

        return self.config.sample_resources["videos"][video_type]

    def list_available_resources(self):
        """列出可用资源"""
        print("📁 可用资源:")

        print("\n📸 图片资源:")
        for img_type, img_info in self.config.sample_resources["images"].items():
            print(f"  • {img_type}: {img_info['description']}")
            print(f"    标签: {', '.join(img_info['tags'])}")

        print("\n🎬 视频资源:")
        for vid_type, vid_info in self.config.sample_resources["videos"].items():
            print(f"  • {vid_type}: {vid_info['title']}")
            print(f"    时长: {vid_info['duration']}, 难度: {vid_info['difficulty']}")


class PerformanceMonitor:
    """性能监控器"""

    def __init__(self, config: DemoConfig):
        self.config = config
        self.metrics = {}
        self.start_times = {}

    def start_timer(self, operation: str):
        """开始计时"""
        self.start_times[operation] = time.time()

    def end_timer(self, operation: str) -> float:
        """结束计时并返回耗时"""
        if operation not in self.start_times:
            return 0.0

        duration = time.time() - self.start_times[operation]

        if operation not in self.metrics:
            self.metrics[operation] = []

        self.metrics[operation].append(duration)

        # 检查是否超过目标时间
        targets = self.config.performance_benchmarks.get("response_time_targets", {})
        if operation in targets:
            target_str = targets[operation]
            target_time = float(target_str.replace("< ", "").replace("s", ""))

            if duration > target_time:
                print(
                    f"⚠️ 性能警告: {operation} 耗时 {duration:.2f}s, 超过目标 {target_str}"
                )

        return duration

    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要"""
        summary = {}

        for operation, times in self.metrics.items():
            summary[operation] = {
                "count": len(times),
                "total_time": sum(times),
                "avg_time": sum(times) / len(times),
                "min_time": min(times),
                "max_time": max(times),
            }

        return summary

    def print_performance_report(self):
        """打印性能报告"""
        print("\n📊 性能报告:")
        print("-" * 50)

        summary = self.get_performance_summary()

        for operation, stats in summary.items():
            print(f"🔧 {operation}:")
            print(f"   调用次数: {stats['count']}")
            print(f"   平均耗时: {stats['avg_time']:.2f}s")
            print(f"   最短耗时: {stats['min_time']:.2f}s")
            print(f"   最长耗时: {stats['max_time']:.2f}s")
            print(f"   总耗时: {stats['total_time']:.2f}s")


class UIHelper:
    """UI辅助工具"""

    def __init__(self, config: DemoConfig):
        self.config = config
        self.colors = config.ui_settings.get("console_colors", {})
        self.display_options = config.ui_settings.get("display_options", {})

    def print_colored(self, text: str, color_type: str = "default"):
        """打印彩色文本（简化版, 实际可以使用colorama等库）"""
        # 这里简化处理, 实际应用中可以集成colorama
        color_prefix = {
            "user_input": "👤 ",
            "agent_response": "🤖 ",
            "system_info": "ℹ️ ",
            "error_message": "❌ ",
            "success_message": "✅ ",
        }.get(color_type, "")

        print(f"{color_prefix}{text}")

    def print_section_header(self, title: str, width: int = 60):
        """打印章节标题"""
        print("\n" + "=" * width)
        print(f"{title:^{width}}")
        print("=" * width)

    def print_progress_bar(self, current: int, total: int, width: int = 40):
        """打印进度条"""
        if total == 0:
            return

        progress = current / total
        filled = int(width * progress)
        bar = "█" * filled + "░" * (width - filled)
        percentage = progress * 100

        print(
            f"\r进度: [{bar}] {percentage:.1f}% ({current}/{total})", end="", flush=True
        )

        if current == total:
            print()  # 完成时换行

    def show_thinking_process(self, step: str, details: str = ""):
        """显示思考过程"""
        if self.display_options.get("show_thinking_process", True):
            print(f"🧠 思考: {step}")
            if details:
                print(f"   详情: {details}")

    def show_tool_call(self, tool_name: str, action: str, result_summary: str = ""):
        """显示工具调用"""
        if self.display_options.get("show_tool_calls", True):
            print(f"🔧 工具调用: {tool_name}.{action}")
            if result_summary:
                print(f"   结果: {result_summary}")


class LoggingSetup:
    """日志设置"""

    @staticmethod
    def setup_logging(config: DemoConfig):
        """设置日志"""
        log_config = config.logging_config

        # 创建日志目录
        log_path = Path(log_config.get("file_path", "./logs/demo.log"))
        log_path.parent.mkdir(exist_ok=True)

        # 配置日志
        logging.basicConfig(
            level=getattr(logging, log_config.get("level", "INFO")),
            format=log_config.get(
                "format", "%(asctime)s - %(levelname)s - %(message)s"
            ),
            handlers=[
                logging.FileHandler(log_path, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

        logger = logging.getLogger(__name__)
        logger.info(f"日志系统初始化完成: {log_path}")

        return logger


def load_demo_config(config_path: str = "demo_config.json") -> DemoConfig:
    """便捷函数: 加载演示配置"""
    loader = ConfigLoader(config_path)
    return loader.load_config()


def create_demo_helpers(config: DemoConfig):
    """便捷函数: 创建演示辅助工具"""
    resource_manager = ResourceManager(config)
    performance_monitor = PerformanceMonitor(config)
    ui_helper = UIHelper(config)
    logger = LoggingSetup.setup_logging(config)

    return resource_manager, performance_monitor, ui_helper, logger


# 示例使用
if __name__ == "__main__":
    # 加载配置
    config = load_demo_config()

    # 创建辅助工具
    resource_mgr, perf_monitor, ui_helper, logger = create_demo_helpers(config)

    # 演示功能
    ui_helper.print_section_header("配置测试")

    print(f"配置名称: {config.name}")
    print(f"版本: {config.version}")

    # 列出资源
    resource_mgr.list_available_resources()

    # 性能测试
    perf_monitor.start_timer("test_operation")
    time.sleep(0.1)  # 模拟操作
    duration = perf_monitor.end_timer("test_operation")

    print(f"\n测试操作耗时: {duration:.3f}s")

    perf_monitor.print_performance_report()
