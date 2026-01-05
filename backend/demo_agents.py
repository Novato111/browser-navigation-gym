import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def log(step, message):
    print(f"[{step}] {message}")

def run_agent():
    print("🤖 Agent coming online...")
    
    # 1. Reset the environment (reload page)
    # This ensures we start from a clean slate
    requests.post(f"{BASE_URL}/step", json={"action_type": "reset", "selector": "", "value": ""})
    time.sleep(1) # Wait for page load

    # 2. Define our "Plan"
    # An AI would figure this out by trial and error. We are cheating for the demo.
    actions = [
        {
            "name": "Type Email",
            "action_type": "type",
            "selector": "[data-testid='login-email-input']", 
            "value": "admin@demo.com"
        },
        {
            "name": "Type Password",
            "action_type": "type",
            "selector": "[data-testid='login-password-input']", 
            "value": "password123"
        },
        {
            "name": "Click Login",
            "action_type": "click",
            "selector": "[data-testid='login-submit-btn']", 
            "value": ""
        }
    ]

    # 3. Execute the Plan
    for i, move in enumerate(actions):
        log(i+1, f"Executing: {move['name']}")
        
        # Send action to Backend
        response = requests.post(f"{BASE_URL}/step", json=move)
        data = response.json()
        
        # Check if it worked
        if data['action_result']['status'] == 'failed':
            print(f"❌ Failed: {data['action_result'].get('error')}")
            break
            
        # Optional: Add a small delay so we can watch it happen
        time.sleep(1.5)

    # 4. Check Final Result
    log("FINISH", "Checking if we won...")
    final_state = requests.get(f"{BASE_URL}/state").json()
    
    if final_state['reward'] > 0:
        print("\n🏆 SUCCESS! Reward Received: 100 points")
        print("The Agent successfully logged in.")
    else:
        print("\n💀 FAILED. Reward: 0")
        print("The Agent did not complete the mission.")

if __name__ == "__main__":
    run_agent()