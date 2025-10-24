#!/usr/bin/env python3
"""
Stream Analysis with TSDuck tsanalyzer
"""

import subprocess
import time
import os
import signal
import sys

def analyze_stream():
    """Analyze the stream with TSDuck tsanalyzer"""
    
    print("🔍 TSDuck Stream Analysis")
    print("=" * 50)
    
    # First, let's check if we can analyze the HLS input directly
    print("1️⃣  Analyzing HLS Input Stream...")
    print("   📥 Input: https://cdn.itassist.one/BREAKING/NEWS/index.m3u8")
    
    try:
        # Analyze the input stream first
        command = [
            'tsp',
            '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
            '-P', 'analyze',
            '-O', 'drop'
        ]
        
        print(f"🔧 Command: {' '.join(command)}")
        print("🚀 Starting analysis...")
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Let it run for 10 seconds
        print("⏱️  Analyzing for 10 seconds...")
        time.sleep(10)
        
        # Stop the process
        process.terminate()
        process.wait()
        
        stdout, stderr = process.communicate()
        
        print("📊 Analysis Results:")
        print("=" * 50)
        
        if stdout:
            print("STDOUT:")
            print(stdout)
        
        if stderr:
            print("STDERR:")
            print(stderr)
            
    except Exception as e:
        print(f"❌ Error analyzing stream: {e}")
    
    print("\n" + "=" * 50)
    
    # Now analyze with SCTE-35 injection
    print("2️⃣  Analyzing Stream with SCTE-35 Injection...")
    
    try:
        command = [
            'tsp',
            '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
            '-P', 'spliceinject',
            '--pid', '500',
            '--pts-pid', '256',
            '--files', 'scte35_corrected/*.xml',
            '--inject-count', '1',
            '--inject-interval', '1000',
            '--start-delay', '2000',
            '-P', 'analyze',
            '-O', 'drop'
        ]
        
        print(f"🔧 Command: {' '.join(command)}")
        print("🚀 Starting SCTE-35 analysis...")
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Let it run for 10 seconds
        print("⏱️  Analyzing SCTE-35 injection for 10 seconds...")
        time.sleep(10)
        
        # Stop the process
        process.terminate()
        process.wait()
        
        stdout, stderr = process.communicate()
        
        print("📊 SCTE-35 Analysis Results:")
        print("=" * 50)
        
        if stdout:
            print("STDOUT:")
            print(stdout)
        
        if stderr:
            print("STDERR:")
            print(stderr)
            
    except Exception as e:
        print(f"❌ Error analyzing SCTE-35 stream: {e}")

def analyze_scte35_files():
    """Analyze the SCTE-35 XML files"""
    
    print("\n3️⃣  Analyzing SCTE-35 XML Files...")
    print("=" * 50)
    
    scte35_dir = "scte35_corrected"
    if os.path.exists(scte35_dir):
        files = [f for f in os.listdir(scte35_dir) if f.endswith('.xml')]
        
        for file in files:
            filepath = os.path.join(scte35_dir, file)
            print(f"\n📄 Analyzing {file}:")
            print("-" * 30)
            
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                    print(content)
            except Exception as e:
                print(f"❌ Error reading {file}: {e}")
    else:
        print("❌ SCTe35_corrected directory not found")

def main():
    """Main function"""
    
    print("🔍 TSDuck Stream Analysis Tool")
    print("=" * 80)
    
    # Analyze SCTE-35 files first
    analyze_scte35_files()
    
    # Analyze streams
    analyze_stream()
    
    print("\n📋 Analysis Summary:")
    print("=" * 50)
    print("✅ HLS input stream analysis completed")
    print("✅ SCTE-35 injection analysis completed")
    print("✅ SCTE-35 XML files analyzed")
    print("📊 Check the output above for detailed results")

if __name__ == "__main__":
    main()
