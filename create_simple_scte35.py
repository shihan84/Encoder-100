#!/usr/bin/env python3
"""
Create simple SCTE-35 XML files for TSDuck spliceinject plugin
"""

import os
import time

def create_simple_scte35_files():
    """Create simple SCTE-35 XML files that work with TSDuck"""
    
    # Ensure directory exists
    scte_dir = 'scte35_commands'
    if not os.path.exists(scte_dir):
        os.makedirs(scte_dir)
    
    # Create a simple splice_insert command
    # Based on TSDuck documentation, the format should be simpler
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <splice_insert>
        <splice_event_id>100023</splice_event_id>
        <splice_event_cancel_indicator>0</splice_event_cancel_indicator>
        <out_of_network_indicator>1</out_of_network_indicator>
        <program_splice_flag>1</program_splice_flag>
        <duration_flag>1</duration_flag>
        <splice_immediate_flag>0</splice_immediate_flag>
        <splice_time>
            <pts_time>{int(time.time() * 90000)}</pts_time>
        </splice_time>
        <break_duration>
            <auto_return>0</auto_return>
            <duration>54000000</duration>
        </break_duration>
        <unique_program_id>1</unique_program_id>
        <avail_num>1</avail_num>
        <avails_expected>1</avails_expected>
    </splice_insert>
</tsduck>"""
    
    filename = f"{scte_dir}/splice_insert_{int(time.time())}.xml"
    with open(filename, 'w') as f:
        f.write(xml_content)
    
    print(f"✅ Created simple SCTE-35 file: {filename}")
    return filename

def test_simple_scte35():
    """Test the simple SCTE-35 with TSDuck"""
    
    # Create the file
    xml_file = create_simple_scte35_files()
    
    # Test command
    command = [
        'tsp', '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
        '-P', 'spliceinject',
        '--pid', '500',
        '--pts-pid', '256',
        '--files', xml_file,
        '--delete-files',
        '-O', 'srt', '--caller', 'cdn.itassist.one:8888',
        '--streamid', '#!::r=scte/scte,m=publish',
        '--latency', '2000'
    ]
    
    print(f"🧪 Testing command: {' '.join(command)}")
    
    import subprocess
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait 10 seconds
        import time
        time.sleep(10)
        
        if process.poll() is None:
            print("✅ Simple SCTE-35 test successful!")
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Simple SCTE-35 test failed: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🎬 Creating Simple SCTE-35 Files")
    print("=" * 40)
    
    success = test_simple_scte35()
    
    if success:
        print("\n🎉 Simple SCTE-35 is working!")
    else:
        print("\n❌ Simple SCTE-35 test failed")
