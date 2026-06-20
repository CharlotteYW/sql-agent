# sql-agent

## Test

1.

```
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question":"哪个地方销售额最高"}'
```

2. Start backend: `sql-agent-backend % python -m uvicorn main:app --reload --port 8000`