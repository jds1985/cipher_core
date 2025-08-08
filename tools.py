from typing import Dict, Any
import os, requests

RUNNER_BASE = os.getenv("RUNNER_BASE_URL", "").rstrip("/")

ALLOW_TOOLS = {
    "exec": "/exec",
    "fs_write_one": "/fs/write_one",
    "fs_write_many": "/fs/write_many",
    "git_commit": "/git/commit",
    "test": "/test/run",
    "deploy": "/deploy/trigger"
}

def call_tool(tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    assert tool in ALLOW_TOOLS, "Tool not allowed"
    assert RUNNER_BASE, "RUNNER_BASE_URL not set"
    url = RUNNER_BASE + ALLOW_TOOLS[tool]
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()
