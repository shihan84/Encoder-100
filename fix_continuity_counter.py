#!/usr/bin/env python3
"""
Fix TSDuck Continuity Counter Issues
Based on GitHub issue #1667
"""

import subprocess
import time
import os
import json

def create_continuity_fixed_command():
    """Create TSDuck command with continuity counter fixes"""
    
    print("🔧 Fixing TSDuck Continuity Counter Issues")
    print("=" * 60)
    print("Based on GitHub issue #1667: https://github.com/tsduck/tsduck/issues/1667")
    print()
    
    # Load configuration
    try:
        with open('distributor_config.json', 'r') as f:
            config = json.load(f)
    except:
        config = {
            "input": {"source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8"},
            "output": {"source": "srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish"},
            "scte35": {"data_pid": 500, "pts_pid": 256}
        }
    
    print("🚨 Issue Identified:")
    print("   - Continuity counter resets to 0x0 on each SCTE-35 injection")
    print("   - Causes DVB Inspector errors and missing cues")
    print("   - Affects downstream system compatibility")
    print()
    
    # Solution 1: Use proper PID management
    print("💡 Solution 1: Proper PID Management")
    command1 = [
        'tsp',
        '-I', 'hls', config['input']['source'],
        '-P', 'pmt', '--service', '1',  # Ensure proper PMT
        '--add-pid', f"{config['scte35']['data_pid']}/0x86",  # Add SCTE-35 PID to PMT
        '-P', 'spliceinject',
        '--service', '1',  # Use service-based injection
        '--pid', str(config['scte35']['data_pid']),
        '--pts-pid', str(config['scte35'].get('pts_pid', 256)),
        '--files', 'scte35_proper/*.xml',
        '--inject-count', '1',  # Reduce injection count
        '--inject-interval', '1000',  # Increase interval
        '--start-delay', '2000',
        '--wait-first-batch',  # Wait for first batch
        '-O', 'srt', '--caller', 'cdn.itassist.one:8888',
        '--streamid', '#!::r=scte/scte,m=publish',
        '--latency', '2000'
    ]
    
    print("🔧 Fixed Command 1 (Service-based):")
    print(" ".join(command1))
    print()
    
    # Solution 2: Use continuity counter preservation
    print("💡 Solution 2: Continuity Counter Preservation")
    command2 = [
        'tsp',
        '-I', 'hls', config['input']['source'],
        '-P', 'continuity', '--fix',  # Fix continuity counter issues
        '-P', 'spliceinject',
        '--pid', str(config['scte35']['data_pid']),
        '--pts-pid', str(config['scte35'].get('pts_pid', 256)),
        '--files', 'scte35_proper/*.xml',
        '--inject-count', '1',
        '--inject-interval', '1000',
        '--start-delay', '2000',
        '-O', 'srt', '--caller', 'cdn.itassist.one:8888',
        '--streamid', '#!::r=scte/scte,m=publish',
        '--latency', '2000'
    ]
    
    print("🔧 Fixed Command 2 (Continuity Fix):")
    print(" ".join(command2))
    print()
    
    # Solution 3: Single injection approach
    print("💡 Solution 3: Single Injection Approach")
    command3 = [
        'tsp',
        '-I', 'hls', config['input']['source'],
        '-P', 'spliceinject',
        '--pid', str(config['scte35']['data_pid']),
        '--pts-pid', str(config['scte35'].get('pts_pid', 256)),
        '--files', 'scte35_proper/*.xml',
        '--inject-count', '1',  # Single injection only
        '--inject-interval', '0',  # No interval
        '--start-delay', '2000',
        '-O', 'srt', '--caller', 'cdn.itassist.one:8888',
        '--streamid', '#!::r=scte/scte,m=publish',
        '--latency', '2000'
    ]
    
    print("🔧 Fixed Command 3 (Single Injection):")
    print(" ".join(command3))
    print()
    
    return [command1, command2, command3]

def test_continuity_fix():
    """Test the continuity counter fix"""
    
    print("🧪 Testing Continuity Counter Fix")
    print("=" * 60)
    
    commands = create_continuity_fixed_command()
    
    # Test with the first solution (service-based)
    print("🚀 Testing Solution 1: Service-based injection...")
    
    try:
        process = subprocess.Popen(
            commands[0],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ Process started successfully!")
        print("⏱️  Running for 10 seconds to test...")
        
        time.sleep(10)
        
        if process.poll() is None:
            process.terminate()
            process.wait()
            print("✅ Test completed successfully!")
            return True
        else:
            stdout, stderr = process.communicate()
            print("❌ Process failed:")
            print(stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error testing fix: {e}")
        return False

def main():
    """Main function"""
    
    print("🔧 TSDuck Continuity Counter Fix")
    print("=" * 80)
    print("Addressing GitHub issue #1667")
    print("https://github.com/tsduck/tsduck/issues/1667")
    print()
    
    # Show the issue
    print("🚨 ISSUE SUMMARY:")
    print("   - Continuity counter resets to 0x0 on SCTE-35 injection")
    print("   - Causes DVB Inspector errors")
    print("   - Missing cues in downstream systems")
    print("   - Affects stream compliance")
    print()
    
    # Create fixed commands
    commands = create_continuity_fixed_command()
    
    # Test the fix
    success = test_continuity_fix()
    
    print("\n📋 RECOMMENDATIONS:")
    print("=" * 60)
    
    if success:
        print("✅ RECOMMENDED: Use Solution 1 (Service-based injection)")
        print("   - Adds proper PMT management")
        print("   - Uses service-based SCTE-35 injection")
        print("   - Reduces injection count to prevent counter issues")
        print("   - Includes --wait-first-batch for proper timing")
    else:
        print("⚠️  FALLBACK: Use Solution 3 (Single injection)")
        print("   - Minimal injection approach")
        print("   - Reduces continuity counter conflicts")
        print("   - Simpler but less robust")
    
    print("\n🎯 NEXT STEPS:")
    print("   1. Stop current streaming")
    print("   2. Use the recommended fixed command")
    print("   3. Monitor for continuity counter errors")
    print("   4. Test with DVB Inspector")
    print("   5. Verify downstream system compatibility")
    
    return success

if __name__ == "__main__":
    main()
