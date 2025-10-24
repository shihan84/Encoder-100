#!/usr/bin/env python3
"""
Tests for TSDuck backend functionality
"""

import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tsduck_backend import (
    TSDuckCommandBuilder, SCTE35Manager, StreamAnalyzer, 
    TSDuckPluginManager, ConfigurationManager
)


class TestTSDuckCommandBuilder(unittest.TestCase):
    """Test TSDuck command builder"""
    
    def test_build_input_command_file(self):
        """Test building input command for file"""
        config = {
            'type': 'file',
            'source': '/path/to/input.ts',
            'params': ''
        }
        
        with patch('os.path.exists', return_value=True):
            command = TSDuckCommandBuilder.build_input_command(config)
            expected = ['-I', 'file', '/path/to/input.ts']
            self.assertEqual(command, expected)
    
    def test_build_input_command_udp(self):
        """Test building input command for UDP"""
        config = {
            'type': 'udp',
            'source': '239.1.1.1:1234',
            'params': ''
        }
        
        command = TSDuckCommandBuilder.build_input_command(config)
        expected = ['-I', 'udp', '239.1.1.1:1234']
        self.assertEqual(command, expected)
    
    def test_build_output_command_file(self):
        """Test building output command for file"""
        config = {
            'type': 'file',
            'source': '/path/to/output.ts',
            'params': ''
        }
        
        with patch('os.makedirs'):
            command = TSDuckCommandBuilder.build_output_command(config)
            expected = ['-O', 'file', '/path/to/output.ts']
            self.assertEqual(command, expected)
    
    def test_build_plugin_commands(self):
        """Test building plugin commands"""
        plugins = {
            'analyze': {'enabled': True, 'params': '--pid 0x100'},
            'stats': {'enabled': False, 'params': ''},
            'spliceinject': {'enabled': True, 'params': '--event-id 1'}
        }
        
        command = TSDuckCommandBuilder.build_plugin_commands(plugins)
        expected = ['-P', 'analyze', '--pid', '0x100', '-P', 'spliceinject', '--event-id', '1']
        self.assertEqual(command, expected)
    
    def test_build_full_command(self):
        """Test building full command"""
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
            'analyze': {'enabled': True, 'params': '--pid 0x100'}
        }
        
        tsp_options = {
            'buffer_size': 1000000,
            'realtime': True
        }
        
        with patch('os.path.exists', return_value=True), patch('os.makedirs'):
            command = TSDuckCommandBuilder.build_full_command(
                input_config, output_config, plugins, tsp_options
            )
            
            expected_start = ['tsp', '--buffer-size', '1000000', '--realtime']
            self.assertTrue(command[:len(expected_start)] == expected_start)
            self.assertIn('-I', command)
            self.assertIn('file', command)
            self.assertIn('/path/to/input.ts', command)
            self.assertIn('-P', command)
            self.assertIn('analyze', command)
            self.assertIn('-O', command)
            self.assertIn('/path/to/output.ts', command)


class TestSCTE35Manager(unittest.TestCase):
    """Test SCTE-35 manager"""
    
    def setUp(self):
        self.manager = SCTE35Manager()
    
    def test_create_splice_insert(self):
        """Test creating splice_insert command"""
        splice = self.manager.create_splice_insert(
            event_id=1,
            immediate=True,
            out_of_network=True
        )
        
        self.assertEqual(splice['command_type'], 'splice_insert')
        self.assertEqual(splice['event_id'], 1)
        self.assertTrue(splice['immediate'])
        self.assertTrue(splice['out_of_network'])
    
    def test_create_time_signal(self):
        """Test creating time_signal command"""
        splice = self.manager.create_time_signal(
            event_id=2,
            splice_time='2024-01-01 12:00:00.000'
        )
        
        self.assertEqual(splice['command_type'], 'time_signal')
        self.assertEqual(splice['event_id'], 2)
        self.assertEqual(splice['splice_time'], '2024-01-01 12:00:00.000')
    
    def test_generate_spliceinject_params(self):
        """Test generating spliceinject parameters"""
        config = {
            'event_id': 1,
            'immediate': True,
            'out_of_network': True,
            'unique_program_id': 1,
            'splice_time': '2024-01-01 12:00:00.000',
            'duration': '00:00:30.000'
        }
        
        params = self.manager.generate_spliceinject_params(config)
        
        self.assertIn('--immediate', params)
        self.assertIn('--out-of-network', params)
        self.assertIn('--event-id 1', params)
        self.assertIn('--unique-program-id 1', params)
        self.assertIn('--splice-time 2024-01-01 12:00:00.000', params)
        self.assertIn('--duration 00:00:30.000', params)


class TestStreamAnalyzer(unittest.TestCase):
    """Test stream analyzer"""
    
    def setUp(self):
        self.analyzer = StreamAnalyzer()
    
    def test_parse_analyze_output(self):
        """Test parsing analyze output"""
        output = """
Transport Stream Analysis
Bitrate: 15.2 Mbps
Packets/sec: 25,000
Errors: 0
PCR accuracy: 99.9%
Continuity errors: 0
        """
        
        stats = self.analyzer.parse_analyze_output(output)
        
        self.assertEqual(stats['bitrate'], 15200000)  # 15.2 Mbps
        self.assertEqual(stats['packets_per_second'], 25000)
        self.assertEqual(stats['errors'], 0)
        self.assertEqual(stats['pcr_accuracy'], 99.9)
        self.assertEqual(stats['continuity_errors'], 0)
    
    def test_parse_bitrate(self):
        """Test parsing bitrate strings"""
        self.assertEqual(self.analyzer._parse_bitrate('15.2 Mbps'), 15200000)
        self.assertEqual(self.analyzer._parse_bitrate('1.5 KBPS'), 1500)
        self.assertEqual(self.analyzer._parse_bitrate('2.0 GBPS'), 2000000000)
        self.assertEqual(self.analyzer._parse_bitrate('1000000'), 1000000)


class TestTSDuckPluginManager(unittest.TestCase):
    """Test TSDuck plugin manager"""
    
    def setUp(self):
        self.manager = TSDuckPluginManager()
    
    def test_get_available_plugins(self):
        """Test getting available plugins"""
        plugins = self.manager.available_plugins
        
        self.assertIn('analyze', plugins)
        self.assertIn('spliceinject', plugins)
        self.assertIn('file', plugins)
        
        # Check plugin structure
        analyze_plugin = plugins['analyze']
        self.assertEqual(analyze_plugin['category'], 'processing')
        self.assertIn('description', analyze_plugin)
        self.assertIn('parameters', analyze_plugin)
    
    def test_get_plugins_by_category(self):
        """Test getting plugins by category"""
        input_plugins = self.manager.get_plugins_by_category('input')
        self.assertIn('file', input_plugins)
        self.assertIn('udp', input_plugins)
        
        processing_plugins = self.manager.get_plugins_by_category('processing')
        self.assertIn('analyze', processing_plugins)
        self.assertIn('spliceinject', processing_plugins)


class TestConfigurationManager(unittest.TestCase):
    """Test configuration manager"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.manager = ConfigurationManager(self.temp_file.name)
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_default_config(self):
        """Test default configuration"""
        config = self.manager.config
        
        self.assertIn('input', config)
        self.assertIn('output', config)
        self.assertIn('plugins', config)
        self.assertIn('scte35', config)
        self.assertIn('ui', config)
    
    def test_get_set_config(self):
        """Test getting and setting configuration values"""
        # Test get
        self.assertEqual(self.manager.get('input.type'), 'file')
        self.assertIsNone(self.manager.get('nonexistent.key'))
        self.assertEqual(self.manager.get('nonexistent.key', 'default'), 'default')
        
        # Test set
        self.manager.set('input.type', 'udp')
        self.assertEqual(self.manager.get('input.type'), 'udp')
        
        self.manager.set('new.nested.key', 'value')
        self.assertEqual(self.manager.get('new.nested.key'), 'value')
    
    def test_save_load_config(self):
        """Test saving and loading configuration"""
        # Modify configuration
        self.manager.set('input.type', 'udp')
        self.manager.set('input.source', '239.1.1.1:1234')
        
        # Save configuration
        self.manager.save_config()
        
        # Create new manager and load configuration
        new_manager = ConfigurationManager(self.temp_file.name)
        new_manager.load_config()
        
        # Verify configuration was loaded
        self.assertEqual(new_manager.get('input.type'), 'udp')
        self.assertEqual(new_manager.get('input.source'), '239.1.1.1:1234')


if __name__ == '__main__':
    unittest.main()
