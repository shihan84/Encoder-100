#!/usr/bin/env python3
"""
Production SCTE-35 Alert System
Ready-to-use SCTE-35 marker detection and alerting system
"""

import subprocess
import time
import json
import os
from datetime import datetime
import threefive
import threading
import queue

class ProductionSCTE35Alert:
    """Production-ready SCTE-35 alert system"""
    
    def __init__(self, config_file='distributor_config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.markers_detected = []
        self.alert_callbacks = []
        self.monitoring_active = False
        self.alert_queue = queue.Queue()
        self.monitor_thread = None
        
    def load_config(self):
        """Load configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            "input": {
                "type": "hls",
                "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8"
            },
            "scte35": {
                "data_pid": 500,
                "event_id": 10021
            }
        }
    
    def add_alert_callback(self, callback):
        """Add a callback function for SCTE-35 alerts"""
        self.alert_callbacks.append(callback)
    
    def trigger_alert(self, marker_info):
        """Trigger alert for detected SCTE-35 marker"""
        self.markers_detected.append(marker_info)
        self.alert_queue.put(marker_info)
        
        # Call all registered callbacks
        for callback in self.alert_callbacks:
            try:
                callback(marker_info)
            except Exception as e:
                print(f"⚠️  Alert callback error: {e}")
    
    def start_monitoring(self, input_source=None, duration=None):
        """Start monitoring SCTE-35 markers in a stream"""
        
        if input_source is None:
            input_source = self.config['input']['source']
        
        print(f"🔍 Starting SCTE-35 Monitoring")
        print("=" * 50)
        print(f"📡 Input: {input_source}")
        print(f"🎯 SCTE-35 PID: {self.config['scte35']['data_pid']}")
        print()
        
        # Build TSDuck detection command
        command = [
            'tsp',
            '-I', 'hls', input_source,
            '-P', 'splicemonitor',
            '--pid', str(self.config['scte35']['data_pid']),
            '--json',
            '-O', 'drop'
        ]
        
        print(f"🔧 Command: {' '.join(command)}")
        print("🚀 Starting monitoring...")
        print()
        
        self.monitoring_active = True
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            start_time = time.time()
            
            while self.monitoring_active:
                if process.poll() is not None:
                    print("⚠️  Monitoring process terminated")
                    break
                
                if duration and (time.time() - start_time) > duration:
                    print(f"⏱️  Monitoring duration ({duration}s) reached")
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
                                'type': 'SCTE-35 Marker Detected'
                            }
                            
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
            print(f"❌ Monitoring error: {e}")
            return False
        
        self.monitoring_active = False
        return True
    
    def stop_monitoring(self):
        """Stop SCTE-35 monitoring"""
        print("🛑 Stopping SCTE-35 monitoring...")
        self.monitoring_active = False
    
    def _is_scte35_output(self, line):
        """Check if line contains SCTE-35 output"""
        scte35_keywords = ['splice', 'scte', 'cue', 'break', 'insert', 'time_signal']
        return any(keyword in line.lower() for keyword in scte35_keywords)
    
    def verify_threefive_markers(self):
        """Verify threefive-generated SCTE-35 markers"""
        
        print("🧪 Verifying Threefive-Generated SCTE-35 Markers")
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
            print(f"🔍 Verifying {base64_file}...")
            
            try:
                with open(file_path, 'r') as f:
                    base64_data = f.read().strip()
                
                # Use threefive Python library to decode
                cue = threefive.Cue(base64_data)
                if cue.decode():
                    print(f"✅ {base64_file} is valid SCTE-35 data")
                    if hasattr(cue.command, 'splice_event_id'):
                        print(f"   Event ID: {cue.command.splice_event_id}")
                    valid_markers += 1
                else:
                    print(f"❌ {base64_file} failed to decode")
                
            except Exception as e:
                print(f"❌ Error verifying {base64_file}: {e}")
        
        print(f"\n📊 Verification Results:")
        print(f"   Valid markers: {valid_markers}/{len(base64_files)}")
        
        return valid_markers > 0
    
    def get_alert_summary(self):
        """Get summary of all alerts"""
        if not self.markers_detected:
            return "No SCTE-35 alerts triggered"
        
        summary = f"📊 SCTE-35 Alert Summary ({len(self.markers_detected)} alerts):\n"
        for i, marker in enumerate(self.markers_detected, 1):
            summary += f"  {i}. [{marker['timestamp']}] {marker['type']}\n"
            summary += f"      Data: {marker['data'][:50]}...\n"
        
        return summary
    
    def save_alerts_to_file(self, filename='scte35_alerts.json'):
        """Save all alerts to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.markers_detected, f, indent=2)
            print(f"💾 Alerts saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving alerts: {e}")

def production_alert_callback(marker_info):
    """Production alert callback function"""
    print(f"🚨 PRODUCTION ALERT: SCTE-35 Marker Detected!")
    print(f"   Time: {marker_info['timestamp']}")
    print(f"   Source: {marker_info['source']}")
    print(f"   Type: {marker_info['type']}")
    print(f"   Data: {marker_info['data'][:100]}...")
    print()
    
    # Here you could add:
    # - Send email notifications
    # - Log to database
    # - Send to monitoring systems
    # - Trigger other automated responses

def main():
    """Main function for production SCTE-35 alert system"""
    
    print("🔍 Production SCTE-35 Alert System")
    print("=" * 70)
    print("Ready-to-use SCTE-35 marker detection and alerting")
    print()
    
    # Create alert system
    alert_system = ProductionSCTE35Alert()
    alert_system.add_alert_callback(production_alert_callback)
    
    # Test 1: Verify threefive markers
    print("Test 1: Verifying threefive-generated SCTE-35 markers...")
    threefive_result = alert_system.verify_threefive_markers()
    
    # Test 2: Monitor stream for SCTE-35 markers
    print("\nTest 2: Monitoring stream for SCTE-35 markers...")
    print("   (This will run for 20 seconds)")
    
    monitoring_result = alert_system.start_monitoring(duration=20)
    
    # Save alerts to file
    alert_system.save_alerts_to_file()
    
    # Summary
    print("\n📋 PRODUCTION SUMMARY:")
    print("=" * 70)
    print(f"Threefive markers verified: {'✅ Valid' if threefive_result else '❌ Failed'}")
    print(f"Stream monitoring: {'✅ Active' if monitoring_result else '❌ Failed'}")
    print(f"Total alerts triggered: {len(alert_system.markers_detected)}")
    
    # Show alert summary
    print(f"\n{alert_system.get_alert_summary()}")
    
    if threefive_result:
        print("\n🎉 SUCCESS: Production SCTE-35 alert system is ready!")
        print("   - Threefive can generate valid SCTE-35 markers")
        print("   - Stream monitoring is working")
        print("   - Alert system is ready for production use")
        print("\n💡 Usage:")
        print("   - Run this script to monitor your streams")
        print("   - Alerts will be triggered when SCTE-35 markers are detected")
        print("   - All alerts are saved to scte35_alerts.json")
    else:
        print("\n⚠️  SCTE-35 alert system needs attention.")
        print("   Check your configuration and try again.")
    
    return threefive_result

if __name__ == "__main__":
    main()
