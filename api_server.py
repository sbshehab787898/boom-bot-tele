
import sys
import os
import threading
import time
import importlib.util
from fastapi import FastAPI
import uvicorn
import requests
from requests.sessions import Session

# --- Monitoring & Stats System ---
# We patch requests.Session.request to intercept all outgoing HTTP calls
# This allows us to count total requests, successes, and failures without touching the bot code.

stats = {
    "attack_requests": {
        "total": 0,
        "success": 0,
        "failed": 0
    },
    "telegram_requests": {
        "total": 0,
        "success": 0,
        "failed": 0
    },
    "by_domain": {}
}

active_threads = []

# Store the original request method to call it later
original_request = Session.request

def patched_request(self, method, url, *args, **kwargs):
    global stats
    domain = "unknown"
    is_telegram = False
    
    try:
        if "//" in url:
            parts = url.split("/")
            if len(parts) > 2:
                domain = parts[2]
                if "telegram.org" in domain:
                    is_telegram = True
        else:
            domain = url
    except:
        pass

    # Initialize domain stats if new
    if domain not in stats["by_domain"]:
        stats["by_domain"][domain] = {"total": 0, "success": 0, "failed": 0}

    # Increment counters PRE-request
    stats["by_domain"][domain]["total"] += 1
    
    if is_telegram:
        stats["telegram_requests"]["total"] += 1
    else:
        stats["attack_requests"]["total"] += 1

    try:
        # Call the original method
        response = original_request(self, method, url, *args, **kwargs)
        
        # Check status code (200 OK is success, anything else is failure/blocked)
        if response.status_code == 200:
            if is_telegram:
                stats["telegram_requests"]["success"] += 1
            else:
                stats["attack_requests"]["success"] += 1
            stats["by_domain"][domain]["success"] += 1
        else:
            if is_telegram:
                stats["telegram_requests"]["failed"] += 1
            else:
                stats["attack_requests"]["failed"] += 1
            stats["by_domain"][domain]["failed"] += 1
            
        return response
    except Exception as e:
        if is_telegram:
            stats["telegram_requests"]["failed"] += 1
        else:
            stats["attack_requests"]["failed"] += 1
        stats["by_domain"][domain]["failed"] += 1
        raise e

# Apply the patch
Session.request = patched_request

# --- Import the Existing Bot Code Dynamically ---
# We use importlib because the filename contains non-ASCII characters
bot_filename = "app.py"
module_name = "bot_final_module"

if not os.path.exists(bot_filename):
    print(f"Error: Could not find {bot_filename}")
    sys.exit(1)

# Because the filename contains non-ascii characters, we need to be careful with paths
# Standard python 3 handles this well usually
spec = importlib.util.spec_from_file_location(module_name, bot_filename)
bot_module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = bot_module
spec.loader.exec_module(bot_module)

# Now we have access to the bot's variables and functions via bot_module

# --- FastAPI App Definition ---
app = FastAPI(title="SBS Bot Monitor API", description="API to monitor bot health and stats")

@app.get("/")
def home():
    return {
        "status": "Online",
        "message": "SBS Bot is running securely via Docker Wrapper.",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    # Check if the bot threads are alive
    return {
        "status": "Healthy",
        "bot_active": getattr(bot_module, "bot_active", False),
        "admin_id": getattr(bot_module, "ADMIN_ID", 0),
        "total_users": len(getattr(bot_module, "users_db", {})),
        "uptime_stats": stats["attack_requests"]
    }

@app.get("/stats")
def get_stats():
    # Return the gathered statistics
    return stats

@app.get("/users")
def get_users_summary():
    # Helper to see user counts without exposing full DB
    users = getattr(bot_module, "users_db", {})
    approved = sum(1 for u in users.values() if u.get('approved'))
    blocked = sum(1 for u in users.values() if u.get('blocked'))
    return {
        "total": len(users),
        "approved": approved,
        "blocked": blocked
    }

# --- Start Background Threads ---
def start_bot_threads():
    # Replicating the main block of the original script
    # We must run them as daemon threads so they don't block the API server shutdown
    
    if hasattr(bot_module, "start_bot") and hasattr(bot_module, "public_bot"):
        t1 = threading.Thread(target=bot_module.start_bot, args=(bot_module.public_bot, "Public Bot"), daemon=True)
        t2 = threading.Thread(target=bot_module.start_bot, args=(bot_module.admin_bot, "Admin Bot"), daemon=True)
        
        t1.start()
        t2.start()
        
        active_threads.append(t1)
        active_threads.append(t2)
        print("Background Bot Threads Started Successfully.")
    else:
        print("Error: Could not find start_bot function in module.")

if __name__ == "__main__":
    # Start bots
    start_bot_threads()
    
    # Run API server
    print("Starting API Server on port 8000...")
    # Using 0.0.0.0 for Docker access
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
