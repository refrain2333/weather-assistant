# requests.get() Response 对象详解

## 概述

`response = requests.get(url)` 是Python中使用requests库发送HTTP GET请求的基本语法。这行代码返回一个Response对象，包含了服务器响应的所有信息。

## Response 对象结构

### 1. 基本属性

| 属性 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `status_code` | int | HTTP状态码 | 200 |
| `ok` | bool | 请求是否成功(status_code < 400) | True |
| `url` | str | 实际请求的URL | https://wttr.in/北京?format=j1 |
| `encoding` | str | 响应编码 | utf-8 |
| `elapsed` | timedelta | 请求耗时 | 0:00:00.523456 |

### 2. 响应内容

| 属性/方法 | 返回类型 | 说明 | 用法 |
|-----------|----------|------|------|
| `response.text` | str | 解码后的文本内容 | `print(response.text)` |
| `response.content` | bytes | 原始字节内容 | `binary_data = response.content` |
| `response.json()` | dict/list | 解析JSON响应 | `data = response.json()` |

### 3. 响应头信息

```python
response.headers = {
    'content-type': 'application/json',
    'content-length': '1234',
    'server': 'nginx',
    'cache-control': 'no-cache'
}
```

## 实际应用示例

### 天气API调用流程

```python
import requests

# 1. 构建请求URL
url = f"https://wttr.in/{city}?format=j1"

# 2. 发送GET请求
response = requests.get(url)

# 3. 检查请求状态
response.raise_for_status()  # 失败时抛出异常

# 4. 解析JSON数据
data = response.json()

# 5. 提取天气信息
current = data['current_condition'][0]
weather = current['weatherDesc'][0]['value']
temp = current['temp_C']
```

### Response对象在天气查询中的数据流

```
HTTP请求 → Response对象 → JSON解析 → 数据提取 → 格式化输出
    ↓           ↓           ↓          ↓          ↓
requests.get() → response → response.json() → data[...] → "北京晴天，15°C"
```

## 常用方法说明

### 错误处理
```python
try:
    response = requests.get(url)
    response.raise_for_status()  # 检查HTTP错误
except requests.exceptions.RequestException as e:
    print(f"网络请求失败: {e}")
```

### 数据验证
```python
if response.ok:
    data = response.json()
    # 处理数据
else:
    print(f"请求失败，状态码: {response.status_code}")
```

## 天气API返回数据结构

### 顶层结构
```json
{
    "current_condition": [...],  // 当前天气
    "nearest_area": [...],       // 地理信息
    "request": [...],           // 请求参数
    "weather": [...]            // 天气预报
}
```

### 当前天气字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| `weatherDesc[0].value` | 天气描述 | "Sunny" |
| `temp_C` | 摄氏温度 | "15" |
| `humidity` | 湿度百分比 | "39" |
| `winddir16Point` | 风向 | "SSE" |
| `windspeedKmph` | 风速(公里/小时) | "7" |
| `pressure` | 气压 | "1022" |
| `visibility` | 能见度 | "10" |
| `uvIndex` | 紫外线指数 | "0" |

## 最佳实践

### 1. 异常处理
```python
def get_weather_safe(city: str) -> str:
    try:
        response = requests.get(f"https://wttr.in/{city}?format=j1")
        response.raise_for_status()
        data = response.json()
        # 数据处理逻辑
        return f"{city}天气: {data['current_condition'][0]['weatherDesc'][0]['value']}"
    except requests.exceptions.RequestException as e:
        return f"网络错误: {e}"
    except (KeyError, IndexError) as e:
        return f"数据解析错误: {e}"
```

### 2. 性能优化
```python
# 设置超时时间
response = requests.get(url, timeout=10)

# 使用会话复用连接
with requests.Session() as session:
    response = session.get(url)
```

## 总结

Response对象是HTTP请求的核心，它封装了：
- **状态信息**：请求是否成功、状态码等
- **元数据**：响应头、编码、URL等
- **实际内容**：文本、JSON、二进制数据
- **便利方法**：JSON解析、错误检查等

掌握Response对象的使用是进行HTTP请求编程的基础，特别是在API调用和数据处理场景中。
