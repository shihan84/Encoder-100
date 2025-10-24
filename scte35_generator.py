#!/usr/bin/env python3
"""
SCTE-35 Command Generator for Distributor Requirements
Generates XML SCTE-35 splice commands for TSDuck injection
"""

import os
import time
import json
from datetime import datetime, timedelta

class SCTE35Generator:
    """Generate SCTE-35 splice commands for distributor requirements"""
    
    def __init__(self, config_file='distributor_config.json'):
        """Initialize with distributor configuration"""
        self.config = self.load_config(config_file)
        self.scte_dir = 'scte35_commands'
        self.ensure_scte_dir()
    
    def load_config(self, config_file):
        """Load distributor configuration"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Configuration file {config_file} not found")
            return None
    
    def ensure_scte_dir(self):
        """Ensure SCTE-35 commands directory exists"""
        if not os.path.exists(self.scte_dir):
            os.makedirs(self.scte_dir)
            print(f"📁 Created SCTE-35 commands directory: {self.scte_dir}")
    
    def generate_cue_out(self, event_id=None, duration=None, pts_offset=0):
        """Generate CUE-OUT (Program Out Point) command"""
        if not event_id:
            event_id = self.config['scte35']['event_id']
        if not duration:
            duration = self.config['scte35']['ad_duration']
        
        # Calculate PTS (90kHz clock)
        pts_time = int(time.time() * 90000) + pts_offset
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <splice_insert>
        <splice_event_id>{event_id}</splice_event_id>
        <splice_event_cancel_indicator>0</splice_event_cancel_indicator>
        <out_of_network_indicator>1</out_of_network_indicator>
        <program_splice_flag>1</program_splice_flag>
        <duration_flag>1</duration_flag>
        <splice_immediate_flag>0</splice_immediate_flag>
        <splice_time>
            <pts_time>{pts_time}</pts_time>
        </splice_time>
        <break_duration>
            <auto_return>0</auto_return>
            <duration>{duration * 90000}</duration>
        </break_duration>
        <unique_program_id>1</unique_program_id>
        <avail_num>1</avail_num>
        <avails_expected>1</avails_expected>
    </splice_insert>
</tsduck>"""
        
        filename = f"{self.scte_dir}/cue_out_{event_id}_{int(time.time())}.xml"
        with open(filename, 'w') as f:
            f.write(xml_content)
        
        print(f"✅ Generated CUE-OUT command: {filename}")
        return filename
    
    def generate_cue_in(self, event_id=None, pts_offset=0):
        """Generate CUE-IN (Program In Point) command"""
        if not event_id:
            event_id = self.config['scte35']['event_id'] + 1
        
        # Calculate PTS (90kHz clock)
        pts_time = int(time.time() * 90000) + pts_offset
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <splice_insert>
        <splice_event_id>{event_id}</splice_event_id>
        <splice_event_cancel_indicator>0</splice_event_cancel_indicator>
        <out_of_network_indicator>0</out_of_network_indicator>
        <program_splice_flag>1</program_splice_flag>
        <splice_immediate_flag>0</splice_immediate_flag>
        <splice_time>
            <pts_time>{pts_time}</pts_time>
        </splice_time>
        <unique_program_id>1</unique_program_id>
        <avail_num>1</avail_num>
        <avails_expected>1</avails_expected>
    </splice_insert>
</tsduck>"""
        
        filename = f"{self.scte_dir}/cue_in_{event_id}_{int(time.time())}.xml"
        with open(filename, 'w') as f:
            f.write(xml_content)
        
        print(f"✅ Generated CUE-IN command: {filename}")
        return filename
    
    def generate_crash_out(self, event_id=None, pts_offset=0):
        """Generate CRASH-OUT (Emergency Program Out) command"""
        if not event_id:
            event_id = self.config['scte35']['event_id'] + 2
        
        # Calculate PTS (90kHz clock)
        pts_time = int(time.time() * 90000) + pts_offset
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <splice_insert>
        <splice_event_id>{event_id}</splice_event_id>
        <splice_event_cancel_indicator>0</splice_event_cancel_indicator>
        <out_of_network_indicator>1</out_of_network_indicator>
        <program_splice_flag>1</program_splice_flag>
        <splice_immediate_flag>1</splice_immediate_flag>
        <unique_program_id>1</unique_program_id>
        <avail_num>1</avail_num>
        <avails_expected>1</avails_expected>
    </splice_insert>
</tsduck>"""
        
        filename = f"{self.scte_dir}/crash_out_{event_id}_{int(time.time())}.xml"
        with open(filename, 'w') as f:
            f.write(xml_content)
        
        print(f"✅ Generated CRASH-OUT command: {filename}")
        return filename
    
    def generate_time_signal(self, event_id=None, pts_offset=0):
        """Generate TIME_SIGNAL command for timing reference"""
        if not event_id:
            event_id = self.config['scte35']['event_id'] + 3
        
        # Calculate PTS (90kHz clock)
        pts_time = int(time.time() * 90000) + pts_offset
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <time_signal>
        <splice_time>
            <pts_time>{pts_time}</pts_time>
        </splice_time>
    </time_signal>
</tsduck>"""
        
        filename = f"{self.scte_dir}/time_signal_{event_id}_{int(time.time())}.xml"
        with open(filename, 'w') as f:
            f.write(xml_content)
        
        print(f"✅ Generated TIME_SIGNAL command: {filename}")
        return filename
    
    def generate_all_commands(self):
        """Generate all SCTE-35 commands for testing"""
        print("🎬 Generating SCTE-35 Commands for Distributor Requirements")
        print("=" * 60)
        
        commands = []
        
        # Generate CUE-OUT (Program Out Point)
        commands.append(self.generate_cue_out())
        
        # Generate CUE-IN (Program In Point) - 10 seconds later
        commands.append(self.generate_cue_in(pts_offset=10*90000))
        
        # Generate CRASH-OUT (Emergency Program Out)
        commands.append(self.generate_crash_out(pts_offset=20*90000))
        
        # Generate TIME_SIGNAL for timing reference
        commands.append(self.generate_time_signal(pts_offset=30*90000))
        
        print(f"\n📋 Generated {len(commands)} SCTE-35 commands")
        print(f"📁 Commands saved in: {self.scte_dir}/")
        
        return commands
    
    def create_tsduck_command(self):
        """Create the complete TSDuck command with SCTE-35 injection"""
        if not self.config:
            return None
        
        command = [
            'tsp',
            '-I', 'hls', self.config['input']['source'],
            '-P', 'spliceinject',
            '--pid', str(self.config['scte35']['data_pid']),
            '--files', f'{self.scte_dir}/*.xml',
            '--delete-files',
            '--inject-count', '2',
            '--inject-interval', '800',
            '-O', 'ip', self.config['output']['source'].replace('udp://', '')
        ]
        
        return command
    
    def print_tsduck_command(self):
        """Print the complete TSDuck command"""
        command = self.create_tsduck_command()
        if command:
            print("\n🔧 Complete TSDuck Command:")
            print(" ".join(command))
            print("\n📝 Command Explanation:")
            print("  -I hls: Input from HLS stream")
            print("  -P spliceinject: Inject SCTE-35 commands")
            print("  --pid: SCTE-35 data PID")
            print("  --files: Monitor XML files in scte35_commands/")
            print("  --delete-files: Remove files after injection")
            print("  --inject-count: Inject each command 2 times")
            print("  --inject-interval: 800ms between injections")
            print("  -O ip: Output via UDP/IP")
        else:
            print("❌ Could not create TSDuck command")

def main():
    """Main function to generate SCTE-35 commands"""
    generator = SCTE35Generator()
    
    if not generator.config:
        print("❌ No configuration available")
        return
    
    print("🚀 SCTE-35 Command Generator")
    print("=" * 50)
    print(f"📋 Configuration loaded from: distributor_config.json")
    print(f"🎯 Event ID: {generator.config['scte35']['event_id']}")
    print(f"⏱️  Ad Duration: {generator.config['scte35']['ad_duration']} seconds")
    print(f"📡 SCTE-35 PID: {generator.config['scte35']['data_pid']}")
    print()
    
    # Generate all commands
    commands = generator.generate_all_commands()
    
    # Print TSDuck command
    generator.print_tsduck_command()
    
    print(f"\n🎉 SCTE-35 setup complete!")
    print(f"📁 Commands directory: {generator.scte_dir}/")
    print(f"🔧 Ready to run TSDuck with SCTE-35 injection")

if __name__ == "__main__":
    main()
