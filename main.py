"""主程序入口 - 智能旅行助手"""
import os
from dotenv import load_dotenv
from llm_client import OpenAICompatibleClient
from agent import TravelAgent

def load_config():
    """从环境变量或 .env 文件加载配置"""
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL", "YOUR_BASE_URL")
    model_id = os.environ.get("OPENAI_MODEL", "YOUR_MODEL_ID")
    tavily_api_key = os.environ.get("TAVILY_API_KEY", "YOUR_TAVILY_API_KEY")
    os.environ['TAVILY_API_KEY'] = tavily_api_key
    return api_key, base_url, model_id, tavily_api_key

def validate_config(api_key: str, base_url: str, model_id: str):
    """验证配置是否有效"""
    if api_key == "YOUR_API_KEY" or base_url == "YOUR_BASE_URL" or model_id == "YOUR_MODEL_ID":
        print("警告: 请先配置环境变量或创建 .env 文件")
        print("方式1: 创建 .env 文件（推荐）")
        print("方式2: 设置环境变量:")
        print("  export OPENAI_API_KEY='your_key'")
        print("  export OPENAI_BASE_URL='your_url'")
        print("  export OPENAI_MODEL='your_model'")
        print("  export TAVILY_API_KEY='your_tavily_key'")
        return False
    return True

def main():
    """主执行函数"""
    api_key, base_url, model_id, tavily_api_key = load_config()
    if not validate_config(api_key, base_url, model_id):
        return
    llm_client = OpenAICompatibleClient(model=model_id, api_key=api_key, base_url=base_url)
    agent = TravelAgent(llm_client)
    user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
    agent.run(user_prompt)

if __name__ == "__main__":
    main()
