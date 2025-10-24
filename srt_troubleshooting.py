#!/usr/bin/env python3
"""
SRT Connection Troubleshooting Tool
Helps diagnose and fix SRT connection issues
"""

import subprocess
import sys
import time
import socket
from urllib.parse import urlparse

def test_srt_connection(host, port, streamid=None):
    """Test SRT connection with various parameters"""
    print(f"🔍 Testing SRT connection to {host}:{port}")
    print(f"📡 Stream ID: {streamid}")
    print("=" * 60)
    
    # Test 1: Basic connectivity
    print("\n1. Testing basic network connectivity...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            print("✅ Network connectivity: OK")
        else:
            print(f"❌ Network connectivity: FAILED (Error: {result})")
            return False
    except Exception as e:
        print(f"❌ Network connectivity: FAILED ({e})")
        return False
    
    # Test 2: SRT connection with minimal parameters
    print("\n2. Testing SRT connection with minimal parameters...")
    cmd = [
        'tsp', '-I', 'null', 
        '-O', 'srt', '--caller', f'{host}:{port}',
        '--latency', '2000'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ SRT connection (minimal): OK")
        else:
            print(f"❌ SRT connection (minimal): FAILED")
            print(f"   Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⏰ SRT connection (minimal): TIMEOUT")
    except Exception as e:
        print(f"❌ SRT connection (minimal): FAILED ({e})")
    
    # Test 3: SRT connection with stream ID
    if streamid:
        print(f"\n3. Testing SRT connection with stream ID...")
        cmd = [
            'tsp', '-I', 'null',
            '-O', 'srt', '--caller', f'{host}:{port}',
            '--streamid', streamid,
            '--latency', '2000'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ SRT connection (with stream ID): OK")
            else:
                print(f"❌ SRT connection (with stream ID): FAILED")
                print(f"   Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("⏰ SRT connection (with stream ID): TIMEOUT")
        except Exception as e:
            print(f"❌ SRT connection (with stream ID): FAILED ({e})")
    
    # Test 4: SRT connection with different latency values
    print(f"\n4. Testing SRT connection with different latency values...")
    latencies = [1000, 2000, 5000, 10000]
    
    for latency in latencies:
        print(f"   Testing latency: {latency}ms")
        cmd = [
            'tsp', '-I', 'null',
            '-O', 'srt', '--caller', f'{host}:{port}',
            '--latency', str(latency)
        ]
        
        if streamid:
            cmd.extend(['--streamid', streamid])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"   ✅ Latency {latency}ms: OK")
                break
            else:
                print(f"   ❌ Latency {latency}ms: FAILED")
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Latency {latency}ms: TIMEOUT")
        except Exception as e:
            print(f"   ❌ Latency {latency}ms: FAILED ({e})")
    
    # Test 5: SRT connection with different transmission types
    print(f"\n5. Testing SRT connection with different transmission types...")
    transtypes = ['live', 'file', 'default']
    
    for transtype in transtypes:
        print(f"   Testing transmission type: {transtype}")
        cmd = [
            'tsp', '-I', 'null',
            '-O', 'srt', '--caller', f'{host}:{port}',
            '--transtype', transtype,
            '--latency', '2000'
        ]
        
        if streamid:
            cmd.extend(['--streamid', streamid])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"   ✅ Transmission type {transtype}: OK")
                break
            else:
                print(f"   ❌ Transmission type {transtype}: FAILED")
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Transmission type {transtype}: TIMEOUT")
        except Exception as e:
            print(f"   ❌ Transmission type {transtype}: FAILED ({e})")
    
    return True

def suggest_fixes():
    """Suggest common fixes for SRT connection issues"""
    print("\n" + "=" * 60)
    print("🔧 SUGGESTED FIXES FOR SRT CONNECTION ISSUES")
    print("=" * 60)
    
    fixes = [
        "1. **Check Server Status**: Verify the SRT server is running and accepting connections",
        "2. **Firewall Settings**: Ensure port 8888 is open in firewall",
        "3. **Stream ID Format**: Verify the stream ID format matches server expectations",
        "4. **Latency Settings**: Try different latency values (1000ms, 2000ms, 5000ms)",
        "5. **Transmission Type**: Try different transmission types (live, file, default)",
        "6. **Network Path**: Check if there are network routing issues",
        "7. **SRT Version**: Ensure client and server SRT versions are compatible",
        "8. **Authentication**: Check if server requires authentication or encryption",
        "9. **Connection Mode**: Try listener mode instead of caller mode",
        "10. **Server Configuration**: Verify server is configured to accept your stream ID"
    ]
    
    for fix in fixes:
        print(fix)
    
    print("\n" + "=" * 60)
    print("🎯 RECOMMENDED COMMAND VARIATIONS TO TRY:")
    print("=" * 60)
    
    commands = [
        "# Basic connection without stream ID:",
        "tsp -I null -O srt --caller cdn.itassist.one:8888 --latency 2000",
        "",
        "# Connection with different latency:",
        "tsp -I null -O srt --caller cdn.itassist.one:8888 --latency 5000",
        "",
        "# Connection with live transmission type:",
        "tsp -I null -O srt --caller cdn.itassist.one:8888 --transtype live --latency 2000",
        "",
        "# Connection with file transmission type:",
        "tsp -I null -O srt --caller cdn.itassist.one:8888 --transtype file --latency 2000",
        "",
        "# Connection with different stream ID format:",
        "tsp -I null -O srt --caller cdn.itassist.one:8888 --streamid 'scte/scte' --latency 2000",
        "",
        "# Connection with encryption (if required):",
        "tsp -I null -O srt --caller cdn.itassist.one:8888 --passphrase 'yourpassphrase' --latency 2000"
    ]
    
    for cmd in commands:
        print(cmd)

def main():
    """Main troubleshooting function"""
    print("🚀 SRT Connection Troubleshooting Tool")
    print("=" * 60)
    
    # Parse the SRT URL
    srt_url = "srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish"
    
    try:
        parsed = urlparse(srt_url)
        host = parsed.hostname
        port = parsed.port
        streamid = parsed.query.split('streamid=')[1] if 'streamid=' in parsed.query else None
        
        print(f"📡 SRT URL: {srt_url}")
        print(f"🌐 Host: {host}")
        print(f"🔌 Port: {port}")
        print(f"🆔 Stream ID: {streamid}")
        
        # Run tests
        test_srt_connection(host, port, streamid)
        
        # Suggest fixes
        suggest_fixes()
        
    except Exception as e:
        print(f"❌ Error parsing SRT URL: {e}")
        print("Please check the SRT URL format")

if __name__ == "__main__":
    main()
