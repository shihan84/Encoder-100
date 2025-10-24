#!/usr/bin/env python3
"""
Start TSDuck SCTE-35 Streaming with Monitoring
"""

import subprocess
import time
import os
import signal
import sys

def start_streaming():
    """Start TSDuck SCTE-35 streaming"""
    
    print("🎬 Starting TSDuck SCTE-35 Streaming")
    print("=" * 60)
    
    # Check if SCTE-35 files exist
    scte35_dir = "scte35_proper"
    if not os.path.exists(scte35_dir):
        print(f"❌ SCTE-35 directory not found: {scte35_dir}")
        return False
    
    scte35_files = [f for f in os.listdir(scte35_dir) if f.endswith('.xml')]
    if not scte35_files:
        print(f"❌ No SCTE-35 XML files found in {scte35_dir}")
        return False
    
    print(f"✅ Found {len(scte35_files)} SCTE-35 files:")
    for file in scte35_files:
        print(f"   📄 {file}")
    
    # Build TSDuck command
    command = [
        'tsp',
        '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
        '-P', 'spliceinject',
        '--pid', '500',
        '--pts-pid', '256',
        '--files', f'{scte35_dir}/*.xml',
        '--inject-count', '2',
        '--inject-interval', '800',
        '--start-delay', '2000',
        '-O', 'srt',
        '--caller', 'cdn.itassist.one:8888',
        '--streamid', '#!::r=scte/scte,m=publish',
        '--latency', '2000'
    ]
    
    print(f"\n🚀 Starting TSDuck streaming...")
    print(f"🔧 Command: {' '.join(command)}")
    print()
    
    try:
        # Start the process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("✅ TSDuck process started!")
        print("📊 Stream Configuration:")
        print("   📥 Input: HLS stream")
        print("   🎬 Processing: SCTE-35 injection")
        print("   📤 Output: SRT stream")
        print("   🎯 SCTE-35 PID: 500")
        print("   ⏰ PTS PID: 256")
        print("   🔄 Inject Count: 2")
        print("   ⏱️  Inject Interval: 800ms")
        print("   ⏰ Start Delay: 2000ms")
        print("   🌐 SRT Server: cdn.itassist.one:8888")
        print("   🆔 Stream ID: #!::r=scte/scte,m=publish")
        print("   ⏱️  Latency: 2000ms")
        print()
        
        # Monitor the process
        print("📡 Monitoring stream...")
        print("Press Ctrl+C to stop streaming")
        print()
        
        start_time = time.time()
        
        while True:
            # Check if process is still running
            if process.poll() is not None:
                print("❌ TSDuck process stopped unexpectedly")
                stdout, stderr = process.communicate()
                if stderr:
                    print("STDERR:", stderr)
                return False
            
            # Show status every 10 seconds
            elapsed = int(time.time() - start_time)
            if elapsed % 10 == 0 and elapsed > 0:
                print(f"⏱️  Stream running for {elapsed} seconds...")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping stream...")
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
                print("✅ Stream stopped gracefully")
            except subprocess.TimeoutExpired:
                process.kill()
                print("⚠️  Stream force stopped")
        return True
        
    except Exception as e:
        print(f"❌ Error starting stream: {e}")
        if process.poll() is None:
            process.kill()
        return False

def main():
    """Main function"""
    
    print("🎬 TSDuck SCTE-35 Streaming Launcher")
    print("=" * 80)
    
    success = start_streaming()
    
    if success:
        print("\n🎉 Streaming completed successfully!")
    else:
        print("\n❌ Streaming failed or stopped unexpectedly")
        sys.exit(1)

if __name__ == "__main__":
    main()

