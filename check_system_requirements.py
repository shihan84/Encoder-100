#!/usr/bin/env python3
"""
System Requirements Checker for IBE-100
Verifies that the target system has all required dependencies before launching
"""

import subprocess
import sys
import os
import platform

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_result(check_name, status, details=""):
    """Print a check result"""
    status_icon = "✅" if status else "❌"
    status_text = "PASS" if status else "FAIL"
    print(f"{status_icon} {check_name}: {status_text}")
    if details:
        print(f"   {details}")
    return status

def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        print_result(
            f"Python {version_str}",
            True,
            "Version 3.8+ required"
        )
        return True
    else:
        print_result(
            f"Python {version_str}",
            False,
            "Version 3.8+ required"
        )
        return False

def check_tsduck():
    """Check TSDuck installation"""
    print_header("Checking TSDuck Installation")
    
    # Try to find tsp in common locations
    tsp_paths = [
        "tsp",  # In PATH
        "C:\\Program Files\\TSDuck\\bin\\tsp.exe",
        "C:\\Program Files (x86)\\TSDuck\\bin\\tsp.exe",
        "/usr/local/bin/tsp",
        "/usr/bin/tsp",
        "/opt/tsduck/bin/tsp",
    ]
    
    tsp_found = False
    tsp_version = None
    
    for tsp_path in tsp_paths:
        try:
            result = subprocess.run(
                [tsp_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                tsp_found = True
                tsp_version = result.stdout.strip()
                print_result(
                    "TSDuck installed",
                    True,
                    f"Path: {tsp_path}\n   {tsp_version}"
                )
                break
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    if not tsp_found:
        print_result(
            "TSDuck installed",
            False,
            "TSDuck not found. Please install from: https://tsduck.io/download/"
        )
        return False
    
    return True

def check_tsduck_plugins():
    """Check required TSDuck plugins"""
    print_header("Checking TSDuck Plugins")
    
    required_plugins = [
        "hls",           # HLS input
        "srt",           # SRT streaming
        "spliceinject",  # SCTE-35 injection
        "pmt",           # PMT handling
        "services",      # Service info
        "ip",            # UDP/TCP
    ]
    
    # Try to get plugin list
    try:
        result = subprocess.run(
            ["tsp", "--list-plugins"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            available_plugins = result.stdout.lower()
            all_found = True
            
            for plugin in required_plugins:
                if plugin in available_plugins:
                    print_result(f"  - {plugin} plugin", True)
                else:
                    print_result(f"  - {plugin} plugin", False, "Missing")
                    all_found = False
            
            return all_found
        else:
            print_result("Plugin list", False, "Could not retrieve plugin list")
            return False
            
    except Exception as e:
        print_result("Plugin check", False, f"Error: {str(e)}")
        return False

def check_network_connectivity():
    """Check basic network connectivity"""
    print_header("Checking Network Connectivity")
    
    # Simple network test
    test_hosts = [
        ("google.com", "Basic internet connectivity"),
    ]
    
    import socket
    
    all_ok = True
    for host, description in test_hosts:
        try:
            socket.create_connection((host, 80), timeout=3)
            print_result(description, True, f"Connection to {host} successful")
        except (socket.gaierror, OSError) as e:
            print_result(description, False, f"Could not connect to {host}")
            all_ok = False
    
    return all_ok

def check_file_permissions():
    """Check file write permissions"""
    print_header("Checking File Permissions")
    
    # Try to create a test file in current directory
    test_file = "ibe100_permission_test.tmp"
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print_result("File write permissions", True, "Can write to current directory")
        return True
    except Exception as e:
        print_result("File write permissions", False, f"Cannot write: {str(e)}")
        return False

def check_scte35_folder():
    """Check if SCTE-35 folder exists"""
    print_header("Checking SCTE-35 Configuration")
    
    scte35_folder = "scte35_final"
    
    if os.path.exists(scte35_folder):
        print_result("SCTE-35 folder exists", True, f"Found: {scte35_folder}")
        
        # Count XML files
        xml_files = [f for f in os.listdir(scte35_folder) if f.endswith('.xml')]
        print_result(
            f"SCTE-35 marker files",
            len(xml_files) > 0,
            f"Found {len(xml_files)} marker files"
        )
        return True
    else:
        print_result("SCTE-35 folder exists", False, "Not found - markers will be created on first use")
        return True  # Not critical, can be created later

def provide_recommendations():
    """Provide recommendations based on system"""
    print_header("Recommendations")
    
    system = platform.system()
    
    print("\n📋 System-Specific Installation Instructions:")
    
    if system == "Windows":
        print("""
Windows Installation:
1. Download TSDuck from: https://tsduck.io/download/tsduck/
2. Run the installer
3. Verify installation: Open Command Prompt and run 'tsp --version'
4. If not found, add TSDuck to PATH:
   - Go to System Properties > Environment Variables
   - Add C:\\Program Files\\TSDuck\\bin to PATH
""")
    elif system == "Linux":
        print("""
Linux Installation:
1. Ubuntu/Debian: sudo apt-get install tsduck
2. CentOS/RHEL: sudo yum install tsduck
3. Or build from source: https://github.com/tsduck/tsduck
4. Verify: tsp --version
""")
    elif system == "Darwin":  # macOS
        print("""
macOS Installation:
1. Install via Homebrew: brew install tsduck
2. Or build from source: https://github.com/tsduck/tsduck
3. Verify: tsp --version
""")
    
    print("\n💡 Quick Test Command:")
    print("   tsp -I file input.ts -O drop")
    
    print("\n📞 Need Help?")
    print("   support@itassist.one")
    print("   https://itassist.one")

def main():
    """Main function"""
    print("=" * 60)
    print("  IBE-100 System Requirements Checker")
    print("  ITAssist Broadcast Encoder - 100")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("TSDuck Installation", check_tsduck),
        ("TSDuck Plugins", check_tsduck_plugins),
        ("Network Connectivity", check_network_connectivity),
        ("File Permissions", check_file_permissions),
        ("SCTE-35 Configuration", check_scte35_folder),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ Error during {check_name}: {str(e)}")
            results.append((check_name, False))
    
    # Summary
    print_header("Summary")
    
    all_passed = all(result for _, result in results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ All checks passed! System is ready to run IBE-100.")
        print("=" * 60)
        return 0
    else:
        print("❌ Some checks failed. Please address the issues above.")
        print("=" * 60)
        provide_recommendations()
        return 1

if __name__ == "__main__":
    sys.exit(main())

