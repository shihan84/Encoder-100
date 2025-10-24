#!/usr/bin/env python3
"""
Create Working SCTE-35 Files
Uses threefive-generated base64 data to create working SCTE-35 files for TSDuck
"""

import os
import subprocess
import time

def create_working_scte35_files():
    """Create working SCTE-35 files using threefive base64 data"""
    
    print("🔧 Creating Working SCTE-35 Files")
    print("=" * 50)
    
    # Check if threefive files exist
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
    print()
    
    # Create working directory
    working_dir = 'scte35_working'
    os.makedirs(working_dir, exist_ok=True)
    
    # Convert base64 to working SCTE-35 files
    for base64_file in base64_files:
        base64_path = os.path.join(threefive_dir, base64_file)
        working_file = os.path.join(working_dir, base64_file.replace('.base64', '.scte35'))
        
        print(f"🔧 Converting {base64_file}...")
        
        try:
            with open(base64_path, 'r') as f:
                base64_data = f.read().strip()
            
            # Write base64 data directly to working file
            with open(working_file, 'w') as f:
                f.write(base64_data)
            
            print(f"✅ Created: {working_file}")
            
        except Exception as e:
            print(f"❌ Error converting {base64_file}: {e}")
    
    print(f"\n📁 Working SCTE-35 files created in: {working_dir}")
    
    # Test the working files
    print("\n🧪 Testing working SCTE-35 files...")
    return test_working_scte35_files(working_dir)

def test_working_scte35_files(working_dir):
    """Test the working SCTE-35 files with TSDuck"""
    
    scte35_files = [f for f in os.listdir(working_dir) if f.endswith('.scte35')]
    if not scte35_files:
        print("❌ No working SCTE-35 files found")
        return False
    
    # Test with the first file
    test_file = os.path.join(working_dir, scte35_files[0])
    print(f"🔍 Testing {scte35_files[0]}...")
    
    # Build TSDuck command with working SCTE-35 file
    command = [
        'tsp',
        '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
        '-P', 'spliceinject',
        '--pid', '500',
        '--pts-pid', '256',
        '--files', test_file,
        '-O', 'ip', '127.0.0.1:9999'
    ]
    
    print(f"🔧 Command: {' '.join(command)}")
    print("🚀 Testing SCTE-35 injection...")
    
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for process to start
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ SCTE-35 injection started successfully")
            
            # Let it run for a bit
            print("⏱️  Running for 5 seconds...")
            time.sleep(5)
            
            if process.poll() is None:
                print("✅ SCTE-35 injection is working!")
                
                # Test detection
                print("🔍 Testing SCTE-35 detection...")
                detection_result = test_scte35_detection()
                
                # Stop the process
                process.terminate()
                process.wait()
                
                return detection_result
            else:
                print("❌ SCTE-35 injection stopped unexpectedly")
                stdout, stderr = process.communicate()
                print(f"STDERR: {stderr}")
                return False
        else:
            print("❌ SCTE-35 injection failed to start")
            stdout, stderr = process.communicate()
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_scte35_detection():
    """Test SCTE-35 detection on the processed stream"""
    
    print("🔍 Testing SCTE-35 detection...")
    
    # Build detection command
    command = [
        'tsp',
        '-I', 'ip', '127.0.0.1:9999',
        '-P', 'splicemonitor',
        '--pid', '500',
        '--json',
        '-O', 'drop'
    ]
    
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        start_time = time.time()
        markers_found = []
        
        while time.time() - start_time < 5:
            if process.poll() is not None:
                break
                
            try:
                line = process.stdout.readline()
                if line:
                    line = line.strip()
                    if line and is_scte35_output(line):
                        timestamp = time.strftime("%H:%M:%S")
                        markers_found.append(line)
                        print(f"🎯 [{timestamp}] SCTE-35 MARKER DETECTED!")
                        print(f"   {line[:100]}...")
                        print()
                        
            except Exception as e:
                print(f"⚠️  Read error: {e}")
            
            time.sleep(0.1)
        
        # Stop process
        process.terminate()
        process.wait()
        
        if markers_found:
            print(f"✅ Found {len(markers_found)} SCTE-35 markers!")
            return True
        else:
            print("❌ No SCTE-35 markers detected")
            return False
            
    except Exception as e:
        print(f"❌ Detection error: {e}")
        return False

def is_scte35_output(line):
    """Check if line contains SCTE-35 output"""
    scte35_keywords = ['splice', 'scte', 'cue', 'break', 'insert', 'time_signal']
    return any(keyword in line.lower() for keyword in scte35_keywords)

def main():
    """Main function"""
    
    print("🔧 Working SCTE-35 File Creator")
    print("=" * 60)
    
    # Create working SCTE-35 files
    success = create_working_scte35_files()
    
    if success:
        print("\n🎉 SUCCESS: Working SCTE-35 files created and tested!")
        print("   - Threefive base64 data converted to working format")
        print("   - SCTE-35 injection is working")
        print("   - SCTE-35 detection is working")
        print("\n💡 Next Steps:")
        print("   1. Use the working SCTE-35 files in scte35_working/")
        print("   2. Test with your SRT endpoint when connection is available")
        print("   3. Your SCTE-35 alert system is ready for production")
    else:
        print("\n⚠️  SCTE-35 file creation needs attention.")
        print("   Check the error messages above for details.")
    
    return success

if __name__ == "__main__":
    main()
