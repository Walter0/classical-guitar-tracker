#!/bin/bash

# Classical Guitar Learning Tracker Launcher
# This script starts the Streamlit app and opens it in the browser

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎸 Classical Guitar Learning Tracker${NC}"
echo "=================================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_FILE="$SCRIPT_DIR/app.py"

# Check if app.py exists
if [ ! -f "$APP_FILE" ]; then
    echo -e "${RED}❌ Error: app.py not found at $APP_FILE${NC}"
    echo "Please make sure this script is in the same directory as your app.py file."
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 is not installed or not in PATH${NC}"
    echo "Please install Python 3 to run this application."
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Streamlit is not installed. Installing...${NC}"
    python3 -m pip install streamlit
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install Streamlit${NC}"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Find a free port
PORT=$(python3 -c "
import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', 0))
    s.listen(1)
    print(s.getsockname()[1])
")

echo -e "${BLUE}🌐 Starting server on port $PORT...${NC}"

# Start Streamlit in the background
python3 -m streamlit run "$APP_FILE" \
    --server.port "$PORT" \
    --browser.gatherUsageStats false \
    --server.headless true \
    --server.enableCORS false &

STREAMLIT_PID=$!

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}👋 Shutting down Classical Guitar Learning Tracker...${NC}"
    kill $STREAMLIT_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for server to be ready
echo -e "${BLUE}⏳ Waiting for server to start...${NC}"
for i in {1..30}; do
    if curl -s "http://localhost:$PORT" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Server ready!${NC}"
        break
    fi
    sleep 1
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ Server failed to start within 30 seconds${NC}"
        kill $STREAMLIT_PID 2>/dev/null
        read -p "Press Enter to exit..."
        exit 1
    fi
done

# Open the browser
echo -e "${GREEN}🚀 Opening http://localhost:$PORT in your browser...${NC}"
open "http://localhost:$PORT"

echo -e "${GREEN}🎸 Classical Guitar Learning Tracker is now running!${NC}"
echo -e "${YELLOW}💡 Close this terminal window to stop the app.${NC}"
echo ""

# Keep the script running and wait for the Streamlit process
wait $STREAMLIT_PID