#!/usr/bin/env python3
"""
Simple SCTE-35 Marker Detector
Quick verification tool for SCTE-35 markers in streams
"""

import subprocess
import time
import json
import os

def detect_scte35_markers(input_source, duration=30):
    """Detect SCTE-35 markers in a stream"""
    
    print(f"🔍 SCTE-35 Marker Detection")
    print("=" * 40)
    print(f"📡 Input: {input_source}")
    print(f"⏱️  Duration: {duration} seconds")
    print(f"🎯 SCTE-35 PID: 500")
    print()
    
    # Build detection command
    command = [
        'tsp',
        '-I', 'hls', input_source,
        '-P', 'splicemonitor',
        '--pid', '500',
        '--json',
        '-O', 'drop'
    ]
    
    print(f"🔧 Command: {' '.join(command)}")
    print()
    
    markers_found = []
    
    try:
        print("🚀 Starting detection...")
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
                
            # Read output
            try:
                line = process.stdout.readline()
                if line:
                    line = line.strip()
                    if line and ('splice' in line.lower() or 'scte' in line.lower()):
                        timestamp = time.strftime("%H:%M:%S")
                        markers_found.append({
                            'timestamp': timestamp,
                            'data': line
                        })
                        print(f"🎯 [{timestamp}] SCTE-35 MARKER FOUND!")
                        print(f"   {line}")
                        print()
            except:
                pass
            
            time.sleep(0.1)
        
        # Stop process
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Results
    print("📊 Detection Results:")
    print("=" * 40)
    
    if markers_found:
        print(f"✅ Found {len(markers_found)} SCTE-35 markers:")
        for i, marker in enumerate(markers_found, 1):
            print(f"   {i}. [{marker['timestamp']}] {marker['data'][:100]}...")
        return True
    else:
        print("❌ No SCTE-35 markers detected")
        print("\nPossible reasons:")
        print("   - No SCTE-35 markers in stream")
        print("   - Markers on different PID")
        print("   - Stream doesn't contain SCTE-35 data")
        return False

def test_your_stream():
    """Test your specific HLS stream"""
    print("🧪 Testing Your HLS Stream for SCTE-35 Markers")
    print("=" * 60)
    
    return detect_scte35_markers(
        "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
        duration=30
    )

def test_injected_stream():
    """Test stream with injected SCTE-35 markers"""
    print("🎬 Testing Stream with Injected SCTE-35 Markers")
    print("=" * 60)
    
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
    
    # Start injection in background
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
    result = detect_scte35_markers("udp://127.0.0.1:9999", duration=20)
    
    # Stop injection
    injection_process.terminate()
    injection_process.wait()
    
    return result

if __name__ == "__main__":
    print("🔍 SCTE-35 Marker Detector")
    print("=" * 50)
    
    print("Choose test:")
    print("1. Test your HLS stream for existing SCTE-35 markers")
    print("2. Test stream with injected SCTE-35 markers")
    print("3. Both tests")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_your_stream()
    elif choice == "2":
        test_injected_stream()
    elif choice == "3":
        print("\n🧪 Running both tests...")
        print("\n" + "="*50)
        test_your_stream()
        print("\n" + "="*50)
        test_injected_stream()
    else:
        print("❌ Invalid choice")
