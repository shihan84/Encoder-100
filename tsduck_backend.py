#!/usr/bin/env python3
"""
TSDuck Backend Integration
Advanced backend services for TSDuck GUI application
"""

import os
import sys
import json
import subprocess
import threading
import time
import queue
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
import logging

# Try to import TSDuck Python bindings
try:
    import tsduck
    TSDUCK_AVAILABLE = True
except ImportError:
    TSDUCK_AVAILABLE = False
    print("Warning: TSDuck Python bindings not available. Using subprocess fallback.")


class TSDuckCommandBuilder:
    """Build TSDuck commands from configuration"""
    
    @staticmethod
    def build_input_command(config: Dict[str, str]) -> List[str]:
        """Build input command from configuration"""
        input_type = config.get('type', 'file').lower()
        source = config.get('source', '')
        params = config.get('params', '')
        
        if not source:
            raise ValueError("Input source is required")
            
        cmd = ['-I', input_type, source]
        
        # Add specific parameters based on input type
        if input_type == 'file':
            if not os.path.exists(source):
                raise FileNotFoundError(f"Input file not found: {source}")
        elif input_type == 'udp':
            # Parse UDP parameters
            if ':' in source:
                host, port = source.split(':', 1)
                cmd.extend(['--local-address', host, '--local-port', port])
        elif input_type == 'tcp':
            if ':' in source:
                host, port = source.split(':', 1)
                cmd.extend(['--server', host, '--port', port])
        elif input_type == 'http':
            cmd.extend(['--url', source])
        elif input_type == 'hls':
            cmd.extend(['--url', source])
        elif input_type == 'srt':
            if ':' in source:
                host, port = source.split(':', 1)
                cmd.extend(['--local-address', host, '--local-port', port])
        elif input_type == 'rist':
            cmd.extend(['--url', source])
        elif input_type in ['dvb-t', 'dvb-s', 'dvb-c']:
            cmd = ['-I', 'dvb']
            if input_type == 'dvb-t':
                cmd.extend(['--tuner', source])
            elif input_type == 'dvb-s':
                cmd.extend(['--satellite', source])
            elif input_type == 'dvb-c':
                cmd.extend(['--cable', source])
        elif input_type == 'atsc':
            cmd.extend(['--tuner', source])
        elif input_type == 'isdb':
            cmd.extend(['--tuner', source])
        elif input_type == 'asi':
            cmd.extend(['--device', source])
        elif input_type == 'dektec':
            cmd.extend(['--device', source])
        elif input_type == 'hides':
            cmd.extend(['--device', source])
        elif input_type == 'vatek':
            cmd.extend(['--device', source])
            
        # Add additional parameters
        if params:
            cmd.extend(params.split())
            
        return cmd
    
    @staticmethod
    def build_output_command(config: Dict[str, str]) -> List[str]:
        """Build output command from configuration"""
        output_type = config.get('type', 'file').lower()
        destination = config.get('source', '')
        params = config.get('params', '')
        
        if not destination:
            raise ValueError("Output destination is required")
            
        cmd = ['-O', output_type, destination]
        
        # Add specific parameters based on output type
        if output_type == 'file':
            # Ensure output directory exists
            output_dir = os.path.dirname(destination)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
        elif output_type == 'udp':
            if ':' in destination:
                host, port = destination.split(':', 1)
                cmd.extend(['--remote-address', host, '--remote-port', port])
        elif output_type == 'tcp':
            if ':' in destination:
                host, port = destination.split(':', 1)
                cmd.extend(['--server', host, '--port', port])
        elif output_type == 'http':
            cmd.extend(['--url', destination])
        elif output_type == 'hls':
            cmd.extend(['--url', destination])
        elif output_type == 'srt':
            if ':' in destination:
                host, port = destination.split(':', 1)
                cmd.extend(['--remote-address', host, '--remote-port', port])
        elif output_type == 'rist':
            cmd.extend(['--url', destination])
        elif output_type == 'asi':
            cmd.extend(['--device', destination])
        elif output_type == 'dektec':
            cmd.extend(['--device', destination])
        elif output_type == 'hides':
            cmd.extend(['--device', destination])
        elif output_type == 'vatek':
            cmd.extend(['--device', destination])
            
        # Add additional parameters
        if params:
            cmd.extend(params.split())
            
        return cmd
    
    @staticmethod
    def build_plugin_commands(plugins: Dict[str, Dict[str, Any]]) -> List[str]:
        """Build plugin commands from configuration"""
        commands = []
        
        for plugin_name, config in plugins.items():
            if config.get('enabled', False):
                commands.extend(['-P', plugin_name])
                params = config.get('params', '')
                if params:
                    commands.extend(params.split())
                    
        return commands
    
    @classmethod
    def build_full_command(cls, input_config: Dict[str, str], 
                          output_config: Dict[str, str],
                          plugins: Dict[str, Dict[str, Any]],
                          tsp_options: Dict[str, Any] = None) -> List[str]:
        """Build complete TSDuck command"""
        if tsp_options is None:
            tsp_options = {}
            
        cmd = ['tsp']
        
        # Add TSP options
        if tsp_options.get('buffer_size'):
            cmd.extend(['--buffer-size', str(tsp_options['buffer_size'])])
        if tsp_options.get('max_flushed_packets'):
            cmd.extend(['--max-flushed-packets', str(tsp_options['max_flushed_packets'])])
        if tsp_options.get('max_input_packets'):
            cmd.extend(['--max-input-packets', str(tsp_options['max_input_packets'])])
        if tsp_options.get('max_output_packets'):
            cmd.extend(['--max-output-packets', str(tsp_options['max_output_packets'])])
        if tsp_options.get('realtime'):
            cmd.append('--realtime')
        if tsp_options.get('monitor'):
            cmd.append('--monitor')
            
        # Add input
        cmd.extend(cls.build_input_command(input_config))
        
        # Add plugins
        cmd.extend(cls.build_plugin_commands(plugins))
        
        # Add output
        cmd.extend(cls.build_output_command(output_config))
        
        return cmd


class SCTE35Manager:
    """Manage SCTE-35 splice information"""
    
    def __init__(self):
        self.splice_events = []
        self.monitoring = False
        
    def create_splice_insert(self, event_id: int, splice_time: str = None,
                           duration: str = None, out_of_network: bool = False,
                           immediate: bool = False, unique_program_id: int = 1,
                           avail_num: int = 0, avails_expected: int = 0) -> Dict[str, Any]:
        """Create a splice_insert command"""
        splice = {
            'command_type': 'splice_insert',
            'event_id': event_id,
            'unique_program_id': unique_program_id,
            'avail_num': avail_num,
            'avails_expected': avails_expected,
            'out_of_network': out_of_network,
            'immediate': immediate
        }
        
        if splice_time:
            splice['splice_time'] = splice_time
        if duration:
            splice['duration'] = duration
            
        return splice
    
    def create_time_signal(self, event_id: int, splice_time: str = None,
                          immediate: bool = False, unique_program_id: int = 1) -> Dict[str, Any]:
        """Create a time_signal command"""
        splice = {
            'command_type': 'time_signal',
            'event_id': event_id,
            'unique_program_id': unique_program_id,
            'immediate': immediate
        }
        
        if splice_time:
            splice['splice_time'] = splice_time
            
        return splice
    
    def create_bandwidth_reservation(self, event_id: int, unique_program_id: int = 1) -> Dict[str, Any]:
        """Create a bandwidth_reservation command"""
        return {
            'command_type': 'bandwidth_reservation',
            'event_id': event_id,
            'unique_program_id': unique_program_id
        }
    
    def create_private_command(self, event_id: int, private_data: bytes,
                              unique_program_id: int = 1) -> Dict[str, Any]:
        """Create a private_command"""
        return {
            'command_type': 'private_command',
            'event_id': event_id,
            'unique_program_id': unique_program_id,
            'private_data': private_data.hex()
        }
    
    def generate_spliceinject_params(self, splice_config: Dict[str, Any]) -> str:
        """Generate parameters for spliceinject plugin"""
        params = []
        
        if splice_config.get('immediate'):
            params.append('--immediate')
        if splice_config.get('out_of_network'):
            params.append('--out-of-network')
            
        params.extend([
            f"--event-id {splice_config['event_id']}",
            f"--unique-program-id {splice_config['unique_program_id']}"
        ])
        
        if 'splice_time' in splice_config:
            params.append(f"--splice-time {splice_config['splice_time']}")
        if 'duration' in splice_config:
            params.append(f"--duration {splice_config['duration']}")
        if 'avail_num' in splice_config:
            params.append(f"--avail-num {splice_config['avail_num']}")
        if 'avails_expected' in splice_config:
            params.append(f"--avails-expected {splice_config['avails_expected']}")
            
        return ' '.join(params)


class StreamAnalyzer:
    """Analyze transport stream statistics"""
    
    def __init__(self):
        self.stats = {
            'bitrate': 0,
            'packets_per_second': 0,
            'errors': 0,
            'pcr_accuracy': 0.0,
            'continuity_errors': 0,
            'services': [],
            'pids': {},
            'tables': {}
        }
        
    def parse_analyze_output(self, output: str) -> Dict[str, Any]:
        """Parse output from analyze plugin"""
        lines = output.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Parse different sections
            if 'Transport Stream Analysis' in line:
                current_section = 'ts'
            elif 'Services' in line:
                current_section = 'services'
            elif 'PID' in line and 'Type' in line:
                current_section = 'pids'
            elif 'Tables' in line:
                current_section = 'tables'
                
            # Parse specific values
            if 'Bitrate:' in line:
                try:
                    bitrate_str = line.split('Bitrate:')[1].strip().split()[0]
                    self.stats['bitrate'] = self._parse_bitrate(bitrate_str)
                except (IndexError, ValueError):
                    pass
            elif 'Packets/sec:' in line:
                try:
                    pps_str = line.split('Packets/sec:')[1].strip().split()[0]
                    self.stats['packets_per_second'] = int(pps_str.replace(',', ''))
                except (IndexError, ValueError):
                    pass
            elif 'Errors:' in line:
                try:
                    errors_str = line.split('Errors:')[1].strip().split()[0]
                    self.stats['errors'] = int(errors_str)
                except (IndexError, ValueError):
                    pass
            elif 'PCR accuracy:' in line:
                try:
                    accuracy_str = line.split('PCR accuracy:')[1].strip().replace('%', '')
                    self.stats['pcr_accuracy'] = float(accuracy_str)
                except (IndexError, ValueError):
                    pass
            elif 'Continuity errors:' in line:
                try:
                    cont_errors_str = line.split('Continuity errors:')[1].strip().split()[0]
                    self.stats['continuity_errors'] = int(cont_errors_str)
                except (IndexError, ValueError):
                    pass
                    
        return self.stats.copy()
    
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


class TSDuckPluginManager:
    """Manage TSDuck plugins and their configurations"""
    
    def __init__(self):
        self.available_plugins = self._get_available_plugins()
        
    def _get_available_plugins(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available TSDuck plugins"""
        return {
            # Input plugins
            'file': {
                'category': 'input',
                'description': 'Read from a file',
                'parameters': ['filename']
            },
            'udp': {
                'category': 'input',
                'description': 'Receive UDP packets',
                'parameters': ['--local-address', '--local-port']
            },
            'tcp': {
                'category': 'input',
                'description': 'Receive TCP connection',
                'parameters': ['--server', '--port']
            },
            'http': {
                'category': 'input',
                'description': 'Receive HTTP stream',
                'parameters': ['--url']
            },
            'hls': {
                'category': 'input',
                'description': 'Receive HLS stream',
                'parameters': ['--url']
            },
            'srt': {
                'category': 'input',
                'description': 'Receive SRT stream',
                'parameters': ['--local-address', '--local-port']
            },
            'rist': {
                'category': 'input',
                'description': 'Receive RIST stream',
                'parameters': ['--url']
            },
            'dvb': {
                'category': 'input',
                'description': 'Receive from DVB tuner',
                'parameters': ['--tuner', '--satellite', '--cable']
            },
            'atsc': {
                'category': 'input',
                'description': 'Receive from ATSC tuner',
                'parameters': ['--tuner']
            },
            'isdb': {
                'category': 'input',
                'description': 'Receive from ISDB tuner',
                'parameters': ['--tuner']
            },
            'asi': {
                'category': 'input',
                'description': 'Receive from ASI interface',
                'parameters': ['--device']
            },
            'dektec': {
                'category': 'input',
                'description': 'Receive from Dektec device',
                'parameters': ['--device']
            },
            'hides': {
                'category': 'input',
                'description': 'Receive from HiDes device',
                'parameters': ['--device']
            },
            'vatek': {
                'category': 'input',
                'description': 'Receive from VATek device',
                'parameters': ['--device']
            },
            
            # Output plugins
            'file': {
                'category': 'output',
                'description': 'Write to a file',
                'parameters': ['filename']
            },
            'udp': {
                'category': 'output',
                'description': 'Send UDP packets',
                'parameters': ['--remote-address', '--remote-port']
            },
            'tcp': {
                'category': 'output',
                'description': 'Send TCP connection',
                'parameters': ['--server', '--port']
            },
            'http': {
                'category': 'output',
                'description': 'Send HTTP stream',
                'parameters': ['--url']
            },
            'hls': {
                'category': 'output',
                'description': 'Send HLS stream',
                'parameters': ['--url']
            },
            'srt': {
                'category': 'output',
                'description': 'Send SRT stream',
                'parameters': ['--remote-address', '--remote-port']
            },
            'rist': {
                'category': 'output',
                'description': 'Send RIST stream',
                'parameters': ['--url']
            },
            'asi': {
                'category': 'output',
                'description': 'Send to ASI interface',
                'parameters': ['--device']
            },
            'dektec': {
                'category': 'output',
                'description': 'Send to Dektec device',
                'parameters': ['--device']
            },
            'hides': {
                'category': 'output',
                'description': 'Send to HiDes device',
                'parameters': ['--device']
            },
            'vatek': {
                'category': 'output',
                'description': 'Send to VATek device',
                'parameters': ['--device']
            },
            
            # Processing plugins
            'analyze': {
                'category': 'processing',
                'description': 'Analyze transport stream',
                'parameters': ['--pid', '--service', '--all-streams']
            },
            'bitrate_monitor': {
                'category': 'processing',
                'description': 'Monitor bitrate',
                'parameters': ['--pid', '--window-size', '--alarm']
            },
            'continuity': {
                'category': 'processing',
                'description': 'Check continuity counters',
                'parameters': ['--fix', '--pid']
            },
            'count': {
                'category': 'processing',
                'description': 'Count packets',
                'parameters': ['--pid', '--service', '--interval']
            },
            'dump': {
                'category': 'processing',
                'description': 'Dump packet content',
                'parameters': ['--pid', '--service', '--format']
            },
            'filter': {
                'category': 'processing',
                'description': 'Filter packets',
                'parameters': ['--pid', '--service', '--negate']
            },
            'inject': {
                'category': 'processing',
                'description': 'Inject sections',
                'parameters': ['--pid', '--file', '--replace']
            },
            'limit': {
                'category': 'processing',
                'description': 'Limit bitrate',
                'parameters': ['--bitrate', '--pid']
            },
            'merge': {
                'category': 'processing',
                'description': 'Merge streams',
                'parameters': ['--input', '--pid-offset']
            },
            'mux': {
                'category': 'processing',
                'description': 'Multiplex services',
                'parameters': ['--service', '--pid']
            },
            'pat': {
                'category': 'processing',
                'description': 'Manipulate PAT',
                'parameters': ['--add-service', '--remove-service']
            },
            'pmt': {
                'category': 'processing',
                'description': 'Manipulate PMT',
                'parameters': ['--service', '--add-pid', '--remove-pid']
            },
            'regulate': {
                'category': 'processing',
                'description': 'Regulate output',
                'parameters': ['--bitrate', '--pcr-based']
            },
            'remap': {
                'category': 'processing',
                'description': 'Remap PIDs',
                'parameters': ['--pid', '--new-pid']
            },
            'spliceinject': {
                'category': 'processing',
                'description': 'Inject SCTE-35 splices',
                'parameters': ['--event-id', '--splice-time', '--duration']
            },
            'splicemonitor': {
                'category': 'processing',
                'description': 'Monitor SCTE-35 splices',
                'parameters': ['--pid', '--json', '--xml']
            },
            'rmsplice': {
                'category': 'processing',
                'description': 'Remove SCTE-35 splices',
                'parameters': ['--pid', '--all']
            },
            'stats': {
                'category': 'processing',
                'description': 'Display statistics',
                'parameters': ['--pid', '--service', '--interval']
            },
            'stuffanalyze': {
                'category': 'processing',
                'description': 'Analyze stuffing',
                'parameters': ['--pid', '--service']
            },
            'svremove': {
                'category': 'processing',
                'description': 'Remove services',
                'parameters': ['--service', '--all']
            },
            'svrename': {
                'category': 'processing',
                'description': 'Rename services',
                'parameters': ['--service', '--new-name']
            },
            'svresync': {
                'category': 'processing',
                'description': 'Resync services',
                'parameters': ['--service', '--pid']
            },
            'teletext': {
                'category': 'processing',
                'description': 'Extract Teletext',
                'parameters': ['--pid', '--service', '--extract']
            },
            'time': {
                'category': 'processing',
                'description': 'Add time info',
                'parameters': ['--pid', '--service', '--utc']
            },
            'tstables': {
                'category': 'processing',
                'description': 'Manipulate tables',
                'parameters': ['--pid', '--service', '--add', '--remove']
            }
        }
    
    def get_plugin_info(self, plugin_name: str) -> Dict[str, Any]:
        """Get information about a specific plugin"""
        return self.available_plugins.get(plugin_name, {})
    
    def get_plugins_by_category(self, category: str) -> List[str]:
        """Get plugins by category"""
        return [name for name, info in self.available_plugins.items() 
                if info.get('category') == category]


class ConfigurationManager:
    """Manage application configuration"""
    
    def __init__(self, config_file: str = "tsduck_gui_config.json"):
        self.config_file = config_file
        self.config = self._load_default_config()
        self.load_config()
        
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            'input': {
                'type': 'file',
                'source': '',
                'params': ''
            },
            'output': {
                'type': 'file',
                'source': '',
                'params': ''
            },
            'tsp_options': {
                'buffer_size': 1000000,
                'max_flushed_packets': 1000,
                'max_input_packets': 1000,
                'max_output_packets': 1000,
                'realtime': False,
                'monitor': False
            },
            'plugins': {},
            'scte35': {
                'monitoring': False,
                'injection': False,
                'events': []
            },
            'ui': {
                'theme': 'dark',
                'window_geometry': None,
                'splitter_state': None
            }
        }
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self._merge_config(self.config, loaded_config)
            except Exception as e:
                print(f"Error loading configuration: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def _merge_config(self, base: Dict[str, Any], update: Dict[str, Any]):
        """Merge configuration dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value


# Example usage and testing
if __name__ == "__main__":
    # Test command builder
    input_config = {
        'type': 'file',
        'source': '/path/to/input.ts',
        'params': ''
    }
    
    output_config = {
        'type': 'file',
        'source': '/path/to/output.ts',
        'params': ''
    }
    
    plugins = {
        'analyze': {'enabled': True, 'params': '--pid 0x100'},
        'spliceinject': {'enabled': True, 'params': '--event-id 1 --immediate'}
    }
    
    command = TSDuckCommandBuilder.build_full_command(input_config, output_config, plugins)
    print("Generated command:", ' '.join(command))
    
    # Test SCTE-35 manager
    scte35 = SCTE35Manager()
    splice = scte35.create_splice_insert(
        event_id=1,
        immediate=True,
        out_of_network=True
    )
    params = scte35.generate_spliceinject_params(splice)
    print("SCTE-35 parameters:", params)
