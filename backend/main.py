from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from browser_env import BrowserGym
import asyncio

app = FastAPI()

# Allow React to talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

env = BrowserGym()

# --- GLOBAL STATE ---
simulation_state = {
    "is_running": False,
    "logs": [],
    "current_step": "Idle",
    "reward": 0,
    "current_task_id": "login"
}

# --- TASK REGISTRY ---
# This defines what the agent does for each mission.
TASKS = {
    "login": {
        "success_text": "Mission Complete", # Text to find on Success Screen
        "steps": [
            {"msg": "Locating Email Field...", "action": "type", "sel": "[data-testid='login-email-input']", "val": "admin@demo.com"},
            {"msg": "Typing Password...", "action": "type", "sel": "[data-testid='login-password-input']", "val": "password123"},
            {"msg": "Clicking Submit...", "action": "click", "sel": "[data-testid='login-submit-btn']", "val": ""}
        ]
    },
    "shopping": {
        "success_text": "Order Placed", # Text to find on Success Screen
        "steps": [
            # Artificial "thinking" step - clicking title (does nothing)
            {"msg": "Scanning Page...", "action": "click", "sel": "h2", "val": ""}, 
            # Correct action - clicking the specific button for Product 2 (Keyboard)
            {"msg": "Adding Keyboard to Cart...", "action": "click", "sel": "[data-testid='add-to-cart-prod-2']", "val": ""}
        ]
    }
}

# --- LIFECYCLE ---
@app.on_event("startup")
async def startup_event():
    print("🚀 Booting up Browser Gym...")
    await env.start()

@app.on_event("shutdown")
async def shutdown_event():
    await env.close()

# --- AGENT LOGIC ---
async def run_agent_logic(task_id: str):
    """The 'Brain' of the agent running in the background"""
    simulation_state["is_running"] = True
    simulation_state["current_task_id"] = task_id
    simulation_state["logs"] = [f"🚀 Starting Task: {task_id.upper()}"]
    simulation_state["reward"] = 0
    
    # 1. Reset Environment to clean state
    await env.execute_action("reset", "", "")
    await asyncio.sleep(1) # Wait for reload

    # 2. Get the plan for this specific task
    task_config = TASKS.get(task_id)
    if not task_config:
        simulation_state["logs"].append(f"❌ Error: Unknown Task {task_id}")
        simulation_state["is_running"] = False
        return

    steps = task_config["steps"]
    success_criteria = task_config["success_text"]

    # 3. Execute Steps
    for step in steps:
        simulation_state["logs"].append(f"🤖 {step['msg']}")
        
        result = await env.execute_action(step["action"], step["sel"], step["val"])
        
        if result["status"] == "failed":
            simulation_state["logs"].append(f"⚠️ Action Failed: {result.get('error')}")
        
        await asyncio.sleep(1.5) # Artificial delay so humans can watch

    # 4. Check Result
    # Pass the specific success text we are looking for
    state = await env.get_state(success_text=success_criteria)
    
    if state["reward"] > 0:
        simulation_state["logs"].append(f"🏆 SUCCESS! Found text: '{success_criteria}'")
        simulation_state["reward"] = 100
    else:
        simulation_state["logs"].append(f"💀 FAILED. Could not find text: '{success_criteria}'")

    simulation_state["is_running"] = False

# --- API ENDPOINTS ---

class StartRequest(BaseModel):
    task_id: str = "login"

@app.get("/status")
def get_status():
    return simulation_state

@app.post("/start-simulation")
async def start_simulation(req: StartRequest, background_tasks: BackgroundTasks):
    if simulation_state["is_running"]:
        return {"status": "Busy, agent is already running"}
    
    # Launch the agent in background
    background_tasks.add_task(run_agent_logic, req.task_id)
    return {"status": "Started", "task": req.task_id}