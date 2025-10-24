#!/usr/bin/env python3
"""
Test SRT connection with different parameters to find working configuration
"""

import subprocess
import time
import json

def test_srt_connection():
    """Test SRT connection with various parameters"""
    
    print("🔍 Testing SRT Connection Parameters")
    print("=" * 50)
    
    # Load configuration
    with open('distributor_config.json', 'r') as f:
        config = json.load(f)
    
    # Different SRT connection attempts
    srt_tests = [
        {
            "name": "Basic SRT with streamid",
            "command": [
                'tsp', '-I', 'hls', config['input']['source'],
                '-O', 'srt', '--caller', 'cdn.itassist.one:8888',
                '--streamid', '#!::r=scte/scte,m=publish',
                '--latency', '2000'
            ]
        },
        {
            "name": "SRT with different latency",
            "command": [
                'tsp', '-I', 'hls', config['input']['source'],
                '-O', 'srt', '--caller', 'cdn.itassist.one:8888',
                '--streamid', '#!::r=scte/scte,m=publish',
                '--latency', '4000'
            ]
        },
        {
            "name": "SRT without streamid",
            "command": [
                'tsp', '-I', 'hls', config['input']['source'],
                '-O', 'srt', '--caller', 'cdn.itassist.one:8888',
                '--latency', '2000'
            ]
        },
        {
            "name": "SRT with different streamid format",
            "command": [
                'tsp', '-I', 'hls', config['input']['source'],
                '-O', 'srt', '--caller', 'cdn.itassist.one:8888',
                '--streamid', 'scte/scte',
                '--latency', '2000'
            ]
        },
        {
            "name": "SRT with listener mode",
            "command": [
                'tsp', '-I', 'hls', config['input']['source'],
                '-O', 'srt', '--listener', 'cdn.itassist.one:8888',
                '--streamid', '#!::r=scte/scte,m=publish',
                '--latency', '2000'
            ]
        }
    ]
    
    for i, test in enumerate(srt_tests, 1):
        print(f"\n🧪 Test {i}: {test['name']}")
        print(f"Command: {' '.join(test['command'])}")
        
        try:
            # Run test for 10 seconds
            process = subprocess.Popen(
                test['command'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for 10 seconds
            time.sleep(10)
            
            # Check if process is still running
            if process.poll() is None:
                print("✅ Connection successful - process still running")
                process.terminate()
                process.wait()
                return test['command']
            else:
                # Process terminated, get error
                stdout, stderr = process.communicate()
                print(f"❌ Connection failed: {stderr.strip()}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n❌ All SRT connection tests failed")
    return None

def test_srt_with_scte35():
    """Test SRT with SCTE-35 injection"""
    
    print("\n🎬 Testing SRT with SCTE-35 Injection")
    print("=" * 50)
    
    # Load configuration
    with open('distributor_config.json', 'r') as f:
        config = json.load(f)
    
    # Test SRT with SCTE-35
    command = [
        'tsp', '-I', 'hls', config['input']['source'],
        '-P', 'spliceinject',
        '--pid', str(config['scte35']['data_pid']),
        '--pts-pid', '256',
        '--files', 'scte35_commands/*.xml',
        '--delete-files',
        '--inject-count', '2',
        '--inject-interval', '800',
        '-O', 'srt', '--caller', 'cdn.itassist.one:8888',
        '--streamid', '#!::r=scte/scte,m=publish',
        '--latency', '2000'
    ]
    
    print(f"Command: {' '.join(command)}")
    
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for 15 seconds
        time.sleep(15)
        
        if process.poll() is None:
            print("✅ SRT with SCTE-35 successful!")
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ SRT with SCTE-35 failed: {stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 SRT Connection Testing")
    print("=" * 50)
    
    # Test basic SRT connection
    working_command = test_srt_connection()
    
    if working_command:
        print(f"\n🎉 Found working SRT configuration!")
        print(f"Working command: {' '.join(working_command)}")
        
        # Test with SCTE-35
        if test_srt_with_scte35():
            print("\n🎉 SRT with SCTE-35 is working!")
            print("Your pipeline is ready: HLS → SCTE-35 → SRT")
        else:
            print("\n⚠️  SRT works but SCTE-35 injection needs adjustment")
    else:
        print("\n❌ SRT connection failed with all tested parameters")
        print("Recommendation: Use UDP output as fallback")

if __name__ == "__main__":
    main()
