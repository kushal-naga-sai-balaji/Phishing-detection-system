#!/bin/bash

# PhishGuard - Automated Demo Runner
# Starts the server, runs simulated scans, and cleans up

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Starting PhishGuard Automated Demo...${NC}"

# 1. Start Backend in Background
echo -e "\n${GREEN}[1/3] Launching Background Server...${NC}"
cd backend
source venv/bin/activate
python main.py > server.log 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# 2. Run Demo Script
echo -e "\n${GREEN}[2/3] Running Simulation Script...${NC}"
# Give server a moment to start
sleep 3
python demo_script.py

# 3. Cleanup
echo -e "\n${GREEN}[3/3] Cleaning up...${NC}"
kill $SERVER_PID
echo -e "${BLUE}✅ Demo Complete! Server stopped.${NC}"
