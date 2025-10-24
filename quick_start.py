#!/usr/bin/env python3
"""
Quick Start Script for TSDuck GUI
Easy setup for distributor streaming
"""

import sys
import os
import subprocess
import json

def check_tsduck():
    """Check if TSDuck is installed"""
    try:
        # Try with full path first
        result = subprocess.run(['/usr/local/bin/tsp', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ TSDuck found: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    try:
        # Try with tsp in PATH
        result = subprocess.run(['tsp', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ TSDuck found: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ TSDuck not found")
    return False

def check_dependencies():
    """Check Python dependencies"""
    required_packages = ['PyQt6', 'numpy', 'matplotlib', 'psutil', 'requests', 'pyqtgraph', 'qdarkstyle']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing.append(package)
    
    return missing

def install_dependencies(missing):
    """Install missing dependencies"""
    if missing:
        print(f"\nInstalling missing packages: {', '.join(missing)}")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing, check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    return True

def create_sample_config():
    """Create sample configuration file"""
    config = {
        "input": {
            "type": "hls",
            "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
            "params": "--url https://cdn.itassist.one/BREAKING/NEWS/index.m3u8"
        },
        "output": {
            "type": "srt",
            "source": "srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish",
            "params": "--remote-address cdn.itassist.one --remote-port 8888 --streamid '#!::r=scte/scte,m=publish' --latency 2000"
        },
        "scte35": {
            "data_pid": 500,
            "null_pid": 8191,
            "event_id": 100023,
            "ad_duration": 600,
            "preroll_duration": 0
        }
    }
    
    try:
        with open('distributor_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Sample configuration created: distributor_config.json")
        return True
    except Exception as e:
        print(f"❌ Failed to create configuration: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 TSDuck GUI - Quick Start Setup")
    print("=" * 50)
    
    # Check TSDuck
    print("\n1. Checking TSDuck installation...")
    if not check_tsduck():
        print("\nPlease install TSDuck:")
        print("  macOS: brew install tsduck")
        print("  Windows: winget install tsduck")
        print("  Linux: sudo apt-get install tsduck")
        return False
    
    # Check dependencies
    print("\n2. Checking Python dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n3. Installing missing dependencies...")
        if not install_dependencies(missing):
            return False
    
    # Create configuration
    print("\n4. Creating sample configuration...")
    create_sample_config()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete! You can now run:")
    print("   python3 launch_distributor.py  # For distributor configuration")
    print("   python3 tsduck_gui.py          # For standard GUI")
    print("   python3 test_gui.py            # To run tests")
    print("\n🎯 Your distributor configuration is ready!")
    print("   Input: HLS stream from cdn.itassist.one")
    print("   Output: SRT stream to cdn.itassist.one:8888")
    print("   SCTE-35: PID 500, Event ID 100023")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
