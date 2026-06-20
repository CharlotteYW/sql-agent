from fastapi import APIRouter
from pydantic import BaseModel
from services.agent import run_agent

router = APIRouter(prefix='/api', tags=["agents"])

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query(req: QueryRequest):
    return run_agent(req.question)