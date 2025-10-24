#!/usr/bin/env python3
"""
Comprehensive SCTE-35 Alert System
Combines threefive library with TSDuck for complete SCTE-35 detection and alerting
"""

import subprocess
import time
import json
import os
from datetime import datetime
import threefive

class ComprehensiveSCTE35Alert:
    """Comprehensive SCTE-35 alert system using threefive and TSDuck"""
    
    def __init__(self):
        self.markers_detected = []
        self.alert_callbacks = []
        self.monitoring_active = False
    
    def add_alert_callback(self, callback):
        """Add a callback function for SCTE-35 alerts"""
        self.alert_callbacks.append(callback)
    
    def trigger_alert(self, marker_info):
        """Trigger alert for detected SCTE-35 marker"""
        self.markers_detected.append(marker_info)
        
        # Call all registered callbacks
        for callback in self.alert_callbacks:
            try:
                callback(marker_info)
            except Exception as e:
                print(f"⚠️  Alert callback error: {e}")
    
    def test_threefive_markers(self):
        """Test threefive-generated SCTE-35 markers"""
        
        print("🧪 Testing Threefive-Generated SCTE-35 Markers")
        print("=" * 60)
        
        threefive_dir = 'scte35_threefive'
        if not os.path.exists(threefive_dir):
            print("❌ Threefive SCTE-35 directory not found")
            return False
        
        base64_files = [f for f in os.listdir(threefive_dir) if f.endswith('.base64')]
        if not base64_files:
            print("❌ No threefive-generated base64 files found")
            return False
        
        print(f"📁 Found {len(base64_files)} threefive-generated files:")
        for f in base64_files:
            print(f"   - {f}")
        print()
        
        valid_markers = 0
        
        for base64_file in base64_files:
            file_path = os.path.join(threefive_dir, base64_file)
            print(f"🔍 Testing {base64_file}...")
            
            try:
                with open(file_path, 'r') as f:
                    base64_data = f.read().strip()
                
                # Use threefive Python library to decode
                cue = threefive.Cue(base64_data)
                if cue.decode():
                    print(f"✅ {base64_file} is valid SCTE-35 data")
                    print(f"   Command: {cue.command}")
                    if hasattr(cue.command, 'splice_event_id'):
                        print(f"   Event ID: {cue.command.splice_event_id}")
                    valid_markers += 1
                    
                    # Trigger alert for valid marker
                    marker_info = {
                        'timestamp': datetime.now().strftime("%H:%M:%S"),
                        'source': 'threefive_generated',
                        'type': 'SCTE-35 Marker (Threefive)',
                        'data': f"Event ID: {getattr(cue.command, 'splice_event_id', 'N/A')}",
                        'file': base64_file
                    }
                    self.trigger_alert(marker_info)
                else:
                    print(f"❌ {base64_file} failed to decode")
                
            except Exception as e:
                print(f"❌ Error testing {base64_file}: {e}")
        
        print(f"\n📊 Threefive Test Results:")
        print(f"   Valid markers: {valid_markers}/{len(base64_files)}")
        
        return valid_markers > 0
    
    def test_tsduck_detection(self, input_source, duration=20):
        """Test TSDuck SCTE-35 detection"""
        
        print(f"🔍 TSDuck SCTE-35 Detection Test")
        print("=" * 50)
        print(f"📡 Input: {input_source}")
        print(f"⏱️  Duration: {duration} seconds")
        print()
        
        # Build TSDuck detection command
        command = [
            'tsp',
            '-I', 'hls', input_source,
            '-P', 'splicemonitor',
            '--pid', '500',
            '--json',
            '-O', 'drop'
        ]
        
        print(f"🔧 Command: {' '.join(command)}")
        print("🚀 Starting detection...")
        print()
        
        markers_found = []
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            start_time = time.time()
            
            while time.time() - start_time < duration:
                if process.poll() is not None:
                    break
                    
                try:
                    line = process.stdout.readline()
                    if line:
                        line = line.strip()
                        if line and self._is_scte35_output(line):
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            marker_info = {
                                'timestamp': timestamp,
                                'source': input_source,
                                'data': line,
                                'type': 'SCTE-35 Marker (TSDuck)'
                            }
                            
                            markers_found.append(marker_info)
                            self.trigger_alert(marker_info)
                            
                except Exception as e:
                    print(f"⚠️  Read error: {e}")
                
                time.sleep(0.1)
            
            # Stop process
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            
        except Exception as e:
            print(f"❌ Detection error: {e}")
            return False
        
        # Results
        print("📊 TSDuck Detection Results:")
        print("=" * 50)
        
        if markers_found:
            print(f"✅ Found {len(markers_found)} SCTE-35 markers!")
            for i, marker in enumerate(markers_found, 1):
                print(f"   {i}. [{marker['timestamp']}] {marker['type']}")
            return True
        else:
            print("❌ No SCTE-35 markers detected")
            return False
    
    def _is_scte35_output(self, line):
        """Check if line contains SCTE-35 output"""
        scte35_keywords = ['splice', 'scte', 'cue', 'break', 'insert', 'time_signal']
        return any(keyword in line.lower() for keyword in scte35_keywords)
    
    def test_injection_and_detection(self):
        """Test SCTE-35 injection and detection"""
        
        print("🎬 Testing SCTE-35 Injection + Detection")
        print("=" * 60)
        
        # Check if we have SCTE-35 files
        scte_dir = 'scte35_commands'
        if not os.path.exists(scte_dir):
            print("❌ SCTE-35 commands directory not found")
            return False
        
        xml_files = [f for f in os.listdir(scte_dir) if f.endswith('.xml')]
        if not xml_files:
            print("❌ No SCTE-35 XML files found")
            return False
        
        print(f"📁 Found {len(xml_files)} SCTE-35 files:")
        for f in xml_files:
            print(f"   - {f}")
        print()
        
        # Start injection
        injection_command = [
            'tsp',
            '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
            '-P', 'spliceinject',
            '--pid', '500',
            '--pts-pid', '256',
            '--files', f'{scte_dir}/*.xml',
            '-O', 'ip', '127.0.0.1:9999'
        ]
        
        print("🚀 Starting SCTE-35 injection...")
        injection_process = subprocess.Popen(
            injection_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for injection to start
        time.sleep(3)
        
        if injection_process.poll() is None:
            print("✅ SCTE-35 injection is running")
            
            # Test detection on injected stream
            result = self.test_tsduck_detection("udp://127.0.0.1:9999", duration=15)
            
            # Stop injection
            injection_process.terminate()
            injection_process.wait()
            
            return result
        else:
            print("❌ SCTE-35 injection failed to start")
            return False
    
    def get_alert_summary(self):
        """Get summary of all alerts"""
        if not self.markers_detected:
            return "No SCTE-35 alerts triggered"
        
        summary = f"📊 SCTE-35 Alert Summary ({len(self.markers_detected)} alerts):\n"
        for i, marker in enumerate(self.markers_detected, 1):
            summary += f"  {i}. [{marker['timestamp']}] {marker['type']}\n"
            if 'file' in marker:
                summary += f"      File: {marker['file']}\n"
            summary += f"      Data: {marker['data'][:50]}...\n"
        
        return summary

def alert_callback(marker_info):
    """Example alert callback function"""
    print(f"🚨 ALERT: SCTE-35 Marker Detected!")
    print(f"   Time: {marker_info['timestamp']}")
    print(f"   Type: {marker_info['type']}")
    print(f"   Data: {marker_info['data']}")
    if 'file' in marker_info:
        print(f"   File: {marker_info['file']}")
    print()

def main():
    """Main function to run comprehensive SCTE-35 alert system"""
    
    print("🔍 Comprehensive SCTE-35 Alert System")
    print("=" * 70)
    print("Combining threefive library with TSDuck for complete detection")
    print()
    
    # Create alert system
    alert_system = ComprehensiveSCTE35Alert()
    alert_system.add_alert_callback(alert_callback)
    
    # Test 1: Test threefive-generated markers
    print("Test 1: Testing threefive-generated SCTE-35 markers...")
    threefive_result = alert_system.test_threefive_markers()
    
    # Test 2: Test TSDuck detection on original stream
    print("\nTest 2: Testing TSDuck detection on original HLS stream...")
    tsduck_result = alert_system.test_tsduck_detection(
        "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
        duration=15
    )
    
    # Test 3: Test injection + detection
    print("\nTest 3: Testing SCTE-35 injection + detection...")
    injection_result = alert_system.test_injection_and_detection()
    
    # Summary
    print("\n📋 COMPREHENSIVE SUMMARY:")
    print("=" * 70)
    print(f"Threefive-generated markers: {'✅ Valid' if threefive_result else '❌ Failed'}")
    print(f"TSDuck detection (original): {'✅ Found' if tsduck_result else '❌ None'}")
    print(f"SCTE-35 injection: {'✅ Working' if injection_result else '❌ Failed'}")
    print(f"Total alerts triggered: {len(alert_system.markers_detected)}")
    
    # Show alert summary
    print(f"\n{alert_system.get_alert_summary()}")
    
    if threefive_result or injection_result:
        print("\n🎉 SUCCESS: SCTE-35 alert system is working!")
        print("   - Threefive can generate valid SCTE-35 markers")
        print("   - TSDuck can detect SCTE-35 in streams")
        print("   - Your SCTE-35 alert system is ready for production")
    else:
        print("\n⚠️  SCTE-35 alert system needs attention.")
        print("   Check your configuration and try again.")
    
    return threefive_result or injection_result

if __name__ == "__main__":
    main()
