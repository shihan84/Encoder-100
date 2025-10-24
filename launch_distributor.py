#!/usr/bin/env python3
"""
Distributor Configuration Launcher
Specialized launcher for distributor streaming requirements
"""

import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tsduck_gui import MainWindow
from distributor_scte35_dialog import DistributorSCTE35Dialog


class DistributorLauncher(QMainWindow):
    """Distributor configuration launcher"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSDuck GUI - Distributor Configuration")
        self.setMinimumSize(800, 600)
        
        self.setup_ui()
        self.load_distributor_config()
        
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Distributor Streaming Configuration")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Configuration display
        self.config_display = QTextEdit()
        self.config_display.setReadOnly(True)
        self.config_display.setFont(QFont("Monaco", 9))
        layout.addWidget(self.config_display)
        
        # Buttons
        button_layout = QVBoxLayout()
        
        self.configure_btn = QPushButton("Configure SCTE-35 & Stream Specs")
        self.configure_btn.clicked.connect(self.configure_scte35)
        self.configure_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        button_layout.addWidget(self.configure_btn)
        
        self.launch_btn = QPushButton("Launch TSDuck GUI with Configuration")
        self.launch_btn.clicked.connect(self.launch_gui)
        self.launch_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 10px; }")
        button_layout.addWidget(self.launch_btn)
        
        self.test_btn = QPushButton("Test Configuration")
        self.test_btn.clicked.connect(self.test_configuration)
        self.test_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; padding: 10px; }")
        button_layout.addWidget(self.test_btn)
        
        layout.addLayout(button_layout)
        central_widget.setLayout(layout)
        
    def load_distributor_config(self):
        """Load distributor configuration"""
        try:
            with open('distributor_config.json', 'r') as f:
                self.config = json.load(f)
            self.update_config_display()
        except FileNotFoundError:
            QMessageBox.warning(self, "Configuration Not Found", 
                              "distributor_config.json not found. Using default configuration.")
            self.config = self.get_default_config()
            self.update_config_display()
            
    def get_default_config(self):
        """Get default distributor configuration"""
        return {
            "input": {
                "type": "hls",
                "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
                "params": ""
            },
            "output": {
                "type": "srt",
                "source": "srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish",
                "params": "--streamid '#!::r=scte/scte,m=publish' --latency 2000"
            },
            "scte35": {
                "data_pid": 500,
                "null_pid": 8191,
                "event_id": 100023,
                "ad_duration": 600,
                "preroll_duration": 0
            }
        }
        
    def update_config_display(self):
        """Update configuration display"""
        config_text = f"""
DISTRIBUTOR STREAMING CONFIGURATION
===================================

INPUT:
  Type: {self.config['input']['type'].upper()}
  Source: {self.config['input']['source']}
  Parameters: {self.config['input']['params']}

OUTPUT:
  Type: {self.config['output']['type'].upper()}
  Destination: {self.config['output']['source']}
  Parameters: {self.config['output']['params']}

SCTE-35 CONFIGURATION:
  Data PID: {self.config['scte35'].get('data_pid', 500)}
  Null PID: {self.config['scte35'].get('null_pid', 8191)}
  Event ID: {self.config['scte35'].get('event_id', 100023)}
  Ad Duration: {self.config['scte35'].get('ad_duration', 600)} seconds
  Pre-roll Duration: {self.config['scte35'].get('preroll_duration', 0)} seconds

STREAM SPECIFICATIONS:
  Video: 1920x1080 H.264, 5 Mbps, GOP 12, 5 B-frames
  Audio: AAC-LC, 128 Kbps, -20 dB LKFS, 48kHz
  SRT Latency: 2000 milliseconds
  Stream ID: #!::r=scte/scte,m=publish

SCTE-35 EVENTS:
  - CUE-OUT: Start of ad break (Program out point)
  - CUE-IN: End of ad break (Program in point)  
  - Crash CUE-IN: Emergency return to program
  - Ad Duration: 600 seconds (10 minutes)
  - Pre-roll: 0 seconds
        """
        self.config_display.setPlainText(config_text)
        
    def configure_scte35(self):
        """Configure SCTE-35 and stream specifications"""
        dialog = DistributorSCTE35Dialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            config = dialog.get_config()
            
            # Update SCTE-35 configuration
            if 'scte35' not in self.config:
                self.config['scte35'] = {}
            self.config['scte35'].update({
                'data_pid': config['scte35']['scte_pid'],
                'null_pid': config['scte35']['null_pid'],
                'event_id': config['scte35']['event_id'],
                'ad_duration': config['scte35']['ad_duration'],
                'preroll_duration': config['scte35']['preroll_duration']
            })
            
            # Update SRT configuration
            srt_url = dialog.generate_srt_url()
            self.config['output']['source'] = srt_url
            self.config['output']['params'] = f"--remote-address {config['srt']['host']} --remote-port {config['srt']['port']} --streamid '{config['srt']['streamid']}' --latency {config['srt']['latency']}"
            
            # Update SCTE-35 injection parameters
            scte35_params = dialog.generate_tsduck_params()
            if 'plugins' not in self.config:
                self.config['plugins'] = {}
            if 'spliceinject' not in self.config['plugins']:
                self.config['plugins']['spliceinject'] = {'enabled': True, 'params': ''}
            self.config['plugins']['spliceinject']['params'] = scte35_params
            
            self.update_config_display()
            
            # Save configuration
            self.save_configuration()
            
            QMessageBox.information(self, "Configuration Updated", 
                                  "SCTE-35 and stream specifications have been updated.")
                                  
    def save_configuration(self):
        """Save configuration to file"""
        try:
            with open('distributor_config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save configuration: {str(e)}")
            
    def test_configuration(self):
        """Test the configuration"""
        try:
            # Test input URL accessibility
            import requests
            response = requests.head(self.config['input']['source'], timeout=5)
            if response.status_code == 200:
                QMessageBox.information(self, "Configuration Test", 
                                      "✅ Input HLS stream is accessible\n"
                                      "✅ Configuration appears valid\n"
                                      "✅ Ready for streaming")
            else:
                QMessageBox.warning(self, "Configuration Test", 
                                  f"⚠️ Input stream returned status: {response.status_code}")
        except Exception as e:
            QMessageBox.warning(self, "Configuration Test", 
                              f"⚠️ Could not test input stream: {str(e)}\n"
                              "Please verify the HLS URL is correct and accessible.")
                              
    def launch_gui(self):
        """Launch TSDuck GUI with distributor configuration"""
        try:
            # Create and configure main window
            self.gui_window = MainWindow()
            
            # Apply distributor configuration
            self.apply_configuration_to_gui()
            
            # Show the GUI
            self.gui_window.show()
            
            # Hide this launcher
            self.hide()
            
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", f"Failed to launch GUI: {str(e)}")
            
    def apply_configuration_to_gui(self):
        """Apply distributor configuration to GUI"""
        # Configure input
        self.gui_window.input_widget.type_combo.setCurrentText(self.config['input']['type'].title())
        self.gui_window.input_widget.source_edit.setText(self.config['input']['source'])
        self.gui_window.input_widget.params_edit.setText(self.config['input']['params'])
        
        # Configure output
        self.gui_window.output_widget.type_combo.setCurrentText(self.config['output']['type'].title())
        self.gui_window.output_widget.source_edit.setText(self.config['output']['source'])
        self.gui_window.output_widget.params_edit.setText(self.config['output']['params'])
        
        # Configure plugins
        if 'plugins' in self.config:
            all_plugins = (self.gui_window.analysis_plugins + self.gui_window.processing_plugins + 
                          self.gui_window.scte35_plugins + self.gui_window.tables_plugins + 
                          self.gui_window.services_plugins)
            
            for plugin in all_plugins:
                if plugin.plugin_name in self.config['plugins']:
                    plugin_config = self.config['plugins'][plugin.plugin_name]
                    plugin.enabled.setChecked(plugin_config.get('enabled', False))
                    plugin.params_edit.setText(plugin_config.get('params', ''))
                    
        QMessageBox.information(self.gui_window, "Configuration Applied", 
                              "Distributor configuration has been applied to TSDuck GUI.\n\n"
                              "You can now start processing with the configured settings.")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("TSDuck Distributor Launcher")
    
    # Set application style
    try:
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
    except ImportError:
        pass
        
    # Create and show launcher
    launcher = DistributorLauncher()
    launcher.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
