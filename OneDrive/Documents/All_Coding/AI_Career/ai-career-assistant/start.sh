#!/usr/bin/env sh
set -e

# Start the Python ML service (uvicorn) in background, then start the Node server in foreground.
# Working directory: script is inside ai-career-assistant

cd "$(dirname "$0")/ml-service"
uvicorn main:app --host 0.0.0.0 --port 8000 &

cd "$(dirname "$0")"
exec node server/server.js
