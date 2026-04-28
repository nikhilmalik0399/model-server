#!/bin/sh

if [ -z "$PROFILE" ]; then
  export PROFILE=balanced
fi

python app/main.py &

uvicorn app.main:app --host 0.0.0.0 --port 8000
