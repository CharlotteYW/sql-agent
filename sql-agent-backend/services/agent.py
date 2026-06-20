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

SYSTEM_PROMPT = """You are a SQL data analysis assistant that can query databases using the following tools
list_tables: view all available tables
describe_table: view the structure of a table
execute_sql: execute SQL queries

Workflow:
1. First use list_tables to see what tables are available
2. Use describe_table to understand the structure of relevant tables
3. Write correct SQL and execute
4. Explain query results in clear language

Only execute SELECT queries, do not modify data."""

def run_agent(user_question: str) -> dict:
    # Build initial messages
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
        
        # Check if response contains tool calls
        if response.choices and len(response.choices) > 0:
            message_content = response.choices[0].message
            
            # Process tool call results
            if hasattr(message_content, 'tool_calls') and message_content.tool_calls:
                messages.append({"role": "assistant", "content": message_content.content})
                tool_results = []
                
                # Process each tool call
                for tool_call in message_content.tool_calls:
                    try:
                        # Parse tool arguments
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
                # No tool calls, return final result
                final_answer = ""
                if message_content.content:
                    final_answer = message_content.content
                return {
                    "steps": steps,
                    "answer": final_answer
                }
        else:
            # No response, return final result
            return {
                "steps": steps,
                "answer": "Sorry, I didn't get a response."
            }