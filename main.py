"""主程序入口 - 智能旅行助手"""
from config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
from llm_client import OpenAICompatibleClient
from agent import TravelAgent

def validate_config() -> None:
    """验证配置是否有效"""
    missing = []
    if OPENAI_API_KEY == "YOUR_API_KEY":
        missing.append("OPENAI_API_KEY")
    if OPENAI_BASE_URL == "YOUR_BASE_URL":
        missing.append("OPENAI_BASE_URL")
    if OPENAI_MODEL == "YOUR_MODEL_ID":
        missing.append("OPENAI_MODEL")
    
    if missing:
        raise ValueError(f"缺少配置: {', '.join(missing)}，请在 .env 文件中配置")

def main():
    """主执行函数"""
    try:
        validate_config()
        llm_client = OpenAICompatibleClient(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
        agent = TravelAgent(llm_client)
        user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
        agent.run(user_prompt)
    except ValueError as e:
        print(f"配置错误: {e}")
    except Exception as e:
        print(f"执行错误: {e}")

if __name__ == "__main__":
    main()
