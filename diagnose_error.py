#!/usr/bin/env python3
"""
Error Code 1 Diagnostic Tool for IBE-100
Helps identify the specific cause of exit code 1 errors
"""

import subprocess
import sys
import os
import json

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_result(title, status, details=""):
    """Print a diagnostic result"""
    icon = "✅" if status else "❌"
    print(f"{icon} {title}")
    if details:
        for line in details.split('\n'):
            print(f"   {line}")
    return status

def check_tsduck_in_path():
    """Check if tsp is accessible in PATH"""
    print_header("Checking TSDuck in PATH")
    
    try:
        result = subprocess.run(
            ["tsp", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print_result("TSDuck accessible", True, result.stdout.strip())
            return True
        else:
            print_result("TSDuck accessible", False, f"Exit code: {result.returncode}")
            return False
            
    except FileNotFoundError:
        print_result(
            "TSDuck accessible",
            False,
            "TSDuck not found in PATH. Try:\n"
            "  Windows: set PATH=%PATH%;C:\\Program Files\\TSDuck\\bin\n"
            "  Linux: export PATH=$PATH:/usr/local/bin\n"
            "  macOS: export PATH=$PATH:/usr/local/bin"
        )
        return False
    except Exception as e:
        print_result("TSDuck check", False, str(e))
        return False

def test_tsduck_command():
    """Test a simple TSDuck command"""
    print_header("Testing TSDuck Execution")
    
    # Try a simple test command
    try:
        result = subprocess.run(
            ["tsp", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print_result("TSDuck executes successfully", True, "")
            return True
        else:
            print_result("TSDuck executes successfully", False, f"Exit code: {result.returncode}")
            return False
            
    except Exception as e:
        print_result("TSDuck execution", False, str(e))
        return False

def check_input_source(config_path="gui_working_config.json"):
    """Check if input source configuration exists and is valid"""
    print_header("Checking Input Source Configuration")
    
    if not os.path.exists(config_path):
        print_result(
            "Configuration file",
            False,
            f"Config file not found: {config_path}"
        )
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print_result("Configuration file", True, f"Found: {config_path}")
        
        # Check for input source
        input_type = config.get('input_type', 'unknown')
        input_source = config.get('input_source', '')
        
        print_result(
            f"Input type: {input_type}",
            bool(input_source),
            f"Source: {input_source[:50]}..." if input_source else "No source configured"
        )
        
        return bool(input_source)
        
    except Exception as e:
        print_result("Config parsing", False, str(e))
        return False

def check_scte35_markers():
    """Check for SCTE-35 marker files"""
    print_header("Checking SCTE-35 Markers")
    
    scte35_folder = "scte35_final"
    
    if os.path.exists(scte35_folder):
        print_result("SCTE-35 folder exists", True, f"Folder: {scte35_folder}")
        
        xml_files = [f for f in os.listdir(scte35_folder) if f.endswith('.xml')]
        print_result(
            "Marker files available",
            len(xml_files) > 0,
            f"Found {len(xml_files)} XML markers"
        )
        
        if xml_files:
            # Check if files are readable
            first_marker = os.path.join(scte35_folder, xml_files[0])
            try:
                with open(first_marker, 'r') as f:
                    content = f.read(100)
                print_result("Markers are readable", True, "")
                return True
            except Exception as e:
                print_result("Markers are readable", False, str(e))
                return False
        
        return True
    else:
        print_result(
            "SCTE-35 folder exists",
            False,
            f"Folder not found: {scte35_folder}\n"
            "   Markers will be created on first use."
        )
        return True  # Not critical

def check_network_connectivity():
    """Test network connectivity"""
    print_header("Checking Network Connectivity")
    
    import socket
    
    # Test basic connectivity
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print_result("Internet connectivity", True, "Can reach internet")
    except Exception:
        print_result("Internet connectivity", False, "No internet connection")
        return False
    
    # Test DNS
    try:
        socket.gethostbyname("google.com")
        print_result("DNS resolution", True, "DNS working")
    except socket.gaierror:
        print_result("DNS resolution", False, "DNS not working")
        return False
    
    return True

def check_output_config(config_path="gui_working_config.json"):
    """Check output configuration"""
    print_header("Checking Output Configuration")
    
    if not os.path.exists(config_path):
        print_result("Config file exists", False, config_path)
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        output_type = config.get('output_type', 'unknown')
        print_result(
            "Output type configured",
            True,
            f"Type: {output_type}"
        )
        
        # Check specific output settings
        if output_type == 'srt':
            srt_host = config.get('output_srt_host', '')
            srt_port = config.get('output_srt_port', '')
            print_result(
                "SRT destination",
                bool(srt_host and srt_port),
                f"Host: {srt_host}, Port: {srt_port}" if srt_host and srt_port else "Not configured"
            )
        elif output_type == 'udp':
            udp_host = config.get('output_udp_host', '')
            udp_port = config.get('output_udp_port', '')
            print_result(
                "UDP destination",
                bool(udp_host and udp_port),
                f"Host: {udp_host}, Port: {udp_port}" if udp_host and udp_port else "Not configured"
            )
        
        return True
        
    except Exception as e:
        print_result("Config check", False, str(e))
        return False

def provide_solutions():
    """Provide specific solutions based on common issues"""
    print_header("Common Solutions for Error Code 1")
    
    solutions = """
1. TSDuck Installation Issues:
   - Verify: tsp --version
   - If not found, add to PATH:
     Windows: set PATH=%PATH%;C:\\Program Files\\TSDuck\\bin
     Linux:   export PATH=$PATH:/usr/local/bin
     macOS:   export PATH=$PATH:/usr/local/bin

2. Missing scte35_final Folder:
   - The app will create this automatically
   - Or create manually: mkdir scte35_final

3. Network Issues:
   - Check input source URL is accessible
   - Test with: curl -I https://your-source/index.m3u8
   - Check firewall settings

4. SRT Connection Issues:
   - Verify SRT server is running and accessible
   - Check SRT server accepts connections
   - Verify streamid format if required

5. Permissions Issues:
   - Ensure write permissions in current directory
   - Check network permissions for SRT/UDP output

6. Configuration Issues:
   - Check config file exists: gui_working_config.json
   - Verify all required fields are set
   - Review input/output settings

7. Missing Dependencies:
   - Windows: Install Visual C++ Redistributable
   - Linux: Install required libraries
   - macOS: Install Xcode Command Line Tools

8. Check Console Output:
   - Look at the actual error message in IBE-100 console
   - Error messages provide specific guidance
   - Common: "tsp: command not found", "Connection refused", etc.
"""
    
    print(solutions)

def main():
    """Main diagnostic function"""
    print("=" * 70)
    print("  IBE-100 Error Code 1 Diagnostic Tool")
    print("  ITAssist Broadcast Encoder - 100")
    print("=" * 70)
    
    results = []
    
    # Run diagnostics
    try:
        results.append(("TSDuck in PATH", check_tsduck_in_path()))
    except Exception as e:
        print(f"Error: {e}")
        results.append(("TSDuck in PATH", False))
    
    try:
        results.append(("TSDuck execution", test_tsduck_command()))
    except Exception as e:
        print(f"Error: {e}")
        results.append(("TSDuck execution", False))
    
    try:
        results.append(("Input configuration", check_input_source()))
    except Exception as e:
        print(f"Error: {e}")
        results.append(("Input configuration", False))
    
    try:
        results.append(("SCTE-35 markers", check_scte35_markers()))
    except Exception as e:
        print(f"Error: {e}")
        results.append(("SCTE-35 markers", False))
    
    try:
        results.append(("Network connectivity", check_network_connectivity()))
    except Exception as e:
        print(f"Error: {e}")
        results.append(("Network connectivity", False))
    
    try:
        results.append(("Output configuration", check_output_config()))
    except Exception as e:
        print(f"Error: {e}")
        results.append(("Output configuration", False))
    
    # Summary
    print_header("Diagnostic Summary")
    
    critical_issues = []
    warnings = []
    
    for check_name, result in results:
        if not result:
            critical_issues.append(check_name)
            print(f"❌ {check_name}: FAILED")
        else:
            print(f"✅ {check_name}: OK")
    
    print("\n" + "=" * 70)
    
    if critical_issues:
        print(f"\n❌ Found {len(critical_issues)} critical issue(s):")
        for issue in critical_issues:
            print(f"   - {issue}")
        
        provide_solutions()
        print("\n💡 Next Steps:")
        print("   1. Address the critical issues listed above")
        print("   2. Re-run this diagnostic tool after fixes")
        print("   3. Check IBE-100 console for specific error messages")
        
        return 1
    else:
        print("\n✅ All basic checks passed!")
        print("\n💡 If you still get error code 1, check:")
        print("   - The exact error message in IBE-100 console")
        print("   - Try running the TSDuck command manually")
        print("   - Check network connectivity to input/output")
        
        provide_solutions()
        return 0

if __name__ == "__main__":
    sys.exit(main())

