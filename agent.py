"""智能体核心模块 - 包含 Thought-Action-Observation 循环逻辑"""
import re
from typing import List, Tuple, Optional
from tools import available_tools
from config import AGENT_SYSTEM_PROMPT, DEFAULT_MAX_ITERATIONS

class TravelAgent:
    """智能旅行助手 - 基于 Thought-Action-Observation 范式"""
    def __init__(self, llm_client, max_iterations: int = DEFAULT_MAX_ITERATIONS):
        self.llm_client = llm_client
        self.max_iterations = max_iterations
        self.prompt_history: List[str] = []
    
    def _truncate_output(self, llm_output: str) -> str:
        """截断 LLM 输出中多余的 Thought-Action 对"""
        match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                print("已截断多余的 Thought-Action 对")
                return truncated
        return llm_output
    
    def _parse_action(self, llm_output: str) -> Tuple[Optional[str], Optional[dict]]:
        """解析 LLM 输出中的 Action，返回 (action_type, action_data)"""
        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            return None, None
        action_str = action_match.group(1).strip()
        if action_str.startswith("finish"):
            finish_match = re.search(r'finish\(answer="(.*)"\)', action_str, re.DOTALL)
            if finish_match:
                return "finish", finish_match.group(1)
            print("解析错误: finish 动作格式不正确。")
            return None, None
        tool_match = re.search(r"(\w+)\(", action_str)
        if not tool_match:
            print("解析错误:无法从 Action 中提取工具名称。")
            return None, None
        tool_name = tool_match.group(1)
        args_match = re.search(r"\((.*)\)", action_str, re.DOTALL)
        if not args_match:
            print("解析错误:无法从 Action 中提取参数。")
            return None, None
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_match.group(1)))
        return "tool_call", {"tool_name": tool_name, "kwargs": kwargs}
    
    def _execute_tool(self, tool_name: str, kwargs: dict) -> str:
        """执行工具调用"""
        if tool_name not in available_tools:
            return f"错误:未定义的工具 '{tool_name}'"
        print(f"正在调用工具: {tool_name}({', '.join([f'{k}={v}' for k, v in kwargs.items()])})")
        return available_tools[tool_name](**kwargs)
    
    def run(self, user_prompt: str) -> Optional[str]:
        """运行智能体的主循环"""
        self.prompt_history = [f"用户请求: {user_prompt}"]
        print(f"用户输入: {user_prompt}\n" + "="*40)
        for i in range(self.max_iterations):
            print(f"\n--- 循环 {i+1} ---\n")
            full_prompt = "\n".join(self.prompt_history)
            llm_output = self.llm_client.generate(full_prompt, AGENT_SYSTEM_PROMPT)
            llm_output = self._truncate_output(llm_output)
            print(f"模型输出:\n{llm_output}\n")
            self.prompt_history.append(llm_output)
            action_type, action_data = self._parse_action(llm_output)
            if action_type is None:
                print("解析错误:模型输出中未找到有效的 Action。")
                break
            if action_type == "finish":
                print(f"\n任务完成，最终答案: {action_data}")
                return action_data
            elif action_type == "tool_call":
                observation = self._execute_tool(action_data["tool_name"], action_data["kwargs"])
                observation_str = f"Observation: {observation}"
                print(f"{observation_str}\n" + "="*40)
                self.prompt_history.append(observation_str)
        print(f"\n达到最大循环次数 ({self.max_iterations})，程序结束。")
        return None
