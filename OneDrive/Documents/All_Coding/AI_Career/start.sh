#!/usr/bin/env sh
set -e

# Start the Python ML service (uvicorn) in background, then start the Node server in foreground.
# Working directory: ai-career-assistant

cd "ai-career-assistant/ml-service"
# Start uvicorn in background; logs will go to stdout/stderr
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Return to repo root and start the Node server (foreground)
cd ../..

# Start Node server (assumes dependencies installed during build)
exec node server/server.js
