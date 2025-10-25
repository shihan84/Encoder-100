#!/usr/bin/env python3
"""
Professional SCTE-35 Widget for IBE-100
Clean, organized interface for SCTE-35 marker management
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, 
    QLineEdit, QPushButton, QComboBox, QSpinBox, QCheckBox, QTextEdit,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QMessageBox, QSplitter, QFrame, QScrollArea, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

class ProfessionalSCTE35Widget(QWidget):
    """Professional SCTE-35 marker management interface"""
    
    marker_generated = pyqtSignal(str, str)  # xml_file, json_file
    
    def __init__(self):
        super().__init__()
        self.scte35_dir = Path("scte35_final")
        self.scte35_dir.mkdir(exist_ok=True)
        self.current_event_id = 10023
        self.setup_ui()
        self.load_existing_markers()
        
    def setup_ui(self):
        """Setup the professional SCTE-35 interface"""
        layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Main content with tabs
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
                padding: 10px 20px;
                margin-right: 2px;
                border-radius: 6px 6px 0 0;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
            }
            QTabBar::tab:hover {
                background-color: #555;
            }
        """)
        
        # Quick Actions Tab
        self.quick_tab = self.create_quick_actions_tab()
        self.tab_widget.addTab(self.quick_tab, "Quick Actions")
        
        # Advanced Configuration Tab
        self.advanced_tab = self.create_advanced_tab()
        self.tab_widget.addTab(self.advanced_tab, "Advanced Config")
        
        # Marker Library Tab
        self.library_tab = self.create_marker_library_tab()
        self.tab_widget.addTab(self.library_tab, "Marker Library")
        
        # Templates Tab
        self.templates_tab = self.create_templates_tab()
        self.tab_widget.addTab(self.templates_tab, "Templates")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
    def create_header(self):
        """Create the header section"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Title
        title = QLabel("SCTE-35 Professional Marker System")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #4CAF50;
                padding: 10px;
            }
        """)
        
        # Status indicator
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #4CAF50;
                background-color: #2a2a2a;
                padding: 8px 15px;
                border-radius: 15px;
                border: 1px solid #4CAF50;
            }
        """)
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status_label)
        
        header_frame.setLayout(layout)
        return header_frame
        
    def create_quick_actions_tab(self):
        """Create the quick actions tab"""
        widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Create scroll area for better visibility
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #2a2a2a;
            }
            QScrollBar:vertical {
                background-color: #3a3a3a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4CAF50;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #45a049;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create scrollable content widget
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        
        # Quick Pre-roll Section
        preroll_group = QGroupBox("Quick Pre-roll Generation")
        preroll_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #4CAF50;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        preroll_layout = QGridLayout()
        
        # Pre-roll time
        preroll_layout.addWidget(QLabel("Pre-roll Time:"), 0, 0)
        self.preroll_time = QSpinBox()
        self.preroll_time.setRange(0, 30)
        self.preroll_time.setValue(2)
        self.preroll_time.setSuffix(" seconds")
        preroll_layout.addWidget(self.preroll_time, 0, 1)
        
        # Ad duration
        preroll_layout.addWidget(QLabel("Ad Duration:"), 1, 0)
        self.ad_duration = QSpinBox()
        self.ad_duration.setRange(30, 1800)
        self.ad_duration.setValue(600)
        self.ad_duration.setSuffix(" seconds")
        preroll_layout.addWidget(self.ad_duration, 1, 1)
        
        # Event ID
        preroll_layout.addWidget(QLabel("Event ID:"), 2, 0)
        self.event_id = QSpinBox()
        self.event_id.setRange(10000, 99999)
        self.event_id.setValue(10023)
        preroll_layout.addWidget(self.event_id, 2, 1)
        
        # Generate button
        self.generate_btn = QPushButton("Generate Pre-roll Marker")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_quick_preroll)
        preroll_layout.addWidget(self.generate_btn, 3, 0, 1, 2)
        
        preroll_group.setLayout(preroll_layout)
        layout.addWidget(preroll_group)
        
        # Quick Templates Section
        templates_group = QGroupBox("Quick Templates")
        templates_group.setStyleSheet(preroll_group.styleSheet())
        
        templates_layout = QGridLayout()
        
        # Template buttons with better spacing and visibility
        templates = [
            ("Standard Pre-roll", "2s pre-roll, 10min ad", 2, 600),
            ("Extended Pre-roll", "5s pre-roll, 5min ad", 5, 300),
            ("Long Pre-roll", "10s pre-roll, 2min ad", 10, 120),
            ("Immediate", "No pre-roll, 10min ad", 0, 600)
        ]
        
        for i, (name, desc, preroll, duration) in enumerate(templates):
            btn = QPushButton(f"{name}\n\n{desc}")
            btn.setMinimumHeight(80)  # Increased height for better visibility
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a2a2a;
                    color: white;
                    font-weight: bold;
                    font-size: 13px;
                    padding: 20px;
                    border-radius: 8px;
                    border: 2px solid #444;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                    border-color: #4CAF50;
                    border-width: 2px;
                }
                QPushButton:pressed {
                    background-color: #4CAF50;
                    color: white;
                }
            """)
            btn.clicked.connect(lambda checked, p=preroll, d=duration: self.apply_template(p, d))
            templates_layout.addWidget(btn, i // 2, i % 2)
        
        templates_group.setLayout(templates_layout)
        layout.addWidget(templates_group)
        
        # Status and output
        status_group = QGroupBox("Generation Status")
        status_group.setStyleSheet(preroll_group.styleSheet())
        
        status_layout = QVBoxLayout()
        
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(150)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #4CAF50;
                border: 1px solid #444;
                border-radius: 4px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)
        self.status_text.setReadOnly(True)
        status_layout.addWidget(self.status_text)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Set up scroll area
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        widget.setLayout(main_layout)
        return widget
        
    def create_advanced_tab(self):
        """Create the advanced configuration tab"""
        widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Create scroll area for better visibility
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #2a2a2a;
            }
            QScrollBar:vertical {
                background-color: #3a3a3a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4CAF50;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #45a049;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create scrollable content widget
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        
        # Advanced SCTE-35 Configuration
        config_group = QGroupBox("Advanced SCTE-35 Configuration")
        config_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #4CAF50;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        config_layout = QGridLayout()
        
        # Advanced parameters
        config_layout.addWidget(QLabel("Unique Program ID:"), 0, 0)
        self.unique_program_id = QSpinBox()
        self.unique_program_id.setRange(1, 65535)
        self.unique_program_id.setValue(1)
        config_layout.addWidget(self.unique_program_id, 0, 1)
        
        config_layout.addWidget(QLabel("Avail Number:"), 1, 0)
        self.avail_num = QSpinBox()
        self.avail_num.setRange(1, 255)
        self.avail_num.setValue(1)
        config_layout.addWidget(self.avail_num, 1, 1)
        
        config_layout.addWidget(QLabel("Avails Expected:"), 2, 0)
        self.avails_expected = QSpinBox()
        self.avails_expected.setRange(1, 255)
        self.avails_expected.setValue(1)
        config_layout.addWidget(self.avails_expected, 2, 1)
        
        config_layout.addWidget(QLabel("Out of Network:"), 3, 0)
        self.out_of_network = QCheckBox("Enable")
        self.out_of_network.setChecked(True)
        config_layout.addWidget(self.out_of_network, 3, 1)
        
        config_layout.addWidget(QLabel("Auto Return:"), 4, 0)
        self.auto_return = QCheckBox("Enable")
        self.auto_return.setChecked(False)
        config_layout.addWidget(self.auto_return, 4, 1)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Batch Generation
        batch_group = QGroupBox("Batch Generation")
        batch_group.setStyleSheet(config_group.styleSheet())
        
        batch_layout = QVBoxLayout()
        
        self.batch_btn = QPushButton("Generate Multiple Markers")
        self.batch_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        self.batch_btn.clicked.connect(self.generate_batch_markers)
        batch_layout.addWidget(self.batch_btn)
        
        batch_group.setLayout(batch_layout)
        layout.addWidget(batch_group)
        
        # Set up scroll area
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        widget.setLayout(main_layout)
        return widget
        
    def create_marker_library_tab(self):
        """Create the marker library tab"""
        widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Create scroll area for better visibility
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #2a2a2a;
            }
            QScrollBar:vertical {
                background-color: #3a3a3a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4CAF50;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #45a049;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create scrollable content widget
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        
        # Marker Library Table
        library_group = QGroupBox("Marker Library")
        library_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #4CAF50;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        library_layout = QVBoxLayout()
        
        # Table for existing markers
        self.marker_table = QTableWidget()
        self.marker_table.setColumnCount(6)
        self.marker_table.setHorizontalHeaderLabels([
            "Event ID", "Type", "Pre-roll", "Duration", "Created", "Actions"
        ])
        
        # Style the table
        self.marker_table.setStyleSheet("""
            QTableWidget {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #3a3a3a;
                color: white;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #444;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
            }
        """)
        
        # Set column widths
        header = self.marker_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        library_layout.addWidget(self.marker_table)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh Library")
        self.refresh_btn.clicked.connect(self.load_existing_markers)
        action_layout.addWidget(self.refresh_btn)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_selected_marker)
        action_layout.addWidget(self.delete_btn)
        
        action_layout.addStretch()
        library_layout.addLayout(action_layout)
        
        library_group.setLayout(library_layout)
        layout.addWidget(library_group)
        
        # Set up scroll area
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        widget.setLayout(main_layout)
        return widget
        
    def create_templates_tab(self):
        """Create the templates tab"""
        widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Create scroll area for better visibility
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #2a2a2a;
            }
            QScrollBar:vertical {
                background-color: #3a3a3a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4CAF50;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #45a049;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create scrollable content widget
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        
        # Professional Templates
        templates_group = QGroupBox("Professional Broadcast Templates")
        templates_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #4CAF50;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        templates_layout = QGridLayout()
        
        # Professional templates
        professional_templates = [
            ("News Break", "2s pre-roll, 3min ad", 2, 180, 10030),
            ("Commercial Break", "5s pre-roll, 2min ad", 5, 120, 10031),
            ("Emergency Alert", "0s pre-roll, 1min ad", 0, 60, 10032),
            ("Sports Timeout", "10s pre-roll, 4min ad", 10, 240, 10033),
            ("Weather Alert", "0s pre-roll, 30s ad", 0, 30, 10034),
            ("Promo Break", "3s pre-roll, 1.5min ad", 3, 90, 10035)
        ]
        
        for i, (name, desc, preroll, duration, event_id) in enumerate(professional_templates):
            template_btn = QPushButton(f"{name}\n\n{desc}")
            template_btn.setMinimumHeight(90)  # Increased height for better visibility
            template_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a2a2a;
                    color: white;
                    font-weight: bold;
                    font-size: 13px;
                    padding: 20px;
                    border-radius: 8px;
                    border: 2px solid #444;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                    border-color: #4CAF50;
                    border-width: 2px;
                }
                QPushButton:pressed {
                    background-color: #4CAF50;
                    color: white;
                }
            """)
            template_btn.clicked.connect(lambda checked, p=preroll, d=duration, e=event_id: self.apply_professional_template(p, d, e))
            templates_layout.addWidget(template_btn, i // 2, i % 2)
        
        templates_group.setLayout(templates_layout)
        layout.addWidget(templates_group)
        
        # Set up scroll area
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        widget.setLayout(main_layout)
        return widget
        
    def generate_quick_preroll(self):
        """Generate a quick pre-roll marker"""
        try:
            preroll_seconds = self.preroll_time.value()
            ad_duration = self.ad_duration.value()
            event_id = self.event_id.value()
            
            xml_file, json_file = self.generate_preroll_marker(
                event_id=event_id,
                preroll_seconds=preroll_seconds,
                ad_duration=ad_duration
            )
            
            self.status_text.append(f"[SUCCESS] Generated pre-roll marker:")
            self.status_text.append(f"  Event ID: {event_id}")
            self.status_text.append(f"  Pre-roll: {preroll_seconds}s")
            self.status_text.append(f"  Duration: {ad_duration}s")
            self.status_text.append(f"  Files: {xml_file}")
            self.status_text.append("")
            
            self.status_label.setText("Marker Generated")
            self.load_existing_markers()
            self.marker_generated.emit(xml_file, json_file)
            
        except Exception as e:
            self.status_text.append(f"[ERROR] Failed to generate marker: {e}")
            self.status_label.setText("Error")
            
    def apply_template(self, preroll, duration):
        """Apply a quick template"""
        self.preroll_time.setValue(preroll)
        self.ad_duration.setValue(duration)
        self.event_id.setValue(self.current_event_id)
        self.current_event_id += 1
        
    def apply_professional_template(self, preroll, duration, event_id):
        """Apply a professional template"""
        self.preroll_time.setValue(preroll)
        self.ad_duration.setValue(duration)
        self.event_id.setValue(event_id)
        
        # Auto-generate the marker
        self.generate_quick_preroll()
        
    def generate_batch_markers(self):
        """Generate multiple markers with different configurations"""
        try:
            configurations = [
                {"preroll": 2, "duration": 600, "event_id": 10040},
                {"preroll": 5, "duration": 300, "event_id": 10041},
                {"preroll": 10, "duration": 120, "event_id": 10042},
                {"preroll": 0, "duration": 600, "event_id": 10043}
            ]
            
            self.status_text.append("[INFO] Generating batch markers...")
            
            for config in configurations:
                xml_file, json_file = self.generate_preroll_marker(
                    event_id=config["event_id"],
                    preroll_seconds=config["preroll"],
                    ad_duration=config["duration"]
                )
                self.status_text.append(f"  Generated: Event {config['event_id']} ({config['preroll']}s pre-roll, {config['duration']}s ad)")
            
            self.status_text.append("[SUCCESS] Batch generation completed!")
            self.load_existing_markers()
            
        except Exception as e:
            self.status_text.append(f"[ERROR] Batch generation failed: {e}")
            
    def generate_preroll_marker(self, event_id, preroll_seconds, ad_duration):
        """Generate a pre-roll SCTE-35 marker"""
        # Calculate PTS time (90kHz clock)
        current_time = int(time.time() * 90000)
        preroll_pts = preroll_seconds * 90000
        pts_time = current_time + preroll_pts
        
        # Calculate ad duration in PTS
        ad_duration_pts = ad_duration * 90000
        
        # Generate XML content (TSDuck format)
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <splice_information_table protocol_version="0" pts_adjustment="0" tier="0xFFF">
        <splice_insert splice_event_id="{event_id}" splice_event_cancel="false" out_of_network="true" splice_immediate="false" pts_time="{pts_time}" unique_program_id="{self.unique_program_id.value()}" avail_num="{self.avail_num.value()}" avails_expected="{self.avails_expected.value()}">
            <break_duration auto_return="{'true' if self.auto_return.isChecked() else 'false'}" duration="{ad_duration_pts}" />
        </splice_insert>
    </splice_information_table>
</tsduck>"""
        
        # Generate JSON content (for reference)
        json_content = {
            "scte35_marker": {
                "type": "Pre-roll",
                "event_id": event_id,
                "preroll_seconds": preroll_seconds,
                "ad_duration_seconds": ad_duration,
                "pts_time": pts_time,
                "ad_duration_pts": ad_duration_pts,
                "timestamp": datetime.now().isoformat(),
                "description": f"Pre-roll marker with {preroll_seconds}s lead time and {ad_duration}s ad duration"
            }
        }
        
        # Create filenames
        timestamp = int(time.time())
        xml_filename = self.scte35_dir / f"preroll_{event_id}_{timestamp}.xml"
        json_filename = self.scte35_dir / f"preroll_{event_id}_{timestamp}.json"
        
        # Write files
        with open(xml_filename, 'w') as f:
            f.write(xml_content)
        
        with open(json_filename, 'w') as f:
            json.dump(json_content, f, indent=2)
        
        return str(xml_filename), str(json_filename)
        
    def load_existing_markers(self):
        """Load existing markers into the library table"""
        self.marker_table.setRowCount(0)
        
        # Find all marker files
        marker_files = list(self.scte35_dir.glob("preroll_*.xml"))
        
        for marker_file in marker_files:
            try:
                # Parse filename to get event ID and timestamp
                parts = marker_file.stem.split('_')
                if len(parts) >= 3:
                    event_id = parts[1]
                    timestamp = parts[2]
                    
                    # Read JSON file for details
                    json_file = marker_file.with_suffix('.json')
                    if json_file.exists():
                        with open(json_file, 'r') as f:
                            data = json.load(f)
                            marker_info = data['scte35_marker']
                            
                            # Add to table
                            row = self.marker_table.rowCount()
                            self.marker_table.insertRow(row)
                            
                            self.marker_table.setItem(row, 0, QTableWidgetItem(str(marker_info['event_id'])))
                            self.marker_table.setItem(row, 1, QTableWidgetItem("Pre-roll"))
                            self.marker_table.setItem(row, 2, QTableWidgetItem(f"{marker_info['preroll_seconds']}s"))
                            self.marker_table.setItem(row, 3, QTableWidgetItem(f"{marker_info['ad_duration_seconds']}s"))
                            self.marker_table.setItem(row, 4, QTableWidgetItem(marker_info['timestamp'][:19]))
                            
                            # Action button
                            action_btn = QPushButton("Use")
                            action_btn.setStyleSheet("""
                                QPushButton {
                                    background-color: #4CAF50;
                                    color: white;
                                    font-weight: bold;
                                    padding: 4px 8px;
                                    border-radius: 3px;
                                    border: none;
                                }
                                QPushButton:hover {
                                    background-color: #45a049;
                                }
                            """)
                            action_btn.clicked.connect(lambda checked, f=str(marker_file): self.use_marker(f))
                            self.marker_table.setCellWidget(row, 5, action_btn)
                            
            except Exception as e:
                print(f"Error loading marker {marker_file}: {e}")
                
    def use_marker(self, marker_file):
        """Use an existing marker"""
        try:
            # Read the marker file and extract parameters
            with open(marker_file, 'r') as f:
                content = f.read()
                
            # Extract event ID from XML
            import re
            event_id_match = re.search(r'splice_event_id="(\d+)"', content)
            if event_id_match:
                event_id = int(event_id_match.group(1))
                self.event_id.setValue(event_id)
                
            self.status_text.append(f"[INFO] Using marker: {marker_file}")
            self.status_label.setText("Marker Selected")
            
        except Exception as e:
            self.status_text.append(f"[ERROR] Failed to use marker: {e}")
            
    def delete_selected_marker(self):
        """Delete the selected marker"""
        current_row = self.marker_table.currentRow()
        if current_row >= 0:
            event_id = self.marker_table.item(current_row, 0).text()
            
            # Find and delete files
            marker_files = list(self.scte35_dir.glob(f"preroll_{event_id}_*.xml"))
            for marker_file in marker_files:
                try:
                    marker_file.unlink()
                    json_file = marker_file.with_suffix('.json')
                    if json_file.exists():
                        json_file.unlink()
                except Exception as e:
                    self.status_text.append(f"[ERROR] Failed to delete {marker_file}: {e}")
                    
            self.status_text.append(f"[SUCCESS] Deleted marker {event_id}")
            self.load_existing_markers()
        else:
            self.status_text.append("[WARNING] No marker selected")
