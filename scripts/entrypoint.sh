#!/bin/sh

if [ -z "$PROFILE" ]; then
  export PROFILE=balanced
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
