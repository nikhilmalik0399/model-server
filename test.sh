#!/bin/bash
set -e

docker build -t model-server .

for profile in throughput latency balanced
do
  echo "Testing $profile..."

  docker run -d -p 8000:8000 -e PROFILE=$profile --name test-$profile model-server

  echo "Waiting for readiness..."
  for i in {1..15}; do
    if curl -s http://localhost:8000/v1/health/ready; then
      break
    fi
    sleep 2
  done

  curl -f http://localhost:8000/v1/health/ready

  curl -X POST http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"messages":[{"role":"user","content":"Explain DevOps"}]}'

  curl http://localhost:8000/v1/profiles | grep $profile

  docker rm -f test-$profile
done

echo "ALL TESTS PASSED"
