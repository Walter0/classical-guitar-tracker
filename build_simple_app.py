#!/usr/bin/env python3
"""
Build script for creating a simple standalone Classical Guitar Learning Tracker
This version doesn't use PyQt5 and is more reliable
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed")

def create_simple_spec():
    """Create PyInstaller spec file for the simple app"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['simple_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('guitar_icon.png', '.'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('LICENSE', '.'),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.runtime.state',
        'requests',
        'sqlite3',
        'datetime',
        'webbrowser',
        'socket',
        'subprocess',
        'time',
        'signal',
        'atexit'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5', 'PyQt6', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GuitarTrackerSimple',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console for better debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='guitar_icon.png'
)

# Create macOS app bundle
app = BUNDLE(
    exe,
    name='Guitar Tracker Simple.app',
    icon='guitar_icon.png',
    bundle_identifier='com.guitartracker.simple',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'NSRequiresAquaSystemAppearance': 'False',
        'LSUIElement': 'False',
    },
)
'''
    
    with open('guitar_tracker_simple.spec', 'w') as f:
        f.write(spec_content.strip())
    
    print("✅ Created simple PyInstaller spec file")

def build_simple_app():
    """Build the simple standalone application"""
    print("🔨 Building simple standalone application...")
    
    try:
        # Build the app
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller", 
            "--clean", "guitar_tracker_simple.spec"
        ])
        
        print("✅ Simple application built successfully!")
        print("📁 Your app is located in: dist/Guitar Tracker Simple.app")
        print("🎸 This version opens in your browser automatically!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def main():
    """Main build process for simple app"""
    print("🎸 Building Simple Classical Guitar Learning Tracker")
    print("=" * 60)
    print("📝 This version uses your browser (no PyQt5 required)")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ app.py not found. Make sure you're in the guitar-tracker directory.")
        sys.exit(1)
    
    # Install dependencies
    install_pyinstaller()
    
    # Create spec file
    create_simple_spec()
    
    # Build the app
    if build_simple_app():
        print("\n🎉 SUCCESS!")
        print("Your simple Classical Guitar Learning Tracker app is ready!")
        print("This version will:")
        print("  • Show a terminal window with status messages")
        print("  • Automatically open your browser")
        print("  • Work more reliably than the PyQt5 version")
        print()
        print("To install:")
        print('  cp -r "dist/Guitar Tracker Simple.app" /Applications/')
    else:
        print("\n❌ Build failed. Check the error messages above.")

if __name__ == "__main__":
    main()