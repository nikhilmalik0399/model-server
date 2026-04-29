# Model Server (Profile-Aware)

## Build

docker build -t model-server .

## Run

docker run -p 8000:8000 -e PROFILE=balanced model-server

Profiles:
- throughput
- latency
- balanced

## Curl Example

curl -X POST http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{"messages":[{"role":"user","content":"Hello"}]}'

## OpenAI Client Example

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")

resp = client.chat.completions.create(
    model="tinyllama",
    messages=[{"role":"user","content":"Hello"}]
)

print(resp.choices[0].message.content)
