#!/usr/bin/env python3
"""
SCTE-35 XML Generator for IBE-100
Direct XML generation for TSDuck compatibility
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

class SCTE35XMLGenerator:
    """SCTE-35 XML marker generator for TSDuck"""
    
    def __init__(self, output_dir: str = "scte35_final"):
        """Initialize the marker generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.markers_generated = []
    
    def generate_cue_out(self, event_id: int, duration_seconds: int) -> Tuple[str, str]:
        """Generate CUE-OUT (Program Out Point) marker"""
        try:
            # Create filenames
            timestamp = int(time.time())
            base_filename = f"cue_out_{event_id}_{timestamp}"
            xml_file = self.output_dir / f"{base_filename}.xml"
            json_file = self.output_dir / f"{base_filename}.json"
            
            # Generate XML content
            xml_content = self._create_cue_out_xml(event_id, duration_seconds)
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Generate JSON metadata
            json_content = {
                "type": "CUE-OUT",
                "event_id": event_id,
                "duration_seconds": duration_seconds,
                "description": f"Program out point - {duration_seconds}s ad break",
                "timestamp": timestamp,
                "xml_file": str(xml_file)
            }
            
            with open(json_file, 'w') as f:
                json.dump(json_content, f, indent=2)
            
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
            # Create filenames
            timestamp = int(time.time())
            base_filename = f"cue_in_{event_id}_{timestamp}"
            xml_file = self.output_dir / f"{base_filename}.xml"
            json_file = self.output_dir / f"{base_filename}.json"
            
            # Generate XML content
            xml_content = self._create_cue_in_xml(event_id)
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Generate JSON metadata
            json_content = {
                "type": "CUE-IN",
                "event_id": event_id,
                "duration_seconds": 0,
                "description": "Program in point - return to program",
                "timestamp": timestamp,
                "xml_file": str(xml_file)
            }
            
            with open(json_file, 'w') as f:
                json.dump(json_content, f, indent=2)
            
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
            # Create filenames
            timestamp = int(time.time())
            base_filename = f"crash_out_{event_id}_{timestamp}"
            xml_file = self.output_dir / f"{base_filename}.xml"
            json_file = self.output_dir / f"{base_filename}.json"
            
            # Generate XML content
            xml_content = self._create_crash_out_xml(event_id)
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Generate JSON metadata
            json_content = {
                "type": "CRASH-OUT",
                "event_id": event_id,
                "duration_seconds": 0,
                "description": "Emergency program out - immediate break",
                "timestamp": timestamp,
                "xml_file": str(xml_file)
            }
            
            with open(json_file, 'w') as f:
                json.dump(json_content, f, indent=2)
            
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
            # Create filenames
            timestamp = int(time.time())
            base_filename = f"time_signal_{event_id}_{timestamp}"
            xml_file = self.output_dir / f"{base_filename}.xml"
            json_file = self.output_dir / f"{base_filename}.json"
            
            # Generate XML content
            xml_content = self._create_time_signal_xml()
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Generate JSON metadata
            json_content = {
                "type": "TIME_SIGNAL",
                "event_id": event_id,
                "duration_seconds": 0,
                "description": "Time signal for timing reference",
                "timestamp": timestamp,
                "xml_file": str(xml_file)
            }
            
            with open(json_file, 'w') as f:
                json.dump(json_content, f, indent=2)
            
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
            
            # 1. Preroll time signal
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


def test_xml_generation():
    """Test the SCTE-35 XML marker generation"""
    print("🧪 Testing SCTE-35 XML Marker Generation")
    print("=" * 50)
    
    try:
        generator = SCTE35XMLGenerator()
        
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
        
        # Show sample XML content
        print(f"\n📄 Sample XML content (CUE-OUT):")
        with open(markers[0]['files'][0], 'r') as f:
            print(f.read())
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    test_xml_generation()
