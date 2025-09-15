#!/usr/bin/env python3
"""
Build script for creating standalone Classical Guitar Learning Tracker app
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

def create_spec_file():
    """Create PyInstaller spec file for the app"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['desktop_app.py'],
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
        'requests',
        'sqlite3',
        'datetime',
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtWidgets', 
        'PyQt5.QtGui',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebEngineCore',
        'PyQt5.sip',
        'sip'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='ClassicalGuitarTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
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
    name='Classical Guitar Learning Tracker.app',
    icon='guitar_icon.png',
    bundle_identifier='com.guitartracker.app',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'NSRequiresAquaSystemAppearance': 'False',
    },
)
'''
    
    with open('guitar_tracker.spec', 'w') as f:
        f.write(spec_content.strip())
    
    print("✅ Created PyInstaller spec file")

def build_app():
    """Build the standalone application"""
    print("🔨 Building standalone application...")
    
    try:
        # Build the app
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller", 
            "--clean", "guitar_tracker.spec"
        ])
        
        print("✅ Application built successfully!")
        print("📁 Your app is located in: dist/Classical Guitar Learning Tracker.app")
        print("🎸 You can now move this to your Applications folder!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def main():
    """Main build process"""
    print("🎸 Building Classical Guitar Learning Tracker Standalone App")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ app.py not found. Make sure you're in the guitar-tracker directory.")
        sys.exit(1)
    
    # Install dependencies
    install_pyinstaller()
    
    # Create spec file
    create_spec_file()
    
    # Build the app
    if build_app():
        print("\n🎉 SUCCESS!")
        print("Your standalone Classical Guitar Learning Tracker app is ready!")
        print("You can find it in the 'dist' folder.")
    else:
        print("\n❌ Build failed. Check the error messages above.")

if __name__ == "__main__":
    main()