#!/usr/bin/env python3
"""
Working SCTE-35 Detector and Alert System
Properly detects SCTE-35 markers in streams
"""

import subprocess
import time
import os
from datetime import datetime

def detect_scte35_markers(input_source, duration=20, pid=500):
    """Detect SCTE-35 markers in a stream"""
    
    print(f"🔍 SCTE-35 Detection")
    print("=" * 40)
    print(f"📡 Input: {input_source}")
    print(f"⏱️  Duration: {duration} seconds")
    print(f"🎯 SCTE-35 PID: {pid}")
    print()
    
    # Determine input type
    if input_source.startswith('udp://'):
        input_type = 'ip'
        input_param = input_source.replace('udp://', '')
    elif input_source.startswith('http'):
        input_type = 'hls'
        input_param = input_source
    else:
        input_type = 'file'
        input_param = input_source
    
    # Build detection command
    command = [
        'tsp',
        '-I', input_type, input_param,
        '-P', 'splicemonitor',
        '--pid', str(pid),
        '--json',
        '-O', 'drop'
    ]
    
    print(f"🔧 Command: {' '.join(command)}")
    print("🚀 Starting detection...")
    print()
    
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
                break
                
            try:
                line = process.stdout.readline()
                if line:
                    line = line.strip()
                    if line and _is_scte35_marker(line):
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        markers_found.append({
                            'timestamp': timestamp,
                            'data': line
                        })
                        print(f"🎯 [{timestamp}] SCTE-35 MARKER DETECTED!")
                        print(f"   {line[:100]}...")
                        print()
            except:
                pass
            
            time.sleep(0.1)
        
        # Stop process
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Results
    print("📊 Detection Results:")
    print("=" * 40)
    
    if markers_found:
        print(f"✅ Found {len(markers_found)} SCTE-35 markers!")
        return True
    else:
        print("❌ No SCTE-35 markers detected")
        return False

def _is_scte35_marker(line):
    """Check if line contains SCTE-35 marker data"""
    scte35_keywords = ['splice', 'scte', 'cue', 'break', 'insert', 'time_signal']
    return any(keyword in line.lower() for keyword in scte35_keywords)

def test_scte35_injection():
    """Test SCTE-35 injection and detection"""
    
    print("🎬 SCTE-35 Injection Test")
    print("=" * 50)
    
    # Check SCTE-35 files
    scte_dir = 'scte35_commands'
    if not os.path.exists(scte_dir):
        print("❌ SCTE-35 commands directory not found")
        return False
    
    xml_files = [f for f in os.listdir(scte_dir) if f.endswith('.xml')]
    if not xml_files:
        print("❌ No SCTE-35 XML files found")
        return False
    
    print(f"📁 Found {len(xml_files)} SCTE-35 files:")
    for f in xml_files:
        print(f"   - {f}")
    print()
    
    # Start injection
    injection_command = [
        'tsp',
        '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
        '-P', 'spliceinject',
        '--pid', '500',
        '--pts-pid', '256',
        '--files', f'{scte_dir}/*.xml',
        '-O', 'ip', '127.0.0.1:9999'
    ]
    
    print("🚀 Starting SCTE-35 injection...")
    print(f"Command: {' '.join(injection_command)}")
    print()
    
    injection_process = subprocess.Popen(
        injection_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for injection to start
    time.sleep(3)
    
    # Check if injection is running
    if injection_process.poll() is None:
        print("✅ SCTE-35 injection is running")
        
        # Test detection on injected stream
        print("🔍 Testing detection on injected stream...")
        result = detect_scte35_markers("udp://127.0.0.1:9999", duration=15)
        
        # Stop injection
        injection_process.terminate()
        injection_process.wait()
        
        return result
    else:
        print("❌ SCTE-35 injection failed to start")
        stdout, stderr = injection_process.communicate()
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        return False

def main():
    """Main function"""
    
    print("🔍 Working SCTE-35 Detector and Alert System")
    print("=" * 60)
    
    # Test 1: Check original stream
    print("Test 1: Checking original HLS stream for SCTE-35 markers...")
    original_result = detect_scte35_markers(
        "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
        duration=15
    )
    
    # Test 2: Test injection
    print("\nTest 2: Testing SCTE-35 injection and detection...")
    injection_result = test_scte35_injection()
    
    # Summary
    print("\n📋 FINAL SUMMARY:")
    print("=" * 60)
    print(f"Original stream SCTE-35 markers: {'✅ Found' if original_result else '❌ None'}")
    print(f"SCTE-35 injection: {'✅ Working' if injection_result else '❌ Failed'}")
    
    if injection_result:
        print("\n🎉 SUCCESS: SCTE-35 injection and detection working!")
        print("   Your SCTE-35 alert system is ready.")
    else:
        print("\n⚠️  SCTE-35 injection needs attention.")
    
    return injection_result

if __name__ == "__main__":
    main()
