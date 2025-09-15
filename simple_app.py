#!/usr/bin/env python3
"""
Simple standalone Classical Guitar Learning Tracker
Browser-based launcher without PyQt5 dependencies
"""

import subprocess
import sys
import time
import webbrowser
import socket
import requests
import os
import signal
import atexit

class GuitarTrackerLauncher:
    def __init__(self):
        self.streamlit_process = None
        self.port = None
        
    def find_free_port(self):
        """Find a free port for Streamlit"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def wait_for_server(self, timeout=30):
        """Wait for the Streamlit server to be ready"""
        print("⏳ Waiting for server to start...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://localhost:{self.port}", timeout=1)
                if response.status_code == 200:
                    return True
            except:
                time.sleep(0.5)
        return False
    
    def cleanup(self):
        """Clean up the Streamlit process"""
        if self.streamlit_process:
            print("\n👋 Shutting down Classical Guitar Learning Tracker...")
            self.streamlit_process.terminate()
            try:
                self.streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.streamlit_process.kill()
    
    def launch(self):
        """Launch the Classical Guitar Learning Tracker"""
        print("🎸 Classical Guitar Learning Tracker")
        print("=" * 50)
        
        # Register cleanup function
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
        
        # Find a free port
        self.port = self.find_free_port()
        print(f"🌐 Starting server on port {self.port}...")
        
        # Get the directory where this script is located
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle
            app_dir = os.path.dirname(sys.executable)
        else:
            # Running as Python script
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        app_file = os.path.join(app_dir, "app.py")
        
        # Start Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", app_file,
            "--server.port", str(self.port),
            "--browser.gatherUsageStats", "false",
            "--server.headless", "true",
            "--server.enableCORS", "false"
        ]
        
        try:
            self.streamlit_process = subprocess.Popen(
                cmd, 
                cwd=app_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if self.wait_for_server():
                print("✅ Server ready!")
                print(f"🚀 Opening http://localhost:{self.port} in your browser...")
                webbrowser.open(f"http://localhost:{self.port}")
                print("\n🎸 Classical Guitar Learning Tracker is now running!")
                print("💡 Close this window to stop the app.")
                print("💡 Or press Ctrl+C to quit.")
                
                try:
                    # Keep the process running
                    self.streamlit_process.wait()
                except KeyboardInterrupt:
                    pass
                    
            else:
                print("❌ Failed to start server")
                return 1
                
        except Exception as e:
            print(f"❌ Error starting application: {e}")
            return 1
        
        return 0

def main():
    """Main application entry point"""
    launcher = GuitarTrackerLauncher()
    return launcher.launch()

if __name__ == "__main__":
    sys.exit(main())