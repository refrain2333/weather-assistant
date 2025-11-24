# 智能旅行助手

基于 Thought-Action-Observation 范式的智能体实现，能够查询天气并根据天气推荐旅游景点。

## 核心功能

| 功能模块 | 说明 | 实现方式 |
|---------|------|---------|
| 天气查询 | 获取指定城市实时天气 | wttr.in API |
| 景点推荐 | 根据天气状况推荐景点 | Tavily Search API |
| 智能决策 | 自主规划任务执行步骤 | LLM + Thought-Action-Observation 循环 |

## 系统架构

### 模块职责

| 模块 | 文件 | 职责 |
|------|------|------|
| 入口 | main.py | 配置加载、组件初始化、启动智能体 |
| 核心逻辑 | agent.py | TravelAgent 类，实现 Thought-Action-Observation 循环 |
| LLM 客户端 | llm_client.py | OpenAICompatibleClient 类，封装 LLM API 调用 |
| 工具函数 | tools.py | get_weather、get_attraction 工具实现 |
| 配置 | config.py | 系统提示词模板、默认配置常量 |

### 执行流程

```
用户请求 → 配置验证 → LLM 思考 → 解析动作 → 执行工具 → 观察结果 → 循环/完成
```

## 配置要求

| 环境变量 | 说明 | 获取方式 |
|---------|------|---------|
| OPENAI_API_KEY | LLM 服务 API 密钥 | 服务提供商 |
| OPENAI_BASE_URL | LLM 服务地址 | 服务提供商 |
| OPENAI_MODEL | 模型名称 | 服务提供商 |
| TAVILY_API_KEY | Tavily Search API 密钥 | [Tavily官网](https://tavily.com) |

设置方式：方式1（推荐）复制 `.env.example` 为 `.env` 并填入配置；方式2：`export OPENAI_API_KEY="your_key"`

## 安装要求

### 系统要求

| 项目 | 要求 |
|------|------|
| Python 版本 | Python 3.8+ |
| 操作系统 | Windows、macOS、Linux |
| 网络连接 | 需要访问外部 API |

### 安装步骤

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 创建虚拟环境 | `python3 -m venv venv`，激活：`source venv/bin/activate`（Windows：`venv\Scripts\activate`） |
| 2 | 安装依赖 | `pip install -r requirements.txt` |
| 3 | 配置环境变量 | 方式1：复制 `.env.example` 为 `.env` 并填入配置（推荐）<br>方式2：设置环境变量 |

### 依赖包

| 包名 | 最低版本 | 用途 |
|------|---------|------|
| requests | 2.31.0 | HTTP 请求库，天气 API 调用 |
| tavily-python | 0.3.0 | Tavily 搜索 API 客户端 |
| openai | 1.0.0 | OpenAI API 客户端，兼容其他 LLM 服务 |
| python-dotenv | 1.0.0 | 加载 .env 文件配置 |

## 使用方法

运行：`python main.py`

默认任务：查询北京天气并推荐景点

自定义任务：修改 `main.py` 中的 `user_prompt` 变量

## 工作原理

### Thought-Action-Observation 循环

1. **Thought（思考）**：LLM 分析当前状态，规划下一步行动
2. **Action（行动）**：解析并执行工具调用或完成动作
3. **Observation（观察）**：收集工具执行结果
4. **循环**：将观察结果加入上下文，继续下一轮循环
5. **完成**：当收集足够信息时，输出最终答案

### 工具调用机制

- 工具注册：`available_tools` 字典管理所有工具函数
- 参数解析：正则表达式提取工具名称和参数
- 错误处理：工具执行失败返回错误信息，不影响主循环

## 技术特性

- 模块化设计，职责分离清晰
- 兼容 OpenAI API 规范（支持 OpenAI、Azure、Ollama 等）
- 最大循环次数限制（默认5次），防止无限循环
- 完善的错误处理和日志输出

## 注意事项

- 需要网络连接访问外部 API
- 需要配置有效的 API 密钥
- 城市名称建议使用英文或标准中文名称
