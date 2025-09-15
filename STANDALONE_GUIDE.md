# 🎸 Creating a Standalone Classical Guitar Learning Tracker

This guide shows you multiple ways to turn your Streamlit app into a standalone local application.

## 🚀 Quick Start Options

### Option 1: Simple Browser Launcher (Easiest)
**Best for**: Quick daily use, minimal setup

```bash
python3 launch.py
```

This will:
- ✅ Start the app automatically
- ✅ Open your default browser
- ✅ Find an available port
- ✅ Show status messages
- ✅ Clean shutdown with Ctrl+C

### Option 2: Desktop App with GUI (Recommended)
**Best for**: Native app experience, no browser tabs

1. **Install desktop dependencies**:
   ```bash
   pip install PyQt5 PyQtWebEngine requests
   ```

2. **Run the desktop app**:
   ```bash
   python3 desktop_app.py
   ```

This creates a native desktop window with:
- ✅ Native macOS app window
- ✅ Custom app icon
- ✅ No browser interface
- ✅ Clean app management

### Option 3: Reliable Standalone Executable (Recommended for Distribution)
**Best for**: Distribution, no Python required, most reliable

1. **Build the simple standalone app**:
   ```bash
   python3 build_simple_app.py
   ```

2. **Find your app**:
   - Location: `dist/Guitar Tracker Simple.app`
   - Move to Applications folder
   - Double-click to run anywhere
   - Opens in your browser automatically

## 📋 Detailed Instructions

### For Option 1: Simple Launcher

**Pros:**
- ✅ No additional dependencies
- ✅ Uses your default browser
- ✅ Quick to set up
- ✅ Easy to customize

**Cons:**
- ❌ Requires terminal window open
- ❌ Browser-dependent

**Usage:**
1. Open Terminal
2. Navigate to your guitar-tracker folder
3. Run: `python3 launch.py`
4. Your browser opens automatically
5. Close terminal window to stop

### For Option 2: Desktop App

**Pros:**
- ✅ Native app experience
- ✅ No browser UI clutter
- ✅ Custom window controls
- ✅ Feels like a real app

**Cons:**
- ❌ Requires PyQt5 installation
- ❌ Slightly larger memory footprint

**Setup:**
1. **Install dependencies:**
   ```bash
   pip install PyQt5 PyQtWebEngine requests
   ```

2. **Test the desktop app:**
   ```bash
   python3 desktop_app.py
   ```

3. **Create desktop shortcut:**
   - Create an Automator app that runs `python3 /path/to/desktop_app.py`
   - Or use the provided AppleScript

### For Option 3: Standalone Executable

**Pros:**
- ✅ No Python installation needed
- ✅ Fully portable
- ✅ Professional deployment
- ✅ Can distribute to others

**Cons:**
- ❌ Large file size (~150MB)
- ❌ Build process can be complex
- ❌ macOS security warnings

**Build Process:**
1. **Run the build script:**
   ```bash
   python3 build_app.py
   ```

2. **Wait for build to complete** (~5-10 minutes)

3. **Find your app:**
   ```bash
   ls dist/
   # Look for: Classical Guitar Learning Tracker.app
   ```

4. **Install the app:**
   ```bash
   cp -r "dist/Classical Guitar Learning Tracker.app" /Applications/
   ```

## 🛠️ Troubleshooting

### Common Issues:

**"Command not found" errors:**
```bash
# Make sure scripts are executable
chmod +x *.py
```

**Port conflicts:**
```bash
# Kill any existing Streamlit processes
pkill -f streamlit
```

**PyQt5 installation issues on macOS:**
```bash
# If PyQt5 fails to install
brew install pyqt5
pip install PyQt5 --no-cache-dir
```

**Build failures:**
```bash
# Clean build directory
rm -rf build/ dist/ *.spec
python3 build_app.py
```

### macOS Security:

For standalone apps, you may see security warnings:
1. Right-click the app → "Open"
2. Click "Open" in the security dialog
3. Or go to System Preferences → Security & Privacy → Allow

## 📁 File Structure

After setup, your directory will contain:

```
guitar-tracker/
├── app.py                    # Main Streamlit app
├── launch.py                 # Simple browser launcher
├── desktop_app.py           # Desktop GUI wrapper  
├── build_app.py             # Standalone app builder
├── requirements.txt         # Dependencies
├── guitar_icon.svg          # App icon
├── guitar_tracker.db        # Your data
└── dist/                    # Built applications
    └── Classical Guitar Learning Tracker.app
```

## 🎯 Recommendation

**For daily personal use:** Use Option 2 (Desktop App)
- Native app experience
- Clean interface
- Easy to launch

**For sharing with others:** Use Option 3 (Reliable Standalone Executable)
- No Python installation required
- Most reliable (no PyQt5 issues)
- Browser-based interface
- Portable

**For quick testing:** Use Option 1 (Simple Launcher)
- Fastest setup
- Good for development

## 🎸 Enjoy Your Standalone App!

Your Classical Guitar Learning Tracker is now ready to use as a standalone application. Choose the option that best fits your needs and happy practicing! 🎵