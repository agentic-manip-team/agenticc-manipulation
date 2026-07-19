/* ============================================================
   Agentic Manipulation — Control Dashboard
   Frontend logic: connects to the FastAPI backend and keeps
   the UI in sync with task status, scene graph, and plan.
   ============================================================ */

const API_BASE_URL = "http://localhost:8000";
const POLL_INTERVAL_MS = 2000;

// ---------- DOM references ----------
const commandInput = document.getElementById("commandInput");
const sendCommandBtn = document.getElementById("sendCommandBtn");
const statusDot = document.getElementById("statusDot");
const statusLabel = document.getElementById("statusLabel");
const taskState = document.getElementById("taskState");
const currentStep = document.getElementById("currentStep");
const planSteps = document.getElementById("planSteps");
const sceneObjects = document.getElementById("sceneObjects");
const quickChips = document.querySelectorAll(".chip");

// ---------- Connection state ----------
function setConnected(isConnected) {
  statusDot.classList.toggle("connected", isConnected);
  statusLabel.textContent = isConnected ? "Connected" : "Disconnected";
}

// ---------- API helpers ----------
async function apiGet(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) throw new Error(`GET ${path} failed: ${response.status}`);
  return response.json();
}

async function apiPost(path, body) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(`POST ${path} failed: ${response.status}`);
  return response.json();
}

// ---------- Command submission ----------
async function sendCommand(commandText) {
  if (!commandText.trim()) return;

  sendCommandBtn.disabled = true;
  sendCommandBtn.querySelector("span").textContent = "Sending…";

  try {
    await apiPost("/command", { command: commandText });
    commandInput.value = "";
  } catch (error) {
    console.error("Failed to send command:", error);
  } finally {
    sendCommandBtn.disabled = false;
    sendCommandBtn.querySelector("span").textContent = "Send Command";
  }
}

sendCommandBtn.addEventListener("click", () => {
  sendCommand(commandInput.value);
});

commandInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendCommand(commandInput.value);
  }
});

quickChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    const command = chip.dataset.cmd;
    commandInput.value = command;
    sendCommand(command);
  });
});

// ---------- Rendering: status ----------
function renderStatus(status) {
  taskState.textContent = status.state || "IDLE";
  currentStep.textContent = status.current_step ?? "—";
}

// ---------- Rendering: task plan ----------
function renderPlan(plan) {
  const steps = plan.steps || [];

  if (steps.length === 0) {
    planSteps.innerHTML = `<li class="plan-step empty">No active plan yet. Send a command to begin.</li>`;
    return;
  }

  planSteps.innerHTML = steps
    .map((step, index) => {
      const stateClass = step.completed ? "done" : step.active ? "active" : "";
      return `
        <li class="plan-step ${stateClass}">
          <span class="step-index">${index + 1}</span>
          <span>${step.action || "STEP"} ${step.description ? "— " + step.description : ""}</span>
        </li>
      `;
    })
    .join("");
}

// ---------- Rendering: scene graph ----------
function renderScene(scene) {
  const objects = scene.objects || [];

  if (objects.length === 0) {
    sceneObjects.innerHTML = `<p class="empty-state">No objects detected yet.</p>`;
    return;
  }

  sceneObjects.innerHTML = objects
    .map(
      (obj) => `
        <div class="scene-object-card">
          <div class="scene-object-name">${obj.label || obj.id}</div>
          <div class="scene-object-meta">
            <span>x: ${obj.position_3d?.x?.toFixed(2) ?? "—"}</span>
            <span>y: ${obj.position_3d?.y?.toFixed(2) ?? "—"}</span>
            <span>z: ${obj.position_3d?.z?.toFixed(2) ?? "—"}</span>
          </div>
        </div>
      `
    )
    .join("");
}

// ---------- Polling loop ----------
async function pollBackend() {
  try {
    const [status, plan, scene] = await Promise.all([
      apiGet("/status"),
      apiGet("/plan"),
      apiGet("/scene"),
    ]);

    setConnected(true);
    renderStatus(status);
    renderPlan(plan);
    renderScene(scene);
  } catch (error) {
    console.error("Polling error:", error);
    setConnected(false);
  }
}

// Start polling once the page has loaded
pollBackend();
setInterval(pollBackend, POLL_INTERVAL_MS);