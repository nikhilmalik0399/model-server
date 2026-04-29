from fastapi import FastAPI, Response
import yaml, os, time, logging, signal, sys
from app.model_loader import load_model

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
ready = False

# load manifest
with open("etc/model_manifest.yaml") as f:
    manifest = yaml.safe_load(f)

PROFILE = os.getenv("PROFILE", "balanced")

if PROFILE not in manifest["profiles"]:
    print(f"Invalid PROFILE: {PROFILE}")
    print("Valid:", list(manifest["profiles"].keys()))
    exit(1)

config = manifest["profiles"][PROFILE]
model_path = manifest["model"]["path"]

logger.info(f"Starting with PROFILE={PROFILE}")
logger.info(f"Config: {config}")

# load model
model = load_model(model_path, config["threads"])
ready = True

# graceful shutdown
def shutdown_handler(signum, frame):
    logger.info("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

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
    return {"data": [{"id": "tinyllama"}]}

@app.get("/v1/profiles")
def profiles():
    return {"active": PROFILE, "profiles": manifest["profiles"]}

@app.post("/v1/chat/completions")
def chat(req: dict):
    prompt = req["messages"][-1]["content"]

    logger.info(f"Request: {prompt}")

    output = model(
        prompt,
        max_new_tokens=config["max_new_tokens"],
        temperature=config["temperature"]
    )

    return {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "tinyllama",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": output
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(output.split()),
            "total_tokens": len(prompt.split()) + len(output.split())
        }
    }
