#!/usr/bin/env python3
"""
SCTE-35 Marker Generation Widget for IBE-100
GUI widget for creating and managing SCTE-35 markers
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, 
    QLabel, QLineEdit, QPushButton, QSpinBox, QComboBox, QCheckBox,
    QTextEdit, QTableWidget, QTableWidgetItem, QTabWidget, QSplitter,
    QFileDialog, QMessageBox, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont, QIcon

try:
    from scte35_xml_generator import SCTE35XMLGenerator
    XML_GENERATOR_AVAILABLE = True
except ImportError:
    XML_GENERATOR_AVAILABLE = False
    SCTE35XMLGenerator = None


class MarkerGenerationThread(QThread):
    """Thread for generating SCTE-35 markers"""
    marker_generated = pyqtSignal(dict)
    generation_finished = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, marker_type: str, params: Dict[str, Any]):
        super().__init__()
        self.marker_type = marker_type
        self.params = params
        self.generator = None
    
    def run(self):
        """Generate the marker"""
        try:
            if not XML_GENERATOR_AVAILABLE:
                self.error_occurred.emit("SCTE-35 XML generator not available")
                return
            
            self.generator = SCTE35XMLGenerator()
            
            if self.marker_type == "CUE_OUT":
                xml_file, json_file = self.generator.generate_cue_out(
                    self.params['event_id'],
                    self.params['duration'],
                    self.params.get('pts_offset', 0),
                    self.params.get('out_of_network', True),
                    self.params.get('immediate', False)
                )
            elif self.marker_type == "CUE_IN":
                xml_file, json_file = self.generator.generate_cue_in(
                    self.params['event_id'],
                    self.params.get('pts_offset', 0),
                    self.params.get('immediate', False)
                )
            elif self.marker_type == "CRASH_OUT":
                xml_file, json_file = self.generator.generate_crash_out(
                    self.params['event_id'],
                    self.params.get('pts_offset', 0)
                )
            elif self.marker_type == "TIME_SIGNAL":
                xml_file, json_file = self.generator.generate_time_signal(
                    self.params['event_id'],
                    self.params.get('pts_offset', 0)
                )
            elif self.marker_type == "AD_BREAK_SEQUENCE":
                sequence = self.generator.generate_ad_break_sequence(
                    self.params['base_event_id'],
                    self.params['ad_duration'],
                    self.params.get('preroll_seconds', 2)
                )
                self.generation_finished.emit(sequence)
                return
            else:
                self.error_occurred.emit(f"Unknown marker type: {self.marker_type}")
                return
            
            marker_info = {
                'type': self.marker_type,
                'event_id': self.params['event_id'],
                'xml_file': xml_file,
                'json_file': json_file,
                'timestamp': self.params.get('timestamp', '')
            }
            
            self.marker_generated.emit(marker_info)
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to generate marker: {str(e)}")


class SCTE35GenerationWidget(QWidget):
    """SCTE-35 Marker Generation Widget"""
    
    def __init__(self):
        super().__init__()
        self.generator = None
        self.generated_markers = []
        self.setup_ui()
        
        # Initialize generator if XML generator is available
        if XML_GENERATOR_AVAILABLE:
            try:
                self.generator = SCTE35XMLGenerator()
            except Exception as e:
                print(f"⚠️ Failed to initialize SCTE-35 generator: {e}")
    
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("🎬 SCTE-35 Marker Generation")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Status indicator
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Ready to generate markers")
        if XML_GENERATOR_AVAILABLE:
            self.status_label.setText("✅ SCTE-35 XML generator available - Ready to generate markers")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        else:
            self.status_label.setText("❌ SCTE-35 XML generator not available")
            self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        main_layout.addLayout(status_layout)
        
        # Create tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Individual Markers Tab
        self.setup_individual_markers_tab()
        
        # Ad Break Sequence Tab
        self.setup_ad_break_tab()
        
        # Generated Markers Tab
        self.setup_generated_markers_tab()
        
        # Actions
        actions_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("🗑️ Clear All Markers")
        self.clear_button.clicked.connect(self.clear_all_markers)
        self.clear_button.setStyleSheet("font-size: 14px; padding: 10px;")
        actions_layout.addWidget(self.clear_button)
        
        self.refresh_button = QPushButton("🔄 Refresh List")
        self.refresh_button.clicked.connect(self.refresh_markers_list)
        self.refresh_button.setStyleSheet("font-size: 14px; padding: 10px;")
        actions_layout.addWidget(self.refresh_button)
        
        actions_layout.addStretch()
        main_layout.addLayout(actions_layout)
        
        self.setLayout(main_layout)
    
    def setup_individual_markers_tab(self):
        """Setup individual markers generation tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Marker Type Selection
        type_group = QGroupBox("Marker Type")
        type_layout = QVBoxLayout()
        
        self.marker_type = QComboBox()
        self.marker_type.addItems([
            "CUE_OUT - Program Out Point",
            "CUE_IN - Program In Point", 
            "CRASH_OUT - Emergency Program Out",
            "TIME_SIGNAL - Timing Reference"
        ])
        self.marker_type.setStyleSheet("font-size: 14px; padding: 8px;")
        self.marker_type.currentTextChanged.connect(self.on_marker_type_changed)
        type_layout.addWidget(self.marker_type)
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # Parameters
        params_group = QGroupBox("Parameters")
        params_layout = QGridLayout()
        
        # Event ID
        params_layout.addWidget(QLabel("Event ID:"), 0, 0)
        self.event_id = QSpinBox()
        self.event_id.setRange(1, 999999)
        self.event_id.setValue(10021)
        self.event_id.setStyleSheet("font-size: 13px; padding: 8px;")
        params_layout.addWidget(self.event_id, 0, 1)
        
        # Duration (for CUE_OUT)
        self.duration_label = QLabel("Duration (seconds):")
        params_layout.addWidget(self.duration_label, 1, 0)
        self.duration = QSpinBox()
        self.duration.setRange(0, 3600)
        self.duration.setValue(30)
        self.duration.setStyleSheet("font-size: 13px; padding: 8px;")
        params_layout.addWidget(self.duration, 1, 1)
        
        # PTS Offset
        params_layout.addWidget(QLabel("PTS Offset (90kHz):"), 2, 0)
        self.pts_offset = QSpinBox()
        self.pts_offset.setRange(-90000, 90000)
        self.pts_offset.setValue(0)
        self.pts_offset.setSuffix(" ticks")
        self.pts_offset.setStyleSheet("font-size: 13px; padding: 8px;")
        params_layout.addWidget(self.pts_offset, 2, 1)
        
        # Options
        options_layout = QVBoxLayout()
        
        self.out_of_network = QCheckBox("Out of Network (ad break)")
        self.out_of_network.setChecked(True)
        self.out_of_network.setStyleSheet("font-size: 13px;")
        options_layout.addWidget(self.out_of_network)
        
        self.immediate = QCheckBox("Immediate (no timing)")
        self.immediate.setChecked(False)
        self.immediate.setStyleSheet("font-size: 13px;")
        options_layout.addWidget(self.immediate)
        
        params_layout.addLayout(options_layout, 3, 0, 1, 2)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Generate Button
        self.generate_button = QPushButton("🎬 Generate Marker")
        self.generate_button.clicked.connect(self.generate_individual_marker)
        self.generate_button.setStyleSheet("font-size: 16px; padding: 12px; background-color: #4CAF50; color: white; font-weight: bold;")
        layout.addWidget(self.generate_button)
        
        # Progress
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "🎯 Individual Markers")
    
    def setup_ad_break_tab(self):
        """Setup ad break sequence generation tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Ad Break Configuration
        config_group = QGroupBox("Ad Break Configuration")
        config_layout = QGridLayout()
        
        # Base Event ID
        config_layout.addWidget(QLabel("Base Event ID:"), 0, 0)
        self.base_event_id = QSpinBox()
        self.base_event_id.setRange(1, 999999)
        self.base_event_id.setValue(10025)
        self.base_event_id.setStyleSheet("font-size: 13px; padding: 8px;")
        config_layout.addWidget(self.base_event_id, 0, 1)
        
        # Ad Duration
        config_layout.addWidget(QLabel("Ad Duration (seconds):"), 1, 0)
        self.ad_duration = QSpinBox()
        self.ad_duration.setRange(1, 3600)
        self.ad_duration.setValue(60)
        self.ad_duration.setStyleSheet("font-size: 13px; padding: 8px;")
        config_layout.addWidget(self.ad_duration, 1, 1)
        
        # Preroll Duration
        config_layout.addWidget(QLabel("Preroll (seconds):"), 2, 0)
        self.preroll_duration = QSpinBox()
        self.preroll_duration.setRange(0, 60)
        self.preroll_duration.setValue(2)
        self.preroll_duration.setStyleSheet("font-size: 13px; padding: 8px;")
        config_layout.addWidget(self.preroll_duration, 2, 1)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Sequence Preview
        preview_group = QGroupBox("Sequence Preview")
        preview_layout = QVBoxLayout()
        
        self.sequence_preview = QTextEdit()
        self.sequence_preview.setMaximumHeight(150)
        self.sequence_preview.setStyleSheet("font-family: monospace; font-size: 12px;")
        self.sequence_preview.setPlainText("Click 'Preview Sequence' to see the generated markers")
        preview_layout.addWidget(self.sequence_preview)
        
        preview_button = QPushButton("👁️ Preview Sequence")
        preview_button.clicked.connect(self.preview_ad_break_sequence)
        preview_button.setStyleSheet("font-size: 14px; padding: 8px;")
        preview_layout.addWidget(preview_button)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Generate Sequence Button
        self.generate_sequence_button = QPushButton("🎬 Generate Ad Break Sequence")
        self.generate_sequence_button.clicked.connect(self.generate_ad_break_sequence)
        self.generate_sequence_button.setStyleSheet("font-size: 16px; padding: 12px; background-color: #2196F3; color: white; font-weight: bold;")
        layout.addWidget(self.generate_sequence_button)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "📺 Ad Break Sequence")
    
    def setup_generated_markers_tab(self):
        """Setup generated markers management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Markers Table
        table_group = QGroupBox("Generated Markers")
        table_layout = QVBoxLayout()
        
        self.markers_table = QTableWidget()
        self.markers_table.setColumnCount(6)
        self.markers_table.setHorizontalHeaderLabels([
            "Type", "Event ID", "Duration", "Immediate", "XML File", "JSON File"
        ])
        self.markers_table.setStyleSheet("font-size: 12px;")
        self.markers_table.horizontalHeader().setStretchLastSection(True)
        table_layout.addWidget(self.markers_table)
        
        # Table Actions
        table_actions = QHBoxLayout()
        
        self.view_xml_button = QPushButton("📄 View XML")
        self.view_xml_button.clicked.connect(self.view_xml_file)
        self.view_xml_button.setStyleSheet("font-size: 12px; padding: 6px;")
        table_actions.addWidget(self.view_xml_button)
        
        self.view_json_button = QPushButton("📋 View JSON")
        self.view_json_button.clicked.connect(self.view_json_file)
        self.view_json_button.setStyleSheet("font-size: 12px; padding: 6px;")
        table_actions.addWidget(self.view_json_button)
        
        self.delete_marker_button = QPushButton("🗑️ Delete Marker")
        self.delete_marker_button.clicked.connect(self.delete_selected_marker)
        self.delete_marker_button.setStyleSheet("font-size: 12px; padding: 6px;")
        table_actions.addWidget(self.delete_marker_button)
        
        table_actions.addStretch()
        table_layout.addLayout(table_actions)
        
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        # Summary
        summary_group = QGroupBox("Summary")
        summary_layout = QVBoxLayout()
        
        self.summary_text = QTextEdit()
        self.summary_text.setMaximumHeight(100)
        self.summary_text.setStyleSheet("font-family: monospace; font-size: 11px;")
        summary_layout.addWidget(self.summary_text)
        
        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "📋 Generated Markers")
    
    def on_marker_type_changed(self):
        """Handle marker type change"""
        marker_type = self.marker_type.currentText()
        
        # Show/hide duration field based on marker type
        if "CUE_OUT" in marker_type:
            self.duration_label.setVisible(True)
            self.duration.setVisible(True)
        else:
            self.duration_label.setVisible(False)
            self.duration.setVisible(False)
        
        # Update immediate checkbox visibility
        if "CRASH_OUT" in marker_type:
            self.immediate.setChecked(True)
            self.immediate.setEnabled(False)
        else:
            self.immediate.setEnabled(True)
    
    def generate_individual_marker(self):
        """Generate individual marker"""
        if not XML_GENERATOR_AVAILABLE:
            QMessageBox.warning(self, "Generator Missing", 
                              "SCTE-35 XML generator is not available.")
            return
        
        try:
            marker_type = self.marker_type.currentText().split(" - ")[0]
            
            params = {
                'event_id': self.event_id.value(),
                'duration': self.duration.value(),
                'pts_offset': self.pts_offset.value(),
                'out_of_network': self.out_of_network.isChecked(),
                'immediate': self.immediate.isChecked(),
                'timestamp': str(int(time.time()))
            }
            
            # Start generation thread
            self.generation_thread = MarkerGenerationThread(marker_type, params)
            self.generation_thread.marker_generated.connect(self.on_marker_generated)
            self.generation_thread.error_occurred.connect(self.on_generation_error)
            self.generation_thread.start()
            
            # Show progress
            self.progress.setVisible(True)
            self.progress.setRange(0, 0)  # Indeterminate progress
            self.generate_button.setEnabled(False)
            
        except Exception as e:
            QMessageBox.critical(self, "Generation Error", f"Failed to start marker generation: {str(e)}")
    
    def generate_ad_break_sequence(self):
        """Generate ad break sequence"""
        if not XML_GENERATOR_AVAILABLE:
            QMessageBox.warning(self, "Generator Missing", 
                              "SCTE-35 XML generator is not available.")
            return
        
        try:
            params = {
                'base_event_id': self.base_event_id.value(),
                'ad_duration': self.ad_duration.value(),
                'preroll_seconds': self.preroll_duration.value()
            }
            
            # Start generation thread
            self.generation_thread = MarkerGenerationThread("AD_BREAK_SEQUENCE", params)
            self.generation_thread.generation_finished.connect(self.on_sequence_generated)
            self.generation_thread.error_occurred.connect(self.on_generation_error)
            self.generation_thread.start()
            
            # Show progress
            self.progress.setVisible(True)
            self.progress.setRange(0, 0)  # Indeterminate progress
            self.generate_sequence_button.setEnabled(False)
            
        except Exception as e:
            QMessageBox.critical(self, "Generation Error", f"Failed to start sequence generation: {str(e)}")
    
    def preview_ad_break_sequence(self):
        """Preview ad break sequence"""
        base_id = self.base_event_id.value()
        duration = self.ad_duration.value()
        preroll = self.preroll_duration.value()
        
        preview_text = f"""Ad Break Sequence Preview:
        
1. TIME_SIGNAL (Event ID: {base_id})
   - Preroll signal ({preroll}s before ad break)
   - File: time_signal_{base_id}_*.xml

2. CUE-OUT (Event ID: {base_id + 1})
   - Ad break start ({duration}s duration)
   - File: cue_out_{base_id + 1}_*.xml

3. CUE-IN (Event ID: {base_id + 2})
   - Return to program
   - File: cue_in_{base_id + 2}_*.xml

Total: 3 markers for complete ad break sequence
Duration: {duration} seconds
Preroll: {preroll} seconds before"""
        
        self.sequence_preview.setPlainText(preview_text)
    
    def on_marker_generated(self, marker_info):
        """Handle marker generation completion"""
        self.generated_markers.append(marker_info)
        self.refresh_markers_list()
        
        # Hide progress and re-enable button
        self.progress.setVisible(False)
        self.generate_button.setEnabled(True)
        
        # Show success message
        QMessageBox.information(self, "Marker Generated", 
                              f"✅ {marker_info['type']} marker generated successfully!\n"
                              f"Event ID: {marker_info['event_id']}\n"
                              f"Files: {marker_info['xml_file']}, {marker_info['json_file']}")
    
    def on_sequence_generated(self, sequence):
        """Handle ad break sequence generation completion"""
        for marker in sequence:
            self.generated_markers.append({
                'type': marker['type'],
                'event_id': marker['event_id'],
                'xml_file': marker['files'][0],
                'json_file': marker['files'][1],
                'description': marker['description']
            })
        
        self.refresh_markers_list()
        
        # Hide progress and re-enable button
        self.progress.setVisible(False)
        self.generate_sequence_button.setEnabled(True)
        
        # Show success message
        QMessageBox.information(self, "Sequence Generated", 
                              f"✅ Ad break sequence generated successfully!\n"
                              f"Generated {len(sequence)} markers\n"
                              f"Duration: {self.ad_duration.value()} seconds")
    
    def on_generation_error(self, error_message):
        """Handle generation error"""
        self.progress.setVisible(False)
        self.generate_button.setEnabled(True)
        self.generate_sequence_button.setEnabled(True)
        
        QMessageBox.critical(self, "Generation Error", f"Failed to generate marker: {error_message}")
    
    def refresh_markers_list(self):
        """Refresh the markers list table"""
        self.markers_table.setRowCount(len(self.generated_markers))
        
        for row, marker in enumerate(self.generated_markers):
            self.markers_table.setItem(row, 0, QTableWidgetItem(marker['type']))
            self.markers_table.setItem(row, 1, QTableWidgetItem(str(marker['event_id'])))
            
            duration = marker.get('duration', 'N/A')
            self.markers_table.setItem(row, 2, QTableWidgetItem(str(duration)))
            
            immediate = marker.get('immediate', False)
            self.markers_table.setItem(row, 3, QTableWidgetItem("Yes" if immediate else "No"))
            
            xml_file = Path(marker['xml_file']).name
            self.markers_table.setItem(row, 4, QTableWidgetItem(xml_file))
            
            json_file = Path(marker['json_file']).name
            self.markers_table.setItem(row, 5, QTableWidgetItem(json_file))
        
        # Update summary
        self.update_summary()
    
    def update_summary(self):
        """Update the summary text"""
        total_markers = len(self.generated_markers)
        
        if total_markers == 0:
            summary_text = "No markers generated yet"
        else:
            marker_types = {}
            for marker in self.generated_markers:
                marker_type = marker['type']
                marker_types[marker_type] = marker_types.get(marker_type, 0) + 1
            
            summary_lines = [f"Total markers: {total_markers}"]
            for marker_type, count in marker_types.items():
                summary_lines.append(f"{marker_type}: {count}")
            
            summary_text = "\n".join(summary_lines)
        
        self.summary_text.setPlainText(summary_text)
    
    def view_xml_file(self):
        """View selected XML file"""
        current_row = self.markers_table.currentRow()
        if current_row >= 0:
            marker = self.generated_markers[current_row]
            xml_file = marker['xml_file']
            
            try:
                with open(xml_file, 'r') as f:
                    content = f.read()
                
                # Show in a dialog
                dialog = QMessageBox(self)
                dialog.setWindowTitle(f"XML Content - {Path(xml_file).name}")
                dialog.setText(content)
                dialog.setDetailedText(f"File: {xml_file}")
                dialog.exec()
                
            except Exception as e:
                QMessageBox.critical(self, "File Error", f"Failed to read XML file: {str(e)}")
    
    def view_json_file(self):
        """View selected JSON file"""
        current_row = self.markers_table.currentRow()
        if current_row >= 0:
            marker = self.generated_markers[current_row]
            json_file = marker['json_file']
            
            try:
                with open(json_file, 'r') as f:
                    content = f.read()
                
                # Show in a dialog
                dialog = QMessageBox(self)
                dialog.setWindowTitle(f"JSON Content - {Path(json_file).name}")
                dialog.setText(content)
                dialog.setDetailedText(f"File: {json_file}")
                dialog.exec()
                
            except Exception as e:
                QMessageBox.critical(self, "File Error", f"Failed to read JSON file: {str(e)}")
    
    def delete_selected_marker(self):
        """Delete selected marker"""
        current_row = self.markers_table.currentRow()
        if current_row >= 0:
            marker = self.generated_markers[current_row]
            
            reply = QMessageBox.question(self, "Delete Marker", 
                                       f"Delete {marker['type']} marker (Event ID: {marker['event_id']})?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    # Delete files
                    os.remove(marker['xml_file'])
                    os.remove(marker['json_file'])
                    
                    # Remove from list
                    del self.generated_markers[current_row]
                    self.refresh_markers_list()
                    
                    QMessageBox.information(self, "Marker Deleted", "Marker deleted successfully")
                    
                except Exception as e:
                    QMessageBox.critical(self, "Delete Error", f"Failed to delete marker: {str(e)}")
    
    def clear_all_markers(self):
        """Clear all generated markers"""
        if not self.generated_markers:
            QMessageBox.information(self, "No Markers", "No markers to clear")
            return
        
        reply = QMessageBox.question(self, "Clear All Markers", 
                                   f"Delete all {len(self.generated_markers)} markers?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Delete all files
                for marker in self.generated_markers:
                    try:
                        os.remove(marker['xml_file'])
                        os.remove(marker['json_file'])
                    except:
                        pass  # File might already be deleted
                
                # Clear list
                self.generated_markers.clear()
                self.refresh_markers_list()
                
                QMessageBox.information(self, "Markers Cleared", "All markers cleared successfully")
                
            except Exception as e:
                QMessageBox.critical(self, "Clear Error", f"Failed to clear markers: {str(e)}")
    
    def get_generated_markers(self) -> List[Dict[str, Any]]:
        """Get list of generated markers"""
        return self.generated_markers.copy()
    
    def get_markers_directory(self) -> str:
        """Get the markers output directory"""
        if self.generator:
            return str(self.generator.output_dir)
        return "scte35_final"


# Test the widget
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    widget = SCTE35GenerationWidget()
    widget.show()
    sys.exit(app.exec())
