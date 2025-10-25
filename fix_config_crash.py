#!/usr/bin/env python3
"""
Fix for IBE-100 configuration loading crash
This script creates a safe configuration loading method
"""

import json
import os
import sys
from typing import Dict, Any, Optional

def safe_load_configuration(file_path: str) -> Optional[Dict[str, Any]]:
    """Safely load configuration from file with error handling"""
    try:
        if not os.path.exists(file_path):
            print(f"Configuration file not found: {file_path}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Validate required fields
        if not isinstance(config, dict):
            print("Configuration file is not a valid JSON object")
            return None
        
        # Ensure required sections exist
        if "input" not in config:
            config["input"] = {"type": "hls", "source": "", "params": ""}
        if "output" not in config:
            config["output"] = {"type": "srt", "source": "", "params": ""}
        if "service" not in config:
            config["service"] = {
                "service_name": "SCTE-35 Stream",
                "provider_name": "ITAssist",
                "service_id": 1,
                "vpid": 256,
                "apid": 257,
                "scte35_pid": 500,
                "null_pid": 8191,
                "pcr_pid": 256
            }
        if "scte35" not in config:
            config["scte35"] = {
                "ad_duration": 600,
                "event_id": 100023,
                "preroll_duration": 0,
                "pmt_enabled": True,
                "pmt_params": "",
                "spliceinject_enabled": True,
                "spliceinject_params": ""
            }
        
        return config
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

def create_default_config() -> Dict[str, Any]:
    """Create a default configuration"""
    return {
        "name": "Default Configuration",
        "description": "Default IBE-100 configuration",
        "input": {
            "type": "hls",
            "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8",
            "params": ""
        },
        "output": {
            "type": "srt",
            "source": "srt://cdn.itassist.one:8888",
            "params": "--caller cdn.itassist.one:8888 --latency 2000"
        },
        "service": {
            "service_name": "SCTE-35 Stream",
            "provider_name": "ITAssist",
            "service_id": 1,
            "vpid": 256,
            "apid": 257,
            "scte35_pid": 500,
            "null_pid": 8191,
            "pcr_pid": 256
        },
        "scte35": {
            "ad_duration": 600,
            "event_id": 100023,
            "preroll_duration": 0,
            "pmt_enabled": True,
            "pmt_params": "",
            "spliceinject_enabled": True,
            "spliceinject_params": ""
        }
    }

def fix_config_files():
    """Fix existing configuration files"""
    config_files = [
        "config_1_basic.json",
        "config_2_simple_streamid.json",
        "config_3_live_mode.json",
        "config_4_high_latency.json",
        "config_5_listener_mode.json",
        "config_6_udp_fallback.json",
        "config_7_tcp_fallback.json",
        "config_8_file_output.json"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"Fixing {config_file}...")
            config = safe_load_configuration(config_file)
            if config:
                # Add missing sections
                if "service" not in config:
                    config["service"] = {
                        "service_name": "SCTE-35 Stream",
                        "provider_name": "ITAssist",
                        "service_id": 1,
                        "vpid": 256,
                        "apid": 257,
                        "scte35_pid": 500,
                        "null_pid": 8191,
                        "pcr_pid": 256
                    }
                if "scte35" not in config:
                    config["scte35"] = {
                        "ad_duration": 600,
                        "event_id": 100023,
                        "preroll_duration": 0,
                        "pmt_enabled": True,
                        "pmt_params": "",
                        "spliceinject_enabled": True,
                        "spliceinject_params": ""
                    }
                
                # Save fixed configuration
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
                print(f"Fixed {config_file}")

if __name__ == "__main__":
    print("Fixing IBE-100 configuration files...")
    fix_config_files()
    print("Configuration files fixed!")
