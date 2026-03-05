"""多模态配置文件 - 支持真实的视觉和视频理解API"""

import os
from typing import Dict, Any, Optional


class MultimodalConfig:
    """多模态配置类"""

    def __init__(self):
        # 视觉理解API配置
        self.vision_config = {
            # OpenAI GPT-4V
            "openai_gpt4v": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": "gpt-4-vision-preview",
                "max_tokens": 1000,
                "enabled": bool(os.getenv("OPENAI_API_KEY")),
            },
            # Google Gemini Vision
            "google_gemini": {
                "api_key": os.getenv("GOOGLE_API_KEY"),
                "model": "gemini-pro-vision",
                "enabled": bool(os.getenv("GOOGLE_API_KEY")),
            },
            # Claude 3 Vision
            "claude_vision": {
                "api_key": os.getenv("ANTHROPIC_API_KEY"),
                "model": "claude-3-opus-20240229",
                "enabled": bool(os.getenv("ANTHROPIC_API_KEY")),
            },
            # 本地模型（如果有GPU）
            "local_vision": {
                "model_path": "./models/blip2",
                "device": "cuda" if os.getenv("CUDA_AVAILABLE") else "cpu",
                "enabled": False,  # 需要手动启用
            },
        }

        # 视频理解API配置
        self.video_config = {
            # OpenAI GPT-4V (通过关键帧)
            "openai_keyframes": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": "gpt-4-vision-preview",
                "frame_interval": 30,  # 每30秒提取一帧
                "enabled": bool(os.getenv("OPENAI_API_KEY")),
            },
            # Google Video Intelligence API
            "google_video_ai": {
                "api_key": os.getenv("GOOGLE_API_KEY"),
                "enabled": bool(os.getenv("GOOGLE_API_KEY")),
            },
            # 本地视频分析
            "local_video": {"model_path": "./models/video_analysis", "enabled": False},
        }

        # 语音识别配置
        self.speech_config = {
            "openai_whisper": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": "whisper-1",
                "enabled": bool(os.getenv("OPENAI_API_KEY")),
            },
            "local_whisper": {
                "model_size": "base",
                "enabled": True,  # Whisper可以本地运行
            },
        }

    def get_available_vision_provider(self) -> Optional[str]:
        """获取可用的视觉理解提供商"""
        for provider, config in self.vision_config.items():
            if config.get("enabled", False):
                return provider
        return None

    def get_available_video_provider(self) -> Optional[str]:
        """获取可用的视频理解提供商"""
        for provider, config in self.video_config.items():
            if config.get("enabled", False):
                return provider
        return None

    def get_available_speech_provider(self) -> Optional[str]:
        """获取可用的语音识别提供商"""
        for provider, config in self.speech_config.items():
            if config.get("enabled", False):
                return provider
        return None


# 环境变量设置指南
ENV_SETUP_GUIDE = """
🔧 环境变量设置指南

为了使用真实的多模态API, 请设置以下环境变量: 

1. OpenAI API (推荐): 
   export OPENAI_API_KEY="your-openai-api-key"

2. Google API: 
   export GOOGLE_API_KEY="your-google-api-key"

3. Anthropic API: 
   export ANTHROPIC_API_KEY="your-anthropic-api-key"

4. 如果有CUDA GPU: 
   export CUDA_AVAILABLE="true"

Windows用户请使用: 
set OPENAI_API_KEY=your-openai-api-key

或者在Python中设置: 
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"
"""


def print_setup_guide():
    """打印设置指南"""
    print(ENV_SETUP_GUIDE)


def check_multimodal_capabilities():
    """检查多模态能力"""
    config = MultimodalConfig()

    print("🔍 检查多模态能力...")
    print("=" * 50)

    # 检查视觉理解
    vision_provider = config.get_available_vision_provider()
    if vision_provider:
        print(f"✅ 视觉理解: {vision_provider}")
    else:
        print("❌ 视觉理解: 未配置")

    # 检查视频理解
    video_provider = config.get_available_video_provider()
    if video_provider:
        print(f"✅ 视频理解: {video_provider}")
    else:
        print("❌ 视频理解: 未配置")

    # 检查语音识别
    speech_provider = config.get_available_speech_provider()
    if speech_provider:
        print(f"✅ 语音识别: {speech_provider}")
    else:
        print("❌ 语音识别: 未配置")

    if not any([vision_provider, video_provider, speech_provider]):
        print("\n⚠️ 未检测到多模态API配置")
        print("将使用模拟模式进行演示")
        print_setup_guide()

    return {
        "vision": vision_provider,
        "video": video_provider,
        "speech": speech_provider,
    }


# 真实API调用示例（需要API密钥）
def call_real_vision_api(image_path: str, prompt: str = "描述这张图片") -> str:
    """调用真实的视觉API"""
    config = MultimodalConfig()
    provider = config.get_available_vision_provider()

    if not provider:
        return "未配置视觉API, 使用模拟结果"

    try:
        if provider == "openai_gpt4v":
            return _call_openai_vision(
                image_path, prompt, config.vision_config[provider]
            )
        elif provider == "google_gemini":
            return _call_google_vision(
                image_path, prompt, config.vision_config[provider]
            )
        elif provider == "claude_vision":
            return _call_claude_vision(
                image_path, prompt, config.vision_config[provider]
            )
        else:
            return "不支持的视觉API提供商"
    except Exception as e:
        return f"API调用失败: {str(e)}"


def _call_openai_vision(image_path: str, prompt: str, config: Dict[str, Any]) -> str:
    """调用OpenAI GPT-4V API"""
    try:
        import openai
        import base64

        # 读取并编码图片
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        client = openai.OpenAI(api_key=config["api_key"])

        response = client.chat.completions.create(
            model=config["model"],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=config["max_tokens"],
        )

        return response.choices[0].message.content

    except ImportError:
        return "请安装openai库: pip install openai"
    except Exception as e:
        return f"OpenAI API调用失败: {str(e)}"


def _call_google_vision(image_path: str, prompt: str, config: Dict[str, Any]) -> str:
    """调用Google Gemini Vision API"""
    try:
        import google.generativeai as genai
        from PIL import Image

        genai.configure(api_key=config["api_key"])
        model = genai.GenerativeModel(config["model"])

        image = Image.open(image_path)
        response = model.generate_content([prompt, image])

        return response.text

    except ImportError:
        return "请安装google-generativeai库: pip install google-generativeai"
    except Exception as e:
        return f"Google API调用失败: {str(e)}"


def _call_claude_vision(image_path: str, prompt: str, config: Dict[str, Any]) -> str:
    """调用Claude Vision API"""
    try:
        import anthropic
        import base64

        # 读取并编码图片
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        client = anthropic.Anthropic(api_key=config["api_key"])

        response = client.messages.create(
            model=config["model"],
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )

        return response.content[0].text

    except ImportError:
        return "请安装anthropic库: pip install anthropic"
    except Exception as e:
        return f"Claude API调用失败: {str(e)}"


if __name__ == "__main__":
    check_multimodal_capabilities()
