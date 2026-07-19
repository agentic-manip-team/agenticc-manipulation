"""
Web UI Backend
FastAPI server that bridges the browser-based UI with the ROS2 system.

Endpoints:
  POST /command  -> publish a user command to the /user/command ROS2 topic
  GET  /status   -> return current task execution status
  GET  /scene    -> return the latest scene graph
  GET  /plan     -> return the latest task plan
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Agentic Manipulation Web UI Backend")

# Allow the frontend (served separately) to call this API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# In-memory state — will be replaced with real ROS2 topic subscriptions
# once the vision, planning, and motion agents are integrated.
# ------------------------------------------------------------------
_latest_status = {"state": "IDLE", "current_step": None}

_latest_scene_graph = {
    "objects": [
        {
            "id": "obj_001",
            "label": "red_cube",
            "position_3d": {"x": 0.35, "y": 0.00, "z": 0.775},
        },
        {
            "id": "obj_002",
            "label": "grey_bin",
            "position_3d": {"x": 0.52, "y": 0.20, "z": 0.770},
        },
    ]
}

_latest_plan = {"steps": []}


class CommandRequest(BaseModel):
    command: str


@app.post("/command")
async def send_command(request: CommandRequest):
    """
    Receive a user command from the browser and publish it to ROS2.

    TODO: replace this placeholder with an actual ROS2 publisher call
    on the /user/command topic. For now, this simulates a task plan
    so the dashboard has something to display during demos.
    """
    global _latest_status, _latest_plan

    _latest_status = {"state": "RUNNING", "current_step": 1}

    _latest_plan = {
        "steps": [
            {"action": "OPEN_GRIPPER", "description": "Prepare gripper", "completed": True, "active": False},
            {"action": "MOVE_TO", "description": "Approach target object", "completed": True, "active": False},
            {"action": "CLOSE_GRIPPER", "description": "Grasp object", "completed": False, "active": True},
            {"action": "MOVE_TO", "description": "Transport to destination", "completed": False, "active": False},
            {"action": "OPEN_GRIPPER", "description": "Release object", "completed": False, "active": False},
        ]
    }

    return {"received_command": request.command, "status": "queued"}


@app.get("/status")
async def get_status():
    """Return the current task execution status."""
    # TODO: subscribe to /execution/status and /monitoring/task_result
    return _latest_status


@app.get("/scene")
async def get_scene():
    """Return the latest scene graph produced by the vision pipeline."""
    # TODO: subscribe to /scene/scene_graph
    return _latest_scene_graph


@app.get("/plan")
async def get_plan():
    """Return the latest task plan produced by the planning agent."""
    # TODO: subscribe to /planning/task_plan
    return _latest_plan


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}