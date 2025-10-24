#!/usr/bin/env python3
"""
TSDuck GUI Launcher
Simple launcher script with dependency checking
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_tsduck():
    """Check if TSDuck is available"""
    try:
        result = subprocess.run(['tsp', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"TSDuck found: {result.stdout.strip()}")
            return True
        else:
            print("TSDuck not found in PATH")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("TSDuck not found in PATH")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'PyQt6',
        'numpy',
        'matplotlib',
        'psutil',
        'requests',
        'pyqtgraph',
        'qdarkstyle'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PyQt6':
                import PyQt6
            elif package == 'numpy':
                import numpy
            elif package == 'matplotlib':
                import matplotlib
            elif package == 'psutil':
                import psutil
            elif package == 'requests':
                import requests
            elif package == 'pyqtgraph':
                import pyqtgraph
            elif package == 'qdarkstyle':
                import qdarkstyle
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    return True

def check_tsduck_python_bindings():
    """Check if TSDuck Python bindings are available"""
    try:
        import tsduck
        print("✓ TSDuck Python bindings available")
        return True
    except ImportError:
        print("⚠ TSDuck Python bindings not available (will use subprocess mode)")
        return False

def install_dependencies():
    """Install missing dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def main():
    """Main launcher function"""
    print("TSDuck GUI Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check TSDuck
    tsduck_available = check_tsduck()
    if not tsduck_available:
        print("\nTSDuck is required but not found.")
        print("Please install TSDuck:")
        print("  macOS: brew install tsduck")
        print("  Windows: winget install tsduck")
        print("  Linux: sudo apt-get install tsduck")
        sys.exit(1)
    
    # Check dependencies
    print("\nChecking dependencies...")
    if not check_dependencies():
        print("\nSome dependencies are missing.")
        response = input("Would you like to install them now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            if not install_dependencies():
                sys.exit(1)
        else:
            print("Please install dependencies manually: pip install -r requirements.txt")
            sys.exit(1)
    
    # Check TSDuck Python bindings
    print("\nChecking TSDuck Python bindings...")
    check_tsduck_python_bindings()
    
    # Launch application
    print("\nLaunching TSDuck GUI...")
    try:
        from tsduck_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
