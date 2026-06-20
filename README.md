# sql-agent

## Test

1.

```
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question":"which are has the highese sales?"}'
```

2. Start backend: `sql-agent-backend % python -m uvicorn main:app --reload --port 8000`

<img width="883" height="756" alt="image" src="https://github.com/user-attachments/assets/b3f8022a-1ea3-49a9-b51f-2457d8f3ef4d" />

## TODO:
1. Fix the output format. Currently it is using Ollama and OPENAI client and MCP interface, but some code we are using is Anthropic MCP interface, then the output result looks strange.
2. Add more MCP servers and more functions to support more use case.
3. Improve the UI.
