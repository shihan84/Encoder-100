#!/bin/bash
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
