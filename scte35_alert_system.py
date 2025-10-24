#!/usr/bin/env python3
"""
SCTE-35 Alert System - Working Version
Detects and alerts when SCTE-35 markers are found in streams
"""

import subprocess
import time
import json
import os
from datetime import datetime

class SCTE35AlertSystem:
    """SCTE-35 Alert and Detection System"""
    
    def __init__(self):
        self.markers_detected = []
        self.alert_callbacks = []
    
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
    
    def detect_markers(self, input_source, duration=30, pid=500):
        """Detect SCTE-35 markers in a stream"""
        
        print(f"🔍 SCTE-35 Detection Started")
        print("=" * 50)
        print(f"📡 Input: {input_source}")
        print(f"⏱️  Duration: {duration} seconds")
        print(f"🎯 SCTE-35 PID: {pid}")
        print()
        
        # Build detection command
        command = [
            'tsp',
            '-I', 'hls', input_source,
            '-P', 'splicemonitor',
            '--pid', str(pid),
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
                        if line and self._is_scte35_marker(line):
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            marker_info = {
                                'timestamp': timestamp,
                                'source': input_source,
                                'pid': pid,
                                'data': line,
                                'type': 'SCTE-35 Marker'
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
        print("📊 Detection Results:")
        print("=" * 50)
        
        if markers_found:
            print(f"✅ Found {len(markers_found)} SCTE-35 markers!")
            for i, marker in enumerate(markers_found, 1):
                print(f"   {i}. [{marker['timestamp']}] {marker['type']}")
            return True
        else:
            print("❌ No SCTE-35 markers detected")
            return False
    
    def _is_scte35_marker(self, line):
        """Check if line contains SCTE-35 marker data"""
        scte35_keywords = ['splice', 'scte', 'cue', 'break', 'insert', 'time_signal']
        return any(keyword in line.lower() for keyword in scte35_keywords)
    
    def test_injection_and_detection(self):
        """Test SCTE-35 injection and detection"""
        
        print("🎬 SCTE-35 Injection + Detection Test")
        print("=" * 60)
        
        # Check SCTE-35 files
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
        
        # Test detection on injected stream
        print("🔍 Testing detection on injected stream...")
        result = self.detect_markers("udp://127.0.0.1:9999", duration=15, pid=500)
        
        # Stop injection
        injection_process.terminate()
        injection_process.wait()
        
        return result

def alert_callback(marker_info):
    """Example alert callback function"""
    print(f"🚨 ALERT: SCTE-35 Marker Detected!")
    print(f"   Time: {marker_info['timestamp']}")
    print(f"   Source: {marker_info['source']}")
    print(f"   PID: {marker_info['pid']}")
    print(f"   Data: {marker_info['data'][:100]}...")
    print()

def main():
    """Main function to run SCTE-35 alert system"""
    
    print("🔍 SCTE-35 Alert System")
    print("=" * 60)
    
    # Create alert system
    alert_system = SCTE35AlertSystem()
    alert_system.add_alert_callback(alert_callback)
    
    # Test 1: Check original stream
    print("Test 1: Checking original HLS stream...")
    original_markers = alert_system.detect_markers(
        "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
        duration=15
    )
    
    # Test 2: Test injection + detection
    print("\nTest 2: Testing SCTE-35 injection + detection...")
    injected_markers = alert_system.test_injection_and_detection()
    
    # Summary
    print("\n📋 FINAL SUMMARY:")
    print("=" * 60)
    print(f"Original stream SCTE-35 markers: {'✅ Found' if original_markers else '❌ None'}")
    print(f"Injected SCTE-35 markers: {'✅ Working' if injected_markers else '❌ Failed'}")
    print(f"Total markers detected: {len(alert_system.markers_detected)}")
    
    if injected_markers:
        print("\n🎉 SUCCESS: SCTE-35 injection and detection working!")
        print("   Your SCTE-35 alert system is ready for production.")
    else:
        print("\n⚠️  SCTE-35 injection needs attention.")
        print("   Check your SCTE-35 XML files and configuration.")
    
    return injected_markers

if __name__ == "__main__":
    main()
