"""工具模块 - 包含所有可用的工具函数"""
import requests
from config import SEARXNG_URL

def get_weather(city: str) -> str:
    """通过调用 wttr.in API 查询真实的天气信息"""
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']
        return f"{city}当前天气:{weather_desc}，气温{temp_c}摄氏度"
    except requests.exceptions.RequestException as e:
        return f"错误:查询天气时遇到网络问题 - {e}"
    except (KeyError, IndexError) as e:
        return f"错误:解析天气数据失败，可能是城市名称无效 - {e}"

def get_attraction(city: str, weather: str) -> str:
    """根据城市和天气，使用 SearXNG 搜索并返回景点推荐"""
    query = f"{city} {weather}天气 旅游景点推荐"
    try:
        params = {
            "q": query,
            "format": "json"
        }
        response = requests.get(f"{SEARXNG_URL}search", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if not results:
            return "抱歉，没有找到相关的旅游景点推荐。"
        formatted_results = [f"- {result.get('title', '未知')}: {result.get('content', result.get('url', ''))}" 
                            for result in results[:3]]
        return "根据搜索，为您找到以下信息:\n" + "\n".join(formatted_results)
    except requests.exceptions.RequestException as e:
        return f"错误:SearXNG 搜索时遇到网络问题 - {e}"
    except Exception as e:
        return f"错误:执行搜索时出现问题 - {e}"

available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}
