"""LLM 客户端模块 - 用于调用兼容 OpenAI 接口的 LLM 服务"""
from typing import TypeAlias
from openai import OpenAI
from config import LLM_STREAM, LLM_TEMPERATURE, LLM_MAX_TOKENS, LLM_TIMEOUT

GenerateResult: TypeAlias = tuple[str, dict]

class OpenAICompatibleClient:
    """用于调用任何兼容OpenAI接口的LLM服务的客户端"""
    def __init__(self, model: str, api_key: str, base_url: str) -> None:
        self.model = model
        self.stream = LLM_STREAM
        self.temperature = LLM_TEMPERATURE
        self.max_tokens = LLM_MAX_TOKENS
        self.timeout = LLM_TIMEOUT
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=self.timeout)

    def generate(self, prompt: str, system_prompt: str) -> GenerateResult:
        """调用LLM API来生成回应
        Args:
            prompt: 用户输入的提示词
            system_prompt: 系统提示词
        Returns:
            (回应文本, token 消费信息字典)
        Raises:
            ValueError: 当输入为空时
        """
        if not prompt or not system_prompt:
            raise ValueError("prompt 和 system_prompt 不能为空")
        try:
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=self.stream,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            answer = response.choices[0].message.content
            usage = {
                'input_tokens': response.usage.prompt_tokens,
                'output_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }
            return answer, usage
        except ValueError as e:
            raise
        except Exception as e:
            raise
