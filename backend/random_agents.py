import requests
import random
import time

BASE_URL = "http://127.0.0.1:8000"

# List of possible targets on the screen
# In a real AI, the agent would discover these by reading the DOM
POSSIBLE_SELECTORS = [
    "[data-testid='login-email-input']",
    "[data-testid='login-password-input']",
    "[data-testid='login-submit-btn']",
    "h2", # Clicking the title (useless)
    "p"   # Clicking a paragraph (useless)
]

def run_random_agent():
    print("🤪 Random Agent started. It has no idea what it's doing.")
    
    # Reset
    requests.post(f"{BASE_URL}/step", json={"action_type": "reset", "selector": "", "value": ""})
    
    max_steps = 10
    
    for step in range(max_steps):
        # Pick a random action
        action_type = random.choice(["click", "type"])
        selector = random.choice(POSSIBLE_SELECTORS)
        
        # If typing, type gibberish
        value = "admin@demo.com" if random.random() > 0.8 else "hfdjskhf"
        
        print(f"Step {step}: Trying to {action_type} on {selector}...")
        
        requests.post(f"{BASE_URL}/step", json={
            "action_type": action_type,
            "selector": selector,
            "value": value
        })
        
        # Check if we accidentally won
        state = requests.get(f"{BASE_URL}/state").json()
        if state['reward'] > 0:
            print("🤯 WOW! The random agent accidentally solved it!")
            break
            
        time.sleep(0.5)
        
    print("Run complete.")

if __name__ == "__main__":
    run_random_agent()