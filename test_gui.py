#!/usr/bin/env python3
"""
Comprehensive GUI Test Suite for TSDuck GUI
Tests all features and functionality
"""

import sys
import os
import time
import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tsduck_gui import (
    MainWindow, SCTE35Dialog, InputOutputWidget, PluginWidget, 
    SourcePreviewWidget, TSDuckProcessor, StreamMonitor
)


class TestTSDuckGUI(unittest.TestCase):
    """Comprehensive test suite for TSDuck GUI"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test application"""
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)
    
    def setUp(self):
        """Set up for each test"""
        self.window = MainWindow()
        self.window.show()
        QTest.qWaitForWindowExposed(self.window)
    
    def tearDown(self):
        """Clean up after each test"""
        self.window.close()
    
    def test_main_window_creation(self):
        """Test main window creation and basic properties"""
        self.assertIsNotNone(self.window)
        self.assertEqual(self.window.windowTitle(), "TSDuck GUI - MPEG Transport Stream Encoder/Decoder")
        self.assertTrue(self.window.minimumSize().width() >= 1200)
        self.assertTrue(self.window.minimumSize().height() >= 800)
    
    def test_input_output_widgets(self):
        """Test input/output configuration widgets"""
        # Test input widget
        input_widget = self.window.input_widget
        self.assertIsNotNone(input_widget)
        
        # Test type selection
        input_widget.type_combo.setCurrentText("File")
        self.assertEqual(input_widget.type_combo.currentText(), "File")
        
        # Test source input
        test_source = "/path/to/test.ts"
        input_widget.source_edit.setText(test_source)
        self.assertEqual(input_widget.source_edit.text(), test_source)
        
        # Test parameters
        test_params = "--buffer-size 1000000"
        input_widget.params_edit.setText(test_params)
        self.assertEqual(input_widget.params_edit.text(), test_params)
        
        # Test output widget
        output_widget = self.window.output_widget
        self.assertIsNotNone(output_widget)
        
        # Test configuration retrieval
        config = input_widget.get_config()
        self.assertEqual(config['type'], "File")
        self.assertEqual(config['source'], test_source)
        self.assertEqual(config['params'], test_params)
    
    def test_plugin_widgets(self):
        """Test plugin configuration widgets"""
        # Test analysis plugins
        analysis_plugins = self.window.analysis_plugins
        self.assertGreater(len(analysis_plugins), 0)
        
        # Test enabling a plugin
        analyze_plugin = analysis_plugins[0]  # analyze plugin
        analyze_plugin.enabled.setChecked(True)
        analyze_plugin.params_edit.setText("--pid 0x100")
        
        config = analyze_plugin.get_config()
        self.assertTrue(config['enabled'])
        self.assertEqual(config['params'], "--pid 0x100")
        
        # Test processing plugins
        processing_plugins = self.window.processing_plugins
        self.assertGreater(len(processing_plugins), 0)
        
        # Test SCTE-35 plugins
        scte35_plugins = self.window.scte35_plugins
        self.assertGreater(len(scte35_plugins), 0)
        
        # Test tables plugins
        tables_plugins = self.window.tables_plugins
        self.assertGreater(len(tables_plugins), 0)
        
        # Test services plugins
        services_plugins = self.window.services_plugins
        self.assertGreater(len(services_plugins), 0)
    
    def test_scte35_dialog(self):
        """Test SCTE-35 configuration dialog"""
        dialog = SCTE35Dialog(self.window)
        self.assertIsNotNone(dialog)
        
        # Test dialog properties
        self.assertEqual(dialog.windowTitle(), "SCTE-35 Splice Configuration")
        
        # Test splice type selection
        dialog.splice_type.setCurrentText("splice_insert")
        self.assertEqual(dialog.splice_type.currentText(), "splice_insert")
        
        # Test event ID
        dialog.event_id.setValue(123)
        self.assertEqual(dialog.event_id.value(), 123)
        
        # Test immediate checkbox
        dialog.immediate.setChecked(True)
        self.assertTrue(dialog.immediate.isChecked())
        
        # Test out of network checkbox
        dialog.out_of_network.setChecked(True)
        self.assertTrue(dialog.out_of_network.isChecked())
        
        # Test configuration retrieval
        config = dialog.get_config()
        self.assertEqual(config['splice_type'], "splice_insert")
        self.assertEqual(config['event_id'], 123)
        self.assertTrue(config['immediate'])
        self.assertTrue(config['out_of_network'])
        
        dialog.close()
    
    def test_source_preview_widget(self):
        """Test source preview functionality"""
        preview_widget = self.window.source_preview
        self.assertIsNotNone(preview_widget)
        
        # Test preview controls
        self.assertIsNotNone(preview_widget.preview_btn)
        self.assertIsNotNone(preview_widget.stop_preview_btn)
        self.assertIsNotNone(preview_widget.refresh_btn)
        
        # Test preview tabs
        self.assertIsNotNone(preview_widget.preview_tabs)
        self.assertEqual(preview_widget.preview_tabs.count(), 4)  # Stream Info, Services, PIDs, Tables
        
        # Test setting input configuration
        test_config = {
            'type': 'file',
            'source': '/path/to/test.ts',
            'params': ''
        }
        preview_widget.set_input_config(test_config)
        self.assertEqual(preview_widget.input_config, test_config)
        
        # Test preview data population
        preview_widget.populate_preview_data()
        
        # Check that data was populated
        self.assertGreater(len(preview_widget.stream_info_text.toPlainText()), 0)
        self.assertGreater(preview_widget.services_table.rowCount(), 0)
        self.assertGreater(preview_widget.pids_table.rowCount(), 0)
        self.assertGreater(preview_widget.tables_tree.topLevelItemCount(), 0)
    
    def test_configuration_management(self):
        """Test configuration save/load functionality"""
        # Set up test configuration
        self.window.input_widget.type_combo.setCurrentText("UDP")
        self.window.input_widget.source_edit.setText("239.1.1.1:1234")
        self.window.input_widget.params_edit.setText("--local-address 0.0.0.0")
        
        self.window.output_widget.type_combo.setCurrentText("File")
        self.window.output_widget.source_edit.setText("/path/to/output.ts")
        
        # Enable some plugins
        self.window.analysis_plugins[0].enabled.setChecked(True)
        self.window.analysis_plugins[0].params_edit.setText("--all-streams")
        
        # Get configuration
        config = self.window.get_configuration()
        
        # Verify configuration structure
        self.assertIn('input', config)
        self.assertIn('output', config)
        self.assertIn('plugins', config)
        
        # Verify input configuration
        self.assertEqual(config['input']['type'], "UDP")
        self.assertEqual(config['input']['source'], "239.1.1.1:1234")
        self.assertEqual(config['input']['params'], "--local-address 0.0.0.0")
        
        # Verify output configuration
        self.assertEqual(config['output']['type'], "File")
        self.assertEqual(config['output']['source'], "/path/to/output.ts")
        
        # Verify plugins configuration
        self.assertIn('analyze', config['plugins'])
        self.assertTrue(config['plugins']['analyze']['enabled'])
        self.assertEqual(config['plugins']['analyze']['params'], "--all-streams")
    
    def test_command_building(self):
        """Test TSDuck command building"""
        # Set up test configuration
        self.window.input_widget.type_combo.setCurrentText("File")
        self.window.input_widget.source_edit.setText("/path/to/input.ts")
        
        self.window.output_widget.type_combo.setCurrentText("File")
        self.window.output_widget.source_edit.setText("/path/to/output.ts")
        
        # Enable some plugins
        self.window.analysis_plugins[0].enabled.setChecked(True)
        self.window.analysis_plugins[0].params_edit.setText("--pid 0x100")
        
        # Mock file existence for validation
        with patch('os.path.exists', return_value=True):
            # Build command
            command = self.window.build_tsduck_command()
            
            # Verify command structure
            self.assertIsInstance(command, list)
            self.assertGreater(len(command), 0)
            self.assertEqual(command[0], 'tsp')
            
            # Verify input
            self.assertIn('-I', command)
            self.assertIn('file', command)
            self.assertIn('/path/to/input.ts', command)
            
            # Verify plugins
            self.assertIn('-P', command)
            self.assertIn('analyze', command)
            self.assertIn('--pid', command)
            self.assertIn('0x100', command)
            
            # Verify output
            self.assertIn('-O', command)
            self.assertIn('/path/to/output.ts', command)
    
    def test_scte35_integration(self):
        """Test SCTE-35 integration with plugins"""
        # Configure SCTE-35
        dialog = SCTE35Dialog(self.window)
        dialog.splice_type.setCurrentText("splice_insert")
        dialog.event_id.setValue(1)
        dialog.immediate.setChecked(True)
        dialog.out_of_network.setChecked(True)
        dialog.unique_program_id.setValue(1)
        dialog.avail_num.setValue(1)
        dialog.avails_expected.setValue(1)
        
        config = dialog.get_config()
        
        # Apply configuration
        self.window.configure_scte35()
        
        # Check that spliceinject plugin was configured
        spliceinject_plugin = None
        for plugin in self.window.scte35_plugins:
            if plugin.plugin_name == 'spliceinject':
                spliceinject_plugin = plugin
                break
        
        self.assertIsNotNone(spliceinject_plugin)
        self.assertTrue(spliceinject_plugin.enabled.isChecked())
        
        # Check that parameters were set
        params = spliceinject_plugin.params_edit.text()
        # Note: The configure_scte35 method applies the dialog config, so we need to check what was actually set
        self.assertIn('--event-id 1', params)
        self.assertIn('--unique-program-id 1', params)
        # The immediate and out-of-network flags are only added if the dialog was accepted
        # For this test, we're just checking that the method exists and can be called
        
        dialog.close()
    
    def test_error_handling(self):
        """Test error handling scenarios"""
        # Test empty input source
        self.window.input_widget.source_edit.clear()
        self.window.output_widget.source_edit.setText("/path/to/output.ts")
        
        command = self.window.build_tsduck_command()
        self.assertEqual(command, [])  # Should return empty list for invalid config
        
        # Test empty output destination
        self.window.input_widget.source_edit.setText("/path/to/input.ts")
        self.window.output_widget.source_edit.clear()
        
        command = self.window.build_tsduck_command()
        self.assertEqual(command, [])  # Should return empty list for invalid config
    
    def test_ui_responsiveness(self):
        """Test UI responsiveness and threading"""
        # Test that UI remains responsive during operations
        start_time = time.time()
        
        # Simulate some UI operations
        self.window.input_widget.type_combo.setCurrentText("UDP")
        self.window.input_widget.source_edit.setText("239.1.1.1:1234")
        
        # Enable multiple plugins
        for plugin in self.window.analysis_plugins[:3]:
            plugin.enabled.setChecked(True)
            plugin.params_edit.setText("--test")
        
        # Test configuration retrieval
        config = self.window.get_configuration()
        
        end_time = time.time()
        operation_time = end_time - start_time
        
        # Operations should complete quickly (less than 1 second)
        self.assertLess(operation_time, 1.0)
    
    def test_menu_functionality(self):
        """Test menu functionality"""
        # Test that menus exist
        menubar = self.window.menuBar()
        self.assertIsNotNone(menubar)
        
        # Test that menu bar has actions
        actions = menubar.actions()
        self.assertGreater(len(actions), 0)
        
        # Test that we can find menus by title
        menu_titles = [action.text() for action in actions if action.menu()]
        self.assertIn("File", menu_titles)
        self.assertIn("Tools", menu_titles)
        self.assertIn("Help", menu_titles)
    
    def test_status_bar(self):
        """Test status bar functionality"""
        status_bar = self.window.status_bar
        self.assertIsNotNone(status_bar)
        
        # Test initial status
        self.assertEqual(status_bar.currentMessage(), "Ready")
    
    def test_about_dialog(self):
        """Test about dialog"""
        # This would normally show a dialog, but we can test the method exists
        self.assertTrue(hasattr(self.window, 'show_about'))
        self.assertTrue(callable(self.window.show_about))


class TestTSDuckProcessor(unittest.TestCase):
    """Test TSDuck processor functionality"""
    
    def test_processor_creation(self):
        """Test processor creation"""
        command = ['tsp', '--help']
        processor = TSDuckProcessor(command)
        self.assertIsNotNone(processor)
        self.assertEqual(processor.command, command)
    
    def test_processor_stop(self):
        """Test processor stop functionality"""
        command = ['tsp', '--help']
        processor = TSDuckProcessor(command)
        processor.stop()  # Should not raise an exception


class TestStreamMonitor(unittest.TestCase):
    """Test stream monitor functionality"""
    
    def test_monitor_creation(self):
        """Test monitor creation"""
        monitor = StreamMonitor()
        self.assertIsNotNone(monitor)
    
    def test_monitor_stop(self):
        """Test monitor stop functionality"""
        monitor = StreamMonitor()
        monitor.stop()  # Should not raise an exception


def run_gui_tests():
    """Run all GUI tests"""
    print("Starting TSDuck GUI Test Suite...")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestTSDuckGUI))
    test_suite.addTest(unittest.makeSuite(TestTSDuckProcessor))
    test_suite.addTest(unittest.makeSuite(TestStreamMonitor))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_gui_tests()
    sys.exit(0 if success else 1)
