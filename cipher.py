"""Cipher Orchestrator (LangGraph-style stub)

This is a minimal scaffold so you can immediately wire real LangGraph flows.
Replace the stubs with actual graph nodes and tool calls.
"""
from dataclasses import dataclass
from typing import List, Dict, Any
import os, json, time, uuid
import requests

RUNNER_BASE = os.getenv("RUNNER_BASE_URL", "").rstrip("/")

def runner_call(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    assert RUNNER_BASE, "RUNNER_BASE_URL not set"
    url = f"{RUNNER_BASE}{path}"
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()

@dataclass
class Task:
    id: str
    title: str
    agent: str
    payload: Dict[str, Any]

def create_task(title: str, agent: str, payload: Dict[str, Any]) -> Task:
    return Task(id=str(uuid.uuid4()), title=title, agent=agent, payload=payload)

def agent_frontend(task: Task) -> Dict[str, Any]:
    """Generates a simple page in services/frontend."""
    files = {
        "services/frontend/pages/agent.tsx": """export default function AgentPage(){return (<div className='p-6'>Hello from Agent: {new Date().toISOString()}</div>)}"""
    }
    return runner_call("/fs/write_many", {"files": files, "message": f"Frontend update for task {task.title}"})

def agent_backend(task: Task) -> Dict[str, Any]:
    """Adds a simple endpoint in backend."""
    code = """from fastapi import APIRouter
router = APIRouter()
@router.get('/agent-ping')
def agent_ping():
    return {'ok': True, 'task': '%s'}
""" % task.title
    return runner_call("/fs/write_one", {"path": "services/backend/app/agent_route.py", "content": code, "message": f"Backend update for task {task.title}"})

def agent_qa(task: Task) -> Dict[str, Any]:
    """Adds a trivial test file."""
    test_content = """def test_smoke():
    assert True
"""
    return runner_call("/fs/write_one", {"path": "services/backend/tests/test_smoke.py", "content": test_content, "message": f"QA tests for {task.title}"})

def agent_deployer(task: Task) -> Dict[str, Any]:
    """Opens a Git commit and (optionally) triggers a deploy workflow."""
    return runner_call("/git/commit", {"message": f"Commit from Deployer for {task.title}"})

def run_demo_flow():
    t1 = create_task("Hello World Feature", "Architect", {})
    agent_frontend(t1)
    agent_backend(t1)
    agent_qa(t1)
    agent_deployer(t1)
    return {"status": "ok", "task": t1.id}

if __name__ == "__main__":
    print(json.dumps(run_demo_flow(), indent=2))
