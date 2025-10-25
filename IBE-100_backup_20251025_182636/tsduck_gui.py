#!/usr/bin/env python3
"""
TSDuck GUI Encoder/Decoder
A comprehensive GUI application for MPEG Transport Stream processing using TSDuck
"""

import sys
import os
import json
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import queue

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QTabWidget, QGroupBox, QLabel, QLineEdit, QPushButton,
    QComboBox, QSpinBox, QCheckBox, QTextEdit, QProgressBar, QSlider,
    QFileDialog, QMessageBox, QSplitter, QTreeWidget, QTreeWidgetItem,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QScrollArea,
    QListWidget, QListWidgetItem, QDialog, QDialogButtonBox, QFormLayout
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QSettings, QSize, QRect
)
from PyQt6.QtGui import (
    QFont, QIcon, QPalette, QColor, QPixmap, QAction, QKeySequence
)

# Import GUI optimizations
try:
    from gui_optimizer import (
        OptimizedStyleSheet, PerformanceOptimizer, ResponsiveLayout,
        KeyboardShortcuts, ThemeManager, MemoryOptimizer, LoadingIndicator,
        optimize_main_window
    )
    GUI_OPTIMIZATIONS_AVAILABLE = True
except ImportError:
    GUI_OPTIMIZATIONS_AVAILABLE = False
    print("Warning: GUI optimizations not available")

# Try to import TSDuck Python bindings
try:
    import tsduck
    TSDUCK_AVAILABLE = True
except ImportError:
    TSDUCK_AVAILABLE = False
    print("Warning: TSDuck Python bindings not available. Some features may be limited.")


class TSDuckProcessor(QThread):
    """Thread for running TSDuck commands"""
    output_received = pyqtSignal(str)
    error_received = pyqtSignal(str)
    finished = pyqtSignal(int)  # exit code
    progress_updated = pyqtSignal(int)
    
    def __init__(self, command: List[str]):
        super().__init__()
        self.command = command
        self.process = None
        self._stop_requested = False
        
    def run(self):
        """Execute the TSDuck command"""
        try:
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output in real-time
            while True:
                if self._stop_requested:
                    if self.process:
                        self.process.terminate()
                    break
                    
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.output_received.emit(output.strip())
                    
            # Get any remaining output
            stdout, stderr = self.process.communicate()
            if stdout:
                self.output_received.emit(stdout)
            if stderr:
                self.error_received.emit(stderr)
                
            self.finished.emit(self.process.returncode)
            
        except Exception as e:
            self.error_received.emit(f"Error executing command: {str(e)}")
            self.finished.emit(-1)
    
    def stop(self):
        """Stop the process"""
        self._stop_requested = True
        if self.process:
            self.process.terminate()


class StreamMonitor(QThread):
    """Thread for monitoring stream statistics"""
    stats_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self._running = False
        
    def run(self):
        """Monitor stream statistics"""
        self._running = True
        while self._running:
            # Simulate stream monitoring
            stats = {
                'bitrate': 15000000,  # 15 Mbps
                'packets_per_second': 25000,
                'errors': 0,
                'pcr_accuracy': 99.9,
                'continuity_errors': 0
            }
            self.stats_updated.emit(stats)
            time.sleep(1)
    
    def stop(self):
        """Stop monitoring"""
        self._running = False


class SCTE35Dialog(QDialog):
    """Dialog for SCTE-35 splice configuration"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SCTE-35 Splice Configuration")
        self.setModal(True)
        self.resize(500, 400)
        
        layout = QVBoxLayout()
        
        # Splice type
        form_layout = QFormLayout()
        self.splice_type = QComboBox()
        self.splice_type.addItems([
            "splice_insert",
            "time_signal", 
            "bandwidth_reservation",
            "private_command"
        ])
        form_layout.addRow("Splice Type:", self.splice_type)
        
        # Event ID
        self.event_id = QSpinBox()
        self.event_id.setRange(0, 0x7FFFFFFF)  # Max 32-bit signed integer
        self.event_id.setValue(1)
        form_layout.addRow("Event ID:", self.event_id)
        
        # Splice time
        self.splice_time = QLineEdit()
        self.splice_time.setPlaceholderText("YYYY-MM-DD HH:MM:SS.mmm")
        form_layout.addRow("Splice Time:", self.splice_time)
        
        # Duration
        self.duration = QLineEdit()
        self.duration.setPlaceholderText("HH:MM:SS.mmm")
        form_layout.addRow("Duration:", self.duration)
        
        # Out of network
        self.out_of_network = QCheckBox()
        form_layout.addRow("Out of Network:", self.out_of_network)
        
        # Immediate
        self.immediate = QCheckBox()
        form_layout.addRow("Immediate:", self.immediate)
        
        # Unique program ID
        self.unique_program_id = QSpinBox()
        self.unique_program_id.setRange(0, 0xFFFF)
        self.unique_program_id.setValue(1)
        form_layout.addRow("Unique Program ID:", self.unique_program_id)
        
        # Avail number
        self.avail_num = QSpinBox()
        self.avail_num.setRange(0, 255)
        form_layout.addRow("Avail Number:", self.avail_num)
        
        # Avails expected
        self.avails_expected = QSpinBox()
        self.avails_expected.setRange(0, 255)
        form_layout.addRow("Avails Expected:", self.avails_expected)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_config(self) -> Dict[str, Any]:
        """Get the SCTE-35 configuration"""
        return {
            'splice_type': self.splice_type.currentText(),
            'event_id': self.event_id.value(),
            'splice_time': self.splice_time.text(),
            'duration': self.duration.text(),
            'out_of_network': self.out_of_network.isChecked(),
            'immediate': self.immediate.isChecked(),
            'unique_program_id': self.unique_program_id.value(),
            'avail_num': self.avail_num.value(),
            'avails_expected': self.avails_expected.value()
        }


class InputOutputWidget(QGroupBox):
    """Widget for input/output configuration"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QGridLayout()
        
        # Input/Output type
        layout.addWidget(QLabel("Type:"), 0, 0)
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "File",
            "UDP",
            "TCP", 
            "HTTP",
            "HLS",
            "SRT",
            "RIST",
            "DVB-T",
            "DVB-S",
            "DVB-C",
            "ATSC",
            "ISDB",
            "ASI",
            "Dektec",
            "HiDes",
            "VATek"
        ])
        layout.addWidget(self.type_combo, 0, 1)
        
        # Source/Destination
        layout.addWidget(QLabel("Source/Destination:"), 1, 0)
        self.source_edit = QLineEdit()
        layout.addWidget(self.source_edit, 1, 1)
        
        # Browse button
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_btn, 1, 2)
        
        # Preview button
        self.preview_btn = QPushButton("Preview")
        self.preview_btn.clicked.connect(self.preview_source)
        layout.addWidget(self.preview_btn, 1, 3)
        
        # Additional parameters
        layout.addWidget(QLabel("Parameters:"), 2, 0)
        self.params_edit = QLineEdit()
        self.params_edit.setPlaceholderText("Additional parameters (e.g., --port 1234)")
        layout.addWidget(self.params_edit, 2, 1, 1, 2)
        
        self.setLayout(layout)
    
    def browse_file(self):
        """Browse for file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*)"
        )
        if file_path:
            self.source_edit.setText(file_path)
    
    def preview_source(self):
        """Preview the source (placeholder for now)"""
        source = self.source_edit.text()
        if source:
            # This would trigger the source preview in the main window
            # For now, just show a message
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Source Preview", f"Previewing source: {source}")
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "No Source", "Please specify a source first")
    
    def get_config(self) -> Dict[str, str]:
        """Get configuration"""
        return {
            'type': self.type_combo.currentText(),
            'source': self.source_edit.text(),
            'params': self.params_edit.text()
        }


class PluginWidget(QGroupBox):
    """Widget for plugin configuration"""
    
    def __init__(self, plugin_name: str, parent=None):
        super().__init__(f"Plugin: {plugin_name}", parent)
        self.plugin_name = plugin_name
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Enable checkbox
        self.enabled = QCheckBox("Enable")
        layout.addWidget(self.enabled)
        
        # Parameters
        layout.addWidget(QLabel("Parameters:"))
        self.params_edit = QLineEdit()
        self.params_edit.setPlaceholderText("Plugin parameters")
        layout.addWidget(self.params_edit)
        
        # Description
        self.desc_label = QLabel(self.get_plugin_description())
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(self.desc_label)
        
        self.setLayout(layout)
    
    def get_plugin_description(self) -> str:
        """Get plugin description"""
        descriptions = {
            'analyze': 'Analyze transport stream and display statistics',
            'bitrate_monitor': 'Monitor bitrate and send metrics to InfluxDB',
            'continuity': 'Check and fix continuity counter errors',
            'count': 'Count packets and display statistics',
            'dump': 'Dump packet content in various formats',
            'filter': 'Filter packets based on PID, service, etc.',
            'inject': 'Inject sections or tables into the stream',
            'limit': 'Limit the bitrate of the stream',
            'merge': 'Merge multiple transport streams',
            'mux': 'Multiplex services into a transport stream',
            'pat': 'Manipulate PAT (Program Association Table)',
            'pmt': 'Manipulate PMT (Program Map Table)',
            'regulate': 'Regulate output bitrate',
            'remap': 'Remap PIDs in the transport stream',
            'spliceinject': 'Inject SCTE-35 splice information',
            'splicemonitor': 'Monitor SCTE-35 splice information',
            'stats': 'Display transport stream statistics',
            'stuffanalyze': 'Analyze stuffing packets',
            'svremove': 'Remove services from transport stream',
            'svrename': 'Rename services in transport stream',
            'teletext': 'Extract or inject Teletext data',
            'time': 'Add or modify time information',
            'tstables': 'Manipulate various tables'
        }
        return descriptions.get(self.plugin_name, 'No description available')
    
    def get_config(self) -> Dict[str, Any]:
        """Get plugin configuration"""
        return {
            'enabled': self.enabled.isChecked(),
            'params': self.params_edit.text()
        }


class SourcePreviewWidget(QGroupBox):
    """Widget for source preview functionality"""
    
    def __init__(self, parent=None):
        super().__init__("Source Preview", parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Preview controls
        controls_layout = QHBoxLayout()
        
        self.preview_btn = QPushButton("Preview Source")
        self.preview_btn.clicked.connect(self.start_preview)
        controls_layout.addWidget(self.preview_btn)
        
        self.stop_preview_btn = QPushButton("Stop Preview")
        self.stop_preview_btn.clicked.connect(self.stop_preview)
        self.stop_preview_btn.setEnabled(False)
        controls_layout.addWidget(self.stop_preview_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_preview)
        controls_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(controls_layout)
        
        # Preview tabs
        self.preview_tabs = QTabWidget()
        
        # Stream info tab
        self.stream_info_tab = QWidget()
        stream_layout = QVBoxLayout()
        
        self.stream_info_text = QTextEdit()
        self.stream_info_text.setReadOnly(True)
        if GUI_OPTIMIZATIONS_AVAILABLE:
            PerformanceOptimizer.optimize_text_widget(self.stream_info_text)
        else:
            self.stream_info_text.setFont(QFont("Monaco", 9))  # Use Monaco instead of Courier on macOS
        stream_layout.addWidget(self.stream_info_text)
        
        self.stream_info_tab.setLayout(stream_layout)
        self.preview_tabs.addTab(self.stream_info_tab, "Stream Info")
        
        # Services tab
        self.services_tab = QWidget()
        services_layout = QVBoxLayout()
        
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(4)
        self.services_table.setHorizontalHeaderLabels(["Service ID", "Name", "Type", "PIDs"])
        self.services_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Performance optimizations
        if GUI_OPTIMIZATIONS_AVAILABLE:
            PerformanceOptimizer.optimize_table(self.services_table)
        else:
            self.services_table.setAlternatingRowColors(True)
            self.services_table.setSortingEnabled(False)
            self.services_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        services_layout.addWidget(self.services_table)
        
        self.services_tab.setLayout(services_layout)
        self.preview_tabs.addTab(self.services_tab, "Services")
        
        # PIDs tab
        self.pids_tab = QWidget()
        pids_layout = QVBoxLayout()
        
        self.pids_table = QTableWidget()
        self.pids_table.setColumnCount(5)
        self.pids_table.setHorizontalHeaderLabels(["PID", "Type", "Bitrate", "Packets", "Description"])
        self.pids_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Performance optimizations
        if GUI_OPTIMIZATIONS_AVAILABLE:
            PerformanceOptimizer.optimize_table(self.pids_table)
        else:
            self.pids_table.setAlternatingRowColors(True)
            self.pids_table.setSortingEnabled(False)
            self.pids_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        pids_layout.addWidget(self.pids_table)
        
        self.pids_tab.setLayout(pids_layout)
        self.preview_tabs.addTab(self.pids_tab, "PIDs")
        
        # Tables tab
        self.tables_tab = QWidget()
        tables_layout = QVBoxLayout()
        
        self.tables_tree = QTreeWidget()
        self.tables_tree.setHeaderLabels(["Table", "PID", "Version", "Size", "Last Update"])
        tables_layout.addWidget(self.tables_tree)
        
        self.tables_tab.setLayout(tables_layout)
        self.preview_tabs.addTab(self.tables_tab, "Tables")
        
        layout.addWidget(self.preview_tabs)
        
        self.setLayout(layout)
        
        # Preview processor
        self.preview_processor = None
        self.input_config = None
        
    def start_preview(self):
        """Start source preview"""
        if not self.input_config:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "No Input", "Please configure input source first")
            return
            
        self.preview_btn.setEnabled(False)
        self.stop_preview_btn.setEnabled(True)
        
        # Import and use the real preview processor
        try:
            from source_preview import SourcePreviewProcessor, PreviewDataGenerator
            
            # For now, use sample data. In real implementation, use:
            # self.preview_processor = SourcePreviewProcessor()
            # self.preview_processor.start_preview(self.input_config, self.preview_callback)
            
            # Use sample data for demonstration
            sample_data = PreviewDataGenerator.generate_sample_data()
            self.preview_callback(sample_data)
            
        except ImportError:
            # Fallback to simulated data
            self.populate_preview_data()
        
    def stop_preview(self):
        """Stop source preview"""
        if self.preview_processor:
            self.preview_processor.stop()
        self.preview_btn.setEnabled(True)
        self.stop_preview_btn.setEnabled(False)
        
    def preview_callback(self, data: Dict[str, Any]):
        """Callback for preview data updates"""
        if 'error' in data:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Preview Error", data['error'])
            return
            
        # Update stream info
        if 'stream_info' in data:
            self.update_stream_info(data['stream_info'])
            
        # Update services
        if 'services' in data:
            self.update_services(data['services'])
            
        # Update PIDs
        if 'pids' in data:
            self.update_pids(data['pids'])
            
        # Update tables
        if 'tables' in data:
            self.update_tables(data['tables'])
            
    def update_stream_info(self, stream_info: Dict[str, Any]):
        """Update stream information display"""
        info_text = f"""
Transport Stream Analysis
========================
Bitrate: {stream_info['bitrate']:,} bps ({stream_info['bitrate']/1000000:.1f} Mbps)
Packets/sec: {stream_info['packets_per_second']:,}
Errors: {stream_info['errors']}
PCR accuracy: {stream_info['pcr_accuracy']:.1f}%
Continuity errors: {stream_info['continuity_errors']}
Services: {stream_info['services_count']}
PIDs: {stream_info['pids_count']}

Stream Properties:
"""
        
        # Add video streams
        if stream_info.get('video_streams'):
            info_text += "\nVideo Streams:\n"
            for stream in stream_info['video_streams']:
                info_text += f"- PID {stream['pid']}: {stream['type']}, {stream['resolution']}, {stream['fps']}fps\n"
                
        # Add audio streams
        if stream_info.get('audio_streams'):
            info_text += "\nAudio Streams:\n"
            for stream in stream_info['audio_streams']:
                info_text += f"- PID {stream['pid']}: {stream['type']}, {stream['channels']}, {stream['sample_rate']}\n"
                
        # Add data streams
        if stream_info.get('data_streams'):
            info_text += "\nData Streams:\n"
            for stream in stream_info['data_streams']:
                info_text += f"- PID {stream['pid']}: {stream['type']}"
                if 'languages' in stream:
                    info_text += f" ({', '.join(stream['languages'])})"
                info_text += "\n"
                
        self.stream_info_text.setPlainText(info_text)
        
    def update_services(self, services: List[Dict[str, Any]]):
        """Update services table"""
        self.services_table.setRowCount(len(services))
        for i, service in enumerate(services):
            self.services_table.setItem(i, 0, QTableWidgetItem(service['service_id']))
            self.services_table.setItem(i, 1, QTableWidgetItem(service['name']))
            self.services_table.setItem(i, 2, QTableWidgetItem(service['service_type']))
            self.services_table.setItem(i, 3, QTableWidgetItem(', '.join(service['pids'])))
            
    def update_pids(self, pids: List[Dict[str, Any]]):
        """Update PIDs table"""
        self.pids_table.setRowCount(len(pids))
        for i, pid in enumerate(pids):
            self.pids_table.setItem(i, 0, QTableWidgetItem(pid['pid']))
            self.pids_table.setItem(i, 1, QTableWidgetItem(pid['type']))
            self.pids_table.setItem(i, 2, QTableWidgetItem(f"{pid['bitrate']:,} bps"))
            self.pids_table.setItem(i, 3, QTableWidgetItem(f"{pid['packets']:,}"))
            self.pids_table.setItem(i, 4, QTableWidgetItem(pid['description']))
            
    def update_tables(self, tables: List[Dict[str, Any]]):
        """Update tables tree"""
        self.tables_tree.clear()
        for table in tables:
            item = QTreeWidgetItem([
                table['table_name'],
                table['pid'],
                str(table['version']),
                f"{table['size']} bytes",
                table['last_update']
            ])
            self.tables_tree.addTopLevelItem(item)
            
    def set_input_config(self, input_config: Dict[str, str]):
        """Set input configuration for preview"""
        self.input_config = input_config
        
    def refresh_preview(self):
        """Refresh preview data"""
        if self.preview_btn.isEnabled():
            self.start_preview()
            
    def populate_preview_data(self):
        """Populate preview data (simulated)"""
        # Stream info
        stream_info = """
Transport Stream Analysis
========================
Bitrate: 15.2 Mbps
Packets/sec: 25,000
Errors: 0
PCR accuracy: 99.9%
Continuity errors: 0
Services: 5
PIDs: 20

Stream Properties:
- Video: MPEG-2, 1920x1080, 25fps
- Audio: AC-3, 5.1 channels, 48kHz
- Subtitles: DVB subtitles, multiple languages
- Data: Teletext, EPG
        """
        self.stream_info_text.setPlainText(stream_info)
        
        # Services
        services_data = [
            ("0x100", "BBC One HD", "TV", "0x101, 0x102, 0x103"),
            ("0x200", "BBC Two HD", "TV", "0x201, 0x202, 0x203"),
            ("0x300", "BBC News", "TV", "0x301, 0x302"),
            ("0x400", "Radio 1", "Radio", "0x401"),
            ("0x500", "Radio 2", "Radio", "0x501")
        ]
        
        self.services_table.setRowCount(len(services_data))
        for i, (service_id, name, service_type, pids) in enumerate(services_data):
            self.services_table.setItem(i, 0, QTableWidgetItem(service_id))
            self.services_table.setItem(i, 1, QTableWidgetItem(name))
            self.services_table.setItem(i, 2, QTableWidgetItem(service_type))
            self.services_table.setItem(i, 3, QTableWidgetItem(pids))
            
        # PIDs
        pids_data = [
            ("0x000", "PAT", "1.2 Mbps", "25,000", "Program Association Table"),
            ("0x100", "PMT", "0.1 Mbps", "2,000", "Program Map Table - BBC One"),
            ("0x101", "Video", "12.0 Mbps", "20,000", "MPEG-2 Video"),
            ("0x102", "Audio", "0.2 Mbps", "4,000", "AC-3 Audio"),
            ("0x103", "Subtitles", "0.1 Mbps", "1,000", "DVB Subtitles"),
            ("0x200", "PMT", "0.1 Mbps", "2,000", "Program Map Table - BBC Two"),
            ("0x201", "Video", "12.0 Mbps", "20,000", "MPEG-2 Video"),
            ("0x202", "Audio", "0.2 Mbps", "4,000", "AC-3 Audio"),
            ("0x203", "Subtitles", "0.1 Mbps", "1,000", "DVB Subtitles"),
            ("0x300", "PMT", "0.1 Mbps", "2,000", "Program Map Table - BBC News"),
            ("0x301", "Video", "8.0 Mbps", "15,000", "MPEG-2 Video"),
            ("0x302", "Audio", "0.2 Mbps", "4,000", "AC-3 Audio"),
            ("0x400", "PMT", "0.1 Mbps", "1,000", "Program Map Table - Radio 1"),
            ("0x401", "Audio", "0.1 Mbps", "2,000", "MPEG-1 Audio"),
            ("0x500", "PMT", "0.1 Mbps", "1,000", "Program Map Table - Radio 2"),
            ("0x501", "Audio", "0.1 Mbps", "2,000", "MPEG-1 Audio"),
            ("0x11", "SDT", "0.1 Mbps", "500", "Service Description Table"),
            ("0x12", "EIT", "0.2 Mbps", "1,000", "Event Information Table"),
            ("0x14", "TDT", "0.1 Mbps", "100", "Time & Date Table"),
            ("0x1FFF", "Null", "0.0 Mbps", "0", "Null packets")
        ]
        
        self.pids_table.setRowCount(len(pids_data))
        for i, (pid, pid_type, bitrate, packets, description) in enumerate(pids_data):
            self.pids_table.setItem(i, 0, QTableWidgetItem(pid))
            self.pids_table.setItem(i, 1, QTableWidgetItem(pid_type))
            self.pids_table.setItem(i, 2, QTableWidgetItem(bitrate))
            self.pids_table.setItem(i, 3, QTableWidgetItem(packets))
            self.pids_table.setItem(i, 4, QTableWidgetItem(description))
            
        # Tables
        tables_data = [
            ("PAT", "0x000", "1", "28", "2024-01-01 12:00:00"),
            ("PMT - BBC One", "0x100", "5", "156", "2024-01-01 12:00:00"),
            ("PMT - BBC Two", "0x200", "3", "142", "2024-01-01 12:00:00"),
            ("PMT - BBC News", "0x300", "2", "98", "2024-01-01 12:00:00"),
            ("PMT - Radio 1", "0x400", "1", "45", "2024-01-01 12:00:00"),
            ("PMT - Radio 2", "0x500", "1", "43", "2024-01-01 12:00:00"),
            ("SDT", "0x11", "1", "234", "2024-01-01 12:00:00"),
            ("EIT Present/Following", "0x12", "1", "1,234", "2024-01-01 12:00:00"),
            ("EIT Schedule", "0x12", "1", "5,678", "2024-01-01 12:00:00"),
            ("TDT", "0x14", "1", "12", "2024-01-01 12:00:00")
        ]
        
        for table_name, pid, version, size, last_update in tables_data:
            item = QTreeWidgetItem([table_name, pid, version, size, last_update])
            self.tables_tree.addTopLevelItem(item)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings("TSDuckGUI", "TSDuckGUI")
        self.processor = None
        self.monitor = None
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("TSDuck GUI - MPEG Transport Stream Encoder/Decoder")
        self.setMinimumSize(1200, 800)
        
        # Performance optimizations
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        
        # Apply GUI optimizations if available
        if GUI_OPTIMIZATIONS_AVAILABLE:
            self.theme_manager = optimize_main_window(self)
            
            # Setup memory optimization timer
            self.memory_timer = QTimer()
            self.memory_timer.timeout.connect(self.optimize_memory)
            self.memory_timer.start(30000)  # Optimize every 30 seconds
        else:
            self.theme_manager = None
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left panel - Configuration
        left_panel = self.create_config_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel - Output, monitoring, and preview
        right_panel = self.create_output_panel()
        main_layout.addWidget(right_panel, 2)
        
        central_widget.setLayout(main_layout)
        
    def create_config_panel(self) -> QWidget:
        """Create the configuration panel"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Input configuration
        self.input_widget = InputOutputWidget("Input")
        self.input_widget.source_edit.textChanged.connect(self.update_preview_input)
        layout.addWidget(self.input_widget)
        
        # Output configuration
        self.output_widget = InputOutputWidget("Output")
        layout.addWidget(self.output_widget)
        
        # Plugins tab widget
        plugins_tab = QTabWidget()
        
        # Analysis plugins
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout()
        self.analysis_plugins = self.create_plugin_widgets([
            'analyze', 'bitrate_monitor', 'continuity', 'count', 'dump', 'stats'
        ])
        for plugin in self.analysis_plugins:
            analysis_layout.addWidget(plugin)
        analysis_tab.setLayout(analysis_layout)
        plugins_tab.addTab(analysis_tab, "Analysis")
        
        # Processing plugins
        processing_tab = QWidget()
        processing_layout = QVBoxLayout()
        self.processing_plugins = self.create_plugin_widgets([
            'filter', 'inject', 'limit', 'merge', 'mux', 'remap', 'regulate'
        ])
        for plugin in self.processing_plugins:
            processing_layout.addWidget(plugin)
        processing_tab.setLayout(processing_layout)
        plugins_tab.addTab(processing_tab, "Processing")
        
        # SCTE-35 plugins
        scte35_tab = QWidget()
        scte35_layout = QVBoxLayout()
        self.scte35_plugins = self.create_plugin_widgets([
            'spliceinject', 'splicemonitor', 'rmsplice'
        ])
        for plugin in self.scte35_plugins:
            scte35_layout.addWidget(plugin)
        
        # SCTE-35 configuration button
        scte35_config_btn = QPushButton("Configure SCTE-35 Splice")
        scte35_config_btn.clicked.connect(self.configure_scte35)
        scte35_layout.addWidget(scte35_config_btn)
        
        scte35_tab.setLayout(scte35_layout)
        plugins_tab.addTab(scte35_tab, "SCTE-35")
        
        # Tables plugins
        tables_tab = QWidget()
        tables_layout = QVBoxLayout()
        self.tables_plugins = self.create_plugin_widgets([
            'pat', 'pmt', 'sdt', 'eit', 'nit', 'bat', 'tstables'
        ])
        for plugin in self.tables_plugins:
            tables_layout.addWidget(plugin)
        tables_tab.setLayout(tables_layout)
        plugins_tab.addTab(tables_tab, "Tables")
        
        # Services plugins
        services_tab = QWidget()
        services_layout = QVBoxLayout()
        self.services_plugins = self.create_plugin_widgets([
            'svremove', 'svrename', 'svresync'
        ])
        for plugin in self.services_plugins:
            services_layout.addWidget(plugin)
        services_tab.setLayout(services_layout)
        plugins_tab.addTab(services_tab, "Services")
        
        layout.addWidget(plugins_tab)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Processing")
        self.start_btn.clicked.connect(self.start_processing)
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Processing")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; }")
        control_layout.addWidget(self.stop_btn)
        
        layout.addLayout(control_layout)
        
        panel.setLayout(layout)
        return panel
        
    def create_output_panel(self) -> QWidget:
        """Create the output, monitoring, and preview panel"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Output tabs
        output_tabs = QTabWidget()
        
        # Console output
        console_tab = QWidget()
        console_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        if GUI_OPTIMIZATIONS_AVAILABLE:
            PerformanceOptimizer.optimize_text_widget(self.output_text)
        else:
            self.output_text.setFont(QFont("Monaco", 9))  # Use Monaco instead of Courier on macOS
        console_layout.addWidget(self.output_text)
        
        # Clear button
        clear_btn = QPushButton("Clear Output")
        clear_btn.clicked.connect(self.output_text.clear)
        console_layout.addWidget(clear_btn)
        
        console_tab.setLayout(console_layout)
        output_tabs.addTab(console_tab, "Console Output")
        
        # Statistics
        stats_tab = QWidget()
        stats_layout = QVBoxLayout()
        
        # Statistics table
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["Parameter", "Value"])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Performance optimizations for tables
        if GUI_OPTIMIZATIONS_AVAILABLE:
            PerformanceOptimizer.optimize_table(self.stats_table)
        else:
            self.stats_table.setAlternatingRowColors(True)
            self.stats_table.setSortingEnabled(False)  # Disable sorting for better performance
            self.stats_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Initialize statistics
        stats_data = [
            ("Bitrate", "0 bps"),
            ("Packets/sec", "0"),
            ("Errors", "0"),
            ("PCR Accuracy", "0%"),
            ("Continuity Errors", "0")
        ]
        
        self.stats_table.setRowCount(len(stats_data))
        for i, (param, value) in enumerate(stats_data):
            self.stats_table.setItem(i, 0, QTableWidgetItem(param))
            self.stats_table.setItem(i, 1, QTableWidgetItem(value))
        
        stats_layout.addWidget(self.stats_table)
        stats_tab.setLayout(stats_layout)
        output_tabs.addTab(stats_tab, "Statistics")
        
        # Progress
        progress_tab = QWidget()
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(QLabel("Processing Progress:"))
        progress_layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("Ready")
        progress_layout.addWidget(self.status_label)
        
        progress_tab.setLayout(progress_layout)
        output_tabs.addTab(progress_tab, "Progress")
        
        # Source preview tab
        self.source_preview = SourcePreviewWidget()
        output_tabs.addTab(self.source_preview, "Source Preview")
        
        layout.addWidget(output_tabs)
        
        panel.setLayout(layout)
        return panel
        
    def create_plugin_widgets(self, plugin_names: List[str]) -> List[PluginWidget]:
        """Create plugin widgets"""
        widgets = []
        for name in plugin_names:
            widget = PluginWidget(name)
            widgets.append(widget)
        return widgets
        
    def setup_menu(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Configuration", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_configuration)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Configuration", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_configuration)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Configuration", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_configuration)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        scte35_action = QAction("SCTE-35 Configuration", self)
        scte35_action.triggered.connect(self.configure_scte35)
        tools_menu.addAction(scte35_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        if GUI_OPTIMIZATIONS_AVAILABLE and self.theme_manager:
            theme_action = QAction("Toggle Theme", self)
            theme_action.setShortcut(QKeySequence("Ctrl+T"))
            theme_action.triggered.connect(self.toggle_theme)
            view_menu.addAction(theme_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
    def load_settings(self):
        """Load application settings"""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
            
    def save_settings(self):
        """Save application settings"""
        self.settings.setValue("geometry", self.saveGeometry())
        
    def new_configuration(self):
        """Create new configuration"""
        reply = QMessageBox.question(
            self, "New Configuration", 
            "Are you sure you want to create a new configuration? Unsaved changes will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.reset_configuration()
            
    def open_configuration(self):
        """Open configuration from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Configuration", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config = json.load(f)
                self.load_configuration(config)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open configuration: {str(e)}")
                
    def save_configuration(self):
        """Save configuration to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                config = self.get_configuration()
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=2)
                QMessageBox.information(self, "Success", "Configuration saved successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")
                
    def reset_configuration(self):
        """Reset configuration to defaults"""
        # Reset input/output
        self.input_widget.source_edit.clear()
        self.output_widget.source_edit.clear()
        
        # Reset all plugins
        all_plugins = (self.analysis_plugins + self.processing_plugins + 
                      self.scte35_plugins + self.tables_plugins + self.services_plugins)
        for plugin in all_plugins:
            plugin.enabled.setChecked(False)
            plugin.params_edit.clear()
            
    def get_configuration(self) -> Dict[str, Any]:
        """Get current configuration"""
        config = {
            'input': self.input_widget.get_config(),
            'output': self.output_widget.get_config(),
            'plugins': {}
        }
        
        # Get plugin configurations
        all_plugins = (self.analysis_plugins + self.processing_plugins + 
                      self.scte35_plugins + self.tables_plugins + self.services_plugins)
        for plugin in all_plugins:
            config['plugins'][plugin.plugin_name] = plugin.get_config()
            
        return config
        
    def load_configuration(self, config: Dict[str, Any]):
        """Load configuration"""
        # Load input/output
        if 'input' in config:
            input_config = config['input']
            self.input_widget.type_combo.setCurrentText(input_config.get('type', 'File'))
            self.input_widget.source_edit.setText(input_config.get('source', ''))
            self.input_widget.params_edit.setText(input_config.get('params', ''))
            
        if 'output' in config:
            output_config = config['output']
            self.output_widget.type_combo.setCurrentText(output_config.get('type', 'File'))
            self.output_widget.source_edit.setText(output_config.get('source', ''))
            self.output_widget.params_edit.setText(output_config.get('params', ''))
            
        # Load plugins
        if 'plugins' in config:
            all_plugins = (self.analysis_plugins + self.processing_plugins + 
                          self.scte35_plugins + self.tables_plugins + self.services_plugins)
            for plugin in all_plugins:
                if plugin.plugin_name in config['plugins']:
                    plugin_config = config['plugins'][plugin.plugin_name]
                    plugin.enabled.setChecked(plugin_config.get('enabled', False))
                    plugin.params_edit.setText(plugin_config.get('params', ''))
                    
    def configure_scte35(self):
        """Configure SCTE-35 splice information"""
        dialog = SCTE35Dialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            config = dialog.get_config()
            # Apply SCTE-35 configuration to spliceinject plugin
            for plugin in self.scte35_plugins:
                if plugin.plugin_name == 'spliceinject':
                    plugin.enabled.setChecked(True)
                    # Build parameters from config
                    params = []
                    if config['immediate']:
                        params.append('--immediate')
                    if config['out_of_network']:
                        params.append('--out-of-network')
                    params.extend([
                        f"--event-id {config['event_id']}",
                        f"--unique-program-id {config['unique_program_id']}",
                        f"--avail-num {config['avail_num']}",
                        f"--avails-expected {config['avails_expected']}"
                    ])
                    if config['splice_time']:
                        params.append(f"--splice-time {config['splice_time']}")
                    if config['duration']:
                        params.append(f"--duration {config['duration']}")
                    plugin.params_edit.setText(' '.join(params))
                    break
                    
    def start_processing(self):
        """Start TSDuck processing"""
        try:
            if not TSDUCK_AVAILABLE:
                QMessageBox.warning(
                    self, "TSDuck Not Available", 
                    "TSDuck Python bindings are not available. Please install TSDuck."
                )
                return
                
            # Build TSDuck command
            command = self.build_tsduck_command()
            if not command:
                return
                
            # Validate command
            if len(command) < 3:  # Minimum: tsp -I input -O output
                QMessageBox.warning(
                    self, "Invalid Configuration",
                    "Please configure both input and output sources."
                )
                return
        except Exception as e:
            QMessageBox.critical(
                self, "Configuration Error",
                f"Error building TSDuck command: {str(e)}"
            )
            return
            
        # Start processor
        self.processor = TSDuckProcessor(command)
        self.processor.output_received.connect(self.output_text.append)
        self.processor.error_received.connect(self.output_text.append)
        self.processor.finished.connect(self.processing_finished)
        
        # Start monitor
        self.monitor = StreamMonitor()
        self.monitor.stats_updated.connect(self.update_statistics)
        
        # Update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Processing...")
        self.status_bar.showMessage("Processing started")
        
        # Start threads
        self.processor.start()
        self.monitor.start()
        
    def stop_processing(self):
        """Stop TSDuck processing"""
        if self.processor:
            self.processor.stop()
        if self.monitor:
            self.monitor.stop()
            
    def processing_finished(self, exit_code: int):
        """Handle processing finished"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if exit_code == 0:
            self.status_label.setText("Processing completed successfully")
            self.status_bar.showMessage("Processing completed")
        else:
            self.status_label.setText(f"Processing failed with exit code {exit_code}")
            self.status_bar.showMessage("Processing failed")
            
    def validate_configuration(self) -> bool:
        """Validate current configuration"""
        # Check input configuration
        input_config = self.input_widget.get_config()
        if not input_config['source']:
            QMessageBox.warning(self, "Configuration Error", "Please specify an input source")
            return False
            
        # Check output configuration
        output_config = self.output_widget.get_config()
        if not output_config['source']:
            QMessageBox.warning(self, "Configuration Error", "Please specify an output destination")
            return False
            
        # Check if input file exists (for file inputs)
        if input_config['type'].lower() == 'file':
            if not os.path.exists(input_config['source']):
                QMessageBox.warning(self, "File Not Found", f"Input file not found: {input_config['source']}")
                return False
                
        return True
        
    def build_tsduck_command(self) -> List[str]:
        """Build TSDuck command from configuration"""
        # Validate configuration first
        if not self.validate_configuration():
            return []
            
        command = ['tsp']
        
        # Input
        input_config = self.input_widget.get_config()
        if not input_config['source']:
            QMessageBox.warning(self, "Error", "Please specify an input source")
            return []
            
        input_type = input_config['type'].lower()
        if input_type == 'file':
            command.extend(['-I', 'file', input_config['source']])
        elif input_type == 'udp':
            command.extend(['-I', 'udp', input_config['source']])
        elif input_type == 'tcp':
            command.extend(['-I', 'tcp', input_config['source']])
        elif input_type == 'http':
            command.extend(['-I', 'http', input_config['source']])
        elif input_type == 'hls':
            command.extend(['-I', 'hls', input_config['source']])
        elif input_type == 'srt':
            command.extend(['-I', 'srt', input_config['source']])
        elif input_type == 'rist':
            command.extend(['-I', 'rist', input_config['source']])
        elif input_type == 'dvb-t':
            command.extend(['-I', 'dvb', '--tuner', input_config['source']])
        elif input_type == 'dvb-s':
            command.extend(['-I', 'dvb', '--satellite', input_config['source']])
        elif input_type == 'dvb-c':
            command.extend(['-I', 'dvb', '--cable', input_config['source']])
        elif input_type == 'atsc':
            command.extend(['-I', 'atsc', input_config['source']])
        elif input_type == 'isdb':
            command.extend(['-I', 'isdb', input_config['source']])
        elif input_type == 'asi':
            command.extend(['-I', 'asi', input_config['source']])
        elif input_type == 'dektec':
            command.extend(['-I', 'dektec', input_config['source']])
        elif input_type == 'hides':
            command.extend(['-I', 'hides', input_config['source']])
        elif input_type == 'vatek':
            command.extend(['-I', 'vatek', input_config['source']])
            
        # Add input parameters
        if input_config['params']:
            command.extend(input_config['params'].split())
            
        # Plugins
        all_plugins = (self.analysis_plugins + self.processing_plugins + 
                      self.scte35_plugins + self.tables_plugins + self.services_plugins)
        for plugin in all_plugins:
            config = plugin.get_config()
            if config['enabled']:
                if plugin.plugin_name == 'spliceinject':
                    # Special handling for spliceinject - it uses files, not parameters
                    command.extend(['-P', plugin.plugin_name])
                    # Add PID and PTS-PID if specified
                    if config['params']:
                        # Parse parameters like "--pid 500 --pts-pid 256"
                        param_list = config['params'].split()
                        i = 0
                        while i < len(param_list):
                            param = param_list[i]
                            if param.startswith('--'):
                                command.append(param)
                                # Add value if next item exists and doesn't start with --
                                if i + 1 < len(param_list) and not param_list[i + 1].startswith('--'):
                                    command.append(param_list[i + 1])
                                    i += 1
                            i += 1
                else:
                    # Regular plugin handling
                    command.extend(['-P', plugin.plugin_name])
                    if config['params']:
                        command.extend(config['params'].split())
                    
        # Output
        output_config = self.output_widget.get_config()
        if not output_config['source']:
            QMessageBox.warning(self, "Error", "Please specify an output destination")
            return []
            
        output_type = output_config['type'].lower()
        if output_type == 'file':
            command.extend(['-O', 'file', output_config['source']])
        elif output_type == 'udp':
            # Parse UDP URL: udp://host:port
            udp_url = output_config['source']
            if udp_url.startswith('udp://'):
                host_port = udp_url[6:]  # Remove 'udp://'
                command.extend(['-O', 'ip', host_port])
            else:
                command.extend(['-O', 'ip', udp_url])
        elif output_type == 'tcp':
            command.extend(['-O', 'tcp', output_config['source']])
        elif output_type == 'http':
            command.extend(['-O', 'http', output_config['source']])
        elif output_type == 'hls':
            command.extend(['-O', 'hls', output_config['source']])
        elif output_type == 'srt':
            # Parse SRT URL: srt://host:port?streamid=value
            srt_url = output_config['source']
            if srt_url.startswith('srt://'):
                # Extract host:port from URL
                url_part = srt_url[6:]  # Remove 'srt://'
                if '?' in url_part:
                    host_port = url_part.split('?')[0]
                    streamid_part = url_part.split('?')[1]
                    if 'streamid=' in streamid_part:
                        streamid = streamid_part.split('streamid=')[1]
                        command.extend(['-O', 'srt', '--caller', host_port, '--streamid', streamid])
                    else:
                        command.extend(['-O', 'srt', '--caller', host_port])
                else:
                    command.extend(['-O', 'srt', '--caller', url_part])
            else:
                command.extend(['-O', 'srt', output_config['source']])
        elif output_type == 'rist':
            command.extend(['-O', 'rist', output_config['source']])
        elif output_type == 'asi':
            command.extend(['-O', 'asi', output_config['source']])
        elif output_type == 'dektec':
            command.extend(['-O', 'dektec', output_config['source']])
        elif output_type == 'hides':
            command.extend(['-O', 'hides', output_config['source']])
        elif output_type == 'vatek':
            command.extend(['-O', 'vatek', output_config['source']])
            
        # Add output parameters
        if output_config['params']:
            command.extend(output_config['params'].split())
            
        return command
        
    def update_statistics(self, stats: Dict[str, Any]):
        """Update statistics display"""
        self.stats_table.setItem(0, 1, QTableWidgetItem(f"{stats['bitrate']:,} bps"))
        self.stats_table.setItem(1, 1, QTableWidgetItem(f"{stats['packets_per_second']:,}"))
        self.stats_table.setItem(2, 1, QTableWidgetItem(str(stats['errors'])))
        self.stats_table.setItem(3, 1, QTableWidgetItem(f"{stats['pcr_accuracy']:.1f}%"))
        self.stats_table.setItem(4, 1, QTableWidgetItem(str(stats['continuity_errors'])))
        
    def update_preview_input(self):
        """Update source preview input configuration"""
        if hasattr(self, 'source_preview'):
            input_config = self.input_widget.get_config()
            self.source_preview.set_input_config(input_config)
            
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        if GUI_OPTIMIZATIONS_AVAILABLE and self.theme_manager:
            new_theme = self.theme_manager.toggle_theme()
            self.status_bar.showMessage(f"Switched to {new_theme} theme")
            
    def optimize_memory(self):
        """Optimize memory usage"""
        if GUI_OPTIMIZATIONS_AVAILABLE:
            # Clear old content from text widgets
            if hasattr(self, 'output_text'):
                MemoryOptimizer.clear_text_widget(self.output_text, 1000)
            if hasattr(self, 'stream_info_text'):
                MemoryOptimizer.clear_text_widget(self.stream_info_text, 500)
            
            # Optimize table memory
            if hasattr(self, 'stats_table'):
                MemoryOptimizer.optimize_table_memory(self.stats_table, 1000)
            if hasattr(self, 'services_table'):
                MemoryOptimizer.optimize_table_memory(self.services_table, 5000)
            if hasattr(self, 'pids_table'):
                MemoryOptimizer.optimize_table_memory(self.pids_table, 5000)
            
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, "About TSDuck GUI",
            "TSDuck GUI v1.0\n\n"
            "A comprehensive GUI application for MPEG Transport Stream processing using TSDuck.\n\n"
            "Features:\n"
            "• Full TSDuck integration\n"
            "• SCTE-35 splice information support\n"
            "• Real-time monitoring\n"
            "• Source preview functionality\n"
            "• Plugin configuration\n"
            "• Multiple input/output formats\n\n"
            "Based on TSDuck - The MPEG Transport Stream Toolkit\n"
            "Copyright (c) 2005-2025, Thierry Lelegard"
        )
        
    def closeEvent(self, event):
        """Handle application close"""
        self.save_settings()
        if self.processor:
            self.processor.stop()
        if self.monitor:
            self.monitor.stop()
        event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("TSDuck GUI")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("TSDuckGUI")
    
    # Set application style
    try:
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
    except ImportError:
        pass  # Use default style if qdarkstyle is not available
        
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
