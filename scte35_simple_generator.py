#!/usr/bin/env python3
"""
Simple SCTE-35 Marker Generator for IBE-100
Working implementation using threefive library
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

try:
    import threefive
    THREEFIVE_AVAILABLE = True
except ImportError:
    THREEFIVE_AVAILABLE = False
    print("⚠️ threefive library not available - install with: pip install threefive")

class SimpleSCTE35Generator:
    """Simple SCTE-35 marker generator using threefive library"""
    
    def __init__(self, output_dir: str = "scte35_final"):
        """Initialize the marker generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.markers_generated = []
        
        if not THREEFIVE_AVAILABLE:
            raise ImportError("threefive library is required for SCTE-35 marker generation")
    
    def generate_cue_out(self, event_id: int, duration_seconds: int) -> Tuple[str, str]:
        """Generate CUE-OUT (Program Out Point) marker"""
        try:
            # Create a simple splice_insert using threefive
            cue = threefive.Cue()
            cue.command = threefive.SpliceInsert()
            
            # Set basic parameters
            cue.command.splice_event_id = event_id
            cue.command.splice_event_cancel_indicator = False
            cue.command.out_of_network_indicator = True
            cue.command.program_splice_flag = True
            cue.command.splice_immediate_flag = False
            cue.command.unique_program_id = 1
            cue.command.avail_num = 1
            cue.command.avails_expected = 1
            
            # Set break duration
            if duration_seconds > 0:
                cue.command.duration_flag = True
                cue.command.break_duration = threefive.BreakDuration()
                cue.command.break_duration.auto_return = False
                cue.command.break_duration.duration = duration_seconds * 90000  # Convert to 90kHz
            
            # Generate the cue
            cue.encode()
            
            # Create filenames
            timestamp = int(time.time())
            base_filename = f"cue_out_{event_id}_{timestamp}"
            xml_file = self.output_dir / f"{base_filename}.xml"
            json_file = self.output_dir / f"{base_filename}.json"
            
            # Save as XML (TSDuck format)
            xml_content = self._create_cue_out_xml(event_id, duration_seconds)
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Save as JSON (for reference)
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            self.markers_generated.append({
                'type': 'CUE-OUT',
                'event_id': event_id,
                'duration': duration_seconds,
                'files': [str(xml_file), str(json_file)]
            })
            
            return str(xml_file), str(json_file)
            
        except Exception as e:
            raise Exception(f"Failed to generate CUE-OUT marker: {e}")
    
    def generate_cue_in(self, event_id: int) -> Tuple[str, str]:
        """Generate CUE-IN (Program In Point) marker"""
        try:
            # Create a simple splice_insert using threefive
            cue = threefive.Cue()
            cue.command = threefive.SpliceInsert()
            
            # Set basic parameters
            cue.command.splice_event_id = event_id
            cue.command.splice_event_cancel_indicator = False
            cue.command.out_of_network_indicator = False  # Return to program
            cue.command.program_splice_flag = True
            cue.command.splice_immediate_flag = False
            cue.command.unique_program_id = 1
            cue.command.avail_num = 1
            cue.command.avails_expected = 1
            
            # Generate the cue
            cue.encode()
            
            # Create filenames
            timestamp = int(time.time())
            base_filename = f"cue_in_{event_id}_{timestamp}"
            xml_file = self.output_dir / f"{base_filename}.xml"
            json_file = self.output_dir / f"{base_filename}.json"
            
            # Save as XML (TSDuck format)
            xml_content = self._create_cue_in_xml(event_id)
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Save as JSON (for reference)
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            self.markers_generated.append({
                'type': 'CUE-IN',
                'event_id': event_id,
                'duration': 0,
                'files': [str(xml_file), str(json_file)]
            })
            
            return str(xml_file), str(json_file)
            
        except Exception as e:
            raise Exception(f"Failed to generate CUE-IN marker: {e}")
    
    def generate_crash_out(self, event_id: int) -> Tuple[str, str]:
        """Generate CRASH-OUT (Emergency Program Out) marker"""
        try:
            # Create a simple splice_insert using threefive
            cue = threefive.Cue()
            cue.command = threefive.SpliceInsert()
            
            # Set basic parameters
            cue.command.splice_event_id = event_id
            cue.command.splice_event_cancel_indicator = False
            cue.command.out_of_network_indicator = True
            cue.command.program_splice_flag = True
            cue.command.splice_immediate_flag = True  # Always immediate for crash
            cue.command.unique_program_id = 1
            cue.command.avail_num = 1
            cue.command.avails_expected = 1
            
            # Generate the cue
            cue.encode()
            
            # Create filenames
            timestamp = int(time.time())
            base_filename = f"crash_out_{event_id}_{timestamp}"
            xml_file = self.output_dir / f"{base_filename}.xml"
            json_file = self.output_dir / f"{base_filename}.json"
            
            # Save as XML (TSDuck format)
            xml_content = self._create_crash_out_xml(event_id)
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Save as JSON (for reference)
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            self.markers_generated.append({
                'type': 'CRASH-OUT',
                'event_id': event_id,
                'duration': 0,
                'files': [str(xml_file), str(json_file)]
            })
            
            return str(xml_file), str(json_file)
            
        except Exception as e:
            raise Exception(f"Failed to generate CRASH-OUT marker: {e}")
    
    def generate_time_signal(self, event_id: int) -> Tuple[str, str]:
        """Generate TIME_SIGNAL marker for timing reference"""
        try:
            # Create time_signal cue
            cue = threefive.Cue()
            cue.command = threefive.TimeSignal()
            
            # Generate the cue
            cue.encode()
            
            # Create filenames
            timestamp = int(time.time())
            base_filename = f"time_signal_{event_id}_{timestamp}"
            xml_file = self.output_dir / f"{base_filename}.xml"
            json_file = self.output_dir / f"{base_filename}.json"
            
            # Save as XML (TSDuck format)
            xml_content = self._create_time_signal_xml()
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Save as JSON (for reference)
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            self.markers_generated.append({
                'type': 'TIME_SIGNAL',
                'event_id': event_id,
                'duration': 0,
                'files': [str(xml_file), str(json_file)]
            })
            
            return str(xml_file), str(json_file)
            
        except Exception as e:
            raise Exception(f"Failed to generate TIME_SIGNAL marker: {e}")
    
    def _create_cue_out_xml(self, event_id: int, duration: int) -> str:
        """Create CUE-OUT XML for TSDuck"""
        pts_time = int(time.time() * 90000)
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
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
    
    def _create_cue_in_xml(self, event_id: int) -> str:
        """Create CUE-IN XML for TSDuck"""
        pts_time = int(time.time() * 90000)
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
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
    
    def _create_crash_out_xml(self, event_id: int) -> str:
        """Create CRASH-OUT XML for TSDuck"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
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
    
    def _create_time_signal_xml(self) -> str:
        """Create TIME_SIGNAL XML for TSDuck"""
        pts_time = int(time.time() * 90000)
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <time_signal>
        <splice_time>
            <pts_time>{pts_time}</pts_time>
        </splice_time>
    </time_signal>
</tsduck>"""
    
    def generate_ad_break_sequence(self, base_event_id: int, ad_duration: int, preroll_seconds: int = 2) -> List[Dict[str, Any]]:
        """Generate complete ad break sequence: preroll + cue-out + cue-in"""
        try:
            sequence = []
            
            # 1. Preroll time signal (2 seconds before)
            xml_file, json_file = self.generate_time_signal(base_event_id)
            sequence.append({
                'type': 'TIME_SIGNAL',
                'event_id': base_event_id,
                'description': f'Preroll signal ({preroll_seconds}s before)',
                'files': [xml_file, json_file]
            })
            
            # 2. CUE-OUT (start of ad break)
            xml_file, json_file = self.generate_cue_out(base_event_id + 1, ad_duration)
            sequence.append({
                'type': 'CUE-OUT',
                'event_id': base_event_id + 1,
                'description': f'Ad break start ({ad_duration}s duration)',
                'files': [xml_file, json_file]
            })
            
            # 3. CUE-IN (end of ad break)
            xml_file, json_file = self.generate_cue_in(base_event_id + 2)
            sequence.append({
                'type': 'CUE-IN',
                'event_id': base_event_id + 2,
                'description': 'Return to program',
                'files': [xml_file, json_file]
            })
            
            return sequence
            
        except Exception as e:
            raise Exception(f"Failed to generate ad break sequence: {e}")
    
    def get_generated_markers(self) -> List[Dict[str, Any]]:
        """Get list of all generated markers"""
        return self.markers_generated.copy()
    
    def clear_markers(self):
        """Clear all generated markers and files"""
        try:
            # Remove all files in output directory
            for file_path in self.output_dir.glob("*"):
                if file_path.is_file():
                    file_path.unlink()
            
            # Clear markers list
            self.markers_generated.clear()
            
        except Exception as e:
            raise Exception(f"Failed to clear markers: {e}")


def test_simple_generation():
    """Test the simple SCTE-35 marker generation"""
    print("🧪 Testing Simple SCTE-35 Marker Generation")
    print("=" * 50)
    
    if not THREEFIVE_AVAILABLE:
        print("❌ threefive library not available")
        print("   Install with: pip install threefive")
        return False
    
    try:
        generator = SimpleSCTE35Generator()
        
        # Test individual markers
        print("\n1. Testing individual markers...")
        
        # CUE-OUT
        xml_file, json_file = generator.generate_cue_out(10021, 30)
        print(f"✅ CUE-OUT: {xml_file}")
        
        # CUE-IN
        xml_file, json_file = generator.generate_cue_in(10022)
        print(f"✅ CUE-IN: {json_file}")
        
        # CRASH-OUT
        xml_file, json_file = generator.generate_crash_out(10023)
        print(f"✅ CRASH-OUT: {xml_file}")
        
        # TIME_SIGNAL
        xml_file, json_file = generator.generate_time_signal(10024)
        print(f"✅ TIME_SIGNAL: {json_file}")
        
        # Test ad break sequence
        print("\n2. Testing ad break sequence...")
        sequence = generator.generate_ad_break_sequence(10025, 60, 2)
        print(f"✅ Generated {len(sequence)} markers for ad break sequence")
        
        # Show summary
        markers = generator.get_generated_markers()
        print(f"\n📊 Summary:")
        print(f"   Generated {len(markers)} markers")
        print(f"   Output directory: {generator.output_dir}")
        
        for marker in markers:
            print(f"   - {marker['type']} (Event ID: {marker['event_id']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    test_simple_generation()
