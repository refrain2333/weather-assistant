#!/usr/bin/env python3
"""
简单测试LLM客户端
"""
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from llm_client import OpenAICompatibleClient
from dotenv import load_dotenv
import os

def main():
    # 加载环境变量
    load_dotenv(Path(__file__).parent.parent / '.env')
    
    # 创建客户端
    client = OpenAICompatibleClient(
        model=os.getenv('OPENAI_MODEL'),
        api_key=os.getenv('OPENAI_API_KEY'),
        base_url=os.getenv('OPENAI_BASE_URL')
    )
    
    # 测试对话
    response = client.generate("你好", "你是一个友好的助手")
    print(f"回复: {response}")

if __name__ == "__main__":
    main()
