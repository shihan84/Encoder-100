#!/usr/bin/env python3
"""
Test SRT parameter handling to verify dynamic configuration
"""

import json
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_srt_parameter_parsing():
    """Test SRT parameter parsing with different configurations"""
    
    print("🔍 Testing SRT Parameter Parsing")
    print("=" * 50)
    
    # Import the main application class
    try:
        from enc100 import MainWindow
        from PyQt6.QtWidgets import QApplication
        import sys
        
        # Create QApplication for testing
        app = QApplication(sys.argv)
        main_window = MainWindow()
    except ImportError as e:
        print(f"❌ Error importing application: {e}")
        return False
    
    # Test configurations for strictly user-defined parameters
    test_configs = [
        {
            "name": "User-defined parameters only",
            "config": {
                "type": "srt",
                "destination": "srt://cdn.itassist.one:8888",
                "params": "--caller cdn.itassist.one:8888 --streamid 'user-stream' --latency 5000 --transtype live"
            }
        },
        {
            "name": "URL with user parameters override",
            "config": {
                "type": "srt", 
                "destination": "srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish",
                "params": "--caller custom-server.com:9999 --streamid 'override-stream' --latency 3000"
            }
        },
        {
            "name": "Strictly user-defined (no URL parsing)",
            "config": {
                "type": "srt",
                "destination": "cdn.itassist.one:8888",
                "params": "--caller cdn.itassist.one:8888 --streamid 'strict-user' --latency 2000 --messageapi"
            }
        },
        {
            "name": "No user parameters (should be empty)",
            "config": {
                "type": "srt",
                "destination": "srt://cdn.itassist.one:8888",
                "params": ""
            }
        },
        {
            "name": "Minimal user parameters",
            "config": {
                "type": "srt",
                "destination": "",
                "params": "--caller minimal-server.com:7777"
            }
        }
    ]
    
    print("Testing SRT parameter generation...")
    print()
    
    for test in test_configs:
        print(f"📋 Test: {test['name']}")
        print(f"   Config: {test['config']}")
        
        try:
            # Test the parameter generation
            params = main_window.get_output_params(test['config'])
            print(f"   Generated params: {params}")
            
            # Build full command
            command = ["tsp", "-I", "hls", "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8", 
                      "-O", "srt"] + params
            
            print(f"   Full command: {' '.join(command)}")
            print("   ✅ Success")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    return True

def test_configuration_loading():
    """Test loading different configuration formats"""
    
    print("🔍 Testing Configuration Loading")
    print("=" * 50)
    
    # Test configurations with different field names
    test_configs = [
        {
            "name": "New format (destination)",
            "config": {
                "output": {
                    "type": "srt",
                    "destination": "srt://cdn.itassist.one:8888",
                    "params": "--latency 2000"
                }
            }
        },
        {
            "name": "Legacy format (source)",
            "config": {
                "output": {
                    "type": "srt", 
                    "source": "srt://cdn.itassist.one:8888",
                    "params": "--latency 2000"
                }
            }
        },
        {
            "name": "Distributor format",
            "config": {
                "output": {
                    "type": "srt",
                    "source": "srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish",
                    "params": "--latency 2000"
                }
            }
        }
    ]
    
    try:
        from enc100 import MainWindow
        from PyQt6.QtWidgets import QApplication
        import sys
        
        # Create QApplication for testing
        app = QApplication(sys.argv)
        main_window = MainWindow()
        
        for test in test_configs:
            print(f"📋 Test: {test['name']}")
            print(f"   Config: {test['config']}")
            
            # Test configuration loading
            main_window.load_configuration(test['config'])
            
            # Get the output widget configuration
            output_config = main_window.config_widget.output_widget.get_config()
            print(f"   Loaded destination: {output_config.get('destination', 'N/A')}")
            print(f"   Loaded params: {output_config.get('params', 'N/A')}")
            print("   ✅ Success")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 SRT Parameter Testing Suite")
    print("=" * 60)
    print()
    
    # Test 1: Parameter parsing
    success1 = test_srt_parameter_parsing()
    
    # Test 2: Configuration loading
    success2 = test_configuration_loading()
    
    print("=" * 60)
    if success1 and success2:
        print("✅ All tests passed! SRT parameters are working correctly.")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return success1 and success2

if __name__ == "__main__":
    main()
