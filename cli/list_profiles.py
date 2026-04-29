import yaml, os

with open("etc/model_manifest.yaml") as f:
    manifest = yaml.safe_load(f)

PROFILE = os.getenv("PROFILE", "balanced")

print(f"Active Profile: {PROFILE}\n")

print("Available Profiles:")
for name, cfg in manifest["profiles"].items():
    print(f"- {name}: {cfg}")
