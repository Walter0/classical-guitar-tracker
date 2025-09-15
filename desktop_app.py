#!/usr/bin/env python3
"""
Classical Guitar Learning Tracker - Desktop App
A desktop wrapper for the Streamlit application
"""

import sys
import os
import time
import subprocess
import threading
import signal
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
import requests
import socket

class GuitarTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.streamlit_process = None
        self.port = 8501
        self.setup_ui()
        self.start_streamlit()
        
    def setup_ui(self):
        """Setup the desktop application UI"""
        self.setWindowTitle("🎸 Classical Guitar Learning Tracker")
        self.setGeometry(100, 100, 1200, 800)
        
        # Try to set custom icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "guitar_icon.png")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except:
            pass
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create web view
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # Timer to check when Streamlit is ready
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_streamlit_ready)
        
    def find_free_port(self):
        """Find a free port for Streamlit"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
        
    def start_streamlit(self):
        """Start the Streamlit server in a separate process"""
        # Find free port
        self.port = self.find_free_port()
        
        # Get the directory where the script is located
        app_dir = os.path.dirname(os.path.abspath(__file__))
        app_file = os.path.join(app_dir, "app.py")
        
        # Start Streamlit process
        cmd = [
            sys.executable, "-m", "streamlit", "run", app_file,
            "--server.port", str(self.port),
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--server.enableCORS", "false"
        ]
        
        try:
            self.streamlit_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=app_dir
            )
            
            # Start checking if Streamlit is ready
            self.check_timer.start(500)  # Check every 500ms
            
        except Exception as e:
            print(f"Error starting Streamlit: {e}")
            sys.exit(1)
    
    def check_streamlit_ready(self):
        """Check if Streamlit server is ready"""
        try:
            response = requests.get(f"http://localhost:{self.port}", timeout=1)
            if response.status_code == 200:
                self.check_timer.stop()
                self.web_view.load(QUrl(f"http://localhost:{self.port}"))
        except:
            pass  # Keep checking
    
    def closeEvent(self, event):
        """Handle application close event"""
        if self.streamlit_process:
            self.streamlit_process.terminate()
            self.streamlit_process.wait()
        event.accept()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Classical Guitar Learning Tracker")
    app.setApplicationVersion("1.0")
    
    # Create and show main window
    window = GuitarTrackerApp()
    window.show()
    
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()