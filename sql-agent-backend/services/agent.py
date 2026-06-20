import os
from openai import OpenAI
from dotenv import load_dotenv
from services.tools import TOOL_DEFINITIONS, execute_tool
import json

load_dotenv()

def get_client(provider: str) -> OpenAI:
    if provider == "groq":
        return OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")   
        )
    elif provider == "ollama":
        return OpenAI(
            base_url="http://localhost:11434/v1",
            api_key=os.getenv("OLLAMA_API_KEY") or "ollama"
        )
    else:
        # Default to ollama
        return OpenAI(
            base_url="http://localhost:11434/v1",
            api_key=os.getenv("OLLAMA_API_KEY") or "ollama"
        )

# Use ollama as default provider
client = get_client("ollama")

SYSTEM_PROMPT = """你是一个 SQL 数据分析助手，你可以使用以下工具查询数据库
list_tables:查看所有可用的表
describe_table:查看某张表的结构
execute_sql:执行 SQL 查询

工作流程:
1. 先用 list_tables 了解有哪些表
2. 用 describe_table 了解相关表的结构
3. 写出正确的 SQL 并执行
4. 用清晰的语言解释查询结果

只执行 SELECT 查询，不修改数据。"""

def run_agent(user_question: str) -> dict:
    # 构建初始消息
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]
    steps = []
    
    while True:
        response = client.chat.completions.create(
            model="llama3.1:8b",
            max_tokens=4096,
            temperature=0.0,
            messages=messages
        )
        
        # 检查响应中是否有工具调用
        if response.choices and len(response.choices) > 0:
            message_content = response.choices[0].message
            
            # 处理工具调用结果
            if hasattr(message_content, 'tool_calls') and message_content.tool_calls:
                messages.append({"role": "assistant", "content": message_content.content})
                tool_results = []
                
                # 处理每个工具调用
                for tool_call in message_content.tool_calls:
                    try:
                        # 解析工具参数
                        if isinstance(tool_call.function.arguments, str):
                            args = json.loads(tool_call.function.arguments)
                        else:
                            args = tool_call.function.arguments
                            
                        result = execute_tool(tool_call.function.name, args)
                        steps.append({
                            "tool": tool_call.function.name,
                            "input": args,
                            "result": result
                        })
                        tool_results.append({
                            "type": "tool_result",
                            "tool_call_id": tool_call.id,
                            "content": result
                        })
                    except Exception as e:
                        error_result = json.dumps({"error": str(e)})
                        steps.append({
                            "tool": tool_call.function.name,
                            "input": args,
                            "result": error_result
                        })
                        tool_results.append({
                            "type": "tool_result",
                            "tool_call_id": tool_call.id,
                            "content": error_result
                        })
                
                messages.append({"role": "user", "content": tool_results})
            else:
                # 无工具调用，返回最终结果
                final_answer = ""
                if message_content.content:
                    final_answer = message_content.content
                return {
                    "steps": steps,
                    "answer": final_answer
                }
        else:
            # 无响应，返回最终结果
            return {
                "steps": steps,
                "answer": "抱歉，我没有得到响应。"
            }