from fastapi import FastAPI, Response
import yaml
import os

app = FastAPI()

ready = False

# Load manifest
with open("etc/model_manifest.yaml") as f:
    manifest = yaml.safe_load(f)

# Get profile
PROFILE = os.getenv("PROFILE", "balanced")

if PROFILE not in manifest["profiles"]:
    print(f"Invalid PROFILE: {PROFILE}")
    print("Valid:", list(manifest["profiles"].keys()))
    exit(1)

active_profile = manifest["profiles"][PROFILE]

# Simulate model loading
import time
time.sleep(3)
ready = True

@app.get("/v1/health/live")
def live():
    return {"status": "live"}

@app.get("/v1/health/ready")
def ready_check():
    if ready:
        return {"status": "ready"}
    return Response(status_code=503)

@app.get("/v1/models")
def models():
    return {"data": [{"id": "dummy-model"}]}

@app.get("/v1/profiles")
def profiles():
    return {
        "active": PROFILE,
        "profiles": manifest["profiles"]
    }

@app.post("/v1/chat/completions")
def chat():
    return {
        "id": "123",
        "object": "chat.completion",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": f"Response using {PROFILE} profile"
                }
            }
        ]
    }
