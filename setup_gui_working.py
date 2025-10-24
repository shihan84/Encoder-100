#!/usr/bin/env python3
"""
Quick Setup Script for TSDuck GUI with Working Configuration
This script helps configure the GUI with your proven working settings
"""

import json
import os
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt

def load_working_config():
    """Load the working configuration"""
    try:
        with open('gui_working_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Configuration file not found!")
        return None

def display_working_config():
    """Display the working configuration"""
    config = load_working_config()
    if not config:
        return
    
    print("\n🎯 WORKING TSDuck SCTE-35 CONFIGURATION")
    print("=" * 50)
    print(f"📡 INPUT: {config['input']['type'].upper()}")
    print(f"   Source: {config['input']['source']}")
    print()
    print(f"📤 OUTPUT: {config['output']['type'].upper()}")
    print(f"   Destination: {config['output']['source']}")
    print()
    print(f"🎬 SCTE-35 CONFIGURATION:")
    print(f"   Data PID: {config['scte35']['data_pid']}")
    print(f"   Event ID: {config['scte35']['event_id']}")
    print(f"   Ad Duration: {config['scte35']['ad_duration']} seconds")
    print()
    print(f"📊 STREAM SPECIFICATIONS:")
    print(f"   Video: {config['stream_specs']['video']['resolution']} {config['stream_specs']['video']['codec']}")
    print(f"   Audio: {config['stream_specs']['audio']['codec']} {config['stream_specs']['audio']['bitrate']}")
    print(f"   Latency: {config['stream_specs']['latency']}")
    print()
    print("✅ WORKING COMMAND:")
    print(config['working_command'])
    print()

def show_gui_instructions():
    """Show GUI configuration instructions"""
    instructions = """
🖥️ TSDuck GUI Configuration Instructions
========================================

1. 📋 INPUT TAB:
   - Set Type: HLS
   - Set Source: https://cdn.itassist.one/BREAKING/NEWS/index.m3u8
   - Leave Parameters empty

2. 📤 OUTPUT TAB:
   - Set Type: SRT
   - Set Destination: srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish
   - Set Parameters: --streamid '#!::r=scte/scte,m=publish' --latency 2000

3. 🔧 PLUGINS TAB:
   - Enable PMT Plugin:
     * Service: 1
     * Add PID: 500/0x86
   - Enable SpliceInject Plugin:
     * Service: 1
     * Files: scte35_final/*.xml
     * Inject Count: 1
     * Inject Interval: 1000
     * Start Delay: 2000

4. ▶️ START PROCESSING:
   - Click "Start Processing" button
   - Monitor output in "Console Output" tab
   - Watch for SCTE-35 injection messages

✅ Your system is already tested and working!
The GUI will use the same proven configuration.
"""
    print(instructions)

class WorkingConfigDialog(QDialog):
    """Dialog to show working configuration"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSDuck GUI - Working Configuration")
        self.setMinimumSize(600, 500)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🎯 Your Working TSDuck SCTE-35 Configuration")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Configuration display
        config_text = QTextEdit()
        config_text.setReadOnly(True)
        config_text.setFont(QFont("Monaco", 9))
        
        config = load_working_config()
        if config:
            config_display = f"""
📡 INPUT CONFIGURATION:
  Type: {config['input']['type'].upper()}
  Source: {config['input']['source']}
  Parameters: {config['input']['params']}

📤 OUTPUT CONFIGURATION:
  Type: {config['output']['type'].upper()}
  Destination: {config['output']['source']}
  Parameters: {config['output']['params']}

🎬 SCTE-35 CONFIGURATION:
  Data PID: {config['scte35']['data_pid']}
  Null PID: {config['scte35']['null_pid']}
  Event ID: {config['scte35']['event_id']}
  Ad Duration: {config['scte35']['ad_duration']} seconds
  Pre-roll Duration: {config['scte35']['preroll_duration']} seconds

📊 STREAM SPECIFICATIONS:
  Video: {config['stream_specs']['video']['resolution']} {config['stream_specs']['video']['codec']}
  Audio: {config['stream_specs']['audio']['codec']} {config['stream_specs']['audio']['bitrate']}
  Latency: {config['stream_specs']['latency']}

✅ WORKING COMMAND:
{config['working_command']}

🎯 SCTE-35 MARKERS AVAILABLE:
  - cue_out_10021.xml: Ad break start (600s duration)
  - cue_in_10022.xml: Return to program
  - preroll_10023.xml: Scheduled ad (600s duration)
  - crash_out_10024.xml: Emergency break (30s duration)
"""
            config_text.setPlainText(config_display)
        
        layout.addWidget(config_text)
        
        # Instructions
        instructions = QLabel("""
🖥️ GUI Configuration Steps:
1. Set Input to HLS with your source URL
2. Set Output to SRT with your endpoint
3. Enable PMT and SpliceInject plugins
4. Click "Start Processing"
        """)
        instructions.setStyleSheet("font-size: 12px; margin: 10px; background-color: #f0f0f0; padding: 10px;")
        layout.addWidget(instructions)
        
        # Close button
        close_btn = QPushButton("✅ Got it! Close this dialog")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

def main():
    """Main function"""
    print("🚀 TSDuck GUI Working Configuration Setup")
    print("=" * 40)
    
    # Display configuration
    display_working_config()
    
    # Show GUI instructions
    show_gui_instructions()
    
    # Show GUI dialog if available
    try:
        app = QApplication(sys.argv)
        dialog = WorkingConfigDialog()
        dialog.exec()
    except Exception as e:
        print(f"GUI dialog not available: {e}")
        print("Configuration details shown above.")

if __name__ == "__main__":
    main()
