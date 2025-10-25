#!/usr/bin/env python3
"""
ITAssist Broadcast Encoder - 100 (IBE-100)
Professional SCTE-35 Streaming Solution for Distributors
"""

import sys
import os
import json
import subprocess
import threading
import time
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QTabWidget, QGroupBox, QLabel, QLineEdit, QPushButton,
    QComboBox, QSpinBox, QCheckBox, QTextEdit, QProgressBar,
    QFileDialog, QMessageBox, QSplitter, QFrame, QScrollArea, QTableWidget
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QSettings, QSize
)
from PyQt6.QtGui import (
    QFont, QIcon, QPalette, QColor, QAction, QKeySequence
)


class TSDuckProcessor(QThread):
    """Thread for running TSDuck commands"""
    output_received = pyqtSignal(str)
    error_received = pyqtSignal(str)
    finished = pyqtSignal(int)
    progress_updated = pyqtSignal(int)
    
    def __init__(self, command: List[str]):
        super().__init__()
        self.command = command
        self.process = None
        self._stop_requested = False
        
    def run(self):
        """Execute the TSDuck command"""
        try:
            # Run command without redirecting stdout/stderr to allow direct streaming
            # This is crucial for SRT connections to work properly
            self.process = subprocess.Popen(
                self.command,
                stdout=None,  # Let output go to terminal
                stderr=None,  # Let errors go to terminal
                text=True
            )
            
            # Wait for process to complete or be stopped
            while True:
                if self._stop_requested:
                    if self.process:
                        self.process.terminate()
                    break
                    
                if self.process.poll() is not None:
                    break
                    
                # Small delay to prevent busy waiting
                self.msleep(100)
                
            # Get return code
            return_code = self.process.returncode if self.process else 1
            self.finished.emit(return_code)
            
        except Exception as e:
            self.error_received.emit(f"Error executing command: {str(e)}")
            self.finished.emit(1)
    
    def stop(self):
        """Stop the process"""
        self._stop_requested = True
        if self.process:
            self.process.terminate()


class InputWidget(QWidget):
    """Input configuration widget"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("📡 Input Configuration")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Input group
        input_group = QGroupBox("Input Settings")
        layout = QGridLayout()
        
        # Input type
        layout.addWidget(QLabel("Type:"), 0, 0)
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "HLS", "UDP", "TCP", "File", "SRT", "HTTP", "HTTPS", "DVB", "ASI", 
            "Dektec", "Play", "Duck", "Memory", "Fork", "TSP", "TS", "TSFile",
            "DVB-S", "DVB-T", "DVB-C", "ATSC", "ISDB-T", "DMB-T", "CMMB"
        ])
        self.type_combo.setCurrentText("HLS")
        self.type_combo.setStyleSheet("font-size: 14px; padding: 8px;")
        layout.addWidget(self.type_combo, 0, 1)
        
        # Source URL
        layout.addWidget(QLabel("Source:"), 1, 0)
        self.source_edit = QLineEdit()
        self.source_edit.setText("https://cdn.itassist.one/BREAKING/NEWS/index.m3u8")
        self.source_edit.setPlaceholderText("Enter input source URL or file path")
        self.source_edit.setStyleSheet("font-size: 13px; padding: 10px;")
        layout.addWidget(self.source_edit, 1, 1)
        
        # Input format descriptions
        format_info = QLabel("""
📡 Input Format Examples:
• HLS: https://example.com/stream.m3u8
• UDP: 127.0.0.1:9999
• TCP: 127.0.0.1:9999  
• SRT: srt://host:port
• File: /path/to/file.ts
• HTTP: http://example.com/stream.ts
• DVB: dvb://frequency:polarization
• ASI: /dev/asi0
• Dektec: dtapi://device
        """)
        format_info.setStyleSheet("font-size: 11px; color: #888; padding: 10px; background-color: #1a1a1a; border-radius: 5px;")
        format_info.setWordWrap(True)
        layout.addWidget(format_info, 2, 0, 1, 2)
        
        # Parameters
        layout.addWidget(QLabel("Parameters:"), 3, 0)
        self.params_edit = QLineEdit()
        self.params_edit.setPlaceholderText("Additional input parameters (optional)")
        self.params_edit.setStyleSheet("font-size: 13px; padding: 10px;")
        layout.addWidget(self.params_edit, 3, 1)
        
        input_group.setLayout(layout)
        main_layout.addWidget(input_group)
        
        # Add stretch
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def get_config(self) -> Dict[str, str]:
        """Get input configuration"""
        return {
            "type": self.type_combo.currentText().lower(),
            "source": self.source_edit.text(),
            "params": self.params_edit.text()
        }


class OutputWidget(QWidget):
    """Output configuration widget"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("📤 Output Configuration")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Output group
        output_group = QGroupBox("Output Settings")
        layout = QGridLayout()
        
        # Output type
        layout.addWidget(QLabel("Type:"), 0, 0)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["SRT", "UDP", "TCP", "File", "HLS"])
        self.type_combo.setCurrentText("SRT")
        self.type_combo.setStyleSheet("font-size: 14px; padding: 8px;")
        layout.addWidget(self.type_combo, 0, 1)
        
        # Destination
        layout.addWidget(QLabel("Destination:"), 1, 0)
        self.dest_edit = QLineEdit()
        self.dest_edit.setText("srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish")
        self.dest_edit.setPlaceholderText("Enter output destination")
        self.dest_edit.setStyleSheet("font-size: 13px; padding: 10px;")
        layout.addWidget(self.dest_edit, 1, 1)
        
        # Parameters
        layout.addWidget(QLabel("Parameters:"), 2, 0)
        self.params_edit = QLineEdit()
        self.params_edit.setText("--streamid '#!::r=scte/scte,m=publish' --latency 2000")
        self.params_edit.setPlaceholderText("Additional output parameters")
        self.params_edit.setStyleSheet("font-size: 13px; padding: 10px;")
        layout.addWidget(self.params_edit, 2, 1)
        
        output_group.setLayout(layout)
        main_layout.addWidget(output_group)
        
        # Add stretch
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def get_config(self) -> Dict[str, str]:
        """Get output configuration"""
        return {
            "type": self.type_combo.currentText().lower(),
            "destination": self.dest_edit.text(),
            "params": self.params_edit.text()
        }


class SCTE35Widget(QWidget):
    """SCTE-35 configuration widget with sub-tabs"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("🎬 SCTE-35 Configuration")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Distributor specifications info
        info_label = QLabel("📺 DISTRIBUTOR SPECIFICATIONS: HD 1920x1080, H.264, AAC-LC, SCTE-35 PID 500")
        info_label.setStyleSheet("color: #4CAF50; font-size: 12px; margin: 5px; background-color: #2a2a2a; padding: 8px; border-radius: 4px;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(info_label)
        
        # Create sub-tab widget
        self.sub_tabs = QTabWidget()
        
        # Service & PIDs Tab with Scroll Area
        service_tab = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        scroll_content = QWidget()
        service_layout = QVBoxLayout(scroll_content)
        
        # Distributor Specifications Section - Better Layout
        specs_group = QGroupBox("📺 Distributor Stream Specifications")
        specs_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; margin: 10px; }")
        specs_layout = QVBoxLayout()
        
        # Video Specifications Section
        video_section = QHBoxLayout()
        
        video_left = QVBoxLayout()
        video_left.addWidget(QLabel("📺 VIDEO SPECIFICATIONS"))
        video_left.addWidget(QLabel("Resolution: 1920x1080 HD"))
        video_left.addWidget(QLabel("Codec: H.264"))
        video_left.addWidget(QLabel("Bitrate: 5 Mbps"))
        video_left.addWidget(QLabel("GOP: 12"))
        video_left.addWidget(QLabel("B-Frames: 5"))
        video_left.addWidget(QLabel("Chroma: 4:2:0"))
        video_left.addWidget(QLabel("Aspect Ratio: 16:9"))
        
        video_right = QVBoxLayout()
        video_right.addWidget(QLabel("🎵 AUDIO SPECIFICATIONS"))
        video_right.addWidget(QLabel("Codec: AAC-LC"))
        video_right.addWidget(QLabel("Bitrate: 128 Kbps"))
        video_right.addWidget(QLabel("LKFS: -20 db"))
        video_right.addWidget(QLabel("Sample Rate: 48 Khz"))
        video_right.addWidget(QLabel("PCR: Video Embedded"))
        video_right.addWidget(QLabel("Profile@Level: High@Auto"))
        video_right.addWidget(QLabel("Latency: 2000 ms"))
        
        video_section.addLayout(video_left)
        video_section.addLayout(video_right)
        
        specs_layout.addLayout(video_section)
        specs_group.setLayout(specs_layout)
        service_layout.addWidget(specs_group)
        
        # Service Information Section - Consistent with Plugin Tab
        service_group = QGroupBox("📋 Service Information")
        service_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; margin: 10px; }")
        service_layout_inner = QVBoxLayout()
        
        # Service Name
        service_name_layout = QHBoxLayout()
        service_name_label = QLabel("📺 Service Name:")
        service_name_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        service_name_layout.addWidget(service_name_label)
        self.service_name = QLineEdit()
        self.service_name.setText("SCTE-35 Stream")
        self.service_name.setStyleSheet("font-size: 13px; padding: 10px;")
        service_name_layout.addWidget(self.service_name)
        service_name_layout.addStretch()
        service_layout_inner.addLayout(service_name_layout)
        
        # Provider Name
        provider_layout = QHBoxLayout()
        provider_label = QLabel("🏢 Provider Name:")
        provider_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        provider_layout.addWidget(provider_label)
        self.provider_name = QLineEdit()
        self.provider_name.setText("ITAssist")
        self.provider_name.setStyleSheet("font-size: 13px; padding: 10px;")
        provider_layout.addWidget(self.provider_name)
        provider_layout.addStretch()
        service_layout_inner.addLayout(provider_layout)
        
        # Service ID
        service_id_layout = QHBoxLayout()
        service_id_label = QLabel("🆔 Service ID:")
        service_id_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        service_id_layout.addWidget(service_id_label)
        self.service_id = QSpinBox()
        self.service_id.setRange(1, 65535)
        self.service_id.setValue(1)
        self.service_id.setStyleSheet("font-size: 13px; padding: 10px;")
        service_id_layout.addWidget(self.service_id)
        service_id_layout.addStretch()
        service_layout_inner.addLayout(service_id_layout)
        
        # Bouquet ID
        bouquet_id_layout = QHBoxLayout()
        bouquet_id_label = QLabel("📺 Bouquet ID:")
        bouquet_id_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        bouquet_id_layout.addWidget(bouquet_id_label)
        self.bouquet_id = QSpinBox()
        self.bouquet_id.setRange(1, 65535)
        self.bouquet_id.setValue(1)
        self.bouquet_id.setStyleSheet("font-size: 13px; padding: 10px;")
        bouquet_id_layout.addWidget(self.bouquet_id)
        bouquet_id_layout.addStretch()
        service_layout_inner.addLayout(bouquet_id_layout)
        
        # Original Network ID
        onid_layout = QHBoxLayout()
        onid_label = QLabel("🌐 Original Network ID:")
        onid_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        onid_layout.addWidget(onid_label)
        self.original_network_id = QSpinBox()
        self.original_network_id.setRange(1, 65535)
        self.original_network_id.setValue(1)
        self.original_network_id.setStyleSheet("font-size: 13px; padding: 10px;")
        onid_layout.addWidget(self.original_network_id)
        onid_layout.addStretch()
        service_layout_inner.addLayout(onid_layout)
        
        # Transport Stream ID
        tsid_layout = QHBoxLayout()
        tsid_label = QLabel("📡 Transport Stream ID:")
        tsid_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        tsid_layout.addWidget(tsid_label)
        self.transport_stream_id = QSpinBox()
        self.transport_stream_id.setRange(1, 65535)
        self.transport_stream_id.setValue(1)
        self.transport_stream_id.setStyleSheet("font-size: 13px; padding: 10px;")
        tsid_layout.addWidget(self.transport_stream_id)
        tsid_layout.addStretch()
        service_layout_inner.addLayout(tsid_layout)
        
        service_group.setLayout(service_layout_inner)
        service_layout.addWidget(service_group)
        
        # PID Configuration Section - Consistent with Plugin Tab
        pid_group = QGroupBox("🔧 PID Configuration")
        pid_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; margin: 10px; }")
        pid_layout = QVBoxLayout()
        
        # Video PID
        vpid_layout = QHBoxLayout()
        vpid_label = QLabel("📺 Video PID (VPID):")
        vpid_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        vpid_layout.addWidget(vpid_label)
        self.vpid = QSpinBox()
        self.vpid.setRange(32, 8190)
        self.vpid.setValue(256)
        self.vpid.setStyleSheet("font-size: 13px; padding: 10px;")
        self.vpid.setToolTip("Video stream PID - Set according to distributor requirements")
        vpid_layout.addWidget(self.vpid)
        vpid_layout.addStretch()
        pid_layout.addLayout(vpid_layout)
        
        # Audio PID
        apid_layout = QHBoxLayout()
        apid_label = QLabel("🎵 Audio PID (APID):")
        apid_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        apid_layout.addWidget(apid_label)
        self.apid = QSpinBox()
        self.apid.setRange(32, 8190)
        self.apid.setValue(257)
        self.apid.setStyleSheet("font-size: 13px; padding: 10px;")
        self.apid.setToolTip("Audio stream PID - Set according to distributor requirements")
        apid_layout.addWidget(self.apid)
        apid_layout.addStretch()
        pid_layout.addLayout(apid_layout)
        
        # SCTE-35 PID
        scte35_layout = QHBoxLayout()
        scte35_label = QLabel("🎬 SCTE-35 PID:")
        scte35_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        scte35_layout.addWidget(scte35_label)
        self.scte35_pid = QSpinBox()
        self.scte35_pid.setRange(32, 8190)
        self.scte35_pid.setValue(500)
        self.scte35_pid.setStyleSheet("font-size: 13px; padding: 10px;")
        self.scte35_pid.setToolTip("SCTE-35 stream PID - Set according to distributor requirements")
        scte35_layout.addWidget(self.scte35_pid)
        scte35_layout.addStretch()
        pid_layout.addLayout(scte35_layout)
        
        # Null PID
        null_layout = QHBoxLayout()
        null_label = QLabel("⚫ Null PID:")
        null_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        null_layout.addWidget(null_label)
        self.null_pid = QSpinBox()
        self.null_pid.setRange(0, 8191)
        self.null_pid.setValue(8191)
        self.null_pid.setStyleSheet("font-size: 13px; padding: 10px;")
        self.null_pid.setToolTip("Null stream PID - Set according to distributor requirements")
        null_layout.addWidget(self.null_pid)
        null_layout.addStretch()
        pid_layout.addLayout(null_layout)
        
        # PCR PID
        pcr_layout = QHBoxLayout()
        pcr_label = QLabel("⏰ PCR PID:")
        pcr_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        pcr_layout.addWidget(pcr_label)
        self.pcr_pid = QSpinBox()
        self.pcr_pid.setRange(32, 8190)
        self.pcr_pid.setValue(256)
        self.pcr_pid.setStyleSheet("font-size: 13px; padding: 10px;")
        self.pcr_pid.setToolTip("PCR stream PID - Set according to distributor requirements")
        pcr_layout.addWidget(self.pcr_pid)
        pcr_layout.addStretch()
        pid_layout.addLayout(pcr_layout)
        
        pid_group.setLayout(pid_layout)
        service_layout.addWidget(pid_group)
        
        # SCTE-35 Configuration Section - Consistent with Plugin Tab
        scte_group = QGroupBox("🎬 SCTE-35 Configuration")
        scte_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; margin: 10px; }")
        scte_layout = QVBoxLayout()
        
        # Ad Duration
        ad_duration_layout = QHBoxLayout()
        ad_duration_label = QLabel("⏱️ Ad Duration (seconds):")
        ad_duration_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        ad_duration_layout.addWidget(ad_duration_label)
        self.ad_duration = QSpinBox()
        self.ad_duration.setRange(1, 3600)
        self.ad_duration.setValue(600)
        self.ad_duration.setStyleSheet("font-size: 13px; padding: 10px;")
        self.ad_duration.setToolTip("Ad duration in seconds (default: 600)")
        ad_duration_layout.addWidget(self.ad_duration)
        ad_duration_layout.addStretch()
        scte_layout.addLayout(ad_duration_layout)
        
        # Event ID
        event_id_layout = QHBoxLayout()
        event_id_label = QLabel("🆔 SCTE Event ID:")
        event_id_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        event_id_layout.addWidget(event_id_label)
        self.event_id = QSpinBox()
        self.event_id.setRange(1, 999999)
        self.event_id.setValue(100023)
        self.event_id.setStyleSheet("font-size: 13px; padding: 10px;")
        self.event_id.setToolTip("Unique SCTE Event ID (increments sequentially)")
        event_id_layout.addWidget(self.event_id)
        event_id_layout.addStretch()
        scte_layout.addLayout(event_id_layout)
        
        # Pre-roll Duration
        preroll_layout = QHBoxLayout()
        preroll_label = QLabel("⏰ Pre-roll Duration (0-10s):")
        preroll_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 120px;")
        preroll_layout.addWidget(preroll_label)
        self.preroll_duration = QSpinBox()
        self.preroll_duration.setRange(0, 10)
        self.preroll_duration.setValue(0)
        self.preroll_duration.setStyleSheet("font-size: 13px; padding: 10px;")
        self.preroll_duration.setToolTip("Pre-roll ad duration in seconds (0-10)")
        preroll_layout.addWidget(self.preroll_duration)
        preroll_layout.addStretch()
        scte_layout.addLayout(preroll_layout)
        
        # CUE Information
        cue_info = QLabel("🎯 CUE Information:")
        cue_info.setStyleSheet("font-size: 13px; font-weight: bold; margin-top: 10px;")
        scte_layout.addWidget(cue_info)
        
        cue_info_text = QLabel("🟢 CUE-OUT: Program Out Point\n🔴 CUE-IN: Program In Point\n⚡ Crash Out: Emergency CUE-IN")
        cue_info_text.setStyleSheet("font-size: 12px; color: #ffffff; padding: 10px; background-color: #1a1a1a; border-radius: 5px;")
        scte_layout.addWidget(cue_info_text)
        
        scte_group.setLayout(scte_layout)
        service_layout.addWidget(scte_group)
        
        service_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        
        service_tab_layout = QVBoxLayout(service_tab)
        service_tab_layout.addWidget(scroll_area)
        self.sub_tabs.addTab(service_tab, "📋 Service & PIDs")
        
        # Plugins Tab
        plugins_tab = QWidget()
        plugins_layout = QVBoxLayout()
        
        # PMT Plugin Section
        pmt_group = QGroupBox("PMT Plugin")
        pmt_layout = QVBoxLayout()
        
        self.pmt_enabled = QCheckBox("Enable PMT Plugin")
        self.pmt_enabled.setChecked(True)
        self.pmt_enabled.setStyleSheet("font-size: 14px; font-weight: bold;")
        pmt_layout.addWidget(self.pmt_enabled)
        
        pmt_params_layout = QHBoxLayout()
        pmt_params_layout.addWidget(QLabel("Custom Parameters (optional):"))
        self.pmt_params = QLineEdit()
        self.pmt_params.setPlaceholderText("Leave empty to use defaults, or specify custom PMT parameters")
        self.pmt_params.setStyleSheet("font-size: 13px; padding: 10px;")
        pmt_params_layout.addWidget(self.pmt_params)
        pmt_layout.addLayout(pmt_params_layout)
        
        pmt_group.setLayout(pmt_layout)
        plugins_layout.addWidget(pmt_group)
        
        # SpliceInject Plugin Section
        splice_group = QGroupBox("SpliceInject Plugin")
        splice_layout = QVBoxLayout()
        
        self.spliceinject_enabled = QCheckBox("Enable SpliceInject Plugin")
        self.spliceinject_enabled.setChecked(True)
        self.spliceinject_enabled.setStyleSheet("font-size: 14px; font-weight: bold;")
        splice_layout.addWidget(self.spliceinject_enabled)
        
        splice_params_layout = QHBoxLayout()
        splice_params_layout.addWidget(QLabel("Custom Parameters (optional):"))
        self.spliceinject_params = QLineEdit()
        self.spliceinject_params.setPlaceholderText("Leave empty to use defaults, or specify custom SpliceInject parameters")
        self.spliceinject_params.setStyleSheet("font-size: 13px; padding: 10px;")
        splice_params_layout.addWidget(self.spliceinject_params)
        splice_layout.addLayout(splice_params_layout)
        
        splice_group.setLayout(splice_layout)
        plugins_layout.addWidget(splice_group)
        
        plugins_layout.addStretch()
        plugins_tab.setLayout(plugins_layout)
        self.sub_tabs.addTab(plugins_tab, "🔧 Plugins")
        
        # Markers Tab
        markers_tab = QWidget()
        markers_layout = QVBoxLayout()
        
        markers_group = QGroupBox("Available SCTE-35 Markers")
        markers_content = QVBoxLayout()
        
        markers_text = QLabel("""
• cue_out_10021.xml - Ad break start (600s duration)
• cue_in_10022.xml - Return to program  
• preroll_10023.xml - Scheduled ad (600s duration)
• crash_out_10024.xml - Emergency break (30s duration)
        """)
        markers_text.setStyleSheet("color: #888; font-size: 12px; padding: 15px; background-color: #2a2a2a; border-radius: 5px; line-height: 1.6;")
        markers_text.setWordWrap(True)
        markers_content.addWidget(markers_text)
        
        markers_group.setLayout(markers_content)
        markers_layout.addWidget(markers_group)
        
        markers_layout.addStretch()
        markers_tab.setLayout(markers_layout)
        self.sub_tabs.addTab(markers_tab, "📄 Markers")
        
        # Add sub-tabs to main layout
        main_layout.addWidget(self.sub_tabs)
        
        self.setLayout(main_layout)
    
    def get_config(self) -> Dict[str, Any]:
        """Get SCTE-35 configuration"""
        return {
            "service_name": self.service_name.text() or "SCTE-35 Stream",
            "provider_name": self.provider_name.text() or "ITAssist",
            "service_id": self.service_id.value(),
            "bouquet_id": self.bouquet_id.value(),
            "original_network_id": self.original_network_id.value(),
            "transport_stream_id": self.transport_stream_id.value(),
            "vpid": self.vpid.value(),
            "apid": self.apid.value(),
            "scte35_pid": self.scte35_pid.value(),
            "null_pid": self.null_pid.value(),
            "pcr_pid": self.pcr_pid.value(),
            "ad_duration": self.ad_duration.value(),
            "event_id": self.event_id.value(),
            "preroll_duration": self.preroll_duration.value(),
            "pmt_enabled": self.pmt_enabled.isChecked(),
            "pmt_params": self.pmt_params.text(),
            "spliceinject_enabled": self.spliceinject_enabled.isChecked(),
            "spliceinject_params": self.spliceinject_params.text()
        }


class ConfigurationWidget(QWidget):
    """Enterprise Configuration Widget - All settings in one place"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the configuration interface"""
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("⚙️ Enterprise Configuration")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; margin: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Create scroll area for the entire configuration
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Create sub-tabs for different configuration areas
        self.config_tabs = QTabWidget()
        self.config_tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; background-color: #2a2a2a; }
            QTabBar::tab { background-color: #3a3a3a; color: white; padding: 8px 16px; margin-right: 2px; }
            QTabBar::tab:selected { background-color: #4CAF50; }
            QTabBar::tab:hover { background-color: #555; }
        """)
        
        # Input Configuration
        self.input_widget = InputWidget()
        self.config_tabs.addTab(self.input_widget, "📥 Input")
        
        # Output Configuration  
        self.output_widget = OutputWidget()
        self.config_tabs.addTab(self.output_widget, "📤 Output")
        
        # Service Configuration
        self.service_widget = ServiceConfigWidget()
        self.config_tabs.addTab(self.service_widget, "📺 Service")
        
        # SCTE-35 Configuration
        self.scte35_widget = SCTE35Widget()
        self.config_tabs.addTab(self.scte35_widget, "🎬 SCTE-35")
        
        # TSDuck Configuration
        self.tsduck_widget = TSDuckConfigWidget()
        self.config_tabs.addTab(self.tsduck_widget, "🔧 TSDuck")
        
        content_layout.addWidget(self.config_tabs)
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
    
    def get_all_config(self):
        """Get configuration from all tabs"""
        return {
            "input": self.input_widget.get_config(),
            "output": self.output_widget.get_config(),
            "service": self.service_widget.get_config(),
            "scte35": self.scte35_widget.get_config(),
            "tsduck": self.tsduck_widget.get_config()
        }


class TSDuckConfigWidget(QWidget):
    """TSDuck Configuration Widget"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup TSDuck configuration interface"""
        main_layout = QVBoxLayout()
        
        # TSDuck Path Configuration
        tsduck_group = QGroupBox("🔧 TSDuck Binary Configuration")
        tsduck_layout = QGridLayout()
        
        # TSDuck Binary Path
        tsduck_layout.addWidget(QLabel("TSDuck Binary Path:"), 0, 0)
        self.tsduck_path = QLineEdit()
        self.tsduck_path.setPlaceholderText("Enter full path to TSDuck binary (tsp)")
        self.tsduck_path.setStyleSheet("font-size: 13px; padding: 10px;")
        tsduck_layout.addWidget(self.tsduck_path, 0, 1)
        
        # Browse button
        browse_btn = QPushButton("📁 Browse")
        browse_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 8px; font-size: 12px; }")
        browse_btn.clicked.connect(self.browse_tsduck_path)
        tsduck_layout.addWidget(browse_btn, 0, 2)
        
        # Auto-detect button
        detect_btn = QPushButton("🔍 Auto-detect")
        detect_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; font-size: 12px; }")
        detect_btn.clicked.connect(self.auto_detect_tsduck)
        tsduck_layout.addWidget(detect_btn, 0, 3)
        
        # Test button
        test_btn = QPushButton("✅ Test")
        test_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; padding: 8px; font-size: 12px; }")
        test_btn.clicked.connect(self.test_tsduck_path)
        tsduck_layout.addWidget(test_btn, 0, 4)
        
        tsduck_group.setLayout(tsduck_layout)
        main_layout.addWidget(tsduck_group)
        
        # Platform-specific paths
        platform_group = QGroupBox("💻 Platform-specific Default Paths")
        platform_layout = QVBoxLayout()
        
        platform_info = QLabel("""
        <b>Common TSDuck Installation Paths:</b><br>
        <b>macOS:</b> /usr/local/bin/tsp (Homebrew)<br>
        <b>Linux:</b> /usr/bin/tsp or /usr/local/bin/tsp<br>
        <b>Windows:</b> C:\\Program Files\\TSDuck\\bin\\tsp.exe<br>
        <b>Custom:</b> Enter your specific installation path
        """)
        platform_info.setStyleSheet("font-size: 12px; color: #888; padding: 10px; background-color: #1a1a1a; border-radius: 5px;")
        platform_info.setWordWrap(True)
        platform_layout.addWidget(platform_info)
        
        platform_group.setLayout(platform_layout)
        main_layout.addWidget(platform_group)
        
        # Status display
        status_group = QGroupBox("📊 TSDuck Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Not tested")
        self.status_label.setStyleSheet("font-size: 14px; color: #888;")
        status_layout.addWidget(self.status_label)
        
        self.version_label = QLabel("Version: Unknown")
        self.version_label.setStyleSheet("font-size: 12px; color: #666;")
        status_layout.addWidget(self.version_label)
        
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
        
        # Auto-detect on startup
        self.auto_detect_tsduck()
    
    def browse_tsduck_path(self):
        """Browse for TSDuck binary"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select TSDuck Binary (tsp)", 
            "", 
            "Executable files (*.exe);;All files (*)"
        )
        if file_path:
            self.tsduck_path.setText(file_path)
            self.test_tsduck_path()
    
    def auto_detect_tsduck(self):
        """Auto-detect TSDuck binary path"""
        import shutil
        import platform
        
        # Try common paths
        common_paths = []
        
        if platform.system() == "Windows":
            common_paths = [
                "C:\\Program Files\\TSDuck\\bin\\tsp.exe",
                "C:\\Program Files (x86)\\TSDuck\\bin\\tsp.exe",
                "C:\\tsduck\\bin\\tsp.exe"
            ]
        else:
            common_paths = [
                "/usr/local/bin/tsp",
                "/usr/bin/tsp",
                "/opt/tsduck/bin/tsp",
                "/usr/local/tsduck/bin/tsp"
            ]
        
        # Try shutil.which first
        tsp_path = shutil.which("tsp")
        if tsp_path:
            self.tsduck_path.setText(tsp_path)
            self.test_tsduck_path()
            return
        
        # Try common paths
        for path in common_paths:
            if os.path.exists(path):
                self.tsduck_path.setText(path)
                self.test_tsduck_path()
                return
        
        # If not found, show message
        self.status_label.setText("Status: TSDuck not found - please set path manually")
        self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
    
    def test_tsduck_path(self):
        """Test TSDuck binary path"""
        tsp_path = self.tsduck_path.text().strip()
        if not tsp_path:
            self.status_label.setText("Status: No path specified")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        try:
            import subprocess
            result = subprocess.run([tsp_path, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version_info = result.stdout.strip()
                self.status_label.setText("Status: ✅ TSDuck found and working")
                self.status_label.setStyleSheet("font-size: 14px; color: #4CAF50;")
                self.version_label.setText(f"Version: {version_info}")
            else:
                self.status_label.setText("Status: ❌ TSDuck not working")
                self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
                self.version_label.setText("Version: Error")
        except Exception as e:
            self.status_label.setText(f"Status: ❌ Error: {str(e)}")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            self.version_label.setText("Version: Error")
    
    def get_config(self):
        """Get TSDuck configuration"""
        return {
            "tsduck_path": self.tsduck_path.text().strip() or "tsp"
        }


class ServiceConfigWidget(QWidget):
    """Service Configuration Widget"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup service configuration interface"""
        main_layout = QVBoxLayout()
        
        # Service Information Group
        service_group = QGroupBox("📺 Service Information")
        service_layout = QGridLayout()
        
        # Service Name
        service_layout.addWidget(QLabel("Service Name:"), 0, 0)
        self.service_name = QLineEdit()
        self.service_name.setText("SCTE-35 Stream")
        self.service_name.setStyleSheet("font-size: 13px; padding: 10px;")
        service_layout.addWidget(self.service_name, 0, 1)
        
        # Provider Name
        service_layout.addWidget(QLabel("Provider Name:"), 1, 0)
        self.provider_name = QLineEdit()
        self.provider_name.setText("ITAssist")
        self.provider_name.setStyleSheet("font-size: 13px; padding: 10px;")
        service_layout.addWidget(self.provider_name, 1, 1)
        
        # Service ID
        service_layout.addWidget(QLabel("Service ID:"), 2, 0)
        self.service_id = QSpinBox()
        self.service_id.setRange(1, 65535)
        self.service_id.setValue(1)
        self.service_id.setStyleSheet("font-size: 13px; padding: 10px;")
        service_layout.addWidget(self.service_id, 2, 1)
        
        service_group.setLayout(service_layout)
        main_layout.addWidget(service_group)
        
        # PID Configuration Group
        pid_group = QGroupBox("🔧 PID Configuration")
        pid_layout = QGridLayout()
        
        # Video PID
        pid_layout.addWidget(QLabel("Video PID:"), 0, 0)
        self.vpid = QSpinBox()
        self.vpid.setRange(1, 8191)
        self.vpid.setValue(256)
        self.vpid.setStyleSheet("font-size: 13px; padding: 10px;")
        pid_layout.addWidget(self.vpid, 0, 1)
        
        # Audio PID
        pid_layout.addWidget(QLabel("Audio PID:"), 1, 0)
        self.apid = QSpinBox()
        self.apid.setRange(1, 8191)
        self.apid.setValue(257)
        self.apid.setStyleSheet("font-size: 13px; padding: 10px;")
        pid_layout.addWidget(self.apid, 1, 1)
        
        # SCTE-35 PID
        pid_layout.addWidget(QLabel("SCTE-35 PID:"), 2, 0)
        self.scte35_pid = QSpinBox()
        self.scte35_pid.setRange(1, 8191)
        self.scte35_pid.setValue(500)
        self.scte35_pid.setStyleSheet("font-size: 13px; padding: 10px;")
        pid_layout.addWidget(self.scte35_pid, 2, 1)
        
        # Null PID
        pid_layout.addWidget(QLabel("Null PID:"), 3, 0)
        self.null_pid = QSpinBox()
        self.null_pid.setRange(1, 8191)
        self.null_pid.setValue(8191)
        self.null_pid.setStyleSheet("font-size: 13px; padding: 10px;")
        pid_layout.addWidget(self.null_pid, 3, 1)
        
        # PCR PID
        pid_layout.addWidget(QLabel("PCR PID:"), 4, 0)
        self.pcr_pid = QSpinBox()
        self.pcr_pid.setRange(1, 8191)
        self.pcr_pid.setValue(256)
        self.pcr_pid.setStyleSheet("font-size: 13px; padding: 10px;")
        pid_layout.addWidget(self.pcr_pid, 4, 1)
        
        pid_group.setLayout(pid_layout)
        main_layout.addWidget(pid_group)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def get_config(self):
        """Get service configuration"""
        return {
            "service_name": self.service_name.text() or "SCTE-35 Stream",
            "provider_name": self.provider_name.text() or "ITAssist",
            "service_id": self.service_id.value(),
            "vpid": self.vpid.value(),
            "apid": self.apid.value(),
            "scte35_pid": self.scte35_pid.value(),
            "null_pid": self.null_pid.value(),
            "pcr_pid": self.pcr_pid.value()
        }


class MonitoringWidget(QWidget):
    """Enterprise Monitoring Widget - Real-time analytics and status"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup monitoring interface"""
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("📊 Real-time Monitoring & Analytics")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2196F3; margin: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Create scroll area for monitoring content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Create monitoring tabs
        self.monitor_tabs = QTabWidget()
        self.monitor_tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; background-color: #2a2a2a; }
            QTabBar::tab { background-color: #3a3a3a; color: white; padding: 8px 16px; margin-right: 2px; }
            QTabBar::tab:selected { background-color: #2196F3; }
            QTabBar::tab:hover { background-color: #555; }
        """)
        
        # Console Tab
        self.console_widget = ConsoleWidget()
        self.monitor_tabs.addTab(self.console_widget, "📺 Console")
        
        # Analytics Tab
        self.analytics_widget = AnalyticsWidget()
        self.monitor_tabs.addTab(self.analytics_widget, "📈 Analytics")
        
        # Performance Tab
        self.performance_widget = PerformanceWidget()
        self.monitor_tabs.addTab(self.performance_widget, "⚡ Performance")
        
        content_layout.addWidget(self.monitor_tabs)
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)


class AnalyticsWidget(QWidget):
    """TSDuck Analytics Widget for comprehensive stream analysis"""
    
    def __init__(self):
        super().__init__()
        self.monitor_process = None
        self.setup_ui()
        # Auto-start basic analytics monitoring
        self.start_basic_monitoring()
        
    def setup_ui(self):
        """Setup analytics interface"""
        main_layout = QVBoxLayout()
        
        # TSDuck Monitoring Status
        status_group = QGroupBox("📊 Real-time Stream Analytics")
        status_layout = QHBoxLayout()
        
        self.monitoring_status = QLabel("🟢 Real-time analytics active")
        self.monitoring_status.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        status_layout.addWidget(self.monitoring_status)
        status_layout.addStretch()
        
        # Advanced monitoring controls
        self.advanced_monitoring_btn = QPushButton("🔬 Advanced TSDuck Analysis")
        self.advanced_monitoring_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 8px; font-size: 12px; }")
        self.advanced_monitoring_btn.clicked.connect(self.start_monitoring)
        status_layout.addWidget(self.advanced_monitoring_btn)
        
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)
        
        # Real-time Stream Statistics
        stats_group = QGroupBox("📊 Real-time Stream Statistics")
        stats_layout = QGridLayout()
        
        # Bitrate Monitoring
        stats_layout.addWidget(QLabel("Bitrate:"), 0, 0)
        self.bitrate_label = QLabel("0 Mbps")
        self.bitrate_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        stats_layout.addWidget(self.bitrate_label, 0, 1)
        
        # Packets/sec
        stats_layout.addWidget(QLabel("Packets/sec:"), 1, 0)
        self.packets_label = QLabel("0")
        self.packets_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        stats_layout.addWidget(self.packets_label, 1, 1)
        
        # Continuity Errors
        stats_layout.addWidget(QLabel("Continuity Errors:"), 2, 0)
        self.continuity_errors_label = QLabel("0")
        self.continuity_errors_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #f44336;")
        stats_layout.addWidget(self.continuity_errors_label, 2, 1)
        
        # PCR Jitter
        stats_layout.addWidget(QLabel("PCR Jitter:"), 3, 0)
        self.pcr_jitter_label = QLabel("0 μs")
        self.pcr_jitter_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FF9800;")
        stats_layout.addWidget(self.pcr_jitter_label, 3, 1)
        
        # Service Count
        stats_layout.addWidget(QLabel("Services:"), 4, 0)
        self.services_label = QLabel("0")
        self.services_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3;")
        stats_layout.addWidget(self.services_label, 4, 1)
        
        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)
        
        # SCTE-35 Monitoring
        scte_group = QGroupBox("🎬 SCTE-35 Monitoring")
        scte_layout = QVBoxLayout()
        
        self.scte_status = QLabel("No SCTE-35 markers detected")
        self.scte_status.setStyleSheet("font-size: 14px; color: #FF9800;")
        scte_layout.addWidget(self.scte_status)
        
        # SCTE-35 Events Table
        self.scte_events_table = QTableWidget()
        self.scte_events_table.setColumnCount(4)
        self.scte_events_table.setHorizontalHeaderLabels(["Time", "Event ID", "Type", "Duration"])
        self.scte_events_table.setStyleSheet("QTableWidget { background-color: #2a2a2a; color: white; gridline-color: #555; }")
        scte_layout.addWidget(self.scte_events_table)
        
        scte_group.setLayout(scte_layout)
        main_layout.addWidget(scte_group)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def start_basic_monitoring(self):
        """Start real-time monitoring with actual TSDuck analysis"""
        # Initialize with default values
        self.bitrate_label.setText("0 Mbps")
        self.packets_label.setText("0")
        self.continuity_errors_label.setText("0")
        self.pcr_jitter_label.setText("0 μs")
        self.services_label.setText("0")
        self.scte_status.setText("Real-time monitoring active - analyzing stream...")
        self.scte_status.setStyleSheet("font-size: 14px; color: #4CAF50;")
        
        # Start real-time TSDuck monitoring
        self.start_realtime_analysis()
    
    def start_realtime_analysis(self):
        """Start real-time TSDuck analysis"""
        try:
            import subprocess
            import threading
            
            # Build TSDuck real-time analysis command
            tsp_binary = "/usr/local/bin/tsp"
            
            # Get input configuration from the main window
            try:
                # Try to get the current input configuration
                main_window = self.parent().parent().parent()  # Navigate to MainWindow
                if hasattr(main_window, 'config_widget'):
                    input_config = main_window.config_widget.input_widget.get_config()
                    input_type = input_config.get('type', 'hls').lower()
                    input_source = input_config.get('source', 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8')
                else:
                    # Fallback to default
                    input_type = 'hls'
                    input_source = 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8'
            except:
                # Fallback to default
                input_type = 'hls'
                input_source = 'https://cdn.itassist.one/BREAKING/NEWS/index.m3u8'
            
            # Real-time analysis command with dynamic input
            command = [
                tsp_binary,
                "-I", input_type, input_source,
                # Bitrate monitoring
                "-P", "bitrate_monitor", "--interval", "2", "--min", "1000000", "--max", "10000000",
                # Continuity checking
                "-P", "continuity",
                # PCR monitoring
                "-P", "pcr",
                # Service analysis
                "-P", "analyze", "--pid", "0", "--pid", "1", "--pid", "2", "--pid", "16", "--pid", "17", "--pid", "18", "--pid", "19",
                # SCTE-35 monitoring
                "-P", "splicemonitor",
                # Output to null (monitoring only)
                "-O", "drop"
            ]
            
            # Start TSDuck process
            self.realtime_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Start monitoring thread
            self.realtime_thread = RealtimeAnalysisThread(self.realtime_process)
            self.realtime_thread.data_received.connect(self.update_realtime_metrics)
            self.realtime_thread.start()
            
            self.scte_status.setText("🔍 Real-time TSDuck analysis active")
            self.scte_status.setStyleSheet("font-size: 14px; color: #4CAF50;")
            
        except Exception as e:
            self.scte_status.setText(f"❌ Error starting analysis: {e}")
            self.scte_status.setStyleSheet("font-size: 14px; color: #f44336;")
    
    def update_realtime_metrics(self, data):
        """Update metrics with real TSDuck analysis data"""
        try:
            # Parse TSDuck output for real metrics
            if "bitrate" in data.lower():
                # Extract bitrate from TSDuck output
                import re
                bitrate_match = re.search(r'bitrate[:\s]+(\d+)', data, re.IGNORECASE)
                if bitrate_match:
                    bitrate_bps = int(bitrate_match.group(1))
                    bitrate_mbps = bitrate_bps / 1000000
                    self.bitrate_label.setText(f"{bitrate_mbps:.1f} Mbps")
            
            elif "packets" in data.lower():
                # Extract packet rate
                import re
                packets_match = re.search(r'packets[:\s]+(\d+)', data, re.IGNORECASE)
                if packets_match:
                    packets = int(packets_match.group(1))
                    self.packets_label.setText(f"{packets}")
            
            elif "continuity" in data.lower() and "error" in data.lower():
                # Extract continuity errors
                import re
                errors_match = re.search(r'(\d+)\s+continuity\s+errors?', data, re.IGNORECASE)
                if errors_match:
                    errors = int(errors_match.group(1))
                    self.continuity_errors_label.setText(f"{errors}")
            
            elif "pcr" in data.lower() and "jitter" in data.lower():
                # Extract PCR jitter
                import re
                jitter_match = re.search(r'jitter[:\s]+(\d+)', data, re.IGNORECASE)
                if jitter_match:
                    jitter = int(jitter_match.group(1))
                    self.pcr_jitter_label.setText(f"{jitter} μs")
            
            elif "service" in data.lower():
                # Extract service count
                import re
                services_match = re.search(r'(\d+)\s+services?', data, re.IGNORECASE)
                if services_match:
                    services = int(services_match.group(1))
                    self.services_label.setText(f"{services}")
            
            elif "splice" in data.lower() or "scte" in data.lower():
                # SCTE-35 activity detected
                self.scte_status.setText("🎬 SCTE-35 markers detected - Ad break active")
                self.scte_status.setStyleSheet("font-size: 14px; color: #FF9800;")
            
        except Exception as e:
            print(f"Error parsing TSDuck output: {e}")
    
    def start_monitoring(self):
        """Start advanced TSDuck monitoring"""
        try:
            import subprocess
            
            # Build TSDuck monitoring command
            tsp_binary = "/usr/local/bin/tsp"
            
            # Comprehensive monitoring command based on TSDuck PDF
            command = [
                tsp_binary,
                "-I", "hls", "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                # Bitrate monitoring for all PIDs
                "-P", "bitrate_monitor", "--interval", "1", "--min", "1000000", "--max", "10000000",
                # Continuity checking
                "-P", "continuity",
                # PCR monitoring
                "-P", "pcr",
                # Service discovery
                "-P", "analyze", "--pid", "0", "--pid", "1", "--pid", "2", "--pid", "16", "--pid", "17", "--pid", "18", "--pid", "19",
                # SCTE-35 monitoring
                "-P", "splicemonitor",
                # Output to null (monitoring only)
                "-O", "drop"
            ]
            
            self.monitor_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.advanced_monitoring_btn.setText("🔄 Advanced Analysis Running")
            self.advanced_monitoring_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; font-size: 12px; }")
            self.monitoring_status.setText("🔬 Advanced TSDuck analysis active")
            
            # Start monitoring thread
            self.monitoring_thread = MonitoringThread(self.monitor_process)
            self.monitoring_thread.data_received.connect(self.update_analytics)
            self.monitoring_thread.start()
            
        except Exception as e:
            print(f"Error starting monitoring: {e}")
    
    def stop_monitoring(self):
        """Stop TSDuck monitoring"""
        if self.monitor_process:
            self.monitor_process.terminate()
            self.monitor_process = None
        
        if hasattr(self, 'monitoring_thread'):
            self.monitoring_thread.stop()
        
        self.advanced_monitoring_btn.setText("🔬 Advanced TSDuck Analysis")
        self.advanced_monitoring_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 8px; font-size: 12px; }")
        self.monitoring_status.setText("🟢 Real-time analytics active")
    
    def update_analytics(self, data):
        """Update analytics display with real-time data"""
        # Parse TSDuck output and update labels
        if "bitrate" in data.lower():
            # Extract bitrate information
            pass
        elif "continuity" in data.lower():
            # Extract continuity error information
            pass
        elif "splice" in data.lower():
            # Extract SCTE-35 splice information
            pass


class RealtimeAnalysisThread(QThread):
    """Thread for real-time TSDuck analysis"""
    
    data_received = pyqtSignal(str)
    
    def __init__(self, process):
        super().__init__()
        self.process = process
        self.running = True
    
    def run(self):
        """Monitor TSDuck process output"""
        while self.running and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                if line:
                    self.data_received.emit(line.strip())
            except Exception as e:
                print(f"Real-time analysis error: {e}")
                break
    
    def stop(self):
        """Stop real-time analysis"""
        self.running = False
        if self.process:
            self.process.terminate()
    
    def start_monitoring(self):
        """Start TSDuck monitoring"""
        try:
            import subprocess
            
            # Build TSDuck monitoring command
            tsp_binary = "/usr/local/bin/tsp"  # Use the same binary detection as main app
            
            # Comprehensive monitoring command based on TSDuck PDF
            command = [
                tsp_binary,
                "-I", "hls", "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                # Bitrate monitoring for all PIDs
                "-P", "bitrate_monitor", "--interval", "1", "--min", "1000000", "--max", "10000000",
                # Continuity checking
                "-P", "continuity",
                # PCR monitoring
                "-P", "pcr",
                # Service discovery
                "-P", "analyze", "--pid", "0", "--pid", "1", "--pid", "2", "--pid", "16", "--pid", "17", "--pid", "18", "--pid", "19",
                # SCTE-35 monitoring
                "-P", "splicemonitor",
                # Output to null (monitoring only)
                "-O", "drop"
            ]
            
            self.monitor_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.advanced_monitoring_btn.setText("🔄 Advanced Analysis Running")
            self.advanced_monitoring_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; font-size: 12px; }")
            self.monitoring_status.setText("🔬 Advanced TSDuck analysis active")
            
            # Start monitoring thread
            self.monitoring_thread = MonitoringThread(self.monitor_process)
            self.monitoring_thread.data_received.connect(self.update_analytics)
            self.monitoring_thread.start()
            
        except Exception as e:
            print(f"Error starting monitoring: {e}")
    
    def stop_monitoring(self):
        """Stop TSDuck monitoring"""
        if self.monitor_process:
            self.monitor_process.terminate()
            self.monitor_process = None
        
        if hasattr(self, 'monitoring_thread'):
            self.monitoring_thread.stop()
        
        self.advanced_monitoring_btn.setText("🔬 Advanced TSDuck Analysis")
        self.advanced_monitoring_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 8px; font-size: 12px; }")
        self.monitoring_status.setText("🟢 Real-time analytics active")
    
    def update_analytics(self, data):
        """Update analytics display with real-time data"""
        # Parse TSDuck output and update labels
        if "bitrate" in data.lower():
            # Extract bitrate information
            pass
        elif "continuity" in data.lower():
            # Extract continuity error information
            pass
        elif "splice" in data.lower():
            # Extract SCTE-35 splice information
            pass


class MonitoringThread(QThread):
    """Thread for monitoring TSDuck output"""
    
    data_received = pyqtSignal(str)
    
    def __init__(self, process):
        super().__init__()
        self.process = process
        self.running = True
    
    def run(self):
        """Monitor process output"""
        while self.running and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                if line:
                    self.data_received.emit(line.strip())
            except Exception as e:
                print(f"Monitoring error: {e}")
                break
    
    def stop(self):
        """Stop monitoring"""
        self.running = False


class PerformanceWidget(QWidget):
    """TSDuck Performance monitoring widget with real-time system metrics"""
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_performance)
        self.setup_ui()
        # Start performance monitoring automatically
        self.start_performance_monitoring()
        
    def setup_ui(self):
        """Setup performance interface"""
        main_layout = QVBoxLayout()
        
        # Performance Status
        status_group = QGroupBox("📊 Real-time Performance Monitoring")
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("🟢 Real-time monitoring active")
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        
        # Refresh rate control
        refresh_layout = QHBoxLayout()
        refresh_layout.addWidget(QLabel("Refresh Rate:"))
        self.refresh_combo = QComboBox()
        self.refresh_combo.addItems(["1 second", "2 seconds", "5 seconds", "10 seconds"])
        self.refresh_combo.setCurrentText("1 second")
        self.refresh_combo.setStyleSheet("font-size: 12px; padding: 4px;")
        self.refresh_combo.currentTextChanged.connect(self.update_refresh_rate)
        refresh_layout.addWidget(self.refresh_combo)
        status_layout.addLayout(refresh_layout)
        
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)
        
        # System Performance
        perf_group = QGroupBox("⚡ System Performance")
        perf_layout = QGridLayout()
        
        # CPU Usage
        perf_layout.addWidget(QLabel("CPU Usage:"), 0, 0)
        self.cpu_label = QLabel("0%")
        self.cpu_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        perf_layout.addWidget(self.cpu_label, 0, 1)
        
        # Memory Usage
        perf_layout.addWidget(QLabel("Memory Usage:"), 1, 0)
        self.memory_label = QLabel("0 MB")
        self.memory_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        perf_layout.addWidget(self.memory_label, 1, 1)
        
        # Network Usage
        perf_layout.addWidget(QLabel("Network Usage:"), 2, 0)
        self.network_label = QLabel("0 Mbps")
        self.network_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        perf_layout.addWidget(self.network_label, 2, 1)
        
        # TSDuck Process Status
        perf_layout.addWidget(QLabel("TSDuck Processes:"), 3, 0)
        self.tsduck_processes_label = QLabel("0")
        self.tsduck_processes_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3;")
        perf_layout.addWidget(self.tsduck_processes_label, 3, 1)
        
        # Stream Health
        perf_layout.addWidget(QLabel("Stream Health:"), 4, 0)
        self.stream_health_label = QLabel("Unknown")
        self.stream_health_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FF9800;")
        perf_layout.addWidget(self.stream_health_label, 4, 1)
        
        perf_group.setLayout(perf_layout)
        main_layout.addWidget(perf_group)
        
        # Performance History Chart
        history_group = QGroupBox("📈 Performance History")
        history_layout = QVBoxLayout()
        
        self.performance_text = QTextEdit()
        self.performance_text.setReadOnly(True)
        self.performance_text.setMaximumHeight(200)
        self.performance_text.setStyleSheet("font-family: 'Monaco', 'Consolas', monospace; font-size: 12px;")
        history_layout.addWidget(self.performance_text)
        
        history_group.setLayout(history_layout)
        main_layout.addWidget(history_group)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def start_performance_monitoring(self):
        """Start real-time performance monitoring"""
        self.timer.start(1000)  # Update every second by default
        self.performance_text.append("🚀 Real-time performance monitoring started automatically...")
        self.performance_text.append("📊 Monitoring CPU, Memory, Network, and TSDuck processes...")
    
    def update_refresh_rate(self, rate_text):
        """Update refresh rate for performance monitoring"""
        rate_map = {
            "1 second": 1000,
            "2 seconds": 2000,
            "5 seconds": 5000,
            "10 seconds": 10000
        }
        self.timer.setInterval(rate_map.get(rate_text, 1000))
        self.performance_text.append(f"🔄 Refresh rate updated to {rate_text}")
    
    def update_performance(self):
        """Update performance metrics"""
        try:
            import psutil
            import subprocess
            import random
            
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=0.1)  # Faster sampling
            self.cpu_label.setText(f"{cpu_percent:.1f}%")
            
            # Memory Usage
            memory = psutil.virtual_memory()
            memory_mb = memory.used // (1024*1024)
            self.memory_label.setText(f"{memory_mb} MB")
            
            # Network Usage (simulate streaming activity)
            network = psutil.net_io_counters()
            network_mbps = (network.bytes_sent + network.bytes_recv) // (1024*1024) // 10  # Approximate Mbps
            self.network_label.setText(f"{network_mbps:.1f} Mbps")
            
            # TSDuck Processes
            tsp_processes = 0
            try:
                result = subprocess.run(["pgrep", "-c", "tsp"], capture_output=True, text=True)
                tsp_processes = int(result.stdout.strip()) if result.stdout.strip() else 0
            except:
                pass
            self.tsduck_processes_label.setText(str(tsp_processes))
            
            # Stream Health Assessment with more detailed criteria
            if tsp_processes > 0:
                if cpu_percent < 30 and memory.percent < 70:
                    self.stream_health_label.setText("✅ Excellent")
                    self.stream_health_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
                elif cpu_percent < 50 and memory.percent < 80:
                    self.stream_health_label.setText("✅ Healthy")
                    self.stream_health_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
                elif cpu_percent < 70 and memory.percent < 90:
                    self.stream_health_label.setText("⚠️ Warning")
                    self.stream_health_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FF9800;")
                else:
                    self.stream_health_label.setText("❌ Critical")
                    self.stream_health_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #f44336;")
            else:
                self.stream_health_label.setText("⏹️ No Stream")
                self.stream_health_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #666;")
            
            # Update performance history with more details
            timestamp = time.strftime("%H:%M:%S")
            self.performance_text.append(f"[{timestamp}] CPU: {cpu_percent:.1f}% | Memory: {memory.percent:.1f}% | Network: {network_mbps:.1f} Mbps | TSDuck: {tsp_processes}")
            
            # Keep only last 20 lines
            if self.performance_text.document().blockCount() > 20:
                cursor = self.performance_text.textCursor()
                cursor.movePosition(cursor.MoveOperation.Start)
                cursor.movePosition(cursor.MoveOperation.Down, cursor.MoveMode.KeepAnchor, 1)
                cursor.removeSelectedText()
            
        except ImportError:
            self.performance_text.append("⚠️ psutil not available. Install with: pip install psutil")
            # Fallback to simulated data
            self.update_simulated_performance()
        except Exception as e:
            self.performance_text.append(f"❌ Error updating performance: {e}")
            self.update_simulated_performance()
    
    def update_simulated_performance(self):
        """Update with real system data when psutil is not available"""
        try:
            import subprocess
            import os
            
            # Get real CPU usage using system commands
            try:
                cpu_result = subprocess.run(["top", "-l", "1", "-n", "0"], capture_output=True, text=True, timeout=5)
                cpu_lines = cpu_result.stdout.split('\n')
                for line in cpu_lines:
                    if "CPU usage" in line:
                        cpu_match = re.search(r'(\d+\.\d+)%', line)
                        if cpu_match:
                            cpu_percent = float(cpu_match.group(1))
                            break
                else:
                    cpu_percent = 0.0
            except:
                cpu_percent = 0.0
            
            # Get real memory usage
            try:
                memory_result = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=5)
                # Parse vm_stat output for real memory usage
                memory_mb = 0
                for line in memory_result.stdout.split('\n'):
                    if "Pages free" in line:
                        free_pages = int(re.search(r'(\d+)', line).group(1))
                        memory_mb = free_pages * 4096 // (1024*1024)  # Convert to MB
                        break
            except:
                memory_mb = 0
            
            # Get real network usage
            try:
                network_result = subprocess.run(["netstat", "-i"], capture_output=True, text=True, timeout=5)
                network_mbps = 0
                for line in network_result.stdout.split('\n'):
                    if "en0" in line or "wlan0" in line:
                        parts = line.split()
                        if len(parts) > 6:
                            bytes_out = int(parts[6]) if parts[6].isdigit() else 0
                            network_mbps = bytes_out / (1024*1024)  # Convert to MB
                            break
            except:
                network_mbps = 0
            
            # Get real TSDuck processes
            try:
                tsp_result = subprocess.run(["pgrep", "-c", "tsp"], capture_output=True, text=True, timeout=5)
                tsp_processes = int(tsp_result.stdout.strip()) if tsp_result.stdout.strip() else 0
            except:
                tsp_processes = 0
            
            self.cpu_label.setText(f"{cpu_percent:.1f}%")
            self.memory_label.setText(f"{memory_mb} MB")
            self.network_label.setText(f"{network_mbps:.1f} MB")
            self.tsduck_processes_label.setText(str(tsp_processes))
            
            if tsp_processes > 0:
                self.stream_health_label.setText("✅ Real System Data")
                self.stream_health_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
            else:
                self.stream_health_label.setText("⏹️ No Stream")
                self.stream_health_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #666;")
            
            timestamp = time.strftime("%H:%M:%S")
            self.performance_text.append(f"[{timestamp}] CPU: {cpu_percent:.1f}% | Memory: {memory_mb} MB | Network: {network_mbps:.1f} MB | TSDuck: {tsp_processes} (Real Data)")
            
        except Exception as e:
            self.performance_text.append(f"❌ Error getting real system data: {e}")


class ToolsWidget(QWidget):
    """Enterprise Tools Widget - Analyzer and utilities"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup tools interface"""
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("🔧 Professional Tools & Utilities")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF9800; margin: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Create scroll area for tools content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Create tools tabs
        self.tools_tabs = QTabWidget()
        self.tools_tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; background-color: #2a2a2a; }
            QTabBar::tab { background-color: #3a3a3a; color: white; padding: 8px 16px; margin-right: 2px; }
            QTabBar::tab:selected { background-color: #FF9800; }
            QTabBar::tab:hover { background-color: #555; }
        """)
        
        # Stream Analyzer
        self.analyzer_widget = TSAnalyzerWidget()
        self.tools_tabs.addTab(self.analyzer_widget, "🔍 Stream Analyzer")
        
        # Utilities
        self.utilities_widget = UtilitiesWidget()
        self.tools_tabs.addTab(self.utilities_widget, "🛠️ Utilities")
        
        content_layout.addWidget(self.tools_tabs)
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)


class UtilitiesWidget(QWidget):
    """Utilities Widget for various tools"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup utilities interface"""
        main_layout = QVBoxLayout()
        
        # Stream Testing
        test_group = QGroupBox("🧪 Stream Testing")
        test_layout = QVBoxLayout()
        
        self.test_stream_btn = QPushButton("🔍 Test Stream Quality")
        self.test_stream_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 12px; font-size: 14px; }")
        test_layout.addWidget(self.test_stream_btn)
        
        self.validate_config_btn = QPushButton("✅ Validate Configuration")
        self.validate_config_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 12px; font-size: 14px; }")
        test_layout.addWidget(self.validate_config_btn)
        
        test_group.setLayout(test_layout)
        main_layout.addWidget(test_group)
        
        # System Utilities
        system_group = QGroupBox("🔧 System Utilities")
        system_layout = QVBoxLayout()
        
        self.clear_logs_btn = QPushButton("🗑️ Clear Logs")
        self.clear_logs_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; padding: 12px; font-size: 14px; }")
        system_layout.addWidget(self.clear_logs_btn)
        
        self.export_config_btn = QPushButton("📤 Export Configuration")
        self.export_config_btn.setStyleSheet("QPushButton { background-color: #9C27B0; color: white; font-weight: bold; padding: 12px; font-size: 14px; }")
        system_layout.addWidget(self.export_config_btn)
        
        system_group.setLayout(system_layout)
        main_layout.addWidget(system_group)
        
        main_layout.addStretch()
        self.setLayout(main_layout)


class HelpWidget(QWidget):
    """Help and User Manual widget"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the help interface"""
        main_layout = QVBoxLayout()
        
        # Language selection
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("🌐 Language / भाषा / اللغة:"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "हिंदी (Hindi)", "العربية (Arabic)"])
        self.language_combo.setStyleSheet("font-size: 14px; padding: 8px;")
        self.language_combo.currentTextChanged.connect(self.update_content)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        main_layout.addLayout(lang_layout)
        
        # Create scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Content area
        self.content_area = QTextEdit()
        self.content_area.setReadOnly(True)
        self.content_area.setStyleSheet("font-size: 13px; padding: 15px; background-color: #1a1a1a; color: #ffffff;")
        
        scroll_area.setWidget(self.content_area)
        main_layout.addWidget(scroll_area)
        
        # Load initial content
        self.update_content("English")
        self.setLayout(main_layout)
    
    def update_content(self, language):
        """Update content based on selected language"""
        if language == "English":
            self.load_english_content()
        elif language == "हिंदी (Hindi)":
            self.load_hindi_content()
        else:  # Arabic
            self.load_arabic_content()
    
    def load_english_content(self):
        """Load English help content"""
        content = """
# ITAssist Broadcast Encoder - 100 (IBE-100) User Manual

<div class="toc">
<h3>📋 Table of Contents</h3>
<ul>
<li><a href="#overview">🎯 Overview</a></li>
<li><a href="#quickstart">🚀 Quick Start Guide</a></li>
<li><a href="#configuration">📋 Detailed Configuration</a></li>
<li><a href="#inputformats">🔧 Input Formats</a></li>
<li><a href="#outputformats">📊 Output Formats</a></li>
<li><a href="#scte35">🎬 SCTE-35 Features</a></li>
<li><a href="#analyzer">🔍 Analyzer Features</a></li>
<li><a href="#troubleshooting">🛠️ Troubleshooting</a></li>
<li><a href="#support">📞 Support</a></li>
</ul>
</div>

## 🎯 Overview
<div class="info-box">
<strong>IBE-100</strong> is a professional SCTE-35 streaming solution designed for broadcast distributors. It provides comprehensive TSDuck-based streaming capabilities with advanced ad insertion features for professional broadcast environments.
</div>

## 🚀 Quick Start Guide

<div class="step">
<span class="step-number">1</span>
<strong>Input Configuration</strong>: Select your input source (HLS, UDP, TCP, SRT, etc.)
</div>

<div class="step">
<span class="step-number">2</span>
<strong>Service Configuration</strong>: Set service name, provider, and IDs
</div>

<div class="step">
<span class="step-number">3</span>
<strong>PID Configuration</strong>: Configure Video, Audio, and SCTE-35 PIDs
</div>

<div class="step">
<span class="step-number">4</span>
<strong>SCTE-35 Setup</strong>: Configure ad duration, event IDs, and pre-roll settings
</div>

<div class="step">
<span class="step-number">5</span>
<strong>Start Streaming</strong>: Click "▶️ Start Processing" to begin streaming
</div>

## 📋 Detailed Configuration

### Service Information
<table class="table">
<thead>
<tr>
<th>Parameter</th>
<th>Description</th>
<th>Default Value</th>
<th>Range</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Service Name</strong></td>
<td>Your broadcast service name</td>
<td>SCTE-35 Stream</td>
<td>Any text</td>
</tr>
<tr>
<td><strong>Provider Name</strong></td>
<td>Your organization name</td>
<td>ITAssist</td>
<td>Any text</td>
</tr>
<tr>
<td><strong>Service ID</strong></td>
<td>Unique service identifier</td>
<td>1</td>
<td>1-65535</td>
</tr>
<tr>
<td><strong>Bouquet ID</strong></td>
<td>Service bouquet identifier</td>
<td>1</td>
<td>1-65535</td>
</tr>
<tr>
<td><strong>Original Network ID</strong></td>
<td>Network identifier</td>
<td>1</td>
<td>1-65535</td>
</tr>
<tr>
<td><strong>Transport Stream ID</strong></td>
<td>Stream identifier</td>
<td>1</td>
<td>1-65535</td>
</tr>
</tbody>
</table>

### PID Configuration
<table class="table">
<thead>
<tr>
<th>PID Type</th>
<th>Description</th>
<th>Default Value</th>
<th>Stream Type</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Video PID (VPID)</strong></td>
<td>Video stream PID</td>
<td>256</td>
<td>H.264 (0x1b)</td>
</tr>
<tr>
<td><strong>Audio PID (APID)</strong></td>
<td>Audio stream PID</td>
<td>257</td>
<td>AAC-LC (0x0f)</td>
</tr>
<tr>
<td><strong>SCTE-35 PID</strong></td>
<td>SCTE-35 data PID</td>
<td>500</td>
<td>SCTE-35 (0x86)</td>
</tr>
<tr>
<td><strong>Null PID</strong></td>
<td>Null stream PID</td>
<td>8191</td>
<td>Null (0x1f)</td>
</tr>
<tr>
<td><strong>PCR PID</strong></td>
<td>Program Clock Reference PID</td>
<td>256</td>
<td>PCR (same as video)</td>
</tr>
</tbody>
</table>

### SCTE-35 Configuration
<div class="feature-grid">
<div class="feature-card">
<h4>🎬 Ad Duration</h4>
<p>Duration in seconds for ad breaks</p>
<p><strong>Default:</strong> 600 seconds (10 minutes)</p>
</div>
<div class="feature-card">
<h4>🆔 Event ID</h4>
<p>Unique SCTE event identifier</p>
<p><strong>Default:</strong> 100023</p>
</div>
<div class="feature-card">
<h4>⏰ Pre-roll Duration</h4>
<p>Pre-roll ad duration</p>
<p><strong>Range:</strong> 0-10 seconds</p>
</div>
</div>

## 🔧 Input Formats Supported

### Streaming Protocols
- **HLS**: HTTP Live Streaming (https://example.com/stream.m3u8)
- **SRT**: Secure Reliable Transport (srt://host:port)
- **UDP**: User Datagram Protocol (127.0.0.1:9999)
- **TCP**: Transmission Control Protocol (127.0.0.1:9999)
- **HTTP/HTTPS**: Web-based streaming

### Broadcast Standards
- **DVB-S/T/C**: Digital Video Broadcasting
- **ATSC**: Advanced Television Systems Committee
- **ISDB-T**: Integrated Services Digital Broadcasting
- **DMB-T**: Digital Multimedia Broadcasting
- **CMMB**: China Mobile Multimedia Broadcasting

### Hardware Interfaces
- **ASI**: Asynchronous Serial Interface (/dev/asi0)
- **Dektec**: Professional hardware (dtapi://device)
- **DVB**: Digital Video Broadcasting hardware

## 📊 Output Formats

### SRT Output
- **Endpoint**: srt://cdn.itassist.one:8888
- **Stream ID**: #!::r=scte/scte,m=publish
- **Latency**: 2000ms (2 seconds)

### UDP Output
- **Endpoint**: udp://127.0.0.1:9999
- **Multicast**: udp://239.1.1.1:9999

## 🎬 SCTE-35 Features

### Ad Insertion Events
- **CUE-OUT**: Program out point (start of ad)
- **CUE-IN**: Program in point (end of ad)
- **Crash CUE-IN**: Emergency return to program
- **Pre-roll**: Scheduled ad insertion

### XML Marker Files
- **cue_out_10021.xml**: Ad break start (600s duration)
- **cue_in_10022.xml**: Return to program
- **crash_out_10024.xml**: Emergency return (45s duration)
- **preroll_10023.xml**: Pre-roll ad insertion

## 🔍 Analyzer Features

### Stream Analysis
- **Real-time monitoring**: Bitrate, packets/sec, errors
- **Service discovery**: All services with PID mappings
- **SCTE-35 detection**: Live splice detection and analysis
- **Performance metrics**: CPU, memory, network usage

### Analysis Types
- **Basic Analysis**: Stream overview and statistics
- **Service Analysis**: Detailed service information
- **PID Analysis**: Individual PID monitoring
- **SCTE-35 Analysis**: Splice information monitoring

## 🛠️ Troubleshooting

### Common Issues
1. **Stream Not Starting**
   - Check input URL accessibility
   - Verify TSDuck installation
   - Check network connectivity

2. **PID Issues**
   - Verify PID configuration
   - Check for PID conflicts
   - Ensure proper stream types

3. **SCTE-35 Not Working**
   - Verify XML files exist
   - Check SCTE-35 PID configuration
   - Monitor console for errors

### Error Messages
- **"tsp: command not found"**: TSDuck not installed
- **"Connection refused"**: Network connectivity issues
- **"PID conflict"**: Duplicate PID assignments
- **"XML not found"**: Missing SCTE-35 marker files

## 📞 Support

### Technical Support
- **Email**: support@itassist.one
- **Documentation**: https://tsduck.io/
- **Community**: TSDuck User Forum

### System Requirements
- **OS**: macOS, Linux, Windows
- **TSDuck**: Version 3.30 or later
- **Python**: 3.8 or later
- **PyQt6**: Latest version

## 🔒 Security Notes
- Keep TSDuck updated for security patches
- Use secure network connections (SRT, HTTPS)
- Monitor stream access and permissions
- Regular backup of configuration files

       ---
       
       ## 🏢 Company Information
       
       ### ITAssist Broadcast Solutions
       **Professional Broadcast Technology Solutions**
       
       **📍 Global Offices:**
       - **Dubai, UAE**: Middle East Operations
       - **Mumbai, India**: South Asia Headquarters  
       - **Gurugram, India**: Technology Development Center
       
       **📞 Contact Information:**
       - **Email**: support@itassist.one
       - **Website**: https://itassist.one
       - **Technical Support**: 24/7 Professional Support
       
       **🔧 Services:**
       - Professional SCTE-35 Streaming Solutions
       - Broadcast Technology Consulting
       - Custom Broadcast Software Development
       - Multi-format Stream Processing
       - Enterprise Broadcast Infrastructure
       
       ---
       **© 2024 ITAssist Broadcast Solutions**
       **ITAssist Broadcast Encoder - 100 (IBE-100) v1.0**
       **Professional SCTE-35 Streaming Solution**
       **All Rights Reserved | Licensed Software**
        """
        self.content_area.setHtml(self.format_html(content))
    
    def load_hindi_content(self):
        """Load Hindi help content"""
        content = """
# ITAssist ब्रॉडकास्ट एनकोडर - 100 (IBE-100) उपयोगकर्ता मैनुअल

<div class="toc hindi">
<h3>📋 विषय सूची</h3>
<ul>
<li><a href="#overview">🎯 अवलोकन</a></li>
<li><a href="#quickstart">🚀 त्वरित प्रारंभ गाइड</a></li>
<li><a href="#configuration">📋 विस्तृत कॉन्फ़िगरेशन</a></li>
<li><a href="#inputformats">🔧 इनपुट प्रारूप</a></li>
<li><a href="#outputformats">📊 आउटपुट प्रारूप</a></li>
<li><a href="#scte35">🎬 SCTE-35 सुविधाएं</a></li>
<li><a href="#analyzer">🔍 एनालाइज़र सुविधाएं</a></li>
<li><a href="#troubleshooting">🛠️ समस्या निवारण</a></li>
<li><a href="#support">📞 सहायता</a></li>
</ul>
</div>

## 🎯 अवलोकन
<div class="info-box hindi">
<strong>IBE-100</strong> एक पेशेवर SCTE-35 स्ट्रीमिंग समाधान है जो ब्रॉडकास्ट डिस्ट्रीब्यूटर्स के लिए डिज़ाइन किया गया है। यह पेशेवर ब्रॉडकास्ट वातावरण के लिए उन्नत विज्ञापन सम्मिलन सुविधाओं के साथ व्यापक TSDuck-आधारित स्ट्रीमिंग क्षमताएं प्रदान करता है।
</div>

## 🚀 त्वरित प्रारंभ गाइड

<div class="step hindi">
<span class="step-number">1</span>
<strong>इनपुट कॉन्फ़िगरेशन</strong>: अपना इनपुट स्रोत चुनें (HLS, UDP, TCP, SRT, आदि)
</div>

<div class="step hindi">
<span class="step-number">2</span>
<strong>सेवा कॉन्फ़िगरेशन</strong>: सेवा नाम, प्रदाता, और ID सेट करें
</div>

<div class="step hindi">
<span class="step-number">3</span>
<strong>PID कॉन्फ़िगरेशन</strong>: वीडियो, ऑडियो, और SCTE-35 PID कॉन्फ़िगर करें
</div>

<div class="step hindi">
<span class="step-number">4</span>
<strong>SCTE-35 सेटअप</strong>: विज्ञापन अवधि, इवेंट ID, और प्री-रोल सेटिंग्स कॉन्फ़िगर करें
</div>

<div class="step hindi">
<span class="step-number">5</span>
<strong>स्ट्रीमिंग शुरू करें</strong>: स्ट्रीमिंग शुरू करने के लिए "▶️ Start Processing" पर क्लिक करें
</div>

## 📋 विस्तृत कॉन्फ़िगरेशन

### सेवा सूचना
<table class="table hindi">
<thead>
<tr>
<th>पैरामीटर</th>
<th>विवरण</th>
<th>डिफ़ॉल्ट मान</th>
<th>रेंज</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>सेवा नाम</strong></td>
<td>आपका ब्रॉडकास्ट सेवा नाम</td>
<td>SCTE-35 Stream</td>
<td>कोई भी टेक्स्ट</td>
</tr>
<tr>
<td><strong>प्रदाता नाम</strong></td>
<td>आपके संगठन का नाम</td>
<td>ITAssist</td>
<td>कोई भी टेक्स्ट</td>
</tr>
<tr>
<td><strong>सेवा ID</strong></td>
<td>अद्वितीय सेवा पहचानकर्ता</td>
<td>1</td>
<td>1-65535</td>
</tr>
<tr>
<td><strong>बुके ID</strong></td>
<td>सेवा बुके पहचानकर्ता</td>
<td>1</td>
<td>1-65535</td>
</tr>
<tr>
<td><strong>मूल नेटवर्क ID</strong></td>
<td>नेटवर्क पहचानकर्ता</td>
<td>1</td>
<td>1-65535</td>
</tr>
<tr>
<td><strong>ट्रांसपोर्ट स्ट्रीम ID</strong></td>
<td>स्ट्रीम पहचानकर्ता</td>
<td>1</td>
<td>1-65535</td>
</tr>
</tbody>
</table>

### PID कॉन्फ़िगरेशन
<table class="table hindi">
<thead>
<tr>
<th>PID प्रकार</th>
<th>विवरण</th>
<th>डिफ़ॉल्ट मान</th>
<th>स्ट्रीम प्रकार</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>वीडियो PID (VPID)</strong></td>
<td>वीडियो स्ट्रीम PID</td>
<td>256</td>
<td>H.264 (0x1b)</td>
</tr>
<tr>
<td><strong>ऑडियो PID (APID)</strong></td>
<td>ऑडियो स्ट्रीम PID</td>
<td>257</td>
<td>AAC-LC (0x0f)</td>
</tr>
<tr>
<td><strong>SCTE-35 PID</strong></td>
<td>SCTE-35 डेटा PID</td>
<td>500</td>
<td>SCTE-35 (0x86)</td>
</tr>
<tr>
<td><strong>नल PID</strong></td>
<td>नल स्ट्रीम PID</td>
<td>8191</td>
<td>नल (0x1f)</td>
</tr>
<tr>
<td><strong>PCR PID</strong></td>
<td>प्रोग्राम क्लॉक रेफरेंस PID</td>
<td>256</td>
<td>PCR (वीडियो के समान)</td>
</tr>
</tbody>
</table>

### SCTE-35 कॉन्फ़िगरेशन
<div class="feature-grid hindi">
<div class="feature-card hindi">
<h4>🎬 विज्ञापन अवधि</h4>
<p>विज्ञापन ब्रेक के लिए सेकंड में अवधि</p>
<p><strong>डिफ़ॉल्ट:</strong> 600 सेकंड (10 मिनट)</p>
</div>
<div class="feature-card hindi">
<h4>🆔 इवेंट ID</h4>
<p>अद्वितीय SCTE इवेंट पहचानकर्ता</p>
<p><strong>डिफ़ॉल्ट:</strong> 100023</p>
</div>
<div class="feature-card hindi">
<h4>⏰ प्री-रोल अवधि</h4>
<p>प्री-रोल विज्ञापन अवधि</p>
<p><strong>रेंज:</strong> 0-10 सेकंड</p>
</div>
</div>

## 🔧 समर्थित इनपुट प्रारूप

### स्ट्रीमिंग प्रोटोकॉल
- **HLS**: HTTP लाइव स्ट्रीमिंग (https://example.com/stream.m3u8)
- **SRT**: सिक्योर रिलायबल ट्रांसपोर्ट (srt://host:port)
- **UDP**: यूजर डेटाग्राम प्रोटोकॉल (127.0.0.1:9999)
- **TCP**: ट्रांसमिशन कंट्रोल प्रोटोकॉल (127.0.0.1:9999)
- **HTTP/HTTPS**: वेब-आधारित स्ट्रीमिंग

### ब्रॉडकास्ट मानक
- **DVB-S/T/C**: डिजिटल वीडियो ब्रॉडकास्टिंग
- **ATSC**: एडवांस्ड टेलीविज़न सिस्टम्स कमेटी
- **ISDB-T**: इंटीग्रेटेड सर्विसेज डिजिटल ब्रॉडकास्टिंग
- **DMB-T**: डिजिटल मल्टीमीडिया ब्रॉडकास्टिंग
- **CMMB**: चाइना मोबाइल मल्टीमीडिया ब्रॉडकास्टिंग

### हार्डवेयर इंटरफेस
- **ASI**: एसिंक्रोनस सीरियल इंटरफेस (/dev/asi0)
- **Dektec**: पेशेवर हार्डवेयर (dtapi://device)
- **DVB**: डिजिटल वीडियो ब्रॉडकास्टिंग हार्डवेयर

## 📊 आउटपुट प्रारूप

### SRT आउटपुट
- **एंडपॉइंट**: srt://cdn.itassist.one:8888
- **स्ट्रीम ID**: #!::r=scte/scte,m=publish
- **लेटेंसी**: 2000ms (2 सेकंड)

### UDP आउटपुट
- **एंडपॉइंट**: udp://127.0.0.1:9999
- **मल्टीकास्ट**: udp://239.1.1.1:9999

## 🎬 SCTE-35 सुविधाएं

### विज्ञापन सम्मिलन इवेंट्स
- **CUE-OUT**: प्रोग्राम आउट पॉइंट (विज्ञापन की शुरुआत)
- **CUE-IN**: प्रोग्राम इन पॉइंट (विज्ञापन का अंत)
- **क्रैश CUE-IN**: प्रोग्राम में आपातकालीन वापसी
- **प्री-रोल**: निर्धारित विज्ञापन सम्मिलन

### XML मार्कर फाइलें
- **cue_out_10021.xml**: विज्ञापन ब्रेक शुरुआत (600s अवधि)
- **cue_in_10022.xml**: प्रोग्राम में वापसी
- **crash_out_10024.xml**: आपातकालीन वापसी (45s अवधि)
- **preroll_10023.xml**: प्री-रोल विज्ञापन सम्मिलन

## 🔍 एनालाइज़र सुविधाएं

### स्ट्रीम विश्लेषण
- **रियल-टाइम मॉनिटरिंग**: बिटरेट, पैकेट/सेकंड, त्रुटियां
- **सेवा खोज**: PID मैपिंग के साथ सभी सेवाएं
- **SCTE-35 डिटेक्शन**: लाइव स्प्लिस डिटेक्शन और विश्लेषण
- **प्रदर्शन मेट्रिक्स**: CPU, मेमोरी, नेटवर्क उपयोग

### विश्लेषण प्रकार
- **मूल विश्लेषण**: स्ट्रीम अवलोकन और आंकड़े
- **सेवा विश्लेषण**: विस्तृत सेवा सूचना
- **PID विश्लेषण**: व्यक्तिगत PID मॉनिटरिंग
- **SCTE-35 विश्लेषण**: स्प्लिस सूचना मॉनिटरिंग

## 🛠️ समस्या निवारण

### सामान्य समस्याएं
1. **स्ट्रीम शुरू नहीं हो रहा**
   - इनपुट URL पहुंच की जांच करें
   - TSDuck इंस्टॉलेशन सत्यापित करें
   - नेटवर्क कनेक्टिविटी जांचें

2. **PID समस्याएं**
   - PID कॉन्फ़िगरेशन सत्यापित करें
   - PID संघर्षों की जांच करें
   - उचित स्ट्रीम प्रकार सुनिश्चित करें

3. **SCTE-35 काम नहीं कर रहा**
   - XML फाइलें मौजूद हैं सत्यापित करें
   - SCTE-35 PID कॉन्फ़िगरेशन जांचें
   - त्रुटियों के लिए कंसोल मॉनिटर करें

### त्रुटि संदेश
- **"tsp: command not found"**: TSDuck इंस्टॉल नहीं है
- **"Connection refused"**: नेटवर्क कनेक्टिविटी समस्याएं
- **"PID conflict"**: डुप्लिकेट PID असाइनमेंट
- **"XML not found"**: लापता SCTE-35 मार्कर फाइलें

## 📞 सहायता

### तकनीकी सहायता
- **ईमेल**: support@itassist.one
- **दस्तावेज़**: https://tsduck.io/
- **कम्युनिटी**: TSDuck यूजर फोरम

### सिस्टम आवश्यकताएं
- **OS**: macOS, Linux, Windows
- **TSDuck**: संस्करण 3.30 या बाद में
- **Python**: 3.8 या बाद में
- **PyQt6**: नवीनतम संस्करण

## 🔒 सुरक्षा नोट्स
- सुरक्षा पैच के लिए TSDuck अपडेट रखें
- सुरक्षित नेटवर्क कनेक्शन (SRT, HTTPS) का उपयोग करें
- स्ट्रीम एक्सेस और अनुमतियों की निगरानी करें
- कॉन्फ़िगरेशन फाइलों का नियमित बैकअप

       ---
       
       ## 🏢 कंपनी जानकारी
       
       ### ITAssist ब्रॉडकास्ट सॉल्यूशंस
       **पेशेवर ब्रॉडकास्ट टेक्नोलॉजी सॉल्यूशंस**
       
       **📍 वैश्विक कार्यालय:**
       - **दुबई, यूएई**: मध्य पूर्व संचालन
       - **मुंबई, भारत**: दक्षिण एशिया मुख्यालय
       - **गुरुग्राम, भारत**: प्रौद्योगिकी विकास केंद्र
       
       **📞 संपर्क जानकारी:**
       - **ईमेल**: support@itassist.one
       - **वेबसाइट**: https://itassist.one
       - **तकनीकी सहायता**: 24/7 पेशेवर सहायता
       
       **🔧 सेवाएं:**
       - पेशेवर SCTE-35 स्ट्रीमिंग समाधान
       - ब्रॉडकास्ट टेक्नोलॉजी परामर्श
       - कस्टम ब्रॉडकास्ट सॉफ्टवेयर विकास
       - मल्टी-फॉर्मेट स्ट्रीम प्रोसेसिंग
       - एंटरप्राइज ब्रॉडकास्ट इन्फ्रास्ट्रक्चर
       
       ---
       **© 2024 ITAssist ब्रॉडकास्ट सॉल्यूशंस**
       **ITAssist ब्रॉडकास्ट एनकोडर - 100 (IBE-100) v1.0**
       **पेशेवर SCTE-35 स्ट्रीमिंग समाधान**
       **सभी अधिकार सुरक्षित | लाइसेंस्ड सॉफ्टवेयर**
        """
        self.content_area.setHtml(self.format_html(content))
    
    def load_arabic_content(self):
        """Load Arabic help content"""
        content = """
# ITAssist Broadcast Encoder - 100 (IBE-100) دليل المستخدم

<div class="toc arabic">
<h3>📋 جدول المحتويات</h3>
<ul>
<li><a href="#overview">🎯 نظرة عامة</a></li>
<li><a href="#quickstart">🚀 دليل البدء السريع</a></li>
<li><a href="#configuration">📋 التكوين التفصيلي</a></li>
<li><a href="#inputformats">🔧 تنسيقات الإدخال</a></li>
<li><a href="#outputformats">📊 تنسيقات الإخراج</a></li>
<li><a href="#scte35">🎬 ميزات SCTE-35</a></li>
<li><a href="#analyzer">🔍 ميزات المحلل</a></li>
<li><a href="#troubleshooting">🛠️ استكشاف الأخطاء</a></li>
<li><a href="#support">📞 الدعم</a></li>
</ul>
</div>

## 🎯 نظرة عامة
<div class="info-box arabic">
<strong>IBE-100</strong> هو حل بث SCTE-35 احترافي مصمم لموزعي البث. يوفر قدرات بث شاملة قائمة على TSDuck مع ميزات إدراج إعلانات متقدمة للبيئات البث الاحترافية.
</div>

## 🚀 دليل البدء السريع

<div class="step arabic">
<span class="step-number">1</span>
<strong>تكوين الإدخال</strong>: اختر مصدر الإدخال (HLS، UDP، TCP، SRT، إلخ)
</div>

<div class="step arabic">
<span class="step-number">2</span>
<strong>تكوين الخدمة</strong>: تعيين اسم الخدمة والموفر والمعرفات
</div>

<div class="step arabic">
<span class="step-number">3</span>
<strong>تكوين PID</strong>: تكوين Video و Audio و SCTE-35 PIDs
</div>

<div class="step arabic">
<span class="step-number">4</span>
<strong>إعداد SCTE-35</strong>: تكوين مدة الإعلان ومعرفات الأحداث وإعدادات ما قبل التشغيل
</div>

<div class="step arabic">
<span class="step-number">5</span>
<strong>بدء البث</strong>: انقر على "▶️ Start Processing" لبدء البث
</div>

## 📋 التكوين التفصيلي

### معلومات الخدمة
<table class="table arabic">
<thead>
<tr>
<th>المعامل</th>
<th>الوصف</th>
<th>القيمة الافتراضية</th>
<th>النطاق</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>اسم الخدمة</strong></td>
<td>اسم خدمة البث الخاصة بك</td>
<td>SCTE-35 Stream</td>
<td>أي نص</td>
</tr>
<tr>
<td><strong>اسم المزود</strong></td>
<td>اسم مؤسستك</td>
<td>ITAssist</td>
<td>أي نص</td>
</tr>
<tr>
<td><strong>معرف الخدمة</strong></td>
<td>معرف الخدمة الفريد</td>
<td>1</td>
<td>1-65535</td>
</tr>
<tr>
<td><strong>معرف الباقة</strong></td>
<td>معرف باقة الخدمة</td>
<td>1</td>
<td>1-65535</td>
</tr>
<tr>
<td><strong>معرف الشبكة الأصلية</strong></td>
<td>معرف الشبكة</td>
<td>1</td>
<td>1-65535</td>
</tr>
<tr>
<td><strong>معرف تدفق النقل</strong></td>
<td>معرف التدفق</td>
<td>1</td>
<td>1-65535</td>
</tr>
</tbody>
</table>

### تكوين PID
<table class="table arabic">
<thead>
<tr>
<th>نوع PID</th>
<th>الوصف</th>
<th>القيمة الافتراضية</th>
<th>نوع التدفق</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Video PID (VPID)</strong></td>
<td>PID تدفق الفيديو</td>
<td>256</td>
<td>H.264 (0x1b)</td>
</tr>
<tr>
<td><strong>Audio PID (APID)</strong></td>
<td>PID تدفق الصوت</td>
<td>257</td>
<td>AAC-LC (0x0f)</td>
</tr>
<tr>
<td><strong>SCTE-35 PID</strong></td>
<td>PID بيانات SCTE-35</td>
<td>500</td>
<td>SCTE-35 (0x86)</td>
</tr>
<tr>
<td><strong>Null PID</strong></td>
<td>PID تدفق فارغ</td>
<td>8191</td>
<td>فارغ (0x1f)</td>
</tr>
<tr>
<td><strong>PCR PID</strong></td>
<td>PID مرجع ساعة البرنامج</td>
<td>256</td>
<td>PCR (نفس الفيديو)</td>
</tr>
</tbody>
</table>

### تكوين SCTE-35
<div class="feature-grid arabic">
<div class="feature-card arabic">
<h4>🎬 مدة الإعلان</h4>
<p>المدة بالثواني لاستراحات الإعلانات</p>
<p><strong>افتراضي:</strong> 600 ثانية (10 دقائق)</p>
</div>
<div class="feature-card arabic">
<h4>🆔 معرف الحدث</h4>
<p>معرف حدث SCTE فريد</p>
<p><strong>افتراضي:</strong> 100023</p>
</div>
<div class="feature-card arabic">
<h4>⏰ مدة ما قبل التشغيل</h4>
<p>مدة إعلان ما قبل التشغيل</p>
<p><strong>النطاق:</strong> 0-10 ثواني</p>
</div>
</div>

## 🔧 تنسيقات الإدخال المدعومة

### بروتوكولات البث
- **HLS**: HTTP Live Streaming (https://example.com/stream.m3u8)
- **SRT**: Secure Reliable Transport (srt://host:port)
- **UDP**: User Datagram Protocol (127.0.0.1:9999)
- **TCP**: Transmission Control Protocol (127.0.0.1:9999)
- **HTTP/HTTPS**: بث قائم على الويب

### معايير البث
- **DVB-S/T/C**: Digital Video Broadcasting
- **ATSC**: Advanced Television Systems Committee
- **ISDB-T**: Integrated Services Digital Broadcasting
- **DMB-T**: Digital Multimedia Broadcasting
- **CMMB**: China Mobile Multimedia Broadcasting

### واجهات الأجهزة
- **ASI**: Asynchronous Serial Interface (/dev/asi0)
- **Dektec**: أجهزة احترافية (dtapi://device)
- **DVB**: أجهزة Digital Video Broadcasting

## 📊 تنسيقات الإخراج

### إخراج SRT
- **نقطة النهاية**: srt://cdn.itassist.one:8888
- **معرف التدفق**: #!::r=scte/scte,m=publish
- **الكمون**: 2000ms (2 ثانية)

### إخراج UDP
- **نقطة النهاية**: udp://127.0.0.1:9999
- **البث المتعدد**: udp://239.1.1.1:9999

## 🎬 ميزات SCTE-35

### أحداث إدراج الإعلانات
- **CUE-OUT**: نقطة خروج البرنامج (بداية الإعلان)
- **CUE-IN**: نقطة دخول البرنامج (نهاية الإعلان)
- **Crash CUE-IN**: العودة الطارئة للبرنامج
- **Pre-roll**: إدراج إعلان مجدول

### ملفات XML المحددة
- **cue_out_10021.xml**: بداية استراحة الإعلان (مدة 600s)
- **cue_in_10022.xml**: العودة للبرنامج
- **crash_out_10024.xml**: العودة الطارئة (مدة 45s)
- **preroll_10023.xml**: إدراج إعلان ما قبل التشغيل

## 🔍 ميزات المحلل

### تحليل التدفق
- **المراقبة في الوقت الفعلي**: معدل البت، الحزم/الثانية، الأخطاء
- **اكتشاف الخدمة**: جميع الخدمات مع خرائط PID
- **اكتشاف SCTE-35**: اكتشاف وتحليل الربط المباشر
- **مقاييس الأداء**: استخدام CPU والذاكرة والشبكة

### أنواع التحليل
- **التحليل الأساسي**: نظرة عامة على التدفق والإحصائيات
- **تحليل الخدمة**: معلومات مفصلة عن الخدمة
- **تحليل PID**: مراقبة PID الفردية
- **تحليل SCTE-35**: مراقبة معلومات الربط

## 🛠️ استكشاف الأخطاء وإصلاحها

### المشاكل الشائعة
1. **عدم بدء التدفق**
   - تحقق من إمكانية الوصول لرابط الإدخال
   - تحقق من تثبيت TSDuck
   - تحقق من اتصال الشبكة

2. **مشاكل PID**
   - تحقق من تكوين PID
   - تحقق من تضارب PID
   - تأكد من أنواع التدفق المناسبة

3. **عدم عمل SCTE-35**
   - تحقق من وجود ملفات XML
   - تحقق من تكوين SCTE-35 PID
   - راقب وحدة التحكم للأخطاء

### رسائل الخطأ
- **"tsp: command not found"**: TSDuck غير مثبت
- **"Connection refused"**: مشاكل اتصال الشبكة
- **"PID conflict"**: تعيينات PID مكررة
- **"XML not found"**: ملفات SCTE-35 المحددة مفقودة

## 📞 الدعم

### الدعم التقني
- **البريد الإلكتروني**: support@itassist.one
- **الوثائق**: https://tsduck.io/
- **المجتمع**: منتدى مستخدمي TSDuck

### متطلبات النظام
- **نظام التشغيل**: macOS، Linux، Windows
- **TSDuck**: الإصدار 3.30 أو أحدث
- **Python**: 3.8 أو أحدث
- **PyQt6**: أحدث إصدار

## 🔒 ملاحظات الأمان
- حافظ على تحديث TSDuck للحصول على تصحيحات الأمان
- استخدم اتصالات شبكة آمنة (SRT، HTTPS)
- راقب الوصول للتدفق والأذونات
- نسخ احتياطي منتظم لملفات التكوين

       ---
       
       ## 🏢 معلومات الشركة
       
       ### ITAssist حلول البث
       **حلول تقنية البث الاحترافية**
       
       **📍 المكاتب العالمية:**
       - **دبي، الإمارات**: عمليات الشرق الأوسط
       - **مومباي، الهند**: المقر الرئيسي لجنوب آسيا
       - **جوروجرام، الهند**: مركز تطوير التكنولوجيا
       
       **📞 معلومات الاتصال:**
       - **البريد الإلكتروني**: support@itassist.one
       - **الموقع الإلكتروني**: https://itassist.one
       - **الدعم التقني**: دعم احترافي 24/7
       
       **🔧 الخدمات:**
       - حلول بث SCTE-35 احترافية
       - استشارات تقنية البث
       - تطوير برمجيات البث المخصصة
       - معالجة تدفقات متعددة التنسيقات
       - البنية التحتية للبث المؤسسي
       
       ---
       **© 2024 ITAssist حلول البث**
       **ITAssist Broadcast Encoder - 100 (IBE-100) v1.0**
       **حل بث SCTE-35 احترافي**
       **جميع الحقوق محفوظة | برمجيات مرخصة**
        """
        self.content_area.setHtml(self.format_html(content))
    
    def format_html(self, content):
        """Format content as HTML with professional styling"""
        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; 
                    line-height: 1.7; 
                    color: #ffffff; 
                    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: rgba(0,0,0,0.3);
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                }}
                h1 {{ 
                    color: #4CAF50; 
                    font-size: 32px; 
                    margin-bottom: 30px; 
                    text-align: center;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                    border-bottom: 3px solid #4CAF50;
                    padding-bottom: 15px;
                }}
                h2 {{ 
                    color: #2196F3; 
                    font-size: 24px; 
                    margin-top: 35px; 
                    margin-bottom: 20px; 
                    border-left: 5px solid #2196F3;
                    padding-left: 15px;
                    background: rgba(33, 150, 243, 0.1);
                    padding: 15px;
                    border-radius: 8px;
                }}
                h3 {{ 
                    color: #FF9800; 
                    font-size: 20px; 
                    margin-top: 25px; 
                    margin-bottom: 15px;
                    border-bottom: 2px solid #FF9800;
                    padding-bottom: 8px;
                }}
                h4 {{
                    color: #9C27B0;
                    font-size: 18px;
                    margin-top: 20px;
                    margin-bottom: 12px;
                }}
                p {{ 
                    margin-bottom: 15px; 
                    text-align: justify;
                    font-size: 15px;
                }}
                ul {{ 
                    margin-left: 25px; 
                    margin-bottom: 20px; 
                    background: rgba(255,255,255,0.05);
                    padding: 15px;
                    border-radius: 8px;
                }}
                li {{ 
                    margin-bottom: 8px; 
                    font-size: 15px;
                }}
                ol {{
                    margin-left: 25px;
                    margin-bottom: 20px;
                    background: rgba(255,255,255,0.05);
                    padding: 15px;
                    border-radius: 8px;
                }}
                code {{ 
                    background: linear-gradient(135deg, #2a2a2a, #1a1a1a); 
                    color: #4CAF50; 
                    padding: 4px 8px; 
                    border-radius: 6px; 
                    font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
                    font-size: 14px;
                    border: 1px solid #333;
                    box-shadow: inset 0 1px 3px rgba(0,0,0,0.3);
                }}
                .highlight {{ 
                    background: linear-gradient(135deg, #2a2a2a, #1e1e1e); 
                    padding: 20px; 
                    border-radius: 10px; 
                    border-left: 5px solid #4CAF50;
                    margin: 20px 0;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                }}
                .info-box {{
                    background: linear-gradient(135deg, #1e3a8a, #1e40af);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border-left: 5px solid #3b82f6;
                }}
                .warning-box {{
                    background: linear-gradient(135deg, #dc2626, #ef4444);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border-left: 5px solid #f87171;
                }}
                .success-box {{
                    background: linear-gradient(135deg, #059669, #10b981);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border-left: 5px solid #34d399;
                }}
                .table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background: rgba(255,255,255,0.05);
                    border-radius: 10px;
                    overflow: hidden;
                }}
                .table th {{
                    background: linear-gradient(135deg, #4CAF50, #45a049);
                    color: white;
                    padding: 15px;
                    text-align: left;
                    font-weight: bold;
                }}
                .table td {{
                    padding: 12px 15px;
                    border-bottom: 1px solid rgba(255,255,255,0.1);
                }}
                .table tr:hover {{
                    background: rgba(255,255,255,0.05);
                }}
                .step {{
                    background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 8px;
                    border-left: 4px solid #4CAF50;
                }}
                .step-number {{
                    background: #4CAF50;
                    color: white;
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    margin-right: 15px;
                }}
                .feature-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .feature-card {{
                    background: rgba(255,255,255,0.05);
                    padding: 20px;
                    border-radius: 10px;
                    border: 1px solid rgba(255,255,255,0.1);
                }}
                .feature-card h4 {{
                    color: #4CAF50;
                    margin-top: 0;
                }}
                .toc {{
                    background: rgba(255,255,255,0.05);
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .toc h3 {{
                    color: #4CAF50;
                    margin-top: 0;
                }}
                .toc ul {{
                    list-style: none;
                    padding-left: 0;
                }}
                .toc li {{
                    margin: 8px 0;
                }}
                .toc a {{
                    color: #2196F3;
                    text-decoration: none;
                    font-weight: 500;
                }}
                .toc a:hover {{
                    color: #4CAF50;
                    text-decoration: underline;
                }}
                .arabic {{
                    direction: rtl;
                    text-align: right;
                }}
                .hindi {{
                    font-family: 'Noto Sans Devanagari', 'Arial Unicode MS', sans-serif;
                }}
                .emoji {{
                    font-size: 1.2em;
                    margin-right: 8px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                {content}
            </div>
        </body>
        </html>
        """
        return html


class ConsoleWidget(QGroupBox):
    """Console output widget"""
    
    def __init__(self):
        super().__init__("Console Output")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Monaco", 9))
        self.console.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        layout.addWidget(self.console)
        
        # Clear button
        clear_btn = QPushButton("Clear Console")
        clear_btn.clicked.connect(self.console.clear)
        layout.addWidget(clear_btn)
        
        self.setLayout(layout)
    
    def append_output(self, text: str):
        """Append text to console"""
        self.console.append(text)
        # Auto-scroll to bottom
        scrollbar = self.console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def append_error(self, text: str):
        """Append error text to console"""
        self.console.append(f"<span style='color: #ff6b6b;'>{text}</span>")


class TSAnalyzerWidget(QWidget):
    """TSAnalyzer widget for stream analysis"""
    
    def __init__(self):
        super().__init__()
        self.analyzer_process = None
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("🔍 Analyzer - Stream Analysis")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Analysis Configuration
        config_group = QGroupBox("Analysis Configuration")
        config_layout = QGridLayout()
        
        # Input source
        config_layout.addWidget(QLabel("Input Source:"), 0, 0)
        self.input_source = QComboBox()
        self.input_source.addItems([
            "UDP", "TCP", "File", "HLS", "SRT", "HTTP", "HTTPS", "DVB", "ASI", 
            "Dektec", "Play", "Duck", "Memory", "Fork", "TSP", "TS", "TSFile",
            "DVB-S", "DVB-T", "DVB-C", "ATSC", "ISDB-T", "DMB-T", "CMMB"
        ])
        self.input_source.setCurrentText("UDP")
        self.input_source.setStyleSheet("font-size: 13px; padding: 8px;")
        config_layout.addWidget(self.input_source, 0, 1)
        
        # Input address/URL
        config_layout.addWidget(QLabel("Address/URL:"), 1, 0)
        self.input_address = QLineEdit()
        self.input_address.setText("127.0.0.1:9999")
        self.input_address.setPlaceholderText("Enter input address (e.g., 127.0.0.1:9999, file.ts, srt://host:port)")
        self.input_address.setStyleSheet("font-size: 13px; padding: 8px;")
        config_layout.addWidget(self.input_address, 1, 1)
        
        # Analysis options
        config_layout.addWidget(QLabel("Analysis Options:"), 2, 0)
        self.analysis_options = QComboBox()
        self.analysis_options.addItems([
            "Basic Analysis",
            "Detailed Analysis", 
            "SCTE-35 Focus",
            "Service Analysis",
            "PID Analysis",
            "Bitrate Analysis"
        ])
        self.analysis_options.setCurrentText("SCTE-35 Focus")
        self.analysis_options.setStyleSheet("font-size: 13px; padding: 8px;")
        config_layout.addWidget(self.analysis_options, 2, 1)
        
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_analysis_btn = QPushButton("🔍 Start Analysis")
        self.start_analysis_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        self.start_analysis_btn.clicked.connect(self.start_analysis)
        
        self.stop_analysis_btn = QPushButton("⏹️ Stop Analysis")
        self.stop_analysis_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; padding: 10px; }")
        self.stop_analysis_btn.clicked.connect(self.stop_analysis)
        self.stop_analysis_btn.setEnabled(False)
        
        self.clear_btn = QPushButton("🗑️ Clear Results")
        self.clear_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; padding: 10px; }")
        self.clear_btn.clicked.connect(self.clear_results)
        
        button_layout.addWidget(self.start_analysis_btn)
        button_layout.addWidget(self.stop_analysis_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Analysis results
        results_group = QGroupBox("Analysis Results")
        results_layout = QVBoxLayout()
        
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setFont(QFont("Monaco", 9))
        self.results.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        results_layout.addWidget(self.results)
        
        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)
        
        self.setLayout(main_layout)
    
    def start_analysis(self):
        """Start TSAnalyzer analysis"""
        try:
            input_type = self.input_source.currentText().lower()
            input_address = self.input_address.text()
            analysis_type = self.analysis_options.currentText()
            
            if not input_address:
                QMessageBox.warning(self, "Input Required", "Please enter an input address/URL")
                return
            
            # Build TSAnalyzer command based on analysis type
            command = self.build_analyzer_command(input_type, input_address, analysis_type)
            
            self.results.append(f"🔍 Starting TSAnalyzer analysis...")
            self.results.append(f"📋 Command: {' '.join(command)}")
            self.results.append("=" * 60)
            
            self.analyzer_process = TSDuckProcessor(command)
            self.analyzer_process.output_received.connect(self.results.append)
            self.analyzer_process.error_received.connect(self.append_analysis_error)
            self.analyzer_process.finished.connect(self.analysis_finished)
            
            self.analyzer_process.start()
            
            self.start_analysis_btn.setEnabled(False)
            self.stop_analysis_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start analysis: {str(e)}")
    
    def stop_analysis(self):
        """Stop TSAnalyzer analysis"""
        if self.analyzer_process:
            self.analyzer_process.stop()
            self.results.append("⏹️ Analysis stopped by user")
    
    def analysis_finished(self, exit_code: int):
        """Handle analysis finished"""
        self.start_analysis_btn.setEnabled(True)
        self.stop_analysis_btn.setEnabled(False)
        
        if exit_code == 0:
            self.results.append("=" * 60)
            self.results.append("✅ Analysis completed successfully")
        else:
            self.results.append("=" * 60)
            self.results.append(f"❌ Analysis failed with exit code {exit_code}")
    
    def append_analysis_error(self, text: str):
        """Append error text to analysis results"""
        self.results.append(f"<span style='color: #ff6b6b;'>{text}</span>")
    
    def clear_results(self):
        """Clear analysis results"""
        self.results.clear()
    
    def build_analyzer_command(self, input_type: str, input_address: str, analysis_type: str) -> List[str]:
        """Build TSAnalyzer command"""
        command = ["tsp", "-I", input_type, input_address]
        
        # Add analysis plugin based on type
        if analysis_type == "Basic Analysis":
            command.extend(["-P", "analyze", "-O", "drop"])
        elif analysis_type == "Detailed Analysis":
            command.extend(["-P", "analyze", "--json", "-O", "drop"])
        elif analysis_type == "SCTE-35 Focus":
            command.extend(["-P", "analyze", "--json", "-P", "splicemonitor", "-O", "drop"])
        elif analysis_type == "Service Analysis":
            command.extend(["-P", "analyze", "--json", "-P", "services", "-O", "drop"])
        elif analysis_type == "PID Analysis":
            command.extend(["-P", "analyze", "--json", "-P", "pids", "-O", "drop"])
        elif analysis_type == "Bitrate Analysis":
            command.extend(["-P", "analyze", "--json", "-P", "bitrate_monitor", "-O", "drop"])
        
        return command


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.processor = None
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("ITAssist Broadcast Encoder - 100 (IBE-100)")
        self.setMinimumSize(900, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Enterprise-grade tab organization
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #444; 
                background-color: #2a2a2a; 
                border-radius: 8px;
            }
            QTabBar::tab { 
                background-color: #3a3a3a; 
                color: white; 
                padding: 12px 24px; 
                margin-right: 2px; 
                border-radius: 6px 6px 0 0;
                font-weight: bold;
                font-size: 14px;
            }
            QTabBar::tab:selected { 
                background-color: #4CAF50; 
                color: white;
            }
            QTabBar::tab:hover { 
                background-color: #555; 
            }
        """)
        
        # Configuration Tab - All settings in one place
        self.config_widget = ConfigurationWidget()
        self.tab_widget.addTab(self.config_widget, "⚙️ Configuration")
        
        # Monitoring Tab - Real-time analytics and status
        self.monitoring_widget = MonitoringWidget()
        self.tab_widget.addTab(self.monitoring_widget, "📊 Monitoring")
        
        # Tools Tab - Analyzer and utilities
        self.tools_widget = ToolsWidget()
        self.tab_widget.addTab(self.tools_widget, "🔧 Tools")
        
        # Help Tab - Enterprise documentation
        self.help_widget = HelpWidget()
        self.tab_widget.addTab(self.help_widget, "📚 Help")
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️ Start Processing")
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 12px; font-size: 14px; }")
        self.start_btn.clicked.connect(self.start_processing)
        
        self.stop_btn = QPushButton("⏹️ Stop Processing")
        self.stop_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; padding: 12px; font-size: 14px; }")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        
        self.kill_btn = QPushButton("💀 Kill All Processes")
        self.kill_btn.setStyleSheet("QPushButton { background-color: #ff5722; color: white; font-weight: bold; padding: 12px; font-size: 14px; }")
        self.kill_btn.clicked.connect(self.kill_all_processes)
        
        self.load_config_btn = QPushButton("📁 Load Config")
        self.load_config_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 8px; }")
        self.load_config_btn.clicked.connect(self.load_configuration)
        
        self.save_config_btn = QPushButton("💾 Save Config")
        self.save_config_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; padding: 8px; }")
        self.save_config_btn.clicked.connect(self.save_configuration)
        
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(self.kill_btn)
        control_layout.addWidget(self.load_config_btn)
        control_layout.addWidget(self.save_config_btn)
        control_layout.addStretch()
        
        # Add widgets to main layout
        main_layout.addWidget(self.tab_widget)
        main_layout.addLayout(control_layout)
        
        central_widget.setLayout(main_layout)
        
        # Status bar with footer
        self.statusBar().showMessage("Ready")
        
        # Add permanent footer
        footer_widget = QWidget()
        footer_layout = QHBoxLayout()
        
        # Copyright and company info
        footer_text = QLabel("© 2024 ITAssist Broadcast Solutions | Dubai • Mumbai • Gurugram | Professional SCTE-35 Streaming")
        footer_text.setStyleSheet("""
            QLabel {
                color: #888;
                font-size: 11px;
                padding: 5px;
                background-color: #1a1a1a;
                border-top: 1px solid #333;
            }
        """)
        footer_layout.addWidget(footer_text)
        footer_layout.addStretch()
        
        # Version info
        version_text = QLabel("IBE-100 v1.0")
        version_text.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 11px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        footer_layout.addWidget(version_text)
        
        footer_widget.setLayout(footer_layout)
        footer_widget.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border-top: 1px solid #333;
            }
        """)
        
        # Add footer to status bar
        self.statusBar().addPermanentWidget(footer_widget)
        
    def setup_connections(self):
        """Setup signal connections"""
        pass
    
    def find_tsp_binary(self) -> str:
        """Find TSDuck tsp binary automatically"""
        import shutil
        
        # Try common locations in order of preference
        possible_paths = [
            "/usr/local/bin/tsp",  # macOS Homebrew (most common)
            "/usr/bin/tsp",  # Linux
            "/opt/tsduck/bin/tsp",  # Linux custom install
            "C:\\Program Files\\TSDuck\\bin\\tsp.exe",  # Windows
            "C:\\Program Files (x86)\\TSDuck\\bin\\tsp.exe"  # Windows 32-bit
        ]
        
        # First try absolute paths
        for path in possible_paths:
            if shutil.which(path):
                print(f"✅ Found TSDuck at: {path}")
                return path
        
        # If no absolute path found, try "tsp" in PATH
        tsp_in_path = shutil.which("tsp")
        if tsp_in_path:
            print(f"✅ Found TSDuck in PATH: {tsp_in_path}")
            return tsp_in_path
                
        # Fallback to just "tsp" if nothing found
        print("⚠️ TSDuck not found, using 'tsp' as fallback")
        return "tsp"
    
    def build_command(self) -> List[str]:
        """Build TSDuck command from configuration with manual VPID/APID"""
        # Get configuration from the new enterprise structure
        all_config = self.config_widget.get_all_config()
        input_config = all_config["input"]
        output_config = all_config["output"]
        service_config = all_config["service"]
        scte35_config = all_config["scte35"]
        tsduck_config = all_config["tsduck"]
        
        # Use configured TSDuck path or fallback to auto-detection
        tsp_binary = tsduck_config.get("tsduck_path", "tsp")
        if not tsp_binary or tsp_binary == "tsp":
            tsp_binary = self.find_tsp_binary()
        
        # Debug: Show which TSDuck binary is being used
        print(f"🔍 Using TSDuck binary: {tsp_binary}")
        
        # Get input configuration
        input_type = input_config["type"].lower()
        input_source = input_config["source"]
        input_params = input_config.get("params", "")
        
        # Fix input format according to TSDuck documentation for all input types
        if input_type == "srt":
            # TSDuck SRT input: extract host:port and handle streamid separately
            if "://" in input_source:
                # Extract host:port from srt://host:port?streamid=...
                srt_url = input_source.replace("srt://", "")
                if "?" in srt_url:
                    # Split into host:port and streamid
                    host_port = srt_url.split("?")[0]
                    streamid_part = srt_url.split("?")[1]
                    if "streamid=" in streamid_part:
                        streamid_value = streamid_part.split("streamid=")[1]
                        # Store streamid for later use
                        input_source = host_port
                        # Add streamid as a parameter
                        if not input_params:
                            input_params = f"--streamid {streamid_value}"
                        else:
                            input_params += f" --streamid {streamid_value}"
                    else:
                        input_source = host_port
                else:
                    input_source = srt_url
            else:
                # Already in host:port format
                input_source = input_source
        elif input_type == "udp":
            # TSDuck UDP input: host:port format
            if "://" in input_source:
                clean_url = input_source.replace("udp://", "")
                input_source = clean_url
        elif input_type == "tcp":
            # TSDuck TCP input: host:port format
            if "://" in input_source:
                clean_url = input_source.replace("tcp://", "")
                input_source = clean_url
        elif input_type == "hls":
            # TSDuck HLS input: full URL format
            # Keep the full URL as is for HLS
            pass
        elif input_type == "http" or input_type == "https":
            # TSDuck HTTP input: full URL format
            # Keep the full URL as is
            pass
        elif input_type == "file":
            # TSDuck File input: file path
            # Keep the file path as is
            pass
        elif input_type in ["dvb", "asi", "dektec"]:
            # TSDuck hardware input: device path or parameters
            # Keep as is for hardware inputs
            pass
        
        # Build command with proper service and PID configuration
        # Using official TSDuck documentation patterns
        command = [
            tsp_binary,
            "-I", input_type, input_source,
        ]
        
        # Add input parameters if specified
        if input_params:
            command.extend(input_params.split())
        
        # Add SRT-specific parameters for input
        if input_type == "srt":
            # Add SRT input parameters based on TSDuck documentation
            srt_params = [
                "--transtype", "live",  # Set transmission type to live
                "--messageapi",         # Enable message API for SRT
                "--latency", "2000"     # Set latency to 2000ms
            ]
            command.extend(srt_params)
        
        # Add processing plugins
        command.extend([
            # Set service name and provider using SDT plugin (TSDuck standard)
            "-P", "sdt", "--service", str(service_config["service_id"]), 
            "--name", service_config["service_name"], "--provider", service_config["provider_name"],
            # Remap existing PIDs to distributor requirements
            "-P", "remap", 
            "211=" + str(service_config['vpid']),  # Video: 211 → 256
            "221=" + str(service_config['apid']),  # Audio: 221 → 257
            # Configure PIDs using PMT plugin
            "-P", "pmt", "--service", str(service_config["service_id"]), 
            "--add-pid", f"{service_config['vpid']}/0x1b",  # Video PID with H.264 type
            "--add-pid", f"{service_config['apid']}/0x0f",   # Audio PID with AAC type
            "--add-pid", f"{service_config['scte35_pid']}/0x86",  # SCTE-35 PID
            # Inject SCTE-35 markers
            "-P", "spliceinject", "--service", str(service_config["service_id"]), 
            "--files", "scte35_final/*.xml",
            "--inject-count", "1", "--inject-interval", "1000", "--start-delay", "2000",
            # Output configuration
            "-O", output_config["type"].lower(),
            *self.get_output_params(output_config)
        ])
        return command
    
    def get_output_params(self, output_config):
        """Get output parameters based on output type"""
        output_type = output_config["type"].lower()
        destination = output_config.get("destination", "")
        params = output_config.get("params", "")
        
        if output_type == "srt":
            # SRT parameters are strictly user-defined - no automatic defaults
            srt_params = []
            
            # Only parse destination if it's provided and contains URL info
            if destination:
                if '://' in destination:
                    # Handle srt://host:port format - extract host:port only
                    url_part = destination.split('://', 1)[1]
                    if '?' in url_part:
                        host_port, query = url_part.split('?', 1)
                        # Only add --caller if user hasn't specified it in params
                        if not params or '--caller' not in params:
                            srt_params.extend(["--caller", host_port])
                        
                        # Parse query parameters only if user hasn't specified them
                        for param in query.split('&'):
                            if '=' in param:
                                key, value = param.split('=', 1)
                                if key == 'streamid' and (not params or '--streamid' not in params):
                                    srt_params.extend(["--streamid", value])
                    else:
                        # Only add --caller if user hasn't specified it in params
                        if not params or '--caller' not in params:
                            srt_params.extend(["--caller", url_part])
                else:
                    # Direct host:port format - only add if user hasn't specified --caller
                    if not params or '--caller' not in params:
                        srt_params.extend(["--caller", destination])
            
            # Add ONLY user-defined parameters from params field
            if params:
                param_list = params.split()
                srt_params.extend(param_list)
            
            # Return only user-defined parameters - no defaults
            return srt_params
        elif output_type == "udp":
            return ["--local", destination]
        elif output_type == "tcp":
            return ["--local", destination]
        elif output_type == "file":
            return [destination]
        else:
            # Default parameters
            if destination:
                return [destination]
            return []
    
    def start_processing(self):
        """Start IBE-100 processing"""
        try:
            # Get configuration from the new enterprise structure
            all_config = self.config_widget.get_all_config()
            service_config = all_config["service"]
            scte35_config = all_config["scte35"]
            
            command = self.build_command()
            # Get console widget from monitoring tab
            console_widget = self.monitoring_widget.console_widget
            
            # Get input and output configuration for display
            input_config = all_config["input"]
            output_config = all_config["output"]
            
            # Get the processed input format from build_command
            processed_input_type = input_config["type"].lower()
            processed_input_source = input_config["source"]
            
            # Apply the same input format processing as in build_command
            if processed_input_type == "srt":
                # For SRT, keep the full URL with streamid
                if "://" in processed_input_source:
                    processed_input_source = processed_input_source  # Keep full SRT URL
                else:
                    processed_input_source = processed_input_source
            elif processed_input_type == "udp":
                if "://" in processed_input_source:
                    clean_url = processed_input_source.replace("udp://", "")
                    processed_input_source = clean_url
            elif processed_input_type == "tcp":
                if "://" in processed_input_source:
                    clean_url = processed_input_source.replace("tcp://", "")
                    processed_input_source = clean_url
            
            console_widget.append_output(f"🚀 Starting IBE-100 processing...")
            console_widget.append_output(f"🔍 TSDuck Binary: {command[0]}")
            console_widget.append_output(f"📥 Input Configuration:")
            console_widget.append_output(f"   Type: {input_config['type'].upper()}")
            console_widget.append_output(f"   Source: {input_config['source']}")
            if input_config.get('params'):
                console_widget.append_output(f"   Parameters: {input_config['params']}")
            console_widget.append_output(f"   TSDuck Format: {processed_input_type} {processed_input_source}")
            console_widget.append_output(f"📤 Output Configuration:")
            console_widget.append_output(f"   Type: {output_config['type'].upper()}")
            console_widget.append_output(f"   Destination: {output_config.get('destination', 'N/A')}")
            console_widget.append_output(f"📺 DISTRIBUTOR STREAM SPECIFICATIONS:")
            console_widget.append_output(f"   📺 Video: 1920x1080 HD, H.264, 5 Mbps, GOP:12, B-Frames:5")
            console_widget.append_output(f"   🎵 Audio: AAC-LC, 128 Kbps, -20 db, 48 Khz")
            console_widget.append_output(f"📋 Service Configuration:")
            console_widget.append_output(f"   Service: {service_config['service_name']} (ID: {service_config['service_id']})")
            console_widget.append_output(f"   Provider: {service_config['provider_name']}")
            console_widget.append_output(f"🔄 PID Remapping (HLS → Distributor):")
            console_widget.append_output(f"   Video PID: 211 → {service_config['vpid']} (H.264)")
            console_widget.append_output(f"   Audio PID: 221 → {service_config['apid']} (AAC-LC)")
            console_widget.append_output(f"   SCTE-35 PID: {service_config['scte35_pid']} (unchanged)")
            console_widget.append_output(f"   Null PID: {service_config['null_pid']}")
            console_widget.append_output(f"🎬 SCTE-35 Configuration:")
            console_widget.append_output(f"   Ad Duration: {scte35_config['ad_duration']} seconds")
            console_widget.append_output(f"   Event ID: {scte35_config['event_id']}")
            console_widget.append_output(f"   Pre-roll: {scte35_config['preroll_duration']} seconds")
            console_widget.append_output(f"📋 Command: {' '.join(command)}")
            
            self.processor = TSDuckProcessor(command)
            self.processor.output_received.connect(console_widget.append_output)
            self.processor.error_received.connect(console_widget.append_error)
            self.processor.finished.connect(self.processing_finished)
            
            self.processor.start()
            
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.statusBar().showMessage("Processing...")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start processing: {str(e)}")
    
    def stop_processing(self):
        """Stop IBE-100 processing"""
        if self.processor:
            self.processor.stop()
            self.monitoring_widget.console_widget.append_output("⏹️ Stopping processing...")
    
    def kill_all_processes(self):
        """Kill all TSDuck and related processes"""
        try:
            import subprocess
            import os
            
            self.monitoring_widget.console_widget.append_output("💀 Killing all TSDuck processes...")
            
            # Kill TSDuck processes
            try:
                subprocess.run(["pkill", "-f", "tsp"], check=False)
                self.monitoring_widget.console_widget.append_output("✅ Killed all tsp processes")
            except Exception as e:
                self.monitoring_widget.console_widget.append_output(f"⚠️ Error killing tsp processes: {e}")
            
            # Kill GUI processes
            try:
                subprocess.run(["pkill", "-f", "tsduck_gui_simplified.py"], check=False)
                self.monitoring_widget.console_widget.append_output("✅ Killed all GUI processes")
            except Exception as e:
                self.monitoring_widget.console_widget.append_output(f"⚠️ Error killing GUI processes: {e}")
            
            # Kill any remaining TSDuck processes
            try:
                subprocess.run(["pkill", "-f", "tsduck"], check=False)
                self.monitoring_widget.console_widget.append_output("✅ Killed all TSDuck processes")
            except Exception as e:
                self.monitoring_widget.console_widget.append_output(f"⚠️ Error killing TSDuck processes: {e}")
            
            # Check for remaining processes
            try:
                result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
                tsp_count = result.stdout.count("tsp")
                tsduck_count = result.stdout.count("tsduck")
                
                if tsp_count == 0 and tsduck_count == 0:
                    self.monitoring_widget.console_widget.append_output("✅ All TSDuck processes killed successfully")
                else:
                    self.monitoring_widget.console_widget.append_output(f"⚠️ {tsp_count} tsp processes and {tsduck_count} tsduck processes still running")
                    
            except Exception as e:
                self.monitoring_widget.console_widget.append_output(f"⚠️ Error checking remaining processes: {e}")
            
            # Reset GUI state
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.statusBar().showMessage("All processes killed")
            
        except Exception as e:
            self.monitoring_widget.console_widget.append_output(f"❌ Error killing processes: {e}")
            QMessageBox.critical(self, "Error", f"Failed to kill processes: {str(e)}")
    
    def processing_finished(self, exit_code: int):
        """Handle processing finished"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if exit_code == 0:
            self.statusBar().showMessage("Processing completed successfully")
            self.monitoring_widget.console_widget.append_output("✅ Processing completed successfully")
        else:
            self.statusBar().showMessage(f"Processing failed with exit code {exit_code}")
            self.monitoring_widget.console_widget.append_error(f"❌ Processing failed with exit code {exit_code}")
    
    def load_configuration(self, config_dict=None):
        """Load configuration from file or dictionary"""
        if config_dict is not None:
            # Load from provided dictionary
            self.apply_configuration(config_dict)
            return
        
        # Load from file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Configuration", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config = json.load(f)
                self.apply_configuration(config)
                self.monitoring_widget.console_widget.append_output(f"📁 Configuration loaded from {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load configuration: {str(e)}")
    
    def save_configuration(self):
        """Save configuration to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "tsduck_config.json", "JSON Files (*.json)"
        )
        if file_path:
            try:
                config = self.get_configuration()
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=2)
                self.monitoring_widget.console_widget.append_output(f"💾 Configuration saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")
    
    def get_configuration(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config_widget.get_all_config()
    
    def apply_configuration(self, config: Dict[str, Any]):
        """Apply configuration to widgets"""
        if "input" in config:
            input_config = config["input"]
            self.config_widget.input_widget.type_combo.setCurrentText(input_config.get("type", "hls").title())
            self.config_widget.input_widget.source_edit.setText(input_config.get("source", ""))
            self.config_widget.input_widget.params_edit.setText(input_config.get("params", ""))
        
        if "output" in config:
            output_config = config["output"]
            self.config_widget.output_widget.type_combo.setCurrentText(output_config.get("type", "srt").title())
            
            # Handle both 'destination' and 'source' fields for backward compatibility
            destination = output_config.get("destination", output_config.get("source", ""))
            self.config_widget.output_widget.dest_edit.setText(destination)
            self.config_widget.output_widget.params_edit.setText(output_config.get("params", ""))
        
        if "service" in config:
            service_config = config["service"]
            # Service information
            self.config_widget.service_widget.service_name.setText(service_config.get("service_name", "SCTE-35 Stream"))
            self.config_widget.service_widget.provider_name.setText(service_config.get("provider_name", "ITAssist"))
            self.config_widget.service_widget.service_id.setValue(service_config.get("service_id", 1))
            
            # PID configuration
            self.config_widget.service_widget.vpid.setValue(service_config.get("vpid", 256))
            self.config_widget.service_widget.apid.setValue(service_config.get("apid", 257))
            self.config_widget.service_widget.scte35_pid.setValue(service_config.get("scte35_pid", 500))
            self.config_widget.service_widget.null_pid.setValue(service_config.get("null_pid", 8191))
            self.config_widget.service_widget.pcr_pid.setValue(service_config.get("pcr_pid", 256))
        
        if "scte35" in config:
            scte35_config = config["scte35"]
            # SCTE-35 configuration
            self.config_widget.scte35_widget.ad_duration.setValue(scte35_config.get("ad_duration", 600))
            self.config_widget.scte35_widget.event_id.setValue(scte35_config.get("event_id", 100023))
            self.config_widget.scte35_widget.preroll_duration.setValue(scte35_config.get("preroll_duration", 0))
            
            # Plugin configuration
            self.config_widget.scte35_widget.pmt_enabled.setChecked(scte35_config.get("pmt_enabled", True))
            self.config_widget.scte35_widget.pmt_params.setText(scte35_config.get("pmt_params", ""))
            self.config_widget.scte35_widget.spliceinject_enabled.setChecked(scte35_config.get("spliceinject_enabled", True))
            self.config_widget.scte35_widget.spliceinject_params.setText(scte35_config.get("spliceinject_params", ""))


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("ITAssist Broadcast Encoder - 100 (IBE-100)")
    
        # Set application style
    try:
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
    except ImportError:
        # Fallback style
        app.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; color: #ffffff; }
            QTabWidget::pane { border: 1px solid #555; background-color: #2b2b2b; }
            QTabBar::tab { background-color: #3c3c3c; color: #ffffff; padding: 8px 16px; margin-right: 2px; }
            QTabBar::tab:selected { background-color: #4CAF50; }
            QTabBar::tab:hover { background-color: #555; }
            QGroupBox { font-weight: bold; border: 2px solid #555; border-radius: 8px; margin: 8px; padding-top: 15px; }
            QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 8px 0 8px; color: #4CAF50; }
            QLineEdit { background-color: #3c3c3c; border: 1px solid #555; padding: 8px; border-radius: 4px; font-size: 12px; }
            QComboBox { background-color: #3c3c3c; border: 1px solid #555; padding: 8px; border-radius: 4px; font-size: 12px; }
            QCheckBox { font-size: 12px; spacing: 8px; }
            QCheckBox::indicator { width: 16px; height: 16px; }
            QCheckBox::indicator:checked { background-color: #4CAF50; border: 1px solid #4CAF50; }
            QPushButton { border: none; padding: 8px; border-radius: 6px; font-size: 12px; }
            QPushButton:hover { opacity: 0.9; }
            QPushButton:pressed { opacity: 0.7; }
            QTextEdit { background-color: #1e1e1e; color: #ffffff; border: 1px solid #555; border-radius: 4px; font-family: 'Monaco', 'Consolas', monospace; }
        """)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Load working configuration if available
    try:
        with open('gui_working_config.json', 'r') as f:
            config = json.load(f)
        window.apply_configuration(config)
        window.monitoring_widget.console_widget.append_output("✅ Working configuration loaded automatically")
    except FileNotFoundError:
        window.monitoring_widget.console_widget.append_output("ℹ️ Using default configuration")
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
