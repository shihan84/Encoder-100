#!/usr/bin/env python3
"""
SCTE-35 Marker Monitor and Alert System
Detects and verifies SCTE-35 markers in your stream
"""

import subprocess
import time
import json
import os
from datetime import datetime
import threading
import queue

class SCTE35Monitor:
    """Monitor SCTE-35 markers in transport streams"""
    
    def __init__(self):
        self.monitoring = False
        self.markers_found = []
        self.alert_queue = queue.Queue()
        self.monitor_process = None
        
    def start_monitoring(self, input_source, output_callback=None):
        """Start monitoring SCTE-35 markers in the stream"""
        print("🔍 Starting SCTE-35 Marker Monitoring")
        print("=" * 50)
        
        # Build TSDuck command for SCTE-35 monitoring
        command = [
            'tsp',
            '-I', 'hls', input_source,
            '-P', 'splicemonitor',
            '--pid', '500',  # SCTE-35 PID
            '--json',  # Output in JSON format
            '-O', 'drop'  # Drop output, we only want monitoring
        ]
        
        print(f"📡 Monitoring: {input_source}")
        print(f"🎯 SCTE-35 PID: 500")
        print(f"🔧 Command: {' '.join(command)}")
        print()
        
        try:
            self.monitor_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.monitoring = True
            print("✅ SCTE-35 monitoring started")
            
            # Start monitoring thread
            monitor_thread = threading.Thread(
                target=self._monitor_output,
                args=(output_callback,)
            )
            monitor_thread.daemon = True
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting monitoring: {e}")
            return False
    
    def _monitor_output(self, output_callback):
        """Monitor TSDuck output for SCTE-35 markers"""
        while self.monitoring and self.monitor_process:
            try:
                line = self.monitor_process.stdout.readline()
                if line:
                    self._process_line(line.strip(), output_callback)
                elif self.monitor_process.poll() is not None:
                    break
            except Exception as e:
                print(f"⚠️  Monitoring error: {e}")
                break
    
    def _process_line(self, line, output_callback):
        """Process a line of TSDuck output"""
        try:
            # Try to parse as JSON
            if line.startswith('{'):
                data = json.loads(line)
                if 'splice' in data or 'scte' in data.lower():
                    self._handle_scte35_marker(data, output_callback)
            else:
                # Check for SCTE-35 keywords in text output
                if any(keyword in line.lower() for keyword in ['splice', 'scte', 'cue', 'break']):
                    self._handle_text_marker(line, output_callback)
                    
        except json.JSONDecodeError:
            # Not JSON, check for SCTE-35 keywords
            if any(keyword in line.lower() for keyword in ['splice', 'scte', 'cue', 'break']):
                self._handle_text_marker(line, output_callback)
        except Exception as e:
            print(f"⚠️  Error processing line: {e}")
    
    def _handle_scte35_marker(self, data, output_callback):
        """Handle detected SCTE-35 marker"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        marker_info = {
            'timestamp': timestamp,
            'type': 'SCTE-35 Marker',
            'data': data
        }
        
        self.markers_found.append(marker_info)
        
        print(f"🎯 [{timestamp}] SCTE-35 MARKER DETECTED!")
        print(f"   Data: {json.dumps(data, indent=2)}")
        print()
        
        if output_callback:
            output_callback(marker_info)
    
    def _handle_text_marker(self, line, output_callback):
        """Handle text-based SCTE-35 marker detection"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        marker_info = {
            'timestamp': timestamp,
            'type': 'SCTE-35 Text Marker',
            'data': line
        }
        
        self.markers_found.append(marker_info)
        
        print(f"🎯 [{timestamp}] SCTE-35 MARKER DETECTED!")
        print(f"   Text: {line}")
        print()
        
        if output_callback:
            output_callback(marker_info)
    
    def stop_monitoring(self):
        """Stop SCTE-35 monitoring"""
        print("🛑 Stopping SCTE-35 monitoring...")
        self.monitoring = False
        
        if self.monitor_process:
            self.monitor_process.terminate()
            try:
                self.monitor_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.monitor_process.kill()
        
        print("✅ SCTE-35 monitoring stopped")
    
    def get_markers_summary(self):
        """Get summary of detected markers"""
        if not self.markers_found:
            return "No SCTE-35 markers detected"
        
        summary = f"📊 SCTE-35 Markers Summary ({len(self.markers_found)} found):\n"
        for i, marker in enumerate(self.markers_found, 1):
            summary += f"  {i}. [{marker['timestamp']}] {marker['type']}\n"
        
        return summary

def test_scte35_detection():
    """Test SCTE-35 detection with your stream"""
    print("🧪 Testing SCTE-35 Detection")
    print("=" * 50)
    
    monitor = SCTE35Monitor()
    
    def marker_callback(marker_info):
        """Callback for detected markers"""
        print(f"🚨 ALERT: SCTE-35 marker detected at {marker_info['timestamp']}")
    
    # Start monitoring your HLS stream
    success = monitor.start_monitoring(
        "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
        marker_callback
    )
    
    if not success:
        print("❌ Failed to start monitoring")
        return False
    
    print("⏱️  Monitoring for 30 seconds...")
    print("   (Press Ctrl+C to stop early)")
    
    try:
        time.sleep(30)
    except KeyboardInterrupt:
        print("\n⚠️  Monitoring stopped by user")
    
    monitor.stop_monitoring()
    
    # Show summary
    print("\n" + monitor.get_markers_summary())
    
    if monitor.markers_found:
        print("\n🎉 SCTE-35 markers detected in your stream!")
        return True
    else:
        print("\n⚠️  No SCTE-35 markers detected")
        print("   This could mean:")
        print("   - No markers in the stream")
        print("   - Markers on different PID")
        print("   - Stream doesn't contain SCTE-35 data")
        return False

def monitor_with_scte35_injection():
    """Monitor stream while injecting SCTE-35 markers"""
    print("🎬 Testing SCTE-35 Injection + Monitoring")
    print("=" * 50)
    
    # Check if SCTE-35 files exist
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
    
    # Start injection process
    injection_command = [
        'tsp',
        '-I', 'hls', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8',
        '-P', 'spliceinject',
        '--pid', '500',
        '--pts-pid', '256',
        '--files', f'{scte_dir}/*.xml',
        '-O', 'ip', '127.0.0.1:9999'  # Local UDP for monitoring
    ]
    
    print("🚀 Starting SCTE-35 injection...")
    print(f"Command: {' '.join(injection_command)}")
    
    try:
        injection_process = subprocess.Popen(
            injection_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for injection to start
        time.sleep(3)
        
        # Start monitoring the injected stream
        monitor = SCTE35Monitor()
        
        def marker_callback(marker_info):
            print(f"🎯 INJECTED MARKER DETECTED: {marker_info['timestamp']}")
        
        # Monitor the local UDP stream
        success = monitor.start_monitoring("udp://127.0.0.1:9999", marker_callback)
        
        if success:
            print("⏱️  Monitoring injected stream for 20 seconds...")
            time.sleep(20)
            monitor.stop_monitoring()
            
            print("\n" + monitor.get_markers_summary())
        
        # Stop injection
        injection_process.terminate()
        injection_process.wait()
        
        return len(monitor.markers_found) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 SCTE-35 Marker Monitor and Alert System")
    print("=" * 60)
    
    print("Choose monitoring option:")
    print("1. Monitor existing stream for SCTE-35 markers")
    print("2. Test SCTE-35 injection + monitoring")
    print("3. Both tests")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_scte35_detection()
    elif choice == "2":
        monitor_with_scte35_injection()
    elif choice == "3":
        print("\n🧪 Running both tests...")
        print("\n" + "="*50)
        test_scte35_detection()
        print("\n" + "="*50)
        monitor_with_scte35_injection()
    else:
        print("❌ Invalid choice")
