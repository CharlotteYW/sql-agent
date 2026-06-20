from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.agent import router

app = FastAPI(title ="SQL Helper Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"status": "ok", "message":"SQL Agent running"}