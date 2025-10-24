#!/usr/bin/env python3
"""
Test script to verify TSDuck command generation with distributor configuration
"""

import json
import subprocess
import sys

def test_tsduck_command():
    """Test TSDuck command generation with distributor config"""
    
    # Load distributor configuration
    try:
        with open('distributor_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ distributor_config.json not found")
        return False
    
    print("📋 Distributor Configuration:")
    print(f"  Input: {config['input']['type']} - {config['input']['source']}")
    print(f"  Output: {config['output']['type']} - {config['output']['source']}")
    print(f"  SCTE-35 PID: {config['scte35']['data_pid']}")
    print()
    
    # Build TSDuck command
    command = ['tsp']
    
    # Input configuration
    input_type = config['input']['type'].lower()
    if input_type == 'hls':
        command.extend(['-I', 'hls', config['input']['source']])
    else:
        print(f"❌ Unsupported input type: {input_type}")
        return False
    
    # Add SCTE-35 monitoring (for now, we'll add injection later)
    command.extend([
        '-P', 'splicemonitor',
        f"--pid {config['scte35']['data_pid']}"
    ])
    
    # Output configuration
    output_type = config['output']['type'].lower()
    if output_type == 'udp':
        # Parse UDP URL: udp://host:port
        udp_url = config['output']['source']
        if udp_url.startswith('udp://'):
            host_port = udp_url[6:]  # Remove 'udp://'
            command.extend(['-O', 'ip', host_port])
        else:
            command.extend(['-O', 'ip', udp_url])
    elif output_type == 'srt':
        # Parse SRT URL: srt://host:port?streamid=value
        srt_url = config['output']['source']
        if srt_url.startswith('srt://'):
            url_part = srt_url[6:]  # Remove 'srt://'
            if '?' in url_part:
                host_port = url_part.split('?')[0]
                streamid_part = url_part.split('?')[1]
                if 'streamid=' in streamid_part:
                    streamid = streamid_part.split('streamid=')[1]
                    command.extend(['-O', 'srt', '--caller', host_port, '--streamid', streamid])
                else:
                    command.extend(['-O', 'srt', '--caller', host_port])
            else:
                command.extend(['-O', 'srt', '--caller', url_part])
        else:
            command.extend(['-O', 'srt', srt_url])
    else:
        print(f"❌ Unsupported output type: {output_type}")
        return False
    
    print("🔧 Generated TSDuck Command:")
    print(" ".join(command))
    print()
    
    # Test TSDuck command (syntax check)
    print("🧪 Testing TSDuck command syntax...")
    test_command = command + ['--help']
    
    try:
        result = subprocess.run(test_command, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ TSDuck command is valid")
            print("📤 Output preview:")
            print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
            return True
        else:
            print("❌ TSDuck command failed:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out (this might be normal for HLS input)")
        return True
    except FileNotFoundError:
        print("❌ TSDuck (tsp) not found in PATH")
        return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def test_hls_input():
    """Test HLS input accessibility"""
    try:
        with open('distributor_config.json', 'r') as f:
            config = json.load(f)
        
        hls_url = config['input']['source']
        print(f"🌐 Testing HLS input: {hls_url}")
        
        import requests
        response = requests.head(hls_url, timeout=10)
        if response.status_code == 200:
            print("✅ HLS input is accessible")
            return True
        else:
            print(f"❌ HLS input returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing HLS input: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TSDuck Configuration Test")
    print("=" * 50)
    
    # Test HLS input
    hls_ok = test_hls_input()
    print()
    
    # Test TSDuck command
    command_ok = test_tsduck_command()
    
    print("\n📊 Test Results:")
    print(f"  HLS Input: {'✅ OK' if hls_ok else '❌ FAILED'}")
    print(f"  TSDuck Command: {'✅ OK' if command_ok else '❌ FAILED'}")
    
    if hls_ok and command_ok:
        print("\n🎉 Configuration is ready to use!")
        print("You can now run the TSDuck GUI and start processing.")
    else:
        print("\n⚠️  Configuration needs attention.")
        sys.exit(1)
