# 智能旅行助手

基于 Thought-Action-Observation 范式的智能体实现，能够自主规划任务、查询天气信息，并根据天气状况推荐合适的旅游景点。

## 项目概述

这是一个演示智能体（Agent）系统的项目，展示了如何让大语言模型（LLM）通过工具调用完成复杂任务。智能体能够自主分析用户需求，规划执行步骤，调用外部工具获取信息，并根据结果做出决策。

## 核心功能

### 天气查询
通过调用 wttr.in API 获取指定城市的实时天气信息，包括天气状况和温度。

### 景点推荐
根据城市和天气状况，使用 SearXNG 搜索引擎查找并推荐适合的旅游景点。

### 智能决策
智能体能够自主规划任务执行步骤，通过 Thought-Action-Observation 循环逐步完成复杂任务。

## 系统架构

### 模块结构

项目采用模块化设计，各模块职责清晰：

- **main.py**：程序入口，负责配置验证、组件初始化和启动智能体
- **agent.py**：核心逻辑模块，实现 TravelAgent 类和 Thought-Action-Observation 循环
- **llm_client.py**：LLM 客户端封装，提供统一的接口调用兼容 OpenAI API 的 LLM 服务
- **tools.py**：工具函数模块，包含 get_weather 和 get_attraction 两个工具函数
- **config.py**：配置管理模块，集中管理所有配置参数和系统提示词

### 执行流程

智能体的执行遵循以下流程：

1. 用户输入请求
2. 配置验证（检查 API 密钥等）
3. LLM 思考（分析当前状态，规划下一步）
4. 解析动作（提取工具名称和参数）
5. 执行工具（调用外部 API 获取信息）
6. 观察结果（收集工具执行结果）
7. 循环或完成（根据结果决定继续循环或输出最终答案）

## 工作原理

### Thought-Action-Observation 循环

这是智能体的核心工作机制：

**Thought（思考）**：LLM 分析当前状态和用户需求，规划下一步行动。思考过程会考虑已有的信息和需要获取的信息。

**Action（行动）**：根据思考结果，智能体决定执行的动作。可能是调用工具获取信息，也可能是完成任务并输出答案。

**Observation（观察）**：执行动作后，收集执行结果。如果是工具调用，会获取工具返回的数据；如果是完成动作，会输出最终答案。

**循环机制**：观察结果会被添加到对话历史中，作为下一轮思考的上下文。智能体会根据新的信息继续规划，直到收集到足够信息并完成任务。

### 工具调用机制

智能体通过工具字典管理所有可用工具。当需要调用工具时：

1. 从 LLM 输出中解析工具名称和参数
2. 在工具字典中查找对应的函数对象
3. 执行工具函数并获取结果
4. 将结果格式化为 Observation 格式，加入对话历史

工具执行失败时会返回错误信息，但不会中断主循环，智能体可以根据错误信息调整策略。

## 安装与配置

### 系统要求

- Python 3.8 或更高版本
- 支持 Windows、macOS、Linux 操作系统
- 需要网络连接以访问外部 API

### 安装步骤

1. **创建虚拟环境**（推荐）
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**

   创建 `.env` 文件（在项目根目录），并填入以下配置：

   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_BASE_URL=your_base_url_here
   OPENAI_MODEL=your_model_name_here
   SEARXNG_URL=http://localhost:8888/
   ```

   各配置项说明：
   - `OPENAI_API_KEY`：LLM 服务的 API 密钥
   - `OPENAI_BASE_URL`：LLM 服务的 API 地址（支持 OpenAI、Azure、Ollama 等兼容接口）
   - `OPENAI_MODEL`：要使用的模型名称
   - `SEARXNG_URL`：SearXNG 搜索引擎的地址（默认本地服务）

### 依赖包说明

- **requests**：用于发送 HTTP 请求，调用天气 API
- **openai**：OpenAI API 客户端，兼容其他 LLM 服务
- **python-dotenv**：用于加载 `.env` 文件中的环境变量

## 使用方法

### 基本使用

运行主程序：
```bash
python main.py
```

默认会执行查询上海天气并推荐景点的任务。

### 自定义任务

修改 `main.py` 中的 `user_prompt` 变量即可自定义任务：

```python
user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
```

## 技术特性

### 模块化设计
各模块职责分离，便于维护和扩展。新增工具只需在 `tools.py` 中定义函数并注册到工具字典即可。

### API 兼容性
LLM 客户端兼容 OpenAI API 规范，可以无缝使用 OpenAI、Azure OpenAI、Ollama 等支持相同接口的服务。

### 安全机制
- 最大循环次数限制（默认 5 次），防止无限循环
- 完善的错误处理，工具执行失败不会中断主循环
- 配置验证机制，启动前检查必要配置

### 可观测性
每次循环都会输出详细的执行信息，包括 Token 消费情况、模型输出、工具调用等，便于调试和监控。

## 注意事项

1. **网络连接**：需要稳定的网络连接以访问外部 API（wttr.in 和 SearXNG）

2. **API 配置**：确保配置了有效的 LLM API 密钥和地址

3. **SearXNG 服务**：如果使用本地 SearXNG 服务，需要先启动服务。也可以使用公共 SearXNG 实例

4. **城市名称**：建议使用标准的城市名称（英文或中文），以提高 API 识别准确率

5. **循环限制**：如果任务过于复杂，可能达到最大循环次数限制。可以修改 `config.py` 中的 `DEFAULT_MAX_ITERATIONS` 调整限制

## 扩展开发

### 添加新工具

1. 在 `tools.py` 中定义工具函数
2. 将函数注册到 `available_tools` 字典
3. 在 `config.py` 的系统提示词中说明新工具的用法

### 修改循环逻辑

核心循环逻辑在 `agent.py` 的 `run` 方法中，可以根据需要调整循环策略、错误处理等逻辑。

### 自定义系统提示词

修改 `config.py` 中的 `AGENT_SYSTEM_PROMPT` 可以改变智能体的行为模式和输出格式。
