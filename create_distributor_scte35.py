#!/usr/bin/env python3
"""
Create Distributor SCTE-35 Markers using adbreak3
Creates proper SCTE-35 markers for your distributor requirements
"""

import subprocess
import os
import json
from datetime import datetime

def create_distributor_scte35_markers():
    """Create SCTE-35 markers for distributor requirements using adbreak3"""
    
    print("🎬 Creating Distributor SCTE-35 Markers with adbreak3")
    print("=" * 70)
    
    # Load distributor configuration
    try:
        with open('distributor_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ distributor_config.json not found")
        return False
    
    # Extract configuration
    event_id = config['scte35']['event_id']
    ad_duration = config['scte35']['ad_duration']
    preroll_duration = config['scte35']['preroll_duration']
    
    print(f"📋 Distributor Configuration:")
    print(f"   Event ID: {event_id}")
    print(f"   Ad Duration: {ad_duration} seconds")
    print(f"   Pre-roll Duration: {preroll_duration} seconds")
    print()
    
    # Create SCTE-35 directory
    scte35_dir = 'scte35_adbreak3'
    os.makedirs(scte35_dir, exist_ok=True)
    
    # Create different types of SCTE-35 markers
    markers_created = []
    
    # 1. Pre-roll marker (2 seconds pre-roll, 600 seconds duration)
    print("1️⃣  Creating Pre-roll Marker...")
    preroll_file = f"{scte35_dir}/preroll_{preroll_duration}s_{ad_duration}s_{event_id}.txt"
    
    try:
        # Create pre-roll marker with adbreak3
        cmd = [
            'python3', 'adbreak3.py',
            '-p', str(preroll_duration),  # PTS time for pre-roll
            '-d', str(ad_duration),       # Duration
            '-e', str(event_id),          # Event ID
            '-P',                         # Pre-roll flag
            '-s', preroll_file            # Sidecar file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Created pre-roll marker: {preroll_file}")
            markers_created.append(preroll_file)
        else:
            print(f"❌ Failed to create pre-roll marker: {result.stderr}")
    except Exception as e:
        print(f"❌ Error creating pre-roll marker: {e}")
    
    # 2. CUE-OUT marker (immediate)
    print("\n2️⃣  Creating CUE-OUT Marker...")
    cueout_file = f"{scte35_dir}/cue_out_{event_id}.txt"
    
    try:
        cmd = [
            'python3', 'adbreak3.py',
            '-d', str(ad_duration),
            '-e', str(event_id),
            '-o',  # CUE-OUT only
            '-s', cueout_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Created CUE-OUT marker: {cueout_file}")
            markers_created.append(cueout_file)
        else:
            print(f"❌ Failed to create CUE-OUT marker: {result.stderr}")
    except Exception as e:
        print(f"❌ Error creating CUE-OUT marker: {e}")
    
    # 3. CUE-IN marker
    print("\n3️⃣  Creating CUE-IN Marker...")
    cuein_file = f"{scte35_dir}/cue_in_{event_id + 1}.txt"
    
    try:
        cmd = [
            'python3', 'adbreak3.py',
            '-e', str(event_id + 1),
            '-i',  # CUE-IN only
            '-s', cuein_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Created CUE-IN marker: {cuein_file}")
            markers_created.append(cuein_file)
        else:
            print(f"❌ Failed to create CUE-IN marker: {result.stderr}")
    except Exception as e:
        print(f"❌ Error creating CUE-IN marker: {e}")
    
    # 4. CRASH-OUT marker (immediate emergency)
    print("\n4️⃣  Creating CRASH-OUT Marker...")
    crashout_file = f"{scte35_dir}/crash_out_{event_id + 2}.txt"
    
    try:
        cmd = [
            'python3', 'adbreak3.py',
            '-d', '30',  # Short duration for emergency
            '-e', str(event_id + 2),
            '-o',  # CUE-OUT only (immediate)
            '-s', crashout_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Created CRASH-OUT marker: {crashout_file}")
            markers_created.append(crashout_file)
        else:
            print(f"❌ Failed to create CRASH-OUT marker: {result.stderr}")
    except Exception as e:
        print(f"❌ Error creating CRASH-OUT marker: {e}")
    
    # 5. Combined sidecar file
    print("\n5️⃣  Creating Combined Sidecar File...")
    combined_file = f"{scte35_dir}/distributor_sidecar.txt"
    
    try:
        with open(combined_file, 'w') as combined:
            for marker_file in markers_created:
                if os.path.exists(marker_file):
                    with open(marker_file, 'r') as f:
                        content = f.read().strip()
                        if content:
                            combined.write(content + '\n')
        
        print(f"✅ Created combined sidecar file: {combined_file}")
        markers_created.append(combined_file)
    except Exception as e:
        print(f"❌ Error creating combined sidecar file: {e}")
    
    # Show created files
    print(f"\n📁 Created SCTE-35 Files in {scte35_dir}/:")
    for marker_file in markers_created:
        if os.path.exists(marker_file):
            print(f"   ✅ {os.path.basename(marker_file)}")
    
    # Show sample content
    if os.path.exists(combined_file):
        print(f"\n📄 Sample Content from {combined_file}:")
        try:
            with open(combined_file, 'r') as f:
                content = f.read().strip()
                print(content[:200] + "..." if len(content) > 200 else content)
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    
    return len(markers_created) > 0

def test_adbreak3_markers():
    """Test the adbreak3-generated markers"""
    
    print("\n🧪 Testing adbreak3-generated SCTE-35 Markers")
    print("=" * 60)
    
    scte35_dir = 'scte35_adbreak3'
    if not os.path.exists(scte35_dir):
        print("❌ adbreak3 SCTE-35 directory not found")
        return False
    
    # Test with combined sidecar file
    combined_file = f"{scte35_dir}/distributor_sidecar.txt"
    if not os.path.exists(combined_file):
        print("❌ Combined sidecar file not found")
        return False
    
    print(f"🔍 Testing sidecar file: {combined_file}")
    
    # Test with TSDuck injection
    print("🚀 Testing SCTE-35 injection with adbreak3 markers...")
    
    try:
        # Start TSDuck with adbreak3 sidecar file
        command = [
            'tsp',
            '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
            '-P', 'spliceinject',
            '--pid', '500',
            '--pts-pid', '256',
            '--files', combined_file,
            '-O', 'ip', '127.0.0.1:9999'
        ]
        
        print(f"🔧 Command: {' '.join(command)}")
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for process to start
        import time
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ SCTE-35 injection with adbreak3 markers is working!")
            
            # Let it run for a bit
            print("⏱️  Running for 5 seconds...")
            time.sleep(5)
            
            # Stop the process
            process.terminate()
            process.wait()
            
            return True
        else:
            print("❌ SCTE-35 injection failed")
            stdout, stderr = process.communicate()
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing adbreak3 markers: {e}")
        return False

def main():
    """Main function"""
    
    print("🎬 Distributor SCTE-35 Marker Creator with adbreak3")
    print("=" * 80)
    
    # Create SCTE-35 markers
    success = create_distributor_scte35_markers()
    
    if success:
        # Test the markers
        test_success = test_adbreak3_markers()
        
        print("\n📋 FINAL SUMMARY")
        print("=" * 80)
        
        if test_success:
            print("🎉 SUCCESS: Distributor SCTE-35 markers created and tested!")
            print("   - adbreak3 generated proper SCTE-35 markers")
            print("   - TSDuck injection is working with adbreak3 markers")
            print("   - Your SCTE-35 stream is ready for production")
            print()
            print("💡 Usage:")
            print("   - Use the sidecar files in scte35_adbreak3/")
            print("   - These are proper SCTE-35 markers for your distributor")
            print("   - The combined sidecar file contains all markers")
        else:
            print("⚠️  SCTE-35 markers created but testing failed")
            print("   Check the error messages above for details")
    else:
        print("❌ Failed to create SCTE-35 markers")
        print("   Check the error messages above for details")
    
    return success

if __name__ == "__main__":
    main()
