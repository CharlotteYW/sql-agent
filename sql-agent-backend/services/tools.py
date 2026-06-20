import json
from database.supabase_client import supabase

TOOL_DEFINITIONS = [
    {
        "name": "list_tables",
        "description": "列出数据库中所有可用的表名",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "describe_table",
        "description": "查看某张表的字段名和数据类型",
        "input_schema": {
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "表名"
                }
            },
            "required": ["table_name"]
        }
    },
    {
        "name": "execute_sql",
        "description": "执行 SQL SELECT 查询，返回结果",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "要执行的 SQL SELECT 语句"
                }
            },
            "required": ["query"]
        }
    }
]


def list_tables() -> str:
    result = supabase.rpc("execute_query", {
        "query_text": "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' ORDER BY table_name"
    }).execute()
    tables = [row["table_name"] for row in result.data]
    return json.dumps(tables)


def describe_table(table_name: str) -> str:
    result = supabase.rpc("execute_query", {
        "query_text": "SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '" + table_name + "' AND table_schema = 'public' ORDER BY ordinal_position"
    }).execute()
    return json.dumps(result.data)


def execute_sql(query: str) -> str:
    # 安全检查:只允许 SELECT
    if not query.strip().upper().startswith("SELECT"):
        return json.dumps({"error": "只允许 SELECT 查询"})
    result = supabase.rpc("execute_query", {"query_text": query}).execute()
    return json.dumps(result.data)


def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "list_tables":
        return list_tables()
    elif tool_name == "describe_table":
        return describe_table(tool_input["table_name"])
    elif tool_name == "execute_sql":
        return execute_sql(tool_input["query"])
    else:
        return json.dumps({"error": f"未知工具: {tool_name}"})