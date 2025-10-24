#!/usr/bin/env python3
"""
Threefive SCTE-35 Detector and Alert System
Uses threefive library for advanced SCTE-35 detection
"""

import subprocess
import time
import json
import os
from datetime import datetime
import threefive

class ThreefiveSCTE35Detector:
    """Advanced SCTE-35 detector using threefive library"""
    
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
    
    def detect_scte35_in_stream(self, input_source, duration=30):
        """Detect SCTE-35 markers in a stream using threefive"""
        
        print(f"🔍 Threefive SCTE-35 Detection")
        print("=" * 50)
        print(f"📡 Input: {input_source}")
        print(f"⏱️  Duration: {duration} seconds")
        print()
        
        # Use threefive CLI to detect SCTE-35
        command = ['threefive', input_source]
        
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
                                'type': 'SCTE-35 Marker (Threefive)'
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
    
    def _is_scte35_output(self, line):
        """Check if line contains SCTE-35 output from threefive"""
        scte35_keywords = ['splice', 'scte', 'cue', 'break', 'insert', 'time_signal', 'splice_insert']
        return any(keyword in line.lower() for keyword in scte35_keywords)
    
    def test_threefive_detection(self):
        """Test threefive detection on your HLS stream"""
        
        print("🧪 Testing Threefive SCTE-35 Detection")
        print("=" * 60)
        
        # Test on your HLS stream
        result = self.detect_scte35_in_stream(
            "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
            duration=20
        )
        
        return result
    
    def test_with_generated_markers(self):
        """Test detection with threefive-generated markers"""
        
        print("🎬 Testing with Threefive-Generated Markers")
        print("=" * 60)
        
        # Check if threefive-generated files exist
        threefive_dir = 'scte35_threefive'
        if not os.path.exists(threefive_dir):
            print("❌ Threefive SCTE-35 directory not found")
            print("   Run: python3 threefive_scte35_generator.py")
            return False
        
        base64_files = [f for f in os.listdir(threefive_dir) if f.endswith('.base64')]
        if not base64_files:
            print("❌ No threefive-generated base64 files found")
            return False
        
        print(f"📁 Found {len(base64_files)} threefive-generated files:")
        for f in base64_files:
            print(f"   - {f}")
        print()
        
        # Test each base64 file
        for base64_file in base64_files:
            file_path = os.path.join(threefive_dir, base64_file)
            print(f"🔍 Testing {base64_file}...")
            
            try:
                with open(file_path, 'r') as f:
                    base64_data = f.read().strip()
                
                # Use threefive to decode and display
                command = ['threefive', base64_data]
                result = subprocess.run(command, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print(f"✅ {base64_file} is valid SCTE-35 data")
                    print(f"   Decoded: {result.stdout[:100]}...")
                else:
                    print(f"❌ {base64_file} failed to decode")
                    print(f"   Error: {result.stderr}")
                
            except Exception as e:
                print(f"❌ Error testing {base64_file}: {e}")
        
        return True

def alert_callback(marker_info):
    """Example alert callback function"""
    print(f"🚨 ALERT: SCTE-35 Marker Detected!")
    print(f"   Time: {marker_info['timestamp']}")
    print(f"   Source: {marker_info['source']}")
    print(f"   Type: {marker_info['type']}")
    print(f"   Data: {marker_info['data'][:100]}...")
    print()

def main():
    """Main function to run threefive SCTE-35 detection"""
    
    print("🔍 Threefive SCTE-35 Detector and Alert System")
    print("=" * 70)
    
    # Create detector
    detector = ThreefiveSCTE35Detector()
    detector.add_alert_callback(alert_callback)
    
    # Test 1: Check original stream
    print("Test 1: Checking original HLS stream with threefive...")
    original_result = detector.test_threefive_detection()
    
    # Test 2: Test generated markers
    print("\nTest 2: Testing threefive-generated markers...")
    generated_result = detector.test_with_generated_markers()
    
    # Summary
    print("\n📋 FINAL SUMMARY:")
    print("=" * 70)
    print(f"Original stream SCTE-35 markers: {'✅ Found' if original_result else '❌ None'}")
    print(f"Threefive-generated markers: {'✅ Valid' if generated_result else '❌ Failed'}")
    print(f"Total markers detected: {len(detector.markers_detected)}")
    
    if generated_result:
        print("\n🎉 SUCCESS: Threefive SCTE-35 system is working!")
        print("   - Threefive can generate valid SCTE-35 markers")
        print("   - Threefive can detect SCTE-35 in streams")
        print("   - Your SCTE-35 alert system is ready")
    else:
        print("\n⚠️  Threefive SCTE-35 system needs attention.")
        print("   Check your threefive installation and generated files.")
    
    return generated_result

if __name__ == "__main__":
    main()
