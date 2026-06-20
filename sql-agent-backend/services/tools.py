import json
from database.supabase_client import supabase

TOOL_DEFINITIONS = [
    {
        "name": "list_tables",
        "description": "List all available table names in the database",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "describe_table",
        "description": "View field names and data types of a table",
        "input_schema": {
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "Table name"
                }
            },
            "required": ["table_name"]
        }
    },
    {
        "name": "execute_sql",
        "description": "Execute a SQL SELECT query and return results",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "SQL SELECT statement to execute"
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
    # Security check: only allow SELECT
    if not query.strip().upper().startswith("SELECT"):
        return json.dumps({"error": "only allow select"})
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
        return json.dumps({"error": f"Unknown tool: {tool_name}"})