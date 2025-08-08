from fastapi import FastAPI
from .agent_route import router as agent_router

app = FastAPI(title="DigiSoul Backend", version="0.1.0")
app.include_router(agent_router)

@app.get("/")
def root():
    return {"ok": True, "service": "backend"}
