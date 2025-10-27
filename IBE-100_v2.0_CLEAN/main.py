#!/usr/bin/env python3
"""
ITAssist Broadcast Encoder - 100 (IBE-100) v2.0
Clean, Minimal Implementation
"""

import sys
import os
import shutil
import psutil
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget
from PyQt6.QtWidgets import QPushButton, QLabel, QLineEdit, QSpinBox, QGroupBox, QScrollArea, QComboBox, QTimeEdit, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QTime
from PyQt6.QtGui import QFont, QPixmap

# Set UTF-8 encoding for Windows console
os.system('chcp 65001 >nul 2>&1')

# Find TSDuck installation
def find_tsduck():
    """Find TSDuck installation"""
    # Check common installation paths
    paths = [
        "C:\\Program Files\\TSDuck\\bin\\tsp.exe",
        "C:\\TSDuck\\bin\\tsp.exe",
        "tsp.exe",  # Try PATH
        "tsp"  # Try PATH without extension
    ]
    
    for path in paths:
        if shutil.which(path) or os.path.exists(path):
            if os.path.exists(path):
                return path
            else:
                found = shutil.which(path)
                if found:
                    return found
    
    return "tsp"  # Fallback to tsp if not found

TSDUCK_PATH = find_tsduck()
print(f"[INFO] TSDuck found at: {TSDUCK_PATH}")

class StreamConfigWidget(QWidget):
    """Stream Configuration - Input/Output Settings"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        
        # Input Configuration
        input_group = QGroupBox("Input Stream")
        input_layout = QVBoxLayout()
        
        # Input Type Selection
        from PyQt6.QtWidgets import QComboBox
        input_type_layout = QHBoxLayout()
        input_type_layout.addWidget(QLabel("Input Type:"))
        self.input_type = QComboBox()
        self.input_type.addItems(["HLS (HTTP Live Streaming)", "SRT (Secure Reliable Transport)", "UDP (User Datagram Protocol)", "TCP (Transmission Control Protocol)", "HTTP/HTTPS", "DVB", "ASI"])
        self.input_type.setCurrentText("HLS (HTTP Live Streaming)")
        input_type_layout.addWidget(self.input_type)
        input_layout.addLayout(input_type_layout)
        
        # Input URL/Address
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("Enter stream URL (e.g., https://cdn.example.com/stream/index.m3u8)")
        self.input_url.setText("https://cdn.itassist.one/BREAKING/NEWS/index.m3u8")
        input_layout.addWidget(QLabel("Stream URL/Address:"))
        input_layout.addWidget(self.input_url)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Output Configuration
        output_group = QGroupBox("Output Streams")
        output_layout = QVBoxLayout()
        
        # Output Type Selection
        output_type_layout = QHBoxLayout()
        output_type_layout.addWidget(QLabel("Output Type:"))
        output_type_layout.addStretch()
        self.output_type = QComboBox()
        self.output_type.addItems(["SRT", "HLS", "DASH", "UDP", "TCP", "HTTP/HTTPS", "File"])
        self.output_type.setCurrentText("SRT")
        output_type_layout.addWidget(self.output_type)
        output_layout.addLayout(output_type_layout)
        
        # SRT Destination
        self.output_srt = QLineEdit()
        self.output_srt.setPlaceholderText("Enter SRT destination (e.g., cdn.example.com:8888)")
        self.output_srt.setText("cdn.itassist.one:8888")
        self.output_srt.setVisible(True)
        output_layout.addWidget(QLabel("SRT Destination:"))
        output_layout.addWidget(self.output_srt)
        
        # HLS Output
        self.output_hls = QLineEdit()
        self.output_hls.setPlaceholderText("Enter HLS output directory (e.g., /path/to/output)")
        self.output_hls.setText("output/hls")
        self.output_hls.setVisible(False)
        output_layout.addWidget(QLabel("HLS Output Directory:"))
        output_layout.addWidget(self.output_hls)
        
        # DASH Output
        self.output_dash = QLineEdit()
        self.output_dash.setPlaceholderText("Enter DASH output directory (e.g., /path/to/output)")
        self.output_dash.setText("output/dash")
        self.output_dash.setVisible(False)
        output_layout.addWidget(QLabel("DASH Output Directory:"))
        output_layout.addWidget(self.output_dash)
        
        # Show/Hide based on output type
        self.output_type.currentTextChanged.connect(self.on_output_type_changed)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Service Configuration
        service_group = QGroupBox("Service Configuration")
        service_layout = QVBoxLayout()
        
        # Service Name
        service_name_layout = QHBoxLayout()
        service_name_layout.addWidget(QLabel("Service Name:"))
        self.service_name = QLineEdit()
        self.service_name.setText("SCTE-35 Stream")
        service_name_layout.addWidget(self.service_name)
        service_layout.addLayout(service_name_layout)
        
        # Provider Name
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("Provider Name:"))
        self.provider_name = QLineEdit()
        self.provider_name.setText("ITAssist")
        provider_layout.addWidget(self.provider_name)
        service_layout.addLayout(provider_layout)
        
        # Service ID
        service_id_layout = QHBoxLayout()
        service_id_layout.addWidget(QLabel("Service ID:"))
        self.service_id = QSpinBox()
        self.service_id.setRange(1, 65535)
        self.service_id.setValue(1)
        service_id_layout.addWidget(self.service_id)
        service_layout.addLayout(service_id_layout)
        
        # Video PID
        vpid_layout = QHBoxLayout()
        vpid_layout.addWidget(QLabel("Video PID:"))
        self.vpid = QSpinBox()
        self.vpid.setRange(32, 8190)
        self.vpid.setValue(256)
        vpid_layout.addWidget(self.vpid)
        service_layout.addLayout(vpid_layout)
        
        # Audio PID
        apid_layout = QHBoxLayout()
        apid_layout.addWidget(QLabel("Audio PID:"))
        self.apid = QSpinBox()
        self.apid.setRange(32, 8190)
        self.apid.setValue(257)
        apid_layout.addWidget(self.apid)
        service_layout.addLayout(apid_layout)
        
        # SCTE-35 PID
        scte35_pid_layout = QHBoxLayout()
        scte35_pid_layout.addWidget(QLabel("SCTE-35 PID:"))
        self.scte35_pid = QSpinBox()
        self.scte35_pid.setRange(32, 8190)
        self.scte35_pid.setValue(500)
        scte35_pid_layout.addWidget(self.scte35_pid)
        service_layout.addLayout(scte35_pid_layout)
        
        service_group.setLayout(service_layout)
        layout.addWidget(service_group)
        
        # SRT Configuration
        srt_group = QGroupBox("SRT Configuration")
        srt_layout = QVBoxLayout()
        
        # Stream ID
        streamid_layout = QHBoxLayout()
        streamid_layout.addWidget(QLabel("Stream ID:"))
        self.stream_id = QLineEdit()
        self.stream_id.setText("#!::r=scte/scte,m=publish")
        self.stream_id.setPlaceholderText("Enter Stream ID for SRT (e.g., #!::r=scte/scte,m=publish)")
        streamid_layout.addWidget(self.stream_id)
        srt_layout.addLayout(streamid_layout)
        
        # Latency
        latency_layout = QHBoxLayout()
        latency_layout.addWidget(QLabel("Latency (ms):"))
        self.latency = QSpinBox()
        self.latency.setRange(100, 10000)
        self.latency.setValue(2000)
        self.latency.setSuffix(" ms")
        latency_layout.addWidget(self.latency)
        srt_layout.addLayout(latency_layout)
        
        srt_group.setLayout(srt_layout)
        layout.addWidget(srt_group)
        
        # HLS/DASH Output Settings
        hls_dash_group = QGroupBox("HLS/DASH Output Settings (For Local Server)")
        hls_dash_layout = QVBoxLayout()
        
        # CORS Enable
        cors_layout = QHBoxLayout()
        from PyQt6.QtWidgets import QCheckBox
        self.enable_cors = QCheckBox("Enable CORS Headers (Required for local web server)")
        self.enable_cors.setChecked(True)
        cors_layout.addWidget(self.enable_cors)
        hls_dash_layout.addLayout(cors_layout)
        
        # Segment Duration
        segment_duration_layout = QHBoxLayout()
        segment_duration_layout.addWidget(QLabel("Segment Duration (seconds):"))
        segment_duration_layout.addStretch()
        self.segment_duration = QSpinBox()
        self.segment_duration.setRange(2, 30)
        self.segment_duration.setValue(6)
        self.segment_duration.setSuffix(" seconds")
        segment_duration_layout.addWidget(self.segment_duration)
        hls_dash_layout.addLayout(segment_duration_layout)
        
        # Playlist Window Size
        playlist_window_layout = QHBoxLayout()
        playlist_window_layout.addWidget(QLabel("Playlist Window Size (segments):"))
        playlist_window_layout.addStretch()
        self.playlist_window = QSpinBox()
        self.playlist_window.setRange(3, 20)
        self.playlist_window.setValue(5)
        playlist_window_layout.addWidget(self.playlist_window)
        hls_dash_layout.addLayout(playlist_window_layout)
        
        hls_dash_group.setLayout(hls_dash_layout)
        layout.addWidget(hls_dash_group)
        
        # SCTE-35 Injection Settings
        injection_group = QGroupBox("SCTE-35 Injection Settings")
        injection_layout = QVBoxLayout()
        
        # Start Delay
        start_delay_layout = QHBoxLayout()
        start_delay_layout.addWidget(QLabel("Start Delay (ms):"))
        self.start_delay = QSpinBox()
        self.start_delay.setRange(0, 10000)
        self.start_delay.setValue(2000)
        self.start_delay.setSuffix(" ms")
        start_delay_layout.addWidget(self.start_delay)
        injection_layout.addLayout(start_delay_layout)
        
        # Inject Count
        inject_count_layout = QHBoxLayout()
        inject_count_layout.addWidget(QLabel("Inject Count:"))
        self.inject_count = QSpinBox()
        self.inject_count.setRange(1, 1000)
        self.inject_count.setValue(1)
        inject_count_layout.addWidget(self.inject_count)
        injection_layout.addLayout(inject_count_layout)
        
        # Inject Interval
        inject_interval_layout = QHBoxLayout()
        inject_interval_layout.addWidget(QLabel("Inject Interval (ms):"))
        self.inject_interval = QSpinBox()
        self.inject_interval.setRange(100, 60000)
        self.inject_interval.setValue(1000)
        self.inject_interval.setSuffix(" ms")
        inject_interval_layout.addWidget(self.inject_interval)
        injection_layout.addLayout(inject_interval_layout)
        
        injection_group.setLayout(injection_layout)
        layout.addWidget(injection_group)
        
        layout.addStretch()
        scroll.setWidget(scroll_widget)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
    
    def on_output_type_changed(self, text):
        """Show/hide output fields based on selected output type"""
        # Hide all output fields
        self.output_srt.setVisible(False)
        self.output_hls.setVisible(False)
        self.output_dash.setVisible(False)
        
        # Show relevant field based on output type
        if text == "SRT":
            self.output_srt.setVisible(True)
        elif text == "HLS":
            self.output_hls.setVisible(True)
        elif text == "DASH":
            self.output_dash.setVisible(True)
        else:
            # For other types (UDP, TCP, HTTP, File), show SRT field as general output
            self.output_srt.setVisible(True)
            if text == "File":
                self.output_srt.setPlaceholderText("Enter output file path")
            elif text in ["UDP", "TCP"]:
                self.output_srt.setPlaceholderText("Enter destination (e.g., 224.1.1.1:9999 or tcp://server:port)")
            else:
                self.output_srt.setPlaceholderText("Enter SRT destination (e.g., cdn.example.com:8888)")
    
    def get_config(self):
        return {
            "input_type": self.input_type.currentText(),
            "input_url": self.input_url.text(),
            "output_type": self.output_type.currentText(),
            "output_srt": self.output_srt.text(),
            "output_hls": self.output_hls.text(),
            "output_dash": self.output_dash.text(),
            "enable_cors": self.enable_cors.isChecked(),
            "segment_duration": self.segment_duration.value(),
            "playlist_window": self.playlist_window.value(),
            "service_name": self.service_name.text(),
            "provider_name": self.provider_name.text(),
            "service_id": self.service_id.value(),
            "vpid": self.vpid.value(),
            "apid": self.apid.value(),
            "scte35_pid": self.scte35_pid.value(),
            "stream_id": self.stream_id.text(),
            "latency": self.latency.value(),
            "start_delay": self.start_delay.value(),
            "inject_count": self.inject_count.value(),
            "inject_interval": self.inject_interval.value()
        }


class SCTE35Widget(QWidget):
    """SCTE-35 Marker Generation Tool"""
    
    marker_generated = pyqtSignal(str, str)  # Emits XML file path
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        
        # Title
        title = QLabel("🎬 Generate SCTE-35 Marker")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4CAF50; padding: 10px;")
        layout.addWidget(title)
        
        # Configuration Group
        config_group = QGroupBox("Marker Configuration")
        config_layout = QVBoxLayout()
        
        # Pre-roll Duration
        preroll_layout = QHBoxLayout()
        preroll_layout.addWidget(QLabel("Pre-roll Duration (seconds):"))
        preroll_layout.addStretch()
        self.preroll_duration = QSpinBox()
        self.preroll_duration.setRange(0, 10)
        self.preroll_duration.setValue(2)
        self.preroll_duration.setMinimumWidth(150)
        preroll_layout.addWidget(self.preroll_duration)
        config_layout.addLayout(preroll_layout)
        
        # Ad Duration
        ad_duration_layout = QHBoxLayout()
        ad_duration_layout.addWidget(QLabel("Ad Duration (seconds):"))
        ad_duration_layout.addStretch()
        self.ad_duration = QSpinBox()
        self.ad_duration.setRange(1, 3600)
        self.ad_duration.setValue(600)
        self.ad_duration.setMinimumWidth(150)
        ad_duration_layout.addWidget(self.ad_duration)
        config_layout.addLayout(ad_duration_layout)
        
        # Event ID
        event_id_layout = QHBoxLayout()
        event_id_layout.addWidget(QLabel("Event ID:"))
        event_id_layout.addStretch()
        self.event_id = QSpinBox()
        self.event_id.setRange(10000, 99999)
        self.event_id.setValue(10023)
        self.event_id.setMinimumWidth(150)
        event_id_layout.addWidget(self.event_id)
        config_layout.addLayout(event_id_layout)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Manual Cue Options
        cue_group = QGroupBox("Manual Cue Options")
        cue_layout = QVBoxLayout()
        
        # Cue Type
        cue_type_layout = QHBoxLayout()
        cue_type_layout.addWidget(QLabel("Cue Type:"))
        cue_type_layout.addStretch()
        self.cue_type = QComboBox()
        self.cue_type.addItems(["Pre-roll (Program Transition)", "CUE-OUT (Ad Break Start)", "CUE-IN (Ad Break End)", "Time Signal"])
        self.cue_type.setCurrentText("Pre-roll (Program Transition)")
        cue_type_layout.addWidget(self.cue_type)
        cue_layout.addLayout(cue_type_layout)
        
        # Schedule Time (optional)
        schedule_layout = QHBoxLayout()
        schedule_layout.addWidget(QLabel("Schedule Time (HH:MM:SS):"))
        schedule_layout.addStretch()
        from PyQt6.QtWidgets import QTimeEdit
        from PyQt6.QtCore import QTime
        self.schedule_time = QTimeEdit()
        self.schedule_time.setDisplayFormat("HH:mm:ss")
        self.schedule_time.setTime(QTime.currentTime())
        self.schedule_time.setMinimumWidth(150)
        schedule_layout.addWidget(self.schedule_time)
        cue_layout.addLayout(schedule_layout)
        
        # Enable immediate cue
        from PyQt6.QtWidgets import QCheckBox
        self.immediate_cue = QCheckBox("Trigger Cue Immediately (No Schedule)")
        self.immediate_cue.setChecked(True)
        cue_layout.addWidget(self.immediate_cue)
        
        cue_group.setLayout(cue_layout)
        layout.addWidget(cue_group)
        
        # Generate Button
        self.generate_btn = QPushButton("🎯 Generate SCTE-35 Marker")
        self.generate_btn.setStyleSheet("""
            QPushButton { 
                background-color: #4CAF50; 
                color: white; 
                font-weight: bold; 
                padding: 15px; 
                font-size: 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_marker)
        layout.addWidget(self.generate_btn)
        
        layout.addStretch()
        scroll.setWidget(scroll_widget)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
    
    def generate_marker(self):
        """Generate SCTE-35 marker XML file with manual cue support"""
        try:
            from datetime import datetime
            import json
            
            # Get parameters
            preroll = self.preroll_duration.value()
            ad_duration = self.ad_duration.value()
            event_id = self.event_id.value()
            cue_type = self.cue_type.currentText()
            schedule_time = self.schedule_time.time() if not self.immediate_cue.isChecked() else None
            immediate = self.immediate_cue.isChecked()
            
            # Create scte35_final directory if it doesn't exist
            markers_dir = Path("scte35_final")
            markers_dir.mkdir(exist_ok=True)
            
            # Generate timestamped filename based on cue type
            timestamp = int(datetime.now().timestamp())
            cue_prefix_map = {
                "Pre-roll (Program Transition)": "preroll",
                "CUE-OUT (Ad Break Start)": "cue_out",
                "CUE-IN (Ad Break End)": "cue_in",
                "Time Signal": "time_signal"
            }
            cue_prefix = cue_prefix_map.get(cue_type, "preroll")
            xml_filename = f"{cue_prefix}_{event_id}_{timestamp}.xml"
            json_filename = f"{cue_prefix}_{event_id}_{timestamp}.json"
            
            xml_path = markers_dir / xml_filename
            json_path = markers_dir / json_filename
            
            # Generate XML marker based on cue type
            if cue_type == "Pre-roll (Program Transition)":
                xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<spliceInfoSection protocolVersion="0" ptsAdjustment="0" tier="4095">
    <spliceInsert spliceEventId="{event_id}" 
                  spliceEventCancelIndicator="false" 
                  outOfNetworkIndicator="false" 
                  spliceImmediateFlag="false">
        <program><spliceTime ptsTime="{preroll * 90000}"/></program>
        <breakDuration autoReturn="true">
            <duration>{ad_duration * 90000}</duration>
        </breakDuration>
    </spliceInsert>
</spliceInfoSection>'''
            elif cue_type == "CUE-OUT (Ad Break Start)":
                xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<spliceInfoSection protocolVersion="0" ptsAdjustment="0" tier="4095">
    <spliceInsert spliceEventId="{event_id}" 
                  spliceEventCancelIndicator="false" 
                  outOfNetworkIndicator="true" 
                  spliceImmediateFlag="false">
        <program><spliceTime ptsTime="0"/></program>
        <breakDuration autoReturn="false">
            <duration>{ad_duration * 90000}</duration>
        </breakDuration>
    </spliceInsert>
</spliceInfoSection>'''
            elif cue_type == "CUE-IN (Ad Break End)":
                xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<spliceInfoSection protocolVersion="0" ptsAdjustment="0" tier="4095">
    <spliceInsert spliceEventId="{event_id}" 
                  spliceEventCancelIndicator="false" 
                  outOfNetworkIndicator="false" 
                  spliceImmediateFlag="true">
        <program><spliceTime ptsTime="0"/></program>
    </spliceInsert>
</spliceInfoSection>'''
            else:  # Time Signal
                xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<spliceInfoSection protocolVersion="0" ptsAdjustment="0" tier="4095">
    <spliceTimeSignal spliceEventId="{event_id}" 
                      spliceEventCancelIndicator="false">
        <spliceTime ptsTime="0"/>
    </spliceTimeSignal>
</spliceInfoSection>'''
            
            # Generate JSON metadata
            schedule_str = schedule_time.toString("HH:mm:ss") if schedule_time and not immediate else "Immediate"
            json_data = {
                "scte35_marker": {
                    "event_id": event_id,
                    "cue_type": cue_type,
                    "preroll_seconds": preroll,
                    "ad_duration_seconds": ad_duration,
                    "schedule_time": schedule_str,
                    "immediate": immediate,
                    "created_at": datetime.now().isoformat()
                }
            }
            
            # Write files
            xml_path.write_text(xml_content, encoding='utf-8')
            json_path.write_text(json.dumps(json_data, indent=2), encoding='utf-8')
            
            print(f"[SUCCESS] Generated SCTE-35 marker: {xml_filename}")
            
            # Emit signal
            self.marker_generated.emit(str(xml_path), str(json_path))
            
            return str(xml_path)
            
        except Exception as e:
            print(f"[ERROR] Failed to generate marker: {e}")
            return None


class MonitoringWidget(QWidget):
    """Monitoring and Console Output"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_monitoring()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create tabs for different monitoring views
        self.monitor_tabs = QTabWidget()
        self.monitor_tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; background-color: #2a2a2a; }
            QTabBar::tab { background-color: #3a3a3a; color: white; padding: 8px 16px; }
            QTabBar::tab:selected { background-color: #2196F3; }
        """)
        
        # Console Tab
        from PyQt6.QtWidgets import QTextEdit
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Courier", 10))
        self.console.setStyleSheet("background-color: #1e1e1e; color: #00ff00; padding: 10px;")
        self.monitor_tabs.addTab(self.console, "📺 Console")
        
        # SCTE-35 Monitoring Tab
        self.scte35_monitor = QTextEdit()
        self.scte35_monitor.setReadOnly(True)
        self.scte35_monitor.setFont(QFont("Courier", 10))
        self.scte35_monitor.setStyleSheet("background-color: #1e1e1e; color: #4CAF50; padding: 10px;")
        self.monitor_tabs.addTab(self.scte35_monitor, "🎬 SCTE-35 Status")
        
        # System Metrics Tab
        from PyQt6.QtWidgets import QLabel
        self.system_metrics = QLabel()
        self.system_metrics.setFont(QFont("Courier", 10))
        self.system_metrics.setStyleSheet("background-color: #1e1e1e; color: #ffffff; padding: 10px;")
        self.monitor_tabs.addTab(self.system_metrics, "⚡ System Metrics")
        
        # Local Web Server Tab
        web_server_widget = QWidget()
        web_server_layout = QVBoxLayout()
        
        self.web_server_status = QLabel()
        self.web_server_status.setFont(QFont("Arial", 12))
        self.web_server_status.setStyleSheet("padding: 10px; border: 2px solid #444; border-radius: 4px;")
        self.web_server_status.setText("🌐 Web Server: Stopped")
        
        self.web_server_url = QLineEdit()
        self.web_server_url.setPlaceholderText("http://localhost:8000")
        self.web_server_url.setText("http://localhost:8000")
        
        self.web_server_port = QSpinBox()
        self.web_server_port.setRange(8000, 9999)
        self.web_server_port.setValue(8000)
        self.web_server_port.setSuffix(" - Port")
        
        self.web_server_path = QLineEdit()
        self.web_server_path.setPlaceholderText("output/hls")
        self.web_server_path.setText("output/hls")
        
        from PyQt6.QtWidgets import QPushButton, QHBoxLayout
        self.start_server_btn = QPushButton("▶️ Start Web Server")
        self.start_server_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 4px;")
        self.stop_server_btn = QPushButton("⏹️ Stop Web Server")
        self.stop_server_btn.setEnabled(False)
        self.stop_server_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px; border-radius: 4px;")
        
        web_server_layout.addWidget(self.web_server_status)
        web_server_layout.addWidget(QLabel("Server URL:"))
        web_server_layout.addWidget(self.web_server_url)
        web_server_layout.addWidget(QLabel("Port:"))
        web_server_layout.addWidget(self.web_server_port)
        web_server_layout.addWidget(QLabel("Serving Directory:"))
        web_server_layout.addWidget(self.web_server_path)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_server_btn)
        btn_layout.addWidget(self.stop_server_btn)
        web_server_layout.addLayout(btn_layout)
        
        web_server_widget.setLayout(web_server_layout)
        self.monitor_tabs.addTab(web_server_widget, "🌐 Web Server")
        
        layout.addWidget(self.monitor_tabs)
        self.setLayout(layout)
        
        # Web server instance
        self.web_server_process = None
    
    def setup_monitoring(self):
        """Setup real-time monitoring"""
        # Connect web server buttons
        self.start_server_btn.clicked.connect(self.start_web_server)
        self.stop_server_btn.clicked.connect(self.stop_web_server)
        
        # Timer for system metrics updates
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self.update_metrics)
        self.metrics_timer.start(1000)  # Update every second
    
    def start_web_server(self):
        """Start local web server for HLS/DASH content"""
        import subprocess
        import os
        
        port = self.web_server_port.value()
        path = self.web_server_path.text().strip()
        
        if not path:
            self.web_server_status.setText("❌ Error: Please specify serving directory")
            self.web_server_status.setStyleSheet("padding: 10px; border: 2px solid #f44336; border-radius: 4px; background-color: #3a3a3a;")
            return
        
        # Check if directory exists
        if not os.path.exists(path):
            self.web_server_status.setText(f"❌ Error: Directory '{path}' not found")
            self.web_server_status.setStyleSheet("padding: 10px; border: 2px solid #f44336; border-radius: 4px; background-color: #3a3a3a;")
            return
        
        # Start web server using the embedded serve_hls.py script
        # For production, we'll use a simple embedded server
        try:
            # Create embedded server code
            server_code = f'''
import http.server
import socketserver
import os

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def log_message(self, format, *args):
        pass

os.chdir(r"{path}")
Handler = CORSRequestHandler
with socketserver.TCPServer(("", {port}), Handler) as httpd:
    httpd.serve_forever()
'''
            
            # Save server script
            server_script = f"{path}/_server_{port}.py"
            with open(server_script, 'w') as f:
                f.write(server_code)
            
            # Start server in background
            self.web_server_process = subprocess.Popen(
                ["python", server_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=path
            )
            
            self.web_server_status.setText(f"✅ Web Server: Running on http://localhost:{port}")
            self.web_server_status.setStyleSheet("padding: 10px; border: 2px solid #4CAF50; border-radius: 4px; background-color: #2a3a2a;")
            self.start_server_btn.setEnabled(False)
            self.stop_server_btn.setEnabled(True)
            self.web_server_url.setText(f"http://localhost:{port}")
            
        except Exception as e:
            self.web_server_status.setText(f"❌ Error: {str(e)}")
            self.web_server_status.setStyleSheet("padding: 10px; border: 2px solid #f44336; border-radius: 4px; background-color: #3a3a3a;")
    
    def stop_web_server(self):
        """Stop local web server"""
        if self.web_server_process:
            try:
                self.web_server_process.terminate()
                self.web_server_process.wait(timeout=2)
            except:
                self.web_server_process.kill()
            finally:
                self.web_server_process = None
        
        self.web_server_status.setText("🌐 Web Server: Stopped")
        self.web_server_status.setStyleSheet("padding: 10px; border: 2px solid #444; border-radius: 4px; background-color: #3a3a3a;")
        self.start_server_btn.setEnabled(True)
        self.stop_server_btn.setEnabled(False)
        
        # SCTE-35 monitoring
        self.scte35_timer = QTimer()
        self.scte35_timer.timeout.connect(self.update_scte35_status)
        self.scte35_timer.start(2000)  # Update every 2 seconds
    
    def update_metrics(self):
        """Update system metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used / (1024**3)  # GB
            memory_total = memory.total / (1024**3)  # GB
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used = disk.used / (1024**3)  # GB
            disk_total = disk.total / (1024**3)  # GB
            
            metrics_text = f"""
═══════════════════════════════════════════════════
           SYSTEM METRICS (Real-time)
═══════════════════════════════════════════════════

CPU Usage:      {cpu_percent}%

Memory Usage:   {memory_percent}%
                Used: {memory_used:.2f} GB / {memory_total:.2f} GB

Disk Usage:     {disk_percent}%
                Used: {disk_used:.2f} GB / {disk_total:.2f} GB

═══════════════════════════════════════════════════
"""
            self.system_metrics.setText(metrics_text)
        except Exception as e:
            self.system_metrics.setText(f"Error updating metrics: {e}")
    
    def update_scte35_status(self):
        """Update SCTE-35 monitoring status"""
        try:
            from pathlib import Path
            from datetime import datetime
            
            markers_dir = Path("scte35_final")
            
            if not markers_dir.exists():
                status = "[ERROR] No markers directory found"
                self.scte35_monitor.setText(f"<pre style='color: #f44336;'>{status}</pre>")
                return
            
            xml_files = list(markers_dir.glob("*.xml"))
            
            if not xml_files:
                status = "[WARNING] No SCTE-35 markers found. Generate markers from the SCTE-35 tab."
                self.scte35_monitor.setText(f"<pre style='color: #ff9800;'>{status}</pre>")
                return
            
            # Get latest marker
            latest_file = max(xml_files, key=lambda f: f.stat().st_mtime)
            latest_time = datetime.fromtimestamp(latest_file.stat().st_mtime)
            
            status = f"""
═══════════════════════════════════════════════════
          SCTE-35 MARKER STATUS (Real-time)
═══════════════════════════════════════════════════

Total Markers:      {len(xml_files)}
Latest Marker:      {latest_file.name}
Last Modified:      {latest_time.strftime('%Y-%m-%d %H:%M:%S')}
Marker Directory:   {markers_dir.absolute()}

═══════════════════════════════════════════════════

[INFO] SCTE-35 monitoring active...
[INFO] Ready to inject markers into stream

═══════════════════════════════════════════════════
"""
            self.scte35_monitor.setText(f"<pre style='color: #4CAF50;'>{status}</pre>")
            
        except Exception as e:
            status = f"[ERROR] SCTE-35 monitoring error: {e}"
            self.scte35_monitor.setText(f"<pre style='color: #f44336;'>{status}</pre>")
    
    def append(self, text):
        self.console.append(text)


class MainWindow(QMainWindow):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        self.processor = None
        self.latest_marker = None
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        self.setWindowTitle("ITAssist Broadcast Encoder - 100 (IBE-100) v2.0")
        self.setMinimumSize(800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header with Logo
        header_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_path = Path("logo.png")
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            logo_label.setText("🏠")
            logo_label.setStyleSheet("font-size: 40px;")
        
        # Title
        title_label = QLabel("ITAssist Broadcast Encoder - 100")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50;")
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; background-color: #2a2a2a; }
            QTabBar::tab { background-color: #3a3a3a; color: white; padding: 10px 20px; }
            QTabBar::tab:selected { background-color: #4CAF50; }
        """)
        
        # Stream Configuration Tab
        self.config_widget = StreamConfigWidget()
        self.tab_widget.addTab(self.config_widget, "⚙️ Configuration")
        
        # SCTE-35 Tab
        self.scte35_widget = SCTE35Widget()
        self.tab_widget.addTab(self.scte35_widget, "🎬 SCTE-35")
        
        # Monitoring Tab
        self.monitoring_widget = MonitoringWidget()
        self.tab_widget.addTab(self.monitoring_widget, "📊 Monitoring")
        
        main_layout.addWidget(self.tab_widget)
        
        # Control Buttons
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️ Start Processing")
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 10px;")
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.stop_btn)
        
        self.preview_btn = QPushButton("🔍 Preview Command")
        self.preview_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 10px;")
        control_layout.addWidget(self.preview_btn)
        
        self.save_btn = QPushButton("💾 Save Config")
        self.save_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px;")
        control_layout.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("📁 Load Config")
        self.load_btn.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; padding: 10px;")
        control_layout.addWidget(self.load_btn)
        
        control_layout.addStretch()
        main_layout.addLayout(control_layout)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(10, 5, 10, 5)
        
        # Left side - Company info
        company_label = QLabel("© 2024 ITAssist Broadcast Solutions | Dubai • Mumbai • Gurugram")
        company_label.setStyleSheet("color: #888; font-size: 10px;")
        footer_layout.addWidget(company_label)
        
        # Right side - Version
        version_label = QLabel("IBE-100 v2.0")
        version_label.setStyleSheet("color: #4CAF50; font-size: 11px; font-weight: bold;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        footer_layout.addWidget(version_label)
        
        footer_widget = QWidget()
        footer_widget.setLayout(footer_layout)
        footer_widget.setStyleSheet("background-color: #1a1a1a; border-top: 1px solid #444;")
        main_layout.addWidget(footer_widget)
        
        central_widget.setLayout(main_layout)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                color: #ffffff;
                background-color: #2a2a2a;
            }
            QLineEdit {
                color: #000000;
                background-color: #ffffff;
                border: 2px solid #555;
                border-radius: 4px;
                padding: 5px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QSpinBox {
                color: #000000;
                background-color: #ffffff;
                border: 2px solid #555;
                border-radius: 4px;
                padding: 5px;
                font-size: 13px;
            }
            QGroupBox {
                border: 2px solid #444;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLabel {
                color: #ffffff;
                font-size: 13px;
            }
        """)
    
    def setup_connections(self):
        self.start_btn.clicked.connect(self.start_processing)
        self.stop_btn.clicked.connect(self.stop_processing)
        self.preview_btn.clicked.connect(self.preview_command)
        self.scte35_widget.marker_generated.connect(self.on_marker_generated)
    
    def on_marker_generated(self, xml_file: str, json_file: str):
        """Handle marker generation"""
        self.latest_marker = xml_file
        self.monitoring_widget.append(f"[INFO] Marker generated: {xml_file}")
        print(f"[INFO] Latest marker set to: {xml_file}")
    
    def get_latest_marker(self) -> str:
        """Get the latest SCTE-35 marker file - DYNAMIC, NO hardcoded fallback"""
        from pathlib import Path
        from datetime import datetime
        
        # Look for scte35_final directory
        markers_dir = Path("scte35_final")
        
        if not markers_dir.exists():
            return "ERROR: No markers directory found. Generate a marker first."
        
        # Find all XML marker files
        xml_files = list(markers_dir.glob("*.xml"))
        
        if not xml_files:
            return "ERROR: No marker files found. Generate a marker first."
        
        # Get the latest file by modification time
        latest_file = max(xml_files, key=lambda f: f.stat().st_mtime)
        print(f"[INFO] Selected marker: {latest_file.name}")
        
        # Return relative path for TSDuck
        return str(latest_file)
    
    def build_command(self):
        """Build complete TSDuck command with all distributor requirements"""
        config = self.config_widget.get_config()
        marker = self.get_latest_marker()
        
        # Get values from config
        input_type = config.get("input_type", "HLS (HTTP Live Streaming)")
        input_url = config.get("input_url", "https://cdn.example.com/stream/index.m3u8")
        output_type = config.get("output_type", "SRT")
        output_srt = config.get("output_srt", "cdn.example.com:8888")
        output_hls = config.get("output_hls", "output/hls")
        output_dash = config.get("output_dash", "output/dash")
        enable_cors = config.get("enable_cors", True)
        segment_duration = config.get("segment_duration", 6)
        playlist_window = config.get("playlist_window", 5)
        service_id = config.get("service_id", 1)
        service_name = config.get("service_name", "SCTE-35 Stream")
        provider_name = config.get("provider_name", "ITAssist")
        vpid = config.get("vpid", 256)
        apid = config.get("apid", 257)
        scte35_pid = config.get("scte35_pid", 500)
        stream_id = config.get("stream_id", "#!::r=scte/scte,m=publish")
        latency = config.get("latency", 2000)
        start_delay = config.get("start_delay", 2000)
        inject_count = config.get("inject_count", 1)
        inject_interval = config.get("inject_interval", 1000)
        
        # Determine input plugin based on input type
        input_plugin_map = {
            "HLS (HTTP Live Streaming)": "hls",
            "SRT (Secure Reliable Transport)": "srt",
            "UDP (User Datagram Protocol)": "ip",
            "TCP (Transmission Control Protocol)": "tcp",
            "HTTP/HTTPS": "http",
            "DVB": "dvb",
            "ASI": "asi"
        }
        
        input_plugin = input_plugin_map.get(input_type, "hls")
        
        # Start building command
        command = [
            TSDUCK_PATH,
            "-I", input_plugin, input_url,
            # SDT Plugin - Service Description Table
            "-P", "sdt",
            "--service", str(service_id),
            "--name", service_name,
            "--provider", provider_name,
            # Remap PIDs
            "-P", "remap", f"211={vpid}", f"221={apid}",
            # PMT Plugin - Program Map Table
            "-P", "pmt",
            "--service", str(service_id),
            "--add-pid", f"{vpid}/0x1b",  # Video PID
            "--add-pid", f"{apid}/0x0f",  # Audio PID
            "--add-pid", f"{scte35_pid}/0x86",  # SCTE-35 PID
            # SpliceInject Plugin
            "-P", "spliceinject",
            "--pid", str(scte35_pid),
            "--pts-pid", str(vpid),
            "--files", marker,
            "--inject-count", str(inject_count),
            "--inject-interval", str(inject_interval),
            "--start-delay", str(start_delay),
            # Output based on type
        ]
        
        # Add output based on selected output type
        if output_type == "SRT":
            output_args = ["-O", "srt", "--caller", output_srt, "--streamid", stream_id, "--latency", str(latency)]
        elif output_type == "HLS":
            output_args = ["-O", "hls", "--live", output_hls, "--segment-duration", str(segment_duration), "--playlist-window", str(playlist_window)]
            if enable_cors:
                output_args.extend(["--cors", "*"])
        elif output_type == "DASH":
            output_args = ["-O", "hls", "--live", output_dash, "--dash", "--segment-duration", str(segment_duration), "--playlist-window", str(playlist_window)]
            if enable_cors:
                output_args.extend(["--cors", "*"])
        elif output_type == "UDP":
            output_args = ["-O", "ip", output_srt]
        elif output_type == "TCP":
            output_args = ["-O", "tcp", output_srt]
        elif output_type == "HTTP/HTTPS":
            output_args = ["-O", "http", output_srt]
            if enable_cors:
                output_args.extend(["--cors", "*"])
        else:  # File
            output_args = ["-O", "file", output_srt]
        
        command.extend(output_args)
        
        return command
    
    def preview_command(self):
        """Preview the TSDuck command"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("TSDuck Command Preview")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        marker = self.get_latest_marker()
        info = QLabel(f"📌 Marker: {marker}\n\nTSDuck Command:")
        info.setStyleSheet("font-weight: bold; color: #4CAF50;")
        layout.addWidget(info)
        
        cmd_text = QTextEdit()
        cmd_text.setReadOnly(True)
        cmd_text.setFont(QFont("Courier", 9))
        cmd_text.setStyleSheet("background-color: #1e1e1e; color: #ffffff; padding: 10px;")
        
        command = self.build_command()
        cmd_text.setText(" ".join(command))
        layout.addWidget(cmd_text)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def start_processing(self):
        """Start processing with TSDuck"""
        import subprocess
        import threading
        
        config = self.config_widget.get_config()
        marker = self.get_latest_marker()
        
        if "ERROR" in marker:
            self.monitoring_widget.append(f"[ERROR] {marker}")
            return
        
        self.monitoring_widget.append(f"[INFO] Starting processing...")
        self.monitoring_widget.append(f"[INFO] Using marker: {marker}")
        
        command = self.build_command()
        cmd_str = ' '.join(command)
        self.monitoring_widget.append(f"[INFO] TSDuck Command: {cmd_str}")
        
        # Start TSDuck process in background thread
        def run_tsp():
            try:
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                self.processor = process
                
                # Read output line by line
                for line in process.stdout:
                    self.monitoring_widget.append(f"[TSDuck] {line.strip()}")
                
                process.wait()
                self.monitoring_widget.append(f"[INFO] TSDuck process finished with code: {process.returncode}")
                
            except Exception as e:
                self.monitoring_widget.append(f"[ERROR] Stream error: {e}")
        
        # Run in background thread
        thread = threading.Thread(target=run_tsp, daemon=True)
        thread.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
    
    def stop_processing(self):
        """Stop TSDuck processing"""
        if self.processor:
            self.monitoring_widget.append("[INFO] Stopping TSDuck process...")
            try:
                self.processor.terminate()
                self.processor.wait(timeout=5)
            except:
                self.processor.kill()
            self.processor = None
            self.monitoring_widget.append("[INFO] Processing stopped.")
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
