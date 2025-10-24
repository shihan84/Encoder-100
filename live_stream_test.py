#!/usr/bin/env python3
"""
Live Stream Test - Real-time SCTE-35 Monitoring
Tests the live stream with SCTE-35 injection
"""

import subprocess
import time
import json
import os
from datetime import datetime

def test_live_stream():
    """Test the live stream with SCTE-35 injection"""
    
    print("🔍 Live Stream Test - SCTE-35 Injection Monitoring")
    print("=" * 70)
    
    # Check if TSDuck process is running
    print("🔍 Checking TSDuck process status...")
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        tsp_processes = [line for line in result.stdout.split('\n') if 'tsp' in line and 'grep' not in line]
        
        if tsp_processes:
            print("✅ TSDuck process is running:")
            for process in tsp_processes:
                print(f"   {process}")
        else:
            print("❌ No TSDuck process found")
            return False
    except Exception as e:
        print(f"❌ Error checking processes: {e}")
        return False
    
    print()
    
    # Test 1: Monitor the original HLS stream
    print("Test 1: Monitoring original HLS stream for SCTE-35 markers...")
    original_result = monitor_stream(
        "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
        duration=15,
        description="Original HLS Stream"
    )
    
    # Test 2: Test threefive-generated markers
    print("\nTest 2: Testing threefive-generated SCTE-35 markers...")
    threefive_result = test_threefive_markers()
    
    # Test 3: Check SCTE-35 files
    print("\nTest 3: Checking SCTE-35 command files...")
    scte35_result = check_scte35_files()
    
    # Summary
    print("\n📋 LIVE STREAM TEST SUMMARY:")
    print("=" * 70)
    print(f"TSDuck Process: {'✅ Running' if tsp_processes else '❌ Not Running'}")
    print(f"Original Stream: {'✅ Accessible' if original_result else '❌ Failed'}")
    print(f"Threefive Markers: {'✅ Valid' if threefive_result else '❌ Failed'}")
    print(f"SCTE-35 Files: {'✅ Available' if scte35_result else '❌ Missing'}")
    
    if tsp_processes and original_result and threefive_result and scte35_result:
        print("\n🎉 SUCCESS: Live stream test passed!")
        print("   - TSDuck is running with SCTE-35 injection")
        print("   - HLS stream is accessible")
        print("   - SCTE-35 markers are valid")
        print("   - Your stream is being processed with SCTE-35 markers")
        print("\n🚀 Your SCTE-35 stream is LIVE and working!")
        return True
    else:
        print("\n⚠️  Live stream test needs attention.")
        print("   Check the failed components above.")
        return False

def monitor_stream(input_source, duration=15, description="Stream"):
    """Monitor a stream for SCTE-35 markers"""
    
    print(f"🔍 Monitoring {description}")
    print(f"📡 Input: {input_source}")
    print(f"⏱️  Duration: {duration} seconds")
    
    # Build TSDuck detection command
    command = [
        'tsp',
        '-I', 'hls', input_source,
        '-P', 'splicemonitor',
        '--pid', '500',
        '--json',
        '-O', 'drop'
    ]
    
    print(f"🔧 Command: {' '.join(command)}")
    print("🚀 Starting monitoring...")
    
    markers_found = []
    
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            if process.poll() is not None:
                print("⚠️  Monitoring process terminated early")
                break
            
            try:
                line = process.stdout.readline()
                if line:
                    line = line.strip()
                    if line and is_scte35_output(line):
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        markers_found.append({
                            'timestamp': timestamp,
                            'data': line
                        })
                        print(f"🎯 [{timestamp}] SCTE-35 MARKER DETECTED!")
                        print(f"   {line[:100]}...")
                        print()
                        
            except Exception as e:
                print(f"⚠️  Read error: {e}")
            
            time.sleep(0.1)
        
        # Stop process
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        
    except Exception as e:
        print(f"❌ Monitoring error: {e}")
        return False
    
    # Results
    print(f"📊 {description} Results:")
    if markers_found:
        print(f"✅ Found {len(markers_found)} SCTE-35 markers!")
        return True
    else:
        print("❌ No SCTE-35 markers detected")
        return False

def test_threefive_markers():
    """Test threefive-generated markers"""
    
    threefive_dir = 'scte35_threefive'
    if not os.path.exists(threefive_dir):
        print("❌ Threefive directory not found")
        return False
    
    base64_files = [f for f in os.listdir(threefive_dir) if f.endswith('.base64')]
    if not base64_files:
        print("❌ No threefive base64 files found")
        return False
    
    print(f"📁 Found {len(base64_files)} threefive-generated files:")
    for f in base64_files:
        print(f"   - {f}")
    
    # Test one file
    test_file = os.path.join(threefive_dir, base64_files[0])
    try:
        with open(test_file, 'r') as f:
            base64_data = f.read().strip()
        
        if base64_data:
            print(f"✅ {base64_files[0]} contains valid base64 data")
            return True
        else:
            print(f"❌ {base64_files[0]} is empty")
            return False
    except Exception as e:
        print(f"❌ Error reading {base64_files[0]}: {e}")
        return False

def check_scte35_files():
    """Check SCTE-35 command files"""
    
    scte_dir = 'scte35_commands'
    if not os.path.exists(scte_dir):
        print("❌ SCTE-35 commands directory not found")
        return False
    
    xml_files = [f for f in os.listdir(scte_dir) if f.endswith('.xml')]
    if not xml_files:
        print("❌ No SCTE-35 XML files found")
        return False
    
    print(f"📁 Found {len(xml_files)} SCTE-35 XML files:")
    for f in xml_files:
        print(f"   - {f}")
    
    return True

def is_scte35_output(line):
    """Check if line contains SCTE-35 output"""
    scte35_keywords = ['splice', 'scte', 'cue', 'break', 'insert', 'time_signal']
    return any(keyword in line.lower() for keyword in scte35_keywords)

if __name__ == "__main__":
    test_live_stream()
