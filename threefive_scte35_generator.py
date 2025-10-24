#!/usr/bin/env python3
"""
Threefive SCTE-35 Generator
Uses the threefive library to generate proper SCTE-35 markers
"""

import json
import os
import time
from datetime import datetime
import threefive

class ThreefiveSCTE35Generator:
    """Generate SCTE-35 markers using threefive library"""
    
    def __init__(self, config_file='distributor_config.json', output_dir='scte35_threefive'):
        self.config_file = config_file
        self.output_dir = output_dir
        self.config = self.load_config()
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_config(self):
        """Load distributor configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.config_file} not found.")
            return self.get_default_config()
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.config_file}.")
            return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            "scte35": {
                "data_pid": 500,
                "event_id": 10021,
                "ad_duration": 600,
                "preroll_duration": 2
            }
        }
    
    def generate_cue_out(self, event_id, duration_seconds):
        """Generate a CUE-OUT marker using threefive"""
        try:
            # Create a splice_insert cue
            cue = threefive.Cue()
            cue.command = threefive.SpliceInsert()
            cue.command.splice_event_id = event_id
            cue.command.splice_event_cancel_indicator = False
            cue.command.out_of_network_indicator = True
            cue.command.splice_immediate_flag = False
            cue.command.unique_program_id = 1
            cue.command.avail_num = 1
            cue.command.avails_expected = 1
            
            # Set break duration
            cue.command.break_duration = threefive.BreakDuration()
            cue.command.break_duration.auto_return = False
            cue.command.break_duration.duration = duration_seconds * 90000  # Convert to 90kHz
            
            # Generate the cue
            cue.encode()
            
            # Save as JSON
            json_file = f"{self.output_dir}/cue_out_{event_id}.json"
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            # Save as base64
            base64_file = f"{self.output_dir}/cue_out_{event_id}.base64"
            with open(base64_file, 'w') as f:
                f.write(cue.encode())
            
            print(f"✅ Generated CUE-OUT marker:")
            print(f"   📄 JSON: {json_file}")
            print(f"   📄 Base64: {base64_file}")
            print(f"   🎯 Event ID: {event_id}")
            print(f"   ⏱️  Duration: {duration_seconds}s")
            
            return json_file, base64_file
            
        except Exception as e:
            print(f"❌ Error generating CUE-OUT: {e}")
            return None, None
    
    def generate_cue_in(self, event_id):
        """Generate a CUE-IN marker using threefive"""
        try:
            # Create a splice_insert cue
            cue = threefive.Cue()
            cue.command = threefive.SpliceInsert()
            cue.command.splice_event_id = event_id
            cue.command.splice_event_cancel_indicator = False
            cue.command.out_of_network_indicator = False  # Return to program
            cue.command.splice_immediate_flag = False
            cue.command.unique_program_id = 1
            cue.command.avail_num = 1
            cue.command.avails_expected = 1
            
            # Generate the cue
            cue.encode()
            
            # Save as JSON
            json_file = f"{self.output_dir}/cue_in_{event_id}.json"
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            # Save as base64
            base64_file = f"{self.output_dir}/cue_in_{event_id}.base64"
            with open(base64_file, 'w') as f:
                f.write(cue.encode())
            
            print(f"✅ Generated CUE-IN marker:")
            print(f"   📄 JSON: {json_file}")
            print(f"   📄 Base64: {base64_file}")
            print(f"   🎯 Event ID: {event_id}")
            print(f"   📥 Return to program")
            
            return json_file, base64_file
            
        except Exception as e:
            print(f"❌ Error generating CUE-IN: {e}")
            return None, None
    
    def generate_crash_out(self, event_id):
        """Generate a CRASH-OUT (immediate) marker using threefive"""
        try:
            # Create a splice_insert cue
            cue = threefive.Cue()
            cue.command = threefive.SpliceInsert()
            cue.command.splice_event_id = event_id
            cue.command.splice_event_cancel_indicator = False
            cue.command.out_of_network_indicator = True
            cue.command.splice_immediate_flag = True  # Immediate
            cue.command.unique_program_id = 1
            cue.command.avail_num = 1
            cue.command.avails_expected = 1
            
            # Generate the cue
            cue.encode()
            
            # Save as JSON
            json_file = f"{self.output_dir}/crash_out_{event_id}.json"
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            # Save as base64
            base64_file = f"{self.output_dir}/crash_out_{event_id}.base64"
            with open(base64_file, 'w') as f:
                f.write(cue.encode())
            
            print(f"✅ Generated CRASH-OUT marker:")
            print(f"   📄 JSON: {json_file}")
            print(f"   📄 Base64: {base64_file}")
            print(f"   🎯 Event ID: {event_id}")
            print(f"   🚨 Immediate emergency break")
            
            return json_file, base64_file
            
        except Exception as e:
            print(f"❌ Error generating CRASH-OUT: {e}")
            return None, None
    
    def generate_time_signal(self, event_id):
        """Generate a TIME_SIGNAL marker using threefive"""
        try:
            # Create a time_signal cue
            cue = threefive.Cue()
            cue.command = threefive.TimeSignal()
            # TimeSignal doesn't need event_id, but we'll use it for filename
            
            # Generate the cue
            cue.encode()
            
            # Save as JSON
            json_file = f"{self.output_dir}/time_signal_{event_id}.json"
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            # Save as base64
            base64_file = f"{self.output_dir}/time_signal_{event_id}.base64"
            with open(base64_file, 'w') as f:
                f.write(cue.encode())
            
            print(f"✅ Generated TIME_SIGNAL marker:")
            print(f"   📄 JSON: {json_file}")
            print(f"   📄 Base64: {base64_file}")
            print(f"   🎯 Event ID: {event_id}")
            print(f"   ⏰ Time signal")
            
            return json_file, base64_file
            
        except Exception as e:
            print(f"❌ Error generating TIME_SIGNAL: {e}")
            return None, None
    
    def generate_all_markers(self):
        """Generate all SCTE-35 markers"""
        print("🎬 Generating SCTE-35 Markers with Threefive")
        print("=" * 60)
        
        base_event_id = self.config['scte35']['event_id']
        ad_duration = self.config['scte35']['ad_duration']
        
        generated_files = []
        
        # Generate CUE-OUT
        json_file, base64_file = self.generate_cue_out(base_event_id, ad_duration)
        if json_file:
            generated_files.extend([json_file, base64_file])
        
        # Generate CUE-IN
        json_file, base64_file = self.generate_cue_in(base_event_id + 1)
        if json_file:
            generated_files.extend([json_file, base64_file])
        
        # Generate CRASH-OUT
        json_file, base64_file = self.generate_crash_out(base_event_id + 2)
        if json_file:
            generated_files.extend([json_file, base64_file])
        
        # Generate TIME_SIGNAL
        json_file, base64_file = self.generate_time_signal(base_event_id + 3)
        if json_file:
            generated_files.extend([json_file, base64_file])
        
        print(f"\n📊 Summary:")
        print(f"   Generated {len(generated_files)} files")
        print(f"   Output directory: {self.output_dir}")
        
        return generated_files

def test_threefive_generation():
    """Test threefive SCTE-35 generation"""
    print("🧪 Testing Threefive SCTE-35 Generation")
    print("=" * 50)
    
    generator = ThreefiveSCTE35Generator()
    files = generator.generate_all_markers()
    
    if files:
        print(f"\n🎉 Successfully generated {len(files)} SCTE-35 files!")
        print("   These files can be used with TSDuck or other SCTE-35 tools.")
        return True
    else:
        print("\n❌ Failed to generate SCTE-35 files")
        return False

if __name__ == "__main__":
    test_threefive_generation()
