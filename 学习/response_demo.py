"""response 对象内容演示"""
import requests

# 发送请求
url = 'https://wttr.in/北京?format=j1'
response = requests.get(url)

print("=== Response 对象内容 ===")
print(f"状态码: {response.status_code}")
print(f"是否成功: {response.ok}")
print(f"编码: {response.encoding}")

print("\n=== 响应头 ===")
for key, value in response.headers.items():
    print(f"{key}: {value}")

print("\n=== 原始文本内容 ===")
print(response.text)

print("\n=== 解析后的JSON数据 ===")
data = response.json()
print(f"数据类型: {type(data)}")
print(f"包含的键: {list(data.keys())}")

print("\n=== 当前天气信息 ===")
current = data['current_condition'][0]
print(f"天气描述: {current['weatherDesc'][0]['value']}")
print(f"温度: {current['temp_C']}°C")
print(f"湿度: {current['humidity']}%")
print(f"风向: {current['winddir16Point']}")
print(f"风速: {current['windspeedKmph']} km/h")
