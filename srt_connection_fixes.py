#!/usr/bin/env python3
"""
SRT Connection Fixes and Alternative Configurations
Provides multiple solutions for SRT connection issues
"""

import json
import os

def create_alternative_configs():
    """Create alternative SRT configurations to try"""
    
    configs = {
        "config_1_basic": {
            "name": "Basic SRT Connection (No Stream ID)",
            "description": "Simplest SRT connection without stream ID",
            "input": {
                "type": "hls",
                "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                "params": ""
            },
            "output": {
                "type": "srt",
                "source": "srt://cdn.itassist.one:8888",
                "params": "--caller cdn.itassist.one:8888 --latency 2000"
            },
            "tsduck_command": "tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O srt --caller cdn.itassist.one:8888 --latency 2000"
        },
        
        "config_2_simple_streamid": {
            "name": "Simple Stream ID",
            "description": "SRT connection with simplified stream ID",
            "input": {
                "type": "hls",
                "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                "params": ""
            },
            "output": {
                "type": "srt",
                "source": "srt://cdn.itassist.one:8888",
                "params": "--caller cdn.itassist.one:8888 --streamid 'scte' --latency 2000"
            },
            "tsduck_command": "tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O srt --caller cdn.itassist.one:8888 --streamid 'scte' --latency 2000"
        },
        
        "config_3_live_mode": {
            "name": "Live Transmission Mode",
            "description": "SRT connection optimized for live streaming",
            "input": {
                "type": "hls",
                "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                "params": ""
            },
            "output": {
                "type": "srt",
                "source": "srt://cdn.itassist.one:8888",
                "params": "--caller cdn.itassist.one:8888 --transtype live --latency 2000"
            },
            "tsduck_command": "tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O srt --caller cdn.itassist.one:8888 --transtype live --latency 2000"
        },
        
        "config_4_high_latency": {
            "name": "High Latency Mode",
            "description": "SRT connection with higher latency for better reliability",
            "input": {
                "type": "hls",
                "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                "params": ""
            },
            "output": {
                "type": "srt",
                "source": "srt://cdn.itassist.one:8888",
                "params": "--caller cdn.itassist.one:8888 --latency 5000"
            },
            "tsduck_command": "tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O srt --caller cdn.itassist.one:8888 --latency 5000"
        },
        
        "config_5_listener_mode": {
            "name": "Listener Mode",
            "description": "SRT connection in listener mode (server connects to you)",
            "input": {
                "type": "hls",
                "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                "params": ""
            },
            "output": {
                "type": "srt",
                "source": "srt://0.0.0.0:8888",
                "params": "--listener 0.0.0.0:8888 --latency 2000"
            },
            "tsduck_command": "tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O srt --listener 0.0.0.0:8888 --latency 2000"
        },
        
        "config_6_udp_fallback": {
            "name": "UDP Fallback",
            "description": "UDP output as fallback if SRT doesn't work",
            "input": {
                "type": "hls",
                "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                "params": ""
            },
            "output": {
                "type": "udp",
                "source": "udp://cdn.itassist.one:8888",
                "params": ""
            },
            "tsduck_command": "tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O udp cdn.itassist.one:8888"
        },
        
        "config_7_tcp_fallback": {
            "name": "TCP Fallback",
            "description": "TCP output as fallback if SRT doesn't work",
            "input": {
                "type": "hls",
                "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                "params": ""
            },
            "output": {
                "type": "tcp",
                "source": "tcp://cdn.itassist.one:8888",
                "params": ""
            },
            "tsduck_command": "tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O tcp cdn.itassist.one:8888"
        },
        
        "config_8_file_output": {
            "name": "File Output (Testing)",
            "description": "Output to file for testing purposes",
            "input": {
                "type": "hls",
                "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                "params": ""
            },
            "output": {
                "type": "file",
                "source": "/tmp/test_output.ts",
                "params": ""
            },
            "tsduck_command": "tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O file /tmp/test_output.ts"
        }
    }
    
    return configs

def save_configs():
    """Save alternative configurations to files"""
    configs = create_alternative_configs()
    
    for config_id, config in configs.items():
        filename = f"{config_id}.json"
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Created {filename}: {config['name']}")
    
    # Create a master configuration file
    master_config = {
        "available_configurations": list(configs.keys()),
        "configurations": configs
    }
    
    with open("srt_alternative_configs.json", 'w') as f:
        json.dump(master_config, f, indent=2)
    
    print(f"✅ Created srt_alternative_configs.json: Master configuration file")

def create_test_script():
    """Create a script to test all configurations"""
    
    script_content = '''#!/bin/bash
# SRT Configuration Test Script
# Tests all alternative SRT configurations

echo "🚀 Testing SRT Alternative Configurations"
echo "=========================================="

configs=(
    "config_1_basic"
    "config_2_simple_streamid" 
    "config_3_live_mode"
    "config_4_high_latency"
    "config_5_listener_mode"
    "config_6_udp_fallback"
    "config_7_tcp_fallback"
    "config_8_file_output"
)

for config in "${configs[@]}"; do
    echo ""
    echo "Testing $config..."
    echo "Command: $(jq -r '.tsduck_command' ${config}.json)"
    
    # Extract the command and run it for 5 seconds
    cmd=$(jq -r '.tsduck_command' ${config}.json)
    timeout 5s $cmd &
    pid=$!
    sleep 5
    kill $pid 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ $config: SUCCESS"
    else
        echo "❌ $config: FAILED"
    fi
done

echo ""
echo "🎯 Test completed. Check the results above."
'''
    
    with open("test_srt_configs.sh", 'w') as f:
        f.write(script_content)
    
    os.chmod("test_srt_configs.sh", 0o755)
    print("✅ Created test_srt_configs.sh: Test script for all configurations")

def main():
    """Main function"""
    print("🔧 Creating SRT Alternative Configurations")
    print("=" * 50)
    
    save_configs()
    create_test_script()
    
    print("\n" + "=" * 50)
    print("📋 NEXT STEPS:")
    print("=" * 50)
    print("1. Try the basic configuration first:")
    print("   python3 launch_distributor.py")
    print("   (Use config_1_basic.json)")
    print("")
    print("2. Test all configurations:")
    print("   ./test_srt_configs.sh")
    print("")
    print("3. If SRT doesn't work, try UDP or TCP fallback:")
    print("   (Use config_6_udp_fallback.json or config_7_tcp_fallback.json)")
    print("")
    print("4. Contact your distributor to verify:")
    print("   - SRT server is running")
    print("   - Port 8888 is open")
    print("   - Stream ID format is correct")
    print("   - Authentication requirements")
    print("   - SRT version compatibility")

if __name__ == "__main__":
    main()
