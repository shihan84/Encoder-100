#!/usr/bin/env python3
"""
SCTE-35 Marker Templates for IBE-100
Professional broadcast marker templates for different scenarios
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

class SCTE35Templates:
    """SCTE-35 marker templates for professional broadcast scenarios"""
    
    def __init__(self, output_dir: str = "scte35_final"):
        """Initialize the template system"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.templates_dir = Path("scte35_templates")
        self.templates_dir.mkdir(exist_ok=True)
        self.generated_markers = []
    
    def create_preroll_template(self, event_id: int, ad_duration: int = 30) -> Dict[str, Any]:
        """Create preroll ad break template (before main content)"""
        template = {
            "name": "Preroll Ad Break",
            "description": "Ad break before main program content",
            "scenario": "preroll",
            "markers": [
                {
                    "type": "TIME_SIGNAL",
                    "event_id": event_id,
                    "description": "Preroll timing signal (5s before)",
                    "pts_offset": -5 * 90000,  # 5 seconds before
                    "purpose": "Warn downstream systems of upcoming ad break"
                },
                {
                    "type": "CUE-OUT",
                    "event_id": event_id + 1,
                    "description": f"Preroll ad break start ({ad_duration}s)",
                    "duration": ad_duration,
                    "purpose": "Start of preroll commercial content"
                },
                {
                    "type": "CUE-IN",
                    "event_id": event_id + 2,
                    "description": "Return to main program",
                    "purpose": "End of preroll, start of main content"
                }
            ],
            "total_duration": ad_duration + 5,  # Ad duration + preroll warning
            "use_case": "Live streams, on-demand content, scheduled programming"
        }
        
        return template
    
    def create_midroll_template(self, event_id: int, ad_duration: int = 60, 
                               program_duration: int = 1800) -> Dict[str, Any]:
        """Create midroll ad break template (during main content)"""
        # Calculate midroll timing (middle of program)
        midroll_time = program_duration // 2
        
        template = {
            "name": "Midroll Ad Break",
            "description": "Ad break during main program content",
            "scenario": "midroll",
            "markers": [
                {
                    "type": "TIME_SIGNAL",
                    "event_id": event_id,
                    "description": "Midroll timing signal (10s before)",
                    "pts_offset": (midroll_time - 10) * 90000,
                    "purpose": "Warn of upcoming midroll break"
                },
                {
                    "type": "CUE-OUT",
                    "event_id": event_id + 1,
                    "description": f"Midroll ad break start ({ad_duration}s)",
                    "duration": ad_duration,
                    "pts_offset": midroll_time * 90000,
                    "purpose": "Start of midroll commercial content"
                },
                {
                    "type": "CUE-IN",
                    "event_id": event_id + 2,
                    "description": "Return to main program",
                    "pts_offset": (midroll_time + ad_duration) * 90000,
                    "purpose": "End of midroll, resume main content"
                }
            ],
            "total_duration": ad_duration + 10,  # Ad duration + warning time
            "program_duration": program_duration,
            "midroll_time": midroll_time,
            "use_case": "Long-form content, movies, live events, sports"
        }
        
        return template
    
    def create_postroll_template(self, event_id: int, ad_duration: int = 30) -> Dict[str, Any]:
        """Create postroll ad break template (after main content)"""
        template = {
            "name": "Postroll Ad Break",
            "description": "Ad break after main program content",
            "scenario": "postroll",
            "markers": [
                {
                    "type": "TIME_SIGNAL",
                    "event_id": event_id,
                    "description": "Postroll timing signal (3s before)",
                    "pts_offset": -3 * 90000,  # 3 seconds before
                    "purpose": "Signal end of main content"
                },
                {
                    "type": "CUE-OUT",
                    "event_id": event_id + 1,
                    "description": f"Postroll ad break start ({ad_duration}s)",
                    "duration": ad_duration,
                    "purpose": "Start of postroll commercial content"
                },
                {
                    "type": "CUE-IN",
                    "event_id": event_id + 2,
                    "description": "End of content",
                    "purpose": "End of postroll, end of stream"
                }
            ],
            "total_duration": ad_duration + 3,  # Ad duration + warning time
            "use_case": "End of programs, credits, next program promotion"
        }
        
        return template
    
    def create_scheduled_template(self, event_id: int, scheduled_time: str, 
                                ad_duration: int = 60) -> Dict[str, Any]:
        """Create scheduled ad break template (specific time)"""
        # Parse scheduled time (format: "HH:MM:SS" or "HH:MM")
        try:
            if len(scheduled_time.split(':')) == 2:
                scheduled_time += ":00"  # Add seconds if not provided
            
            time_parts = scheduled_time.split(':')
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds = int(time_parts[2])
            
            # Convert to seconds from midnight
            scheduled_seconds = hours * 3600 + minutes * 60 + seconds
            
        except (ValueError, IndexError):
            # Default to 30 minutes if parsing fails
            scheduled_seconds = 30 * 60
        
        template = {
            "name": "Scheduled Ad Break",
            "description": f"Ad break scheduled for {scheduled_time}",
            "scenario": "scheduled",
            "scheduled_time": scheduled_time,
            "scheduled_seconds": scheduled_seconds,
            "markers": [
                {
                    "type": "TIME_SIGNAL",
                    "event_id": event_id,
                    "description": f"Scheduled timing signal (15s before {scheduled_time})",
                    "pts_offset": (scheduled_seconds - 15) * 90000,
                    "purpose": "Advance warning of scheduled break"
                },
                {
                    "type": "CUE-OUT",
                    "event_id": event_id + 1,
                    "description": f"Scheduled ad break start ({ad_duration}s) at {scheduled_time}",
                    "duration": ad_duration,
                    "pts_offset": scheduled_seconds * 90000,
                    "purpose": "Start of scheduled commercial content"
                },
                {
                    "type": "CUE-IN",
                    "event_id": event_id + 2,
                    "description": "Return to scheduled programming",
                    "pts_offset": (scheduled_seconds + ad_duration) * 90000,
                    "purpose": "End of scheduled break, resume programming"
                }
            ],
            "total_duration": ad_duration + 15,  # Ad duration + warning time
            "use_case": "Scheduled programming, news breaks, regular intervals"
        }
        
        return template
    
    def create_emergency_template(self, event_id: int) -> Dict[str, Any]:
        """Create emergency break template (immediate)"""
        template = {
            "name": "Emergency Break",
            "description": "Immediate emergency program interruption",
            "scenario": "emergency",
            "markers": [
                {
                    "type": "CRASH-OUT",
                    "event_id": event_id,
                    "description": "Emergency program out - immediate",
                    "immediate": True,
                    "purpose": "Immediate emergency interruption"
                },
                {
                    "type": "CUE-IN",
                    "event_id": event_id + 1,
                    "description": "Return to program after emergency",
                    "purpose": "Resume normal programming"
                }
            ],
            "total_duration": 0,  # Immediate execution
            "use_case": "Breaking news, emergency alerts, technical issues"
        }
        
        return template
    
    def create_multi_break_template(self, base_event_id: int, 
                                  break_times: List[int], ad_duration: int = 30) -> Dict[str, Any]:
        """Create multiple ad breaks template"""
        template = {
            "name": "Multiple Ad Breaks",
            "description": f"Multiple ad breaks at specified times",
            "scenario": "multi_break",
            "break_times": break_times,
            "ad_duration": ad_duration,
            "markers": [],
            "total_duration": len(break_times) * (ad_duration + 5),  # Each break + warning
            "use_case": "Long-form content with multiple commercial breaks"
        }
        
        # Generate markers for each break time
        for i, break_time in enumerate(break_times):
            event_id = base_event_id + (i * 3)  # 3 markers per break
            
            # Warning signal
            template["markers"].append({
                "type": "TIME_SIGNAL",
                "event_id": event_id,
                "description": f"Break {i+1} warning (5s before)",
                "pts_offset": (break_time - 5) * 90000,
                "purpose": f"Warning for break {i+1}"
            })
            
            # CUE-OUT
            template["markers"].append({
                "type": "CUE-OUT",
                "event_id": event_id + 1,
                "description": f"Break {i+1} start ({ad_duration}s)",
                "duration": ad_duration,
                "pts_offset": break_time * 90000,
                "purpose": f"Start of break {i+1}"
            })
            
            # CUE-IN
            template["markers"].append({
                "type": "CUE-IN",
                "event_id": event_id + 2,
                "description": f"End of break {i+1}",
                "pts_offset": (break_time + ad_duration) * 90000,
                "purpose": f"End of break {i+1}"
            })
        
        return template
    
    def save_template(self, template: Dict[str, Any], filename: str = None) -> str:
        """Save template to file"""
        if not filename:
            scenario = template.get("scenario", "custom")
            timestamp = int(time.time())
            filename = f"{scenario}_template_{timestamp}.json"
        
        template_file = self.templates_dir / filename
        
        with open(template_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        return str(template_file)
    
    def load_template(self, filename: str) -> Dict[str, Any]:
        """Load template from file"""
        template_file = self.templates_dir / filename
        
        with open(template_file, 'r') as f:
            return json.load(f)
    
    def list_templates(self) -> List[Dict[str, str]]:
        """List all available templates"""
        templates = []
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r') as f:
                    template = json.load(f)
                
                templates.append({
                    "filename": template_file.name,
                    "name": template.get("name", "Unknown"),
                    "scenario": template.get("scenario", "custom"),
                    "description": template.get("description", ""),
                    "use_case": template.get("use_case", ""),
                    "created": time.ctime(template_file.stat().st_mtime)
                })
            except Exception as e:
                print(f"⚠️ Error loading template {template_file}: {e}")
        
        return templates
    
    def generate_from_template(self, template: Dict[str, Any], 
                             base_event_id: int = None) -> List[Dict[str, Any]]:
        """Generate actual markers from template"""
        try:
            from scte35_xml_generator import SCTE35XMLGenerator
            generator = SCTE35XMLGenerator(str(self.output_dir))
            
            generated_markers = []
            markers = template.get("markers", [])
            
            if not base_event_id:
                base_event_id = markers[0].get("event_id", 10000) if markers else 10000
            
            for marker_config in markers:
                marker_type = marker_config.get("type", "")
                event_id = marker_config.get("event_id", base_event_id)
                duration = marker_config.get("duration", 0)
                
                if marker_type == "CUE-OUT":
                    xml_file, json_file = generator.generate_cue_out(event_id, duration)
                elif marker_type == "CUE-IN":
                    xml_file, json_file = generator.generate_cue_in(event_id)
                elif marker_type == "CRASH-OUT":
                    xml_file, json_file = generator.generate_crash_out(event_id)
                elif marker_type == "TIME_SIGNAL":
                    xml_file, json_file = generator.generate_time_signal(event_id)
                else:
                    continue
                
                generated_markers.append({
                    "type": marker_type,
                    "event_id": event_id,
                    "xml_file": xml_file,
                    "json_file": json_file,
                    "description": marker_config.get("description", ""),
                    "purpose": marker_config.get("purpose", "")
                })
            
            return generated_markers
            
        except Exception as e:
            raise Exception(f"Failed to generate markers from template: {e}")
    
    def create_standard_templates(self):
        """Create standard broadcast templates"""
        templates = []
        
        # Preroll template
        preroll = self.create_preroll_template(10000, 30)
        templates.append(("preroll_standard.json", preroll))
        
        # Midroll template
        midroll = self.create_midroll_template(10100, 60, 1800)
        templates.append(("midroll_standard.json", midroll))
        
        # Postroll template
        postroll = self.create_postroll_template(10200, 30)
        templates.append(("postroll_standard.json", postroll))
        
        # Scheduled template
        scheduled = self.create_scheduled_template(10300, "14:30:00", 60)
        templates.append(("scheduled_standard.json", scheduled))
        
        # Emergency template
        emergency = self.create_emergency_template(10400)
        templates.append(("emergency_standard.json", emergency))
        
        # Multi-break template
        multi_break = self.create_multi_break_template(10500, [300, 900, 1500], 30)
        templates.append(("multi_break_standard.json", multi_break))
        
        # Save all templates
        for filename, template in templates:
            self.save_template(template, filename)
        
        return len(templates)


def test_templates():
    """Test the template system"""
    print("🧪 Testing SCTE-35 Template System")
    print("=" * 50)
    
    try:
        templates = SCTE35Templates()
        
        # Create standard templates
        print("\n1. Creating standard templates...")
        count = templates.create_standard_templates()
        print(f"✅ Created {count} standard templates")
        
        # List templates
        print("\n2. Listing available templates...")
        template_list = templates.list_templates()
        for template in template_list:
            print(f"   📄 {template['name']} ({template['scenario']})")
            print(f"      Description: {template['description']}")
            print(f"      Use case: {template['use_case']}")
            print()
        
        # Test template generation
        print("\n3. Testing template generation...")
        preroll_template = templates.create_preroll_template(20000, 45)
        generated = templates.generate_from_template(preroll_template, 20000)
        print(f"✅ Generated {len(generated)} markers from preroll template")
        
        for marker in generated:
            print(f"   - {marker['type']} (Event ID: {marker['event_id']})")
            print(f"     Description: {marker['description']}")
        
        print(f"\n📊 Summary:")
        print(f"   Templates created: {count}")
        print(f"   Markers generated: {len(generated)}")
        print(f"   Output directory: {templates.output_dir}")
        print(f"   Templates directory: {templates.templates_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    test_templates()
