#!/usr/bin/env python3
"""
Simple launcher for Classical Guitar Learning Tracker
Opens the app in your default browser automatically
"""

import subprocess
import sys
import time
import webbrowser
import socket
import requests
from threading import Thread
import os

def find_free_port():
    """Find a free port for Streamlit"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def wait_for_server(port, timeout=30):
    """Wait for the Streamlit server to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"http://localhost:{port}", timeout=1)
            if response.status_code == 200:
                return True
        except:
            time.sleep(0.5)
    return False

def launch_app():
    """Launch the Classical Guitar Learning Tracker"""
    print("🎸 Starting Classical Guitar Learning Tracker...")
    
    # Find a free port
    port = find_free_port()
    
    # Get the directory where this script is located
    app_dir = os.path.dirname(os.path.abspath(__file__))
    app_file = os.path.join(app_dir, "app.py")
    
    # Start Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", app_file,
        "--server.port", str(port),
        "--browser.gatherUsageStats", "false",
        "--server.headless", "true"
    ]
    
    # Start Streamlit in background
    print(f"🌐 Starting server on port {port}...")
    process = subprocess.Popen(cmd, cwd=app_dir)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to start...")
    if wait_for_server(port):
        print("✅ Server ready!")
        print(f"🚀 Opening http://localhost:{port} in your browser...")
        webbrowser.open(f"http://localhost:{port}")
        print("🎸 Classical Guitar Learning Tracker is now running!")
        print("💡 Close this terminal window to stop the app.")
        
        try:
            # Keep the process running
            process.wait()
        except KeyboardInterrupt:
            print("\n👋 Shutting down Classical Guitar Learning Tracker...")
            process.terminate()
            process.wait()
    else:
        print("❌ Failed to start server")
        process.terminate()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(launch_app())