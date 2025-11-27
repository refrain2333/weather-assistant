"""配置模块 - 集中管理所有配置参数"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "YOUR_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "YOUR_MODEL_ID")

# LLM 客户端参数
LLM_STREAM = os.getenv("LLM_STREAM", "false").lower() == "true"
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))

# SearXNG 配置
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8888/")

# 智能体配置
DEFAULT_MAX_ITERATIONS = 5

# 系统提示词
AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

# 重要规则:
1. 每次回复只能包含一个 Thought 和一个 Action
2. 不要一次性输出多个步骤
3. 等待工具执行结果后再进行下一步

# 回复格式:
Thought: [你的思考过程和当前步骤的计划]
Action: [要调用的工具，格式为 function_name(arg_name="arg_value")]

# 任务完成:
当收集到足够信息时，使用 `finish(answer="完整的回答")` 结束。

# 示例:
Thought: 用户想了解北京天气和景点，我需要先查询天气信息
Action: get_weather(city="北京")

请严格按照格式，每次只输出一个 Thought-Action 对！
"""

