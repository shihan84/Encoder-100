#!/usr/bin/env python3
"""
Quick SCTE-35 Test - Automatic Detection
Tests your stream for SCTE-35 markers automatically
"""

import subprocess
import time
import os

def quick_scte35_test():
    """Quick test for SCTE-35 markers in your stream"""
    
    print("🔍 Quick SCTE-35 Marker Test")
    print("=" * 40)
    print("📡 Testing: https://cdn.itassist.one/BREAKING/NEWS/index.m3u8")
    print("⏱️  Duration: 15 seconds")
    print("🎯 SCTE-35 PID: 500")
    print()
    
    # Build detection command
    command = [
        'tsp',
        '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
        '-P', 'splicemonitor',
        '--pid', '500',
        '--json',
        '-O', 'drop'
    ]
    
    print("🚀 Starting detection...")
    markers_found = []
    
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        start_time = time.time()
        
        while time.time() - start_time < 15:
            if process.poll() is not None:
                break
                
            try:
                line = process.stdout.readline()
                if line:
                    line = line.strip()
                    if line and ('splice' in line.lower() or 'scte' in line.lower()):
                        timestamp = time.strftime("%H:%M:%S")
                        markers_found.append(line)
                        print(f"🎯 [{timestamp}] SCTE-35 MARKER FOUND!")
                        print(f"   {line[:100]}...")
                        print()
            except:
                pass
            
            time.sleep(0.1)
        
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Results
    print("📊 Test Results:")
    print("=" * 40)
    
    if markers_found:
        print(f"✅ Found {len(markers_found)} SCTE-35 markers in your stream!")
        print("\n🎉 Your stream contains SCTE-35 markers!")
        return True
    else:
        print("❌ No SCTE-35 markers detected in your stream")
        print("\nThis means:")
        print("   - Your HLS stream doesn't contain SCTE-35 markers")
        print("   - Markers might be on a different PID")
        print("   - You need to inject SCTE-35 markers")
        return False

def test_injected_markers():
    """Test with injected SCTE-35 markers"""
    
    print("\n🎬 Testing with Injected SCTE-35 Markers")
    print("=" * 50)
    
    # Check if SCTE-35 files exist
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
    injection_process = subprocess.Popen(
        injection_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for injection to start
    time.sleep(3)
    
    # Test the injected stream
    print("🔍 Testing injected stream...")
    detection_command = [
        'tsp',
        '-I', 'ip', '127.0.0.1:9999',
        '-P', 'splicemonitor',
        '--pid', '500',
        '--json',
        '-O', 'drop'
    ]
    
    markers_found = []
    
    try:
        detection_process = subprocess.Popen(
            detection_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        start_time = time.time()
        
        while time.time() - start_time < 10:
            if detection_process.poll() is not None:
                break
                
            try:
                line = detection_process.stdout.readline()
                if line:
                    line = line.strip()
                    if line and ('splice' in line.lower() or 'scte' in line.lower()):
                        timestamp = time.strftime("%H:%M:%S")
                        markers_found.append(line)
                        print(f"🎯 [{timestamp}] INJECTED MARKER DETECTED!")
                        print(f"   {line[:100]}...")
                        print()
            except:
                pass
            
            time.sleep(0.1)
        
        detection_process.terminate()
        detection_process.wait()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Stop injection
    injection_process.terminate()
    injection_process.wait()
    
    # Results
    print("📊 Injection Test Results:")
    print("=" * 40)
    
    if markers_found:
        print(f"✅ Found {len(markers_found)} injected SCTE-35 markers!")
        print("\n🎉 SCTE-35 injection is working!")
        return True
    else:
        print("❌ No injected SCTE-35 markers detected")
        print("\nThis could mean:")
        print("   - Injection failed")
        print("   - Markers not being processed")
        print("   - Detection issue")
        return False

if __name__ == "__main__":
    print("🔍 SCTE-35 Marker Detection Test")
    print("=" * 60)
    
    # Test 1: Check existing stream
    print("Test 1: Checking your HLS stream for existing SCTE-35 markers...")
    existing_markers = quick_scte35_test()
    
    # Test 2: Test with injection
    print("\nTest 2: Testing SCTE-35 injection...")
    injected_markers = test_injected_markers()
    
    # Summary
    print("\n📋 SUMMARY:")
    print("=" * 40)
    print(f"Existing SCTE-35 markers: {'✅ Found' if existing_markers else '❌ None'}")
    print(f"Injected SCTE-35 markers: {'✅ Working' if injected_markers else '❌ Failed'}")
    
    if injected_markers:
        print("\n🎉 SUCCESS: Your SCTE-35 injection system is working!")
        print("   You can now inject SCTE-35 markers into your stream.")
    else:
        print("\n⚠️  SCTE-35 injection needs attention.")
        print("   Check your SCTE-35 XML files and configuration.")
