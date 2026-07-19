# Agentic Manipulation System

An AI-driven robotic manipulation system that combines **vision**, **large language model (LLM) planning**, and **ROS2-based motion control** to let a robot arm understand natural-language commands, perceive its environment, and physically manipulate objects — end to end.

> Example: *"Pick up the red cube and place it in the grey bin."*
> The system detects the objects, plans the pick-and-place sequence, and executes it on a simulated Franka Panda arm in Gazebo.

---

## Overview

The system is composed of five cooperating agents, each running as an independent ROS2 node:

| Agent | Responsibility |
|---|---|
| **Vision Agent** | Object detection (GroundingDINO), segmentation (SAM2), depth estimation (Depth Anything V2) |
| **Scene Understanding Agent** | 6D pose estimation (FoundationPose) and scene graph construction |
| **Planning Agent** | Converts natural-language commands + scene graph into a structured task plan via an LLM (GPT-4o / Gemini) |
| **Motion Planning & Execution Agent** | Grasp planning (AnyGrasp) and trajectory execution via MoveIt2 |
| **Monitoring & Recovery Agent** | Detects step failures and triggers recovery strategies |

A web-based **control dashboard** lets a user issue commands and observe the scene graph, task plan, and execution status in real time.

---

## Architecture

```
User Command
     │
     ▼
Web UI  ──────────────►  Planning Agent  ──►  LLM (GPT-4o / Gemini)
                               ▲                     │
                               │                      ▼
                        Scene Graph            Task Plan (JSON)
                               ▲                      │
                               │                      ▼
                     Scene Understanding      Motion Planning Agent
                               ▲                      │
                               │                      ▼
                        Vision Agent  ◄────  Execution Agent (MoveIt2)
                               ▲                      │
                          Camera (Gazebo)       Gazebo Simulator
```

---

## Tech Stack

- **Vision:** GroundingDINO, SAM2, Depth Anything V2, FoundationPose
- **Planning:** OpenAI GPT-4o, Google Gemini (via LiteLLM)
- **Robotics:** ROS2 Humble, MoveIt2, Gazebo, Franka Panda arm
- **Grasping:** AnyGrasp SDK
- **Backend:** FastAPI
- **Frontend:** HTML / CSS / JavaScript (vanilla, no framework)
- **Infrastructure:** Docker, Docker Compose, GitHub Actions (CI/CD)

---

## Project Structure

```
agenticc-manipulation/
├── ros2_ws/src/              # ROS2 packages (vision, planning, motion, monitoring agents)
├── docker/                   # Dockerfiles for vision, ros2, foundation_pose
├── web_ui/                   # Control dashboard (backend + frontend)
├── docs/                     # Installation guides and architecture docs
├── notebooks/                # Jupyter notebooks for model testing
├── tests/                    # Unit and integration tests
├── config/                   # MoveIt2 and system configuration
├── scripts/                  # Setup and utility scripts
├── data/                     # Evaluation data and logs
└── docker-compose.yml        # One-command system startup
```

---

## Getting Started

### Prerequisites
- Ubuntu 22.04 LTS
- Python 3.10+
- Docker Desktop
- ROS2 Humble
- NVIDIA GPU (recommended for vision models; CPU fallback supported)

### Quick Start (Web Dashboard Only)

```bash
# Backend
cd web_ui/backend
python -m venv venv
source venv/Scripts/activate      # Windows (Git Bash)
pip install fastapi uvicorn
uvicorn main:app --reload --port 8000

# Frontend (in a separate terminal)
cd web_ui/frontend
python -m http.server 8080
```

Then open **http://localhost:8080** in your browser.

Full installation instructions (ROS2, Gazebo, vision models) are in [`docs/installation/full_guide.md`](docs/installation/full_guide.md).

---

## Team

| Member | Role |
|---|---|
| M1 | Vision & Perception Lead |
| M2 | Planning & LLM Lead |
| M3 | Robotics & Simulation Lead |
| M4 | Integration & DevOps Lead |
| M5 | Monitoring, Recovery & Testing Lead |

---

## Status

🚧 **In active development** — this project is being built incrementally, with each component developed and tested independently before integration.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.