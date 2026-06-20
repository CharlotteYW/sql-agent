# sql-agent

## Test

1.

```
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question":"which are has the highese sales?"}'
```

2. Start backend: `sql-agent-backend % python -m uvicorn main:app --reload --port 8000`

<img width="880" height="665" alt="image" src="https://github.com/user-attachments/assets/d0fc1e5c-8037-4b36-bffc-4338626fb4db" />

## TODO:
1. Fix the output format. Currently it is using Ollama and OPENAI client and MCP interface, but some code we are using is Anthropic MCP interface, then the output result looks strange.
2. Add more MCP servers and more functions to support more use case.
3. Improve the UI.
