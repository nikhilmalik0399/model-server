import yaml
import os

with open("etc/model_manifest.yaml") as f:
    manifest = yaml.safe_load(f)

PROFILE = os.getenv("PROFILE", "balanced")

print("Active Profile:", PROFILE)
print("Available Profiles:")

for name, config in manifest["profiles"].items():
    print(f"- {name}: {config}")
