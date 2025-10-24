#!/usr/bin/env python3
"""
Source Preview Module
Real-time source analysis and preview for TSDuck GUI
"""

import subprocess
import threading
import queue
import json
import re
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
import logging


@dataclass
class StreamInfo:
    """Stream information data structure"""
    bitrate: int
    packets_per_second: int
    errors: int
    pcr_accuracy: float
    continuity_errors: int
    services_count: int
    pids_count: int
    video_streams: List[Dict[str, Any]]
    audio_streams: List[Dict[str, Any]]
    data_streams: List[Dict[str, Any]]


@dataclass
class ServiceInfo:
    """Service information data structure"""
    service_id: str
    name: str
    service_type: str
    pids: List[str]
    pmt_pid: str
    video_pid: Optional[str]
    audio_pids: List[str]
    subtitle_pids: List[str]


@dataclass
class PIDInfo:
    """PID information data structure"""
    pid: str
    pid_type: str
    bitrate: int
    packets_count: int
    description: str
    stream_type: Optional[str]
    language: Optional[str]


@dataclass
class TableInfo:
    """Table information data structure"""
    table_name: str
    pid: str
    version: int
    size: int
    last_update: datetime
    sections_count: int


class SourcePreviewProcessor:
    """Process source preview using TSDuck"""
    
    def __init__(self):
        self.process = None
        self.output_queue = queue.Queue()
        self.running = False
        self.thread = None
        
    def start_preview(self, input_config: Dict[str, str], callback: Callable[[Dict[str, Any]], None]):
        """Start source preview analysis"""
        if self.running:
            self.stop_preview()
            
        self.running = True
        self.callback = callback
        self.thread = threading.Thread(target=self._preview_worker, args=(input_config,))
        self.thread.daemon = True
        self.thread.start()
        
    def stop_preview(self):
        """Stop source preview"""
        self.running = False
        if self.process:
            self.process.terminate()
        if self.thread:
            self.thread.join(timeout=2.0)
            
    def _preview_worker(self, input_config: Dict[str, str]):
        """Worker thread for source preview"""
        try:
            # Build TSDuck command for analysis
            command = self._build_analysis_command(input_config)
            
            # Start TSDuck process
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Parse output
            self._parse_tsduck_output()
            
        except Exception as e:
            logging.error(f"Error in preview worker: {e}")
            if self.callback:
                self.callback({'error': str(e)})
                
    def _build_analysis_command(self, input_config: Dict[str, str]) -> List[str]:
        """Build TSDuck command for source analysis"""
        command = ['tsp']
        
        # Input
        input_type = input_config.get('type', 'file').lower()
        source = input_config.get('source', '')
        params = input_config.get('params', '')
        
        if input_type == 'file':
            command.extend(['-I', 'file', source])
        elif input_type == 'udp':
            command.extend(['-I', 'udp', source])
        elif input_type == 'tcp':
            command.extend(['-I', 'tcp', source])
        elif input_type == 'http':
            command.extend(['-I', 'http', source])
        elif input_type == 'hls':
            command.extend(['-I', 'hls', source])
        elif input_type == 'srt':
            command.extend(['-I', 'srt', source])
        elif input_type == 'rist':
            command.extend(['-I', 'rist', source])
        elif input_type == 'dvb':
            command.extend(['-I', 'dvb', source])
        elif input_type == 'atsc':
            command.extend(['-I', 'atsc', source])
        elif input_type == 'isdb':
            command.extend(['-I', 'isdb', source])
        elif input_type == 'asi':
            command.extend(['-I', 'asi', source])
        elif input_type == 'dektec':
            command.extend(['-I', 'dektec', source])
        elif input_type == 'hides':
            command.extend(['-I', 'hides', source])
        elif input_type == 'vatek':
            command.extend(['-I', 'vatek', source])
            
        # Add input parameters
        if params:
            command.extend(params.split())
            
        # Analysis plugins
        command.extend([
            '-P', 'analyze', '--all-streams',
            '-P', 'stats', '--interval', '1000',
            '-P', 'continuity',
            '-P', 'tstables', '--all-tables'
        ])
        
        # Output to null (we only want analysis)
        command.extend(['-O', 'null'])
        
        return command
        
    def _parse_tsduck_output(self):
        """Parse TSDuck output for preview data"""
        stream_info = StreamInfo(
            bitrate=0,
            packets_per_second=0,
            errors=0,
            pcr_accuracy=0.0,
            continuity_errors=0,
            services_count=0,
            pids_count=0,
            video_streams=[],
            audio_streams=[],
            data_streams=[]
        )
        
        services = []
        pids = []
        tables = []
        
        try:
            # Read output line by line
            for line in iter(self.process.stdout.readline, ''):
                if not self.running:
                    break
                    
                line = line.strip()
                if not line:
                    continue
                    
                # Parse different types of output
                self._parse_analyze_line(line, stream_info)
                self._parse_stats_line(line, stream_info)
                self._parse_continuity_line(line, stream_info)
                self._parse_tables_line(line, tables)
                
                # Send updates to callback
                if self.callback:
                    self.callback({
                        'stream_info': stream_info,
                        'services': services,
                        'pids': pids,
                        'tables': tables
                    })
                    
        except Exception as e:
            logging.error(f"Error parsing TSDuck output: {e}")
            
    def _parse_analyze_line(self, line: str, stream_info: StreamInfo):
        """Parse analyze plugin output"""
        if 'Bitrate:' in line:
            try:
                bitrate_str = line.split('Bitrate:')[1].strip().split()[0]
                stream_info.bitrate = self._parse_bitrate(bitrate_str)
            except (IndexError, ValueError):
                pass
        elif 'Packets/sec:' in line:
            try:
                pps_str = line.split('Packets/sec:')[1].strip().split()[0]
                stream_info.packets_per_second = int(pps_str.replace(',', ''))
            except (IndexError, ValueError):
                pass
        elif 'Services:' in line:
            try:
                services_str = line.split('Services:')[1].strip().split()[0]
                stream_info.services_count = int(services_str)
            except (IndexError, ValueError):
                pass
        elif 'PIDs:' in line:
            try:
                pids_str = line.split('PIDs:')[1].strip().split()[0]
                stream_info.pids_count = int(pids_str)
            except (IndexError, ValueError):
                pass
                
    def _parse_stats_line(self, line: str, stream_info: StreamInfo):
        """Parse stats plugin output"""
        if 'Errors:' in line:
            try:
                errors_str = line.split('Errors:')[1].strip().split()[0]
                stream_info.errors = int(errors_str)
            except (IndexError, ValueError):
                pass
        elif 'PCR accuracy:' in line:
            try:
                accuracy_str = line.split('PCR accuracy:')[1].strip().replace('%', '')
                stream_info.pcr_accuracy = float(accuracy_str)
            except (IndexError, ValueError):
                pass
                
    def _parse_continuity_line(self, line: str, stream_info: StreamInfo):
        """Parse continuity plugin output"""
        if 'Continuity errors:' in line:
            try:
                cont_errors_str = line.split('Continuity errors:')[1].strip().split()[0]
                stream_info.continuity_errors = int(cont_errors_str)
            except (IndexError, ValueError):
                pass
                
    def _parse_tables_line(self, line: str, tables: List[TableInfo]):
        """Parse tables plugin output"""
        # This would parse table information from TSDuck output
        # For now, we'll simulate some table data
        pass
        
    def _parse_bitrate(self, bitrate_str: str) -> int:
        """Parse bitrate string to integer"""
        bitrate_str = bitrate_str.upper()
        if 'KBPS' in bitrate_str:
            return int(float(bitrate_str.replace('KBPS', '')) * 1000)
        elif 'MBPS' in bitrate_str:
            return int(float(bitrate_str.replace('MBPS', '')) * 1000000)
        elif 'GBPS' in bitrate_str:
            return int(float(bitrate_str.replace('GBPS', '')) * 1000000000)
        else:
            return int(float(bitrate_str))


class PreviewDataGenerator:
    """Generate preview data for demonstration purposes"""
    
    @staticmethod
    def generate_sample_data() -> Dict[str, Any]:
        """Generate sample preview data"""
        return {
            'stream_info': {
                'bitrate': 15200000,  # 15.2 Mbps
                'packets_per_second': 25000,
                'errors': 0,
                'pcr_accuracy': 99.9,
                'continuity_errors': 0,
                'services_count': 5,
                'pids_count': 20,
                'video_streams': [
                    {'pid': '0x101', 'type': 'MPEG-2', 'resolution': '1920x1080', 'fps': 25},
                    {'pid': '0x201', 'type': 'MPEG-2', 'resolution': '1920x1080', 'fps': 25},
                    {'pid': '0x301', 'type': 'MPEG-2', 'resolution': '1280x720', 'fps': 25}
                ],
                'audio_streams': [
                    {'pid': '0x102', 'type': 'AC-3', 'channels': '5.1', 'sample_rate': '48kHz'},
                    {'pid': '0x202', 'type': 'AC-3', 'channels': '5.1', 'sample_rate': '48kHz'},
                    {'pid': '0x401', 'type': 'MPEG-1', 'channels': '2.0', 'sample_rate': '48kHz'}
                ],
                'data_streams': [
                    {'pid': '0x103', 'type': 'DVB Subtitles', 'languages': ['en', 'fr', 'de']},
                    {'pid': '0x11', 'type': 'SDT', 'description': 'Service Description Table'},
                    {'pid': '0x12', 'type': 'EIT', 'description': 'Event Information Table'}
                ]
            },
            'services': [
                {
                    'service_id': '0x100',
                    'name': 'BBC One HD',
                    'service_type': 'TV',
                    'pids': ['0x101', '0x102', '0x103'],
                    'pmt_pid': '0x100',
                    'video_pid': '0x101',
                    'audio_pids': ['0x102'],
                    'subtitle_pids': ['0x103']
                },
                {
                    'service_id': '0x200',
                    'name': 'BBC Two HD',
                    'service_type': 'TV',
                    'pids': ['0x201', '0x202', '0x203'],
                    'pmt_pid': '0x200',
                    'video_pid': '0x201',
                    'audio_pids': ['0x202'],
                    'subtitle_pids': ['0x203']
                },
                {
                    'service_id': '0x300',
                    'name': 'BBC News',
                    'service_type': 'TV',
                    'pids': ['0x301', '0x302'],
                    'pmt_pid': '0x300',
                    'video_pid': '0x301',
                    'audio_pids': ['0x302'],
                    'subtitle_pids': []
                },
                {
                    'service_id': '0x400',
                    'name': 'Radio 1',
                    'service_type': 'Radio',
                    'pids': ['0x401'],
                    'pmt_pid': '0x400',
                    'video_pid': None,
                    'audio_pids': ['0x401'],
                    'subtitle_pids': []
                },
                {
                    'service_id': '0x500',
                    'name': 'Radio 2',
                    'service_type': 'Radio',
                    'pids': ['0x501'],
                    'pmt_pid': '0x500',
                    'video_pid': None,
                    'audio_pids': ['0x501'],
                    'subtitle_pids': []
                }
            ],
            'pids': [
                {'pid': '0x000', 'type': 'PAT', 'bitrate': 1200000, 'packets': 25000, 'description': 'Program Association Table'},
                {'pid': '0x100', 'type': 'PMT', 'bitrate': 100000, 'packets': 2000, 'description': 'Program Map Table - BBC One'},
                {'pid': '0x101', 'type': 'Video', 'bitrate': 12000000, 'packets': 20000, 'description': 'MPEG-2 Video'},
                {'pid': '0x102', 'type': 'Audio', 'bitrate': 200000, 'packets': 4000, 'description': 'AC-3 Audio'},
                {'pid': '0x103', 'type': 'Subtitles', 'bitrate': 100000, 'packets': 1000, 'description': 'DVB Subtitles'},
                {'pid': '0x200', 'type': 'PMT', 'bitrate': 100000, 'packets': 2000, 'description': 'Program Map Table - BBC Two'},
                {'pid': '0x201', 'type': 'Video', 'bitrate': 12000000, 'packets': 20000, 'description': 'MPEG-2 Video'},
                {'pid': '0x202', 'type': 'Audio', 'bitrate': 200000, 'packets': 4000, 'description': 'AC-3 Audio'},
                {'pid': '0x203', 'type': 'Subtitles', 'bitrate': 100000, 'packets': 1000, 'description': 'DVB Subtitles'},
                {'pid': '0x300', 'type': 'PMT', 'bitrate': 100000, 'packets': 2000, 'description': 'Program Map Table - BBC News'},
                {'pid': '0x301', 'type': 'Video', 'bitrate': 8000000, 'packets': 15000, 'description': 'MPEG-2 Video'},
                {'pid': '0x302', 'type': 'Audio', 'bitrate': 200000, 'packets': 4000, 'description': 'AC-3 Audio'},
                {'pid': '0x400', 'type': 'PMT', 'bitrate': 100000, 'packets': 1000, 'description': 'Program Map Table - Radio 1'},
                {'pid': '0x401', 'type': 'Audio', 'bitrate': 100000, 'packets': 2000, 'description': 'MPEG-1 Audio'},
                {'pid': '0x500', 'type': 'PMT', 'bitrate': 100000, 'packets': 1000, 'description': 'Program Map Table - Radio 2'},
                {'pid': '0x501', 'type': 'Audio', 'bitrate': 100000, 'packets': 2000, 'description': 'MPEG-1 Audio'},
                {'pid': '0x11', 'type': 'SDT', 'bitrate': 100000, 'packets': 500, 'description': 'Service Description Table'},
                {'pid': '0x12', 'type': 'EIT', 'bitrate': 200000, 'packets': 1000, 'description': 'Event Information Table'},
                {'pid': '0x14', 'type': 'TDT', 'bitrate': 100000, 'packets': 100, 'description': 'Time & Date Table'},
                {'pid': '0x1FFF', 'type': 'Null', 'bitrate': 0, 'packets': 0, 'description': 'Null packets'}
            ],
            'tables': [
                {'table_name': 'PAT', 'pid': '0x000', 'version': 1, 'size': 28, 'last_update': '2024-01-01 12:00:00', 'sections_count': 1},
                {'table_name': 'PMT - BBC One', 'pid': '0x100', 'version': 5, 'size': 156, 'last_update': '2024-01-01 12:00:00', 'sections_count': 1},
                {'table_name': 'PMT - BBC Two', 'pid': '0x200', 'version': 3, 'size': 142, 'last_update': '2024-01-01 12:00:00', 'sections_count': 1},
                {'table_name': 'PMT - BBC News', 'pid': '0x300', 'version': 2, 'size': 98, 'last_update': '2024-01-01 12:00:00', 'sections_count': 1},
                {'table_name': 'PMT - Radio 1', 'pid': '0x400', 'version': 1, 'size': 45, 'last_update': '2024-01-01 12:00:00', 'sections_count': 1},
                {'table_name': 'PMT - Radio 2', 'pid': '0x500', 'version': 1, 'size': 43, 'last_update': '2024-01-01 12:00:00', 'sections_count': 1},
                {'table_name': 'SDT', 'pid': '0x11', 'version': 1, 'size': 234, 'last_update': '2024-01-01 12:00:00', 'sections_count': 1},
                {'table_name': 'EIT Present/Following', 'pid': '0x12', 'version': 1, 'size': 1234, 'last_update': '2024-01-01 12:00:00', 'sections_count': 1},
                {'table_name': 'EIT Schedule', 'pid': '0x12', 'version': 1, 'size': 5678, 'last_update': '2024-01-01 12:00:00', 'sections_count': 1},
                {'table_name': 'TDT', 'pid': '0x14', 'version': 1, 'size': 12, 'last_update': '2024-01-01 12:00:00', 'sections_count': 1}
            ]
        }


# Example usage
if __name__ == "__main__":
    # Test the preview processor
    processor = SourcePreviewProcessor()
    
    def preview_callback(data):
        print(f"Preview data received: {data}")
        
    input_config = {
        'type': 'file',
        'source': '/path/to/test.ts',
        'params': ''
    }
    
    # Generate sample data for testing
    sample_data = PreviewDataGenerator.generate_sample_data()
    preview_callback(sample_data)
