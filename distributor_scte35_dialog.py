#!/usr/bin/env python3
"""
Distributor SCTE-35 Configuration Dialog
Specialized dialog for distributor requirements
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QLineEdit, QSpinBox, QCheckBox, QComboBox, QDialogButtonBox,
    QGroupBox, QTextEdit, QTabWidget, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from typing import Dict, Any


class DistributorSCTE35Dialog(QDialog):
    """Specialized SCTE-35 dialog for distributor requirements"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Distributor SCTE-35 Configuration")
        self.setModal(True)
        self.resize(600, 500)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        
        # Create tab widget
        tabs = QTabWidget()
        
        # SCTE-35 Configuration tab
        scte35_tab = self.create_scte35_tab()
        tabs.addTab(scte35_tab, "SCTE-35 Configuration")
        
        # Stream Specifications tab
        stream_tab = self.create_stream_specs_tab()
        tabs.addTab(stream_tab, "Stream Specifications")
        
        # SRT Configuration tab
        srt_tab = self.create_srt_tab()
        tabs.addTab(srt_tab, "SRT Configuration")
        
        layout.addWidget(tabs)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        
    def create_scte35_tab(self) -> QWidget:
        """Create SCTE-35 configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # SCTE-35 Event Configuration
        event_group = QGroupBox("SCTE-35 Event Configuration")
        event_layout = QFormLayout()
        
        # Event ID
        self.event_id = QSpinBox()
        self.event_id.setRange(1, 0x7FFFFFFF)
        self.event_id.setValue(100023)
        event_layout.addRow("SCTE Event ID (Unique ID):", self.event_id)
        
        # Ad Duration
        self.ad_duration = QSpinBox()
        self.ad_duration.setRange(1, 3600)
        self.ad_duration.setValue(600)
        self.ad_duration.setSuffix(" seconds")
        event_layout.addRow("Ad Duration:", self.ad_duration)
        
        # Pre-roll Duration
        self.preroll_duration = QSpinBox()
        self.preroll_duration.setRange(0, 10)
        self.preroll_duration.setValue(0)
        self.preroll_duration.setSuffix(" seconds")
        event_layout.addRow("Pre-roll Ad Duration:", self.preroll_duration)
        
        # SCTE Data PID
        self.scte_pid = QSpinBox()
        self.scte_pid.setRange(1, 8191)
        self.scte_pid.setValue(500)
        self.scte_pid.setPrefix("0x")
        self.scte_pid.setDisplayIntegerBase(16)
        event_layout.addRow("SCTE Data PID:", self.scte_pid)
        
        # Null PID
        self.null_pid = QSpinBox()
        self.null_pid.setRange(1, 8191)
        self.null_pid.setValue(8191)
        self.null_pid.setPrefix("0x")
        self.null_pid.setDisplayIntegerBase(16)
        event_layout.addRow("Null PID:", self.null_pid)
        
        # Event Type
        self.event_type = QComboBox()
        self.event_type.addItems([
            "CUE-OUT (Program out point)",
            "CUE-IN (Program in point)",
            "Crash CUE-IN (Emergency return)"
        ])
        event_layout.addRow("Event Type:", self.event_type)
        
        # Out of Network
        self.out_of_network = QCheckBox()
        self.out_of_network.setChecked(True)
        event_layout.addRow("Out of Network:", self.out_of_network)
        
        # Immediate
        self.immediate = QCheckBox()
        self.immediate.setChecked(False)
        event_layout.addRow("Immediate:", self.immediate)
        
        event_group.setLayout(event_layout)
        layout.addWidget(event_group)
        
        # SCTE-35 Examples
        examples_group = QGroupBox("SCTE-35 Examples")
        examples_layout = QVBoxLayout()
        
        examples_text = QTextEdit()
        examples_text.setReadOnly(True)
        examples_text.setMaximumHeight(150)
        examples_text.setPlainText("""
SCTE-35 Event Examples:

1. CUE-OUT (Start of Ad):
   - Event ID: 100023
   - Duration: 600 seconds
   - Type: CUE-OUT
   - Out of Network: Yes

2. CUE-IN (End of Ad):
   - Event ID: 100024
   - Duration: 0 seconds
   - Type: CUE-IN
   - Out of Network: No

3. Crash CUE-IN (Emergency Return):
   - Event ID: 100025
   - Duration: 0 seconds
   - Type: Crash CUE-IN
   - Out of Network: No
        """)
        examples_layout.addWidget(examples_text)
        
        examples_group.setLayout(examples_layout)
        layout.addWidget(examples_group)
        
        widget.setLayout(layout)
        return widget
        
    def create_stream_specs_tab(self) -> QWidget:
        """Create stream specifications tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Video Specifications
        video_group = QGroupBox("Video Specifications")
        video_layout = QFormLayout()
        
        self.video_resolution = QComboBox()
        self.video_resolution.addItems(["1920x1080", "1280x720", "854x480"])
        self.video_resolution.setCurrentText("1920x1080")
        video_layout.addRow("Resolution:", self.video_resolution)
        
        self.video_codec = QComboBox()
        self.video_codec.addItems(["H.264", "H.265", "MPEG-2"])
        self.video_codec.setCurrentText("H.264")
        video_layout.addRow("Codec:", self.video_codec)
        
        self.profile_level = QComboBox()
        self.profile_level.addItems(["High@Auto", "High@4.1", "High@4.0", "Main@4.1"])
        self.profile_level.setCurrentText("High@Auto")
        video_layout.addRow("Profile@Level:", self.profile_level)
        
        self.gop = QSpinBox()
        self.gop.setRange(1, 30)
        self.gop.setValue(12)
        video_layout.addRow("GOP:", self.gop)
        
        self.b_frames = QSpinBox()
        self.b_frames.setRange(0, 10)
        self.b_frames.setValue(5)
        video_layout.addRow("B Frames:", self.b_frames)
        
        self.video_bitrate = QComboBox()
        self.video_bitrate.addItems(["5 Mbps", "4 Mbps", "3 Mbps", "2 Mbps"])
        self.video_bitrate.setCurrentText("5 Mbps")
        video_layout.addRow("Bitrate:", self.video_bitrate)
        
        self.chroma = QComboBox()
        self.chroma.addItems(["4:2:0", "4:2:2", "4:4:4"])
        self.chroma.setCurrentText("4:2:0")
        video_layout.addRow("Chroma:", self.chroma)
        
        self.aspect_ratio = QComboBox()
        self.aspect_ratio.addItems(["16:9", "4:3", "21:9"])
        self.aspect_ratio.setCurrentText("16:9")
        video_layout.addRow("Aspect Ratio:", self.aspect_ratio)
        
        self.pcr_embedded = QCheckBox()
        self.pcr_embedded.setChecked(True)
        video_layout.addRow("PCR Embedded:", self.pcr_embedded)
        
        video_group.setLayout(video_layout)
        layout.addWidget(video_group)
        
        # Audio Specifications
        audio_group = QGroupBox("Audio Specifications")
        audio_layout = QFormLayout()
        
        self.audio_codec = QComboBox()
        self.audio_codec.addItems(["AAC-LC", "AC-3", "MPEG-1 Audio"])
        self.audio_codec.setCurrentText("AAC-LC")
        audio_layout.addRow("Codec:", self.audio_codec)
        
        self.audio_bitrate = QComboBox()
        self.audio_bitrate.addItems(["128 Kbps", "192 Kbps", "256 Kbps", "320 Kbps"])
        self.audio_bitrate.setCurrentText("128 Kbps")
        audio_layout.addRow("Bitrate:", self.audio_bitrate)
        
        self.audio_lkfs = QComboBox()
        self.audio_lkfs.addItems(["-20 db", "-23 db", "-18 db", "-16 db"])
        self.audio_lkfs.setCurrentText("-20 db")
        audio_layout.addRow("LKFS:", self.audio_lkfs)
        
        self.sample_rate = QComboBox()
        self.sample_rate.addItems(["48kHz", "44.1kHz", "96kHz"])
        self.sample_rate.setCurrentText("48kHz")
        audio_layout.addRow("Sample Rate:", self.sample_rate)
        
        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)
        
        widget.setLayout(layout)
        return widget
        
    def create_srt_tab(self) -> QWidget:
        """Create SRT configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # SRT Configuration
        srt_group = QGroupBox("SRT Configuration")
        srt_layout = QFormLayout()
        
        self.srt_host = QLineEdit()
        self.srt_host.setText("cdn.itassist.one")
        srt_layout.addRow("Host:", self.srt_host)
        
        self.srt_port = QSpinBox()
        self.srt_port.setRange(1, 65535)
        self.srt_port.setValue(8888)
        srt_layout.addRow("Port:", self.srt_port)
        
        self.streamid = QLineEdit()
        self.streamid.setText("#!::r=scte/scte,m=publish")
        srt_layout.addRow("Stream ID:", self.streamid)
        
        self.latency = QSpinBox()
        self.latency.setRange(100, 10000)
        self.latency.setValue(2000)
        self.latency.setSuffix(" milliseconds")
        srt_layout.addRow("Latency:", self.latency)
        
        srt_group.setLayout(srt_layout)
        layout.addWidget(srt_group)
        
        # SRT URL Preview
        url_group = QGroupBox("SRT URL Preview")
        url_layout = QVBoxLayout()
        
        self.url_preview = QTextEdit()
        self.url_preview.setReadOnly(True)
        self.url_preview.setMaximumHeight(100)
        self.url_preview.setPlainText("srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish")
        url_layout.addWidget(self.url_preview)
        
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)
        
        widget.setLayout(layout)
        return widget
        
    def get_config(self) -> Dict[str, Any]:
        """Get the complete configuration"""
        return {
            'scte35': {
                'event_id': self.event_id.value(),
                'ad_duration': self.ad_duration.value(),
                'preroll_duration': self.preroll_duration.value(),
                'scte_pid': self.scte_pid.value(),
                'null_pid': self.null_pid.value(),
                'event_type': self.event_type.currentText(),
                'out_of_network': self.out_of_network.isChecked(),
                'immediate': self.immediate.isChecked()
            },
            'video': {
                'resolution': self.video_resolution.currentText(),
                'codec': self.video_codec.currentText(),
                'profile_level': self.profile_level.currentText(),
                'gop': self.gop.value(),
                'b_frames': self.b_frames.value(),
                'bitrate': self.video_bitrate.currentText(),
                'chroma': self.chroma.currentText(),
                'aspect_ratio': self.aspect_ratio.currentText(),
                'pcr_embedded': self.pcr_embedded.isChecked()
            },
            'audio': {
                'codec': self.audio_codec.currentText(),
                'bitrate': self.audio_bitrate.currentText(),
                'lkfs': self.audio_lkfs.currentText(),
                'sample_rate': self.sample_rate.currentText()
            },
            'srt': {
                'host': self.srt_host.text(),
                'port': self.srt_port.value(),
                'streamid': self.streamid.text(),
                'latency': self.latency.value()
            }
        }
    
    def generate_tsduck_params(self) -> str:
        """Generate TSDuck parameters for SCTE-35 injection"""
        config = self.get_config()
        scte35 = config['scte35']
        
        params = [
            f"--pid {scte35['scte_pid']}",
            f"--event-id {scte35['event_id']}",
            f"--unique-program-id 1",
            f"--avail-num 1",
            f"--avails-expected 1"
        ]
        
        if scte35['immediate']:
            params.append("--immediate")
        if scte35['out_of_network']:
            params.append("--out-of-network")
            
        if scte35['ad_duration'] > 0:
            duration_seconds = scte35['ad_duration']
            hours = duration_seconds // 3600
            minutes = (duration_seconds % 3600) // 60
            seconds = duration_seconds % 60
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.000"
            params.append(f"--duration {duration_str}")
            
        return ' '.join(params)
    
    def generate_srt_url(self) -> str:
        """Generate SRT URL"""
        config = self.get_config()
        srt = config['srt']
        return f"srt://{srt['host']}:{srt['port']}?streamid={srt['streamid']}"
