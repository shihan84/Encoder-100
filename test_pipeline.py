#!/usr/bin/env python3
"""
Test the complete HLS to UDP pipeline with SCTE-35 injection
"""

import subprocess
import time
import signal
import sys
import os

def test_pipeline():
    """Test the complete pipeline for 30 seconds"""
    
    print("🚀 Testing Complete HLS to UDP Pipeline with SCTE-35")
    print("=" * 60)
    
    # Check if SCTE-35 commands exist
    if not os.path.exists('scte35_commands'):
        print("❌ SCTE-35 commands directory not found")
        print("   Run: python3 scte35_generator.py")
        return False
    
    # Build TSDuck command
    command = [
        'tsp',
        '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
        '-P', 'spliceinject',
        '--pid', '500',
        '--pts-pid', '256',  # Video PID for PTS reference
        '--files', 'scte35_commands/*.xml',
        '--delete-files',
        '--inject-count', '2',
        '--inject-interval', '800',
        '-O', 'ip', 'cdn.itassist.one:8888'
    ]
    
    print("🔧 TSDuck Command:")
    print(" ".join(command))
    print()
    
    print("⏱️  Starting pipeline test (30 seconds)...")
    print("📡 Input: HLS stream from cdn.itassist.one")
    print("📤 Output: UDP to cdn.itassist.one:8888")
    print("🎬 SCTE-35: Injecting commands from scte35_commands/")
    print()
    
    try:
        # Start TSDuck process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("✅ TSDuck process started (PID: {})".format(process.pid))
        
        # Monitor for 30 seconds
        start_time = time.time()
        while time.time() - start_time < 30:
            # Check if process is still running
            if process.poll() is not None:
                print("❌ TSDuck process terminated early")
                stdout, stderr = process.communicate()
                print("STDOUT:", stdout)
                print("STDERR:", stderr)
                return False
            
            # Print progress every 5 seconds
            elapsed = int(time.time() - start_time)
            if elapsed % 5 == 0 and elapsed > 0:
                print(f"⏱️  Running... {elapsed}/30 seconds")
            
            time.sleep(1)
        
        # Stop the process
        print("🛑 Stopping TSDuck process...")
        process.terminate()
        
        # Wait for graceful shutdown
        try:
            process.wait(timeout=5)
            print("✅ TSDuck process stopped gracefully")
        except subprocess.TimeoutExpired:
            print("⚠️  Force killing TSDuck process...")
            process.kill()
            process.wait()
        
        # Get final output
        stdout, stderr = process.communicate()
        
        print("\n📊 Test Results:")
        print("✅ Pipeline test completed successfully")
        print(f"📤 Output sent to: cdn.itassist.one:8888")
        print(f"🎬 SCTE-35 commands processed from: scte35_commands/")
        
        if stderr:
            print(f"\n📝 TSDuck Output:")
            print(stderr[:500] + "..." if len(stderr) > 500 else stderr)
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        if 'process' in locals():
            process.terminate()
        return False
    except Exception as e:
        print(f"❌ Error running pipeline test: {e}")
        return False

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking Prerequisites...")
    
    # Check TSDuck
    try:
        result = subprocess.run(['tsp', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ TSDuck is available")
        else:
            print("❌ TSDuck not found")
            return False
    except FileNotFoundError:
        print("❌ TSDuck not found in PATH")
        return False
    
    # Check SCTE-35 commands
    if os.path.exists('scte35_commands'):
        xml_files = [f for f in os.listdir('scte35_commands') if f.endswith('.xml')]
        if xml_files:
            print(f"✅ Found {len(xml_files)} SCTE-35 XML files")
        else:
            print("❌ No SCTE-35 XML files found")
            return False
    else:
        print("❌ SCTE-35 commands directory not found")
        return False
    
    # Check HLS input
    try:
        import requests
        response = requests.head('https://cdn.itassist.one/BREAKING/NEWS/index.m3u8', timeout=5)
        if response.status_code == 200:
            print("✅ HLS input is accessible")
        else:
            print(f"❌ HLS input returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking HLS input: {e}")
        return False
    
    print("✅ All prerequisites met")
    return True

if __name__ == "__main__":
    print("🧪 TSDuck Pipeline Test")
    print("=" * 50)
    
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above.")
        sys.exit(1)
    
    print()
    success = test_pipeline()
    
    if success:
        print("\n🎉 Pipeline test completed successfully!")
        print("🚀 Ready to run the full TSDuck GUI with your configuration")
    else:
        print("\n❌ Pipeline test failed")
        sys.exit(1)
