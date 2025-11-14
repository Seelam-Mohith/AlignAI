#!/usr/bin/env sh
set -e
# Delegate to the real start script in the repository root ai-career-assistant folder
cd "$(dirname "$0")/../../ai-career-assistant"
sh start.sh
