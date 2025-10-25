#!/usr/bin/env python3
"""
SCTE-35 Marker Generator for IBE-100
Professional SCTE-35 marker creation with threefive library
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

class SCTE35MarkerGenerator:
    """Professional SCTE-35 marker generator using threefive library"""
    
    def __init__(self, output_dir: str = "scte35_final"):
        """Initialize the marker generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.markers_generated = []
        
        if not THREEFIVE_AVAILABLE:
            raise ImportError("threefive library is required for SCTE-35 marker generation")
    
    def generate_cue_out(self, 
                         event_id: int, 
                         duration_seconds: int,
                         pts_offset: int = 0,
                         out_of_network: bool = True,
                         immediate: bool = False) -> Tuple[str, str]:
        """Generate CUE-OUT (Program Out Point) marker"""
        try:
            # Create splice_insert cue
            cue = threefive.Cue()
            cue.command = threefive.SpliceInsert()
            
            # Set basic parameters
            cue.command.splice_event_id = event_id
            cue.command.splice_event_cancel_indicator = False
            cue.command.out_of_network_indicator = out_of_network
            cue.command.program_splice_flag = True
            cue.command.splice_immediate_flag = immediate
            cue.command.unique_program_id = 1
            cue.command.avail_num = 1
            cue.command.avails_expected = 1
            
            # Set timing
            if not immediate:
                pts_time = int(time.time() * 90000) + pts_offset
                cue.command.splice_time = threefive.SpliceTime()
                cue.command.splice_time.pts_time = pts_time
            
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
            xml_content = self._cue_to_xml(cue, event_id, duration_seconds, pts_offset, immediate)
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Save as JSON (for reference)
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            self.markers_generated.append({
                'type': 'CUE-OUT',
                'event_id': event_id,
                'duration': duration_seconds,
                'immediate': immediate,
                'files': [str(xml_file), str(json_file)]
            })
            
            return str(xml_file), str(json_file)
            
        except Exception as e:
            raise Exception(f"Failed to generate CUE-OUT marker: {e}")
    
    def generate_cue_in(self, 
                       event_id: int,
                       pts_offset: int = 0,
                       immediate: bool = False) -> Tuple[str, str]:
        """Generate CUE-IN (Program In Point) marker"""
        try:
            # Create splice_insert cue
            cue = threefive.Cue()
            cue.command = threefive.SpliceInsert()
            
            # Set basic parameters
            cue.command.splice_event_id = event_id
            cue.command.splice_event_cancel_indicator = False
            cue.command.out_of_network_indicator = False  # Return to program
            cue.command.program_splice_flag = True
            cue.command.splice_immediate_flag = immediate
            cue.command.unique_program_id = 1
            cue.command.avail_num = 1
            cue.command.avails_expected = 1
            
            # Set timing
            if not immediate:
                pts_time = int(time.time() * 90000) + pts_offset
                cue.command.splice_time = threefive.SpliceTime()
                cue.command.splice_time.pts_time = pts_time
            
            # Generate the cue
            cue.encode()
            
            # Create filenames
            timestamp = int(time.time())
            base_filename = f"cue_in_{event_id}_{timestamp}"
            xml_file = self.output_dir / f"{base_filename}.xml"
            json_file = self.output_dir / f"{base_filename}.json"
            
            # Save as XML (TSDuck format)
            xml_content = self._cue_to_xml(cue, event_id, 0, pts_offset, immediate)
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Save as JSON (for reference)
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            self.markers_generated.append({
                'type': 'CUE-IN',
                'event_id': event_id,
                'duration': 0,
                'immediate': immediate,
                'files': [str(xml_file), str(json_file)]
            })
            
            return str(xml_file), str(json_file)
            
        except Exception as e:
            raise Exception(f"Failed to generate CUE-IN marker: {e}")
    
    def generate_crash_out(self, 
                          event_id: int,
                          pts_offset: int = 0) -> Tuple[str, str]:
        """Generate CRASH-OUT (Emergency Program Out) marker"""
        try:
            # Create splice_insert cue
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
            xml_content = self._cue_to_xml(cue, event_id, 0, pts_offset, True)
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Save as JSON (for reference)
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            self.markers_generated.append({
                'type': 'CRASH-OUT',
                'event_id': event_id,
                'duration': 0,
                'immediate': True,
                'files': [str(xml_file), str(json_file)]
            })
            
            return str(xml_file), str(json_file)
            
        except Exception as e:
            raise Exception(f"Failed to generate CRASH-OUT marker: {e}")
    
    def generate_time_signal(self, 
                           event_id: int,
                           pts_offset: int = 0) -> Tuple[str, str]:
        """Generate TIME_SIGNAL marker for timing reference"""
        try:
            # Create time_signal cue
            cue = threefive.Cue()
            cue.command = threefive.TimeSignal()
            
            # Set timing
            pts_time = int(time.time() * 90000) + pts_offset
            cue.command.splice_time = threefive.SpliceTime()
            cue.command.splice_time.pts_time = pts_time
            
            # Generate the cue
            cue.encode()
            
            # Create filenames
            timestamp = int(time.time())
            base_filename = f"time_signal_{event_id}_{timestamp}"
            xml_file = self.output_dir / f"{base_filename}.xml"
            json_file = self.output_dir / f"{base_filename}.json"
            
            # Save as XML (TSDuck format)
            xml_content = self._time_signal_to_xml(pts_time)
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            # Save as JSON (for reference)
            with open(json_file, 'w') as f:
                json.dump(cue.decode(), f, indent=2)
            
            self.markers_generated.append({
                'type': 'TIME_SIGNAL',
                'event_id': event_id,
                'duration': 0,
                'immediate': False,
                'files': [str(xml_file), str(json_file)]
            })
            
            return str(xml_file), str(json_file)
            
        except Exception as e:
            raise Exception(f"Failed to generate TIME_SIGNAL marker: {e}")
    
    def generate_custom_marker(self, 
                              marker_type: str,
                              event_id: int,
                              duration_seconds: int = 0,
                              pts_offset: int = 0,
                              out_of_network: bool = True,
                              immediate: bool = False,
                              custom_params: Dict[str, Any] = None) -> Tuple[str, str]:
        """Generate custom SCTE-35 marker with user-defined parameters"""
        try:
            if marker_type.upper() == "CUE_OUT":
                return self.generate_cue_out(event_id, duration_seconds, pts_offset, out_of_network, immediate)
            elif marker_type.upper() == "CUE_IN":
                return self.generate_cue_in(event_id, pts_offset, immediate)
            elif marker_type.upper() == "CRASH_OUT":
                return self.generate_crash_out(event_id, pts_offset)
            elif marker_type.upper() == "TIME_SIGNAL":
                return self.generate_time_signal(event_id, pts_offset)
            else:
                raise ValueError(f"Unknown marker type: {marker_type}")
                
        except Exception as e:
            raise Exception(f"Failed to generate custom marker: {e}")
    
    def generate_ad_break_sequence(self, 
                                 base_event_id: int,
                                 ad_duration: int,
                                 preroll_seconds: int = 2) -> List[Dict[str, Any]]:
        """Generate complete ad break sequence: preroll + cue-out + cue-in"""
        try:
            sequence = []
            
            # 1. Preroll time signal (2 seconds before)
            preroll_pts = -preroll_seconds * 90000
            xml_file, json_file = self.generate_time_signal(base_event_id, preroll_pts)
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
            cue_in_pts = ad_duration * 90000
            xml_file, json_file = self.generate_cue_in(base_event_id + 2, cue_in_pts)
            sequence.append({
                'type': 'CUE-IN',
                'event_id': base_event_id + 2,
                'description': 'Return to program',
                'files': [xml_file, json_file]
            })
            
            return sequence
            
        except Exception as e:
            raise Exception(f"Failed to generate ad break sequence: {e}")
    
    def _cue_to_xml(self, cue, event_id: int, duration: int, pts_offset: int, immediate: bool) -> str:
        """Convert threefive cue to TSDuck XML format"""
        pts_time = int(time.time() * 90000) + pts_offset
        
        if immediate:
            splice_time_xml = ""
        else:
            splice_time_xml = f"""
        <splice_time>
            <pts_time>{pts_time}</pts_time>
        </splice_time>"""
        
        duration_xml = ""
        if duration > 0:
            duration_xml = f"""
        <break_duration>
            <auto_return>0</auto_return>
            <duration>{duration * 90000}</duration>
        </break_duration>"""
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <splice_insert>
        <splice_event_id>{event_id}</splice_event_id>
        <splice_event_cancel_indicator>0</splice_event_cancel_indicator>
        <out_of_network_indicator>{1 if cue.command.out_of_network_indicator else 0}</out_of_network_indicator>
        <program_splice_flag>1</program_splice_flag>
        <duration_flag>{1 if duration > 0 else 0}</duration_flag>
        <splice_immediate_flag>{1 if immediate else 0}</splice_immediate_flag>{splice_time_xml}{duration_xml}
        <unique_program_id>1</unique_program_id>
        <avail_num>1</avail_num>
        <avails_expected>1</avails_expected>
    </splice_insert>
</tsduck>"""
    
    def _time_signal_to_xml(self, pts_time: int) -> str:
        """Convert time signal to TSDuck XML format"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <time_signal>
        <splice_time>
            <pts_time>{pts_time}</pts_time>
        </splice_time>
    </time_signal>
</tsduck>"""
    
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
    
    def validate_marker(self, xml_file: str) -> Dict[str, Any]:
        """Validate generated marker file"""
        try:
            with open(xml_file, 'r') as f:
                content = f.read()
            
            # Basic XML validation
            if not content.strip().startswith('<?xml'):
                return {'valid': False, 'error': 'Not a valid XML file'}
            
            if '<splice_insert>' not in content and '<time_signal>' not in content:
                return {'valid': False, 'error': 'Not a valid SCTE-35 marker'}
            
            return {'valid': True, 'content': content}
            
        except Exception as e:
            return {'valid': False, 'error': str(e)}


def test_marker_generation():
    """Test the SCTE-35 marker generation"""
    print("🧪 Testing SCTE-35 Marker Generation")
    print("=" * 50)
    
    if not THREEFIVE_AVAILABLE:
        print("❌ threefive library not available")
        print("   Install with: pip install threefive")
        return False
    
    try:
        generator = SCTE35MarkerGenerator()
        
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
    test_marker_generation()
