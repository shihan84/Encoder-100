#!/usr/bin/env python3
"""
ITAssist Broadcast Encoder - 100 (IBE-100)
Professional Software Packaging Configuration
Cross-platform build configuration for PyInstaller
"""

import os
import sys
import platform
from pathlib import Path

# Application Information
APP_NAME = "IBE-100"
APP_VERSION = "1.4.0"
APP_DESCRIPTION = "ITAssist Broadcast Encoder - 100 (IBE-100)"
APP_AUTHOR = "ITAssist Broadcast Solutions"
APP_COMPANY = "ITAssist Broadcast Solutions"
APP_COPYRIGHT = "© 2024 ITAssist Broadcast Solutions | Dubai • Mumbai • Gurugram"

# Platform-specific configurations
PLATFORM = platform.system().lower()

# Build directories
BUILD_DIR = "build"
DIST_DIR = "dist"
SPEC_DIR = "specs"

# Data files to include
DATA_FILES = [
    ("scte35_final", "scte35_final"),
    ("README.md", "."),
    ("LICENSE.txt", "."),
    ("requirements.txt", "."),
]

# TSDuck binary paths (platform-specific)
TSDUCK_PATHS = {
    "darwin": [
        "/usr/local/bin/tsp",
        "/usr/bin/tsp",
        "/opt/tsduck/bin/tsp"
    ],
    "linux": [
        "/usr/bin/tsp",
        "/usr/local/bin/tsp",
        "/opt/tsduck/bin/tsp"
    ],
    "windows": [
        "C:\\Program Files\\TSDuck\\bin\\tsp.exe",
        "C:\\Program Files (x86)\\TSDuck\\bin\\tsp.exe",
        "C:\\tsduck\\bin\\tsp.exe"
    ]
}

# PyInstaller options
PYINSTALLER_OPTIONS = {
    "onefile": {
        "onefile": True,
        "windowed": True,
        "name": f"{APP_NAME}",
        "icon": "assets/icon.ico" if PLATFORM == "windows" else "assets/icon.icns",
        "add_data": DATA_FILES,
        "hidden_imports": [
            "PyQt6.QtCore",
            "PyQt6.QtWidgets",
            "PyQt6.QtGui",
            "psutil"
        ],
        "excludes": [
            "tkinter",
            "matplotlib",
            "numpy",
            "pandas"
        ]
    },
    "onedir": {
        "onedir": True,
        "windowed": True,
        "name": f"{APP_NAME}",
        "icon": "assets/icon.ico" if PLATFORM == "windows" else "assets/icon.icns",
        "add_data": DATA_FILES,
        "hidden_imports": [
            "PyQt6.QtCore",
            "PyQt6.QtWidgets", 
            "PyQt6.QtGui",
            "psutil"
        ],
        "excludes": [
            "tkinter",
            "matplotlib",
            "numpy",
            "pandas"
        ]
    }
}

# Platform-specific build configurations
PLATFORM_CONFIGS = {
    "darwin": {
        "app_bundle": True,
        "icon": "assets/icon.icns",
        "plist": {
            "CFBundleName": APP_NAME,
            "CFBundleDisplayName": APP_NAME,
            "CFBundleIdentifier": f"com.itassist.{APP_NAME.lower()}",
            "CFBundleVersion": APP_VERSION,
            "CFBundleShortVersionString": APP_VERSION,
            "CFBundleInfoDictionaryVersion": "6.0",
            "CFBundleExecutable": APP_NAME,
            "CFBundlePackageType": "APPL",
            "CFBundleSignature": "IBE1",
            "LSMinimumSystemVersion": "10.14.0",
            "NSHighResolutionCapable": True
        }
    },
    "windows": {
        "icon": "assets/icon.ico",
        "version_file": "assets/version_info.txt",
        "nsis_script": "installer/nsis_installer.nsi"
    },
    "linux": {
        "icon": "assets/icon.png",
        "desktop_file": "assets/ibe-100.desktop",
        "appimage": True
    }
}

def get_tsduck_path():
    """Get TSDuck binary path for current platform"""
    import shutil
    
    # Try to find tsp in PATH
    tsp_path = shutil.which("tsp")
    if tsp_path:
        return tsp_path
    
    # Try platform-specific paths
    for path in TSDUCK_PATHS.get(PLATFORM, []):
        if os.path.exists(path):
            return path
    
    return None

def create_build_directories():
    """Create necessary build directories"""
    directories = [BUILD_DIR, DIST_DIR, SPEC_DIR, "assets", "installer"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def get_pyinstaller_command(build_type="onefile"):
    """Generate PyInstaller command for current platform"""
    options = PYINSTALLER_OPTIONS[build_type]
    
    cmd = ["pyinstaller"]
    
    if options.get("onefile"):
        cmd.append("--onefile")
    if options.get("onedir"):
        cmd.append("--onedir")
    if options.get("windowed"):
        cmd.append("--windowed")
    
    cmd.extend(["--name", options["name"]])
    
    if options.get("icon"):
        cmd.extend(["--icon", options["icon"]])
    
    # Add data files
    for src, dst in options.get("add_data", []):
        cmd.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
    
    # Add hidden imports
    for imp in options.get("hidden_imports", []):
        cmd.extend(["--hidden-import", imp])
    
    # Add excludes
    for exc in options.get("excludes", []):
        cmd.extend(["--exclude-module", exc])
    
    # Add main script
    cmd.append("tsduck_gui_simplified.py")
    
    return cmd

if __name__ == "__main__":
    print(f"🔧 {APP_NAME} Build Configuration")
    print(f"📱 Platform: {PLATFORM}")
    print(f"🔍 TSDuck Path: {get_tsduck_path()}")
    print(f"📦 Build Type: Available (onefile, onedir)")
    print(f"🎯 Target: {APP_DESCRIPTION}")
