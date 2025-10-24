#!/usr/bin/env python3
"""
SRT Input Solutions and Alternative Approaches
"""

import subprocess
import time
import os
import json
from datetime import datetime

def analyze_srt_issues():
    """Analyze SRT connection issues and provide solutions"""
    
    print("🔍 SRT Input Analysis and Solutions")
    print("=" * 80)
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📊 SRT CONNECTION ISSUES:")
    print("   ❌ SRT server rejecting connections")
    print("   ❌ ERROR:PEER - Peer rejected connection")
    print("   ❌ Connection setup failure")
    print("   ❌ Same issue as before with SRT output")
    print()
    
    print("💡 SOLUTIONS FOR SRT INPUT:")
    print()
    
    print("1️⃣  ALTERNATIVE SRT INPUT PORTS:")
    print("   ✅ Try different SRT ports (8889, 8890, etc.)")
    print("   ✅ Check if server supports multiple ports")
    print("   📝 Command: tsp -I srt --caller cdn.itassist.one:8889 ...")
    print()
    
    print("2️⃣  SRT INPUT WITH DIFFERENT PARAMETERS:")
    print("   ✅ Try without streamid")
    print("   ✅ Try with different latency settings")
    print("   ✅ Try with different SRT modes")
    print("   📝 Command: tsp -I srt --caller cdn.itassist.one:8888 --latency 2000 ...")
    print()
    
    print("3️⃣  UDP INPUT AS ALTERNATIVE:")
    print("   ✅ Use UDP input instead of SRT")
    print("   ✅ More reliable for continuous streaming")
    print("   ✅ No connection rejection issues")
    print("   📝 Command: tsp -I ip <udp_source> -P spliceinject ...")
    print()
    
    print("4️⃣  HLS INPUT WITH OPTIMIZATION:")
    print("   ✅ Use optimized HLS with large buffers")
    print("   ✅ Accept some segment drops but minimize them")
    print("   ✅ Most reliable option currently available")
    print("   📝 Command: tsp -I hls <url> --buffer-size 2000000 ...")
    print()
    
    print("5️⃣  FILE INPUT FOR TESTING:")
    print("   ✅ Use local file for testing SCTE-35 injection")
    print("   ✅ No network connection issues")
    print("   ✅ Perfect for validation")
    print("   📝 Command: tsp -I file <video.ts> -P spliceinject ...")
    print()

def create_alternative_commands():
    """Create alternative command examples"""
    
    print("🚀 ALTERNATIVE COMMAND EXAMPLES:")
    print("=" * 50)
    print()
    
    print("1️⃣  SRT INPUT - Different Port:")
    print("tsp -I srt --caller cdn.itassist.one:8889 \\")
    print("    --streamid \"#!::r=BREAKING/NEWS,m=publish\" \\")
    print("    -P pmt --service 1 --add-pid 500/0x86 \\")
    print("    -P spliceinject --service 1 \\")
    print("    --files 'scte35_final/*.xml' \\")
    print("    --inject-count 1 --inject-interval 1000 \\")
    print("    --start-delay 2000 \\")
    print("    -O ip 127.0.0.1:9999")
    print()
    
    print("2️⃣  SRT INPUT - Without StreamID:")
    print("tsp -I srt --caller cdn.itassist.one:8888 \\")
    print("    --latency 2000 \\")
    print("    -P pmt --service 1 --add-pid 500/0x86 \\")
    print("    -P spliceinject --service 1 \\")
    print("    --files 'scte35_final/*.xml' \\")
    print("    --inject-count 1 --inject-interval 1000 \\")
    print("    --start-delay 2000 \\")
    print("    -O ip 127.0.0.1:9999")
    print()
    
    print("3️⃣  HLS INPUT - Optimized (RECOMMENDED):")
    print("tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \\")
    print("    --buffer-size 2000000 \\")
    print("    -P pmt --service 1 --add-pid 500/0x86 \\")
    print("    -P spliceinject --service 1 \\")
    print("    --files 'scte35_final/*.xml' \\")
    print("    --inject-count 1 --inject-interval 1000 \\")
    print("    --start-delay 2000 \\")
    print("    --min-bitrate 2000 \\")
    print("    -O ip 127.0.0.1:9999")
    print()
    
    print("4️⃣  UDP INPUT - If Available:")
    print("tsp -I ip 239.1.1.1:1234 \\")
    print("    -P pmt --service 1 --add-pid 500/0x86 \\")
    print("    -P spliceinject --service 1 \\")
    print("    --files 'scte35_final/*.xml' \\")
    print("    --inject-count 1 --inject-interval 1000 \\")
    print("    --start-delay 2000 \\")
    print("    -O ip 127.0.0.1:9999")
    print()
    
    print("5️⃣  FILE INPUT - For Testing:")
    print("tsp -I file test_video.ts \\")
    print("    -P pmt --service 1 --add-pid 500/0x86 \\")
    print("    -P spliceinject --service 1 \\")
    print("    --files 'scte35_final/*.xml' \\")
    print("    --inject-count 1 --inject-interval 1000 \\")
    print("    --start-delay 2000 \\")
    print("    -O file output_with_scte35.ts")
    print()

def create_test_sequence():
    """Create test sequence for different inputs"""
    
    print("🧪 TEST SEQUENCE:")
    print("=" * 30)
    print()
    
    print("1️⃣  Test SRT Input - Port 8889:")
    print("tsp -I srt --caller cdn.itassist.one:8889 \\")
    print("    --streamid \"#!::r=BREAKING/NEWS,m=publish\" \\")
    print("    -P pmt --service 1 --add-pid 500/0x86 \\")
    print("    -P spliceinject --service 1 \\")
    print("    --files 'scte35_final/*.xml' \\")
    print("    --inject-count 1 --inject-interval 1000 \\")
    print("    --start-delay 2000 \\")
    print("    -P analyze -O drop")
    print()
    
    print("2️⃣  Test SRT Input - No StreamID:")
    print("tsp -I srt --caller cdn.itassist.one:8888 \\")
    print("    --latency 2000 \\")
    print("    -P pmt --service 1 --add-pid 500/0x86 \\")
    print("    -P spliceinject --service 1 \\")
    print("    --files 'scte35_final/*.xml' \\")
    print("    --inject-count 1 --inject-interval 1000 \\")
    print("    --start-delay 2000 \\")
    print("    -P analyze -O drop")
    print()
    
    print("3️⃣  Test HLS Input - Optimized:")
    print("tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \\")
    print("    --buffer-size 2000000 \\")
    print("    -P pmt --service 1 --add-pid 500/0x86 \\")
    print("    -P spliceinject --service 1 \\")
    print("    --files 'scte35_final/*.xml' \\")
    print("    --inject-count 1 --inject-interval 1000 \\")
    print("    --start-delay 2000 \\")
    print("    --min-bitrate 2000 \\")
    print("    -P analyze -O drop")
    print()

def main():
    """Main function"""
    analyze_srt_issues()
    create_alternative_commands()
    create_test_sequence()
    
    print("📋 RECOMMENDATIONS:")
    print("=" * 30)
    print("1. Try SRT input with different ports (8889, 8890)")
    print("2. Try SRT input without streamid")
    print("3. Use optimized HLS input as fallback")
    print("4. Consider UDP input if available")
    print("5. Use file input for testing")
    print("6. Contact distributor about SRT server configuration")

if __name__ == "__main__":
    main()
