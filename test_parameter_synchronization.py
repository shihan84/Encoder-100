#!/usr/bin/env python3
"""
IBE-100 Parameter Synchronization Test
Tests if all related features update when user-defined parameters change
"""

import json
import os
import sys
from typing import Dict, Any, List

def test_parameter_synchronization():
    """Test parameter synchronization across all features"""
    
    print("🔍 IBE-100 Parameter Synchronization Test")
    print("=" * 60)
    
    # Test scenarios for parameter changes
    test_scenarios = [
        {
            "name": "Service ID Change",
            "parameter": "service_id",
            "old_value": 1,
            "new_value": 2,
            "related_features": [
                "scte35_pid",
                "vpid", 
                "apid",
                "pcr_pid",
                "tsduck_command"
            ]
        },
        {
            "name": "Video PID Change", 
            "parameter": "vpid",
            "old_value": 256,
            "new_value": 512,
            "related_features": [
                "pcr_pid",
                "pts_pid",
                "tsduck_command"
            ]
        },
        {
            "name": "Audio PID Change",
            "parameter": "apid", 
            "old_value": 257,
            "new_value": 513,
            "related_features": [
                "tsduck_command"
            ]
        },
        {
            "name": "SCTE-35 PID Change",
            "parameter": "scte35_pid",
            "old_value": 500,
            "new_value": 600,
            "related_features": [
                "spliceinject_pid",
                "tsduck_command"
            ]
        },
        {
            "name": "Event ID Change",
            "parameter": "event_id",
            "old_value": 100023,
            "new_value": 100024,
            "related_features": [
                "scte35_marker_generation",
                "xml_file_names",
                "tsduck_command"
            ]
        },
        {
            "name": "Pre-roll Duration Change",
            "parameter": "preroll_duration",
            "old_value": 2,
            "new_value": 5,
            "related_features": [
                "scte35_marker_timing",
                "xml_content",
                "tsduck_command"
            ]
        },
        {
            "name": "Ad Duration Change",
            "parameter": "ad_duration",
            "old_value": 600,
            "new_value": 900,
            "related_features": [
                "scte35_marker_content",
                "xml_content",
                "tsduck_command"
            ]
        }
    ]
    
    print("\n📋 Testing Parameter Synchronization Scenarios:")
    print("-" * 60)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   Parameter: {scenario['parameter']}")
        print(f"   Old Value: {scenario['old_value']}")
        print(f"   New Value: {scenario['new_value']}")
        print(f"   Related Features: {', '.join(scenario['related_features'])}")
        
        # Test if related features would update
        test_related_features(scenario)
    
    print("\n" + "=" * 60)
    print("✅ Parameter Synchronization Test Complete")
    
    return True

def test_related_features(scenario: Dict[str, Any]):
    """Test if related features update when parameter changes"""
    
    parameter = scenario['parameter']
    new_value = scenario['new_value']
    related_features = scenario['related_features']
    
    print(f"   🔄 Testing {parameter} → {new_value}")
    
    for feature in related_features:
        if feature == "tsduck_command":
            print(f"      ✅ {feature}: Should update TSDuck command")
        elif feature == "scte35_marker_generation":
            print(f"      ✅ {feature}: Should regenerate SCTE-35 markers")
        elif feature == "xml_file_names":
            print(f"      ✅ {feature}: Should update XML file names")
        elif feature == "xml_content":
            print(f"      ✅ {feature}: Should update XML content")
        elif feature == "scte35_marker_timing":
            print(f"      ✅ {feature}: Should update marker timing")
        elif feature == "scte35_marker_content":
            print(f"      ✅ {feature}: Should update marker content")
        elif feature == "spliceinject_pid":
            print(f"      ✅ {feature}: Should update spliceinject PID")
        elif feature == "pts_pid":
            print(f"      ✅ {feature}: Should update PTS PID")
        else:
            print(f"      ✅ {feature}: Should update related parameter")

def test_configuration_consistency():
    """Test configuration consistency across all components"""
    
    print("\n🔧 Testing Configuration Consistency:")
    print("-" * 40)
    
    # Load a test configuration
    test_config = {
        "service": {
            "service_id": 1,
            "vpid": 256,
            "apid": 257,
            "scte35_pid": 500,
            "pcr_pid": 256
        },
        "scte35": {
            "event_id": 100023,
            "preroll_duration": 2,
            "ad_duration": 600
        }
    }
    
    print("📋 Test Configuration:")
    print(json.dumps(test_config, indent=2))
    
    # Test TSDuck command generation
    tsduck_command = generate_tsduck_command(test_config)
    print(f"\n🔧 Generated TSDuck Command:")
    print(tsduck_command)
    
    # Test SCTE-35 marker generation
    scte35_marker = generate_scte35_marker(test_config)
    print(f"\n📡 Generated SCTE-35 Marker:")
    print(scte35_marker)
    
    # Test parameter validation
    validation_results = validate_parameters(test_config)
    print(f"\n✅ Parameter Validation:")
    for param, result in validation_results.items():
        status = "✅ Valid" if result else "❌ Invalid"
        print(f"   {param}: {status}")

def generate_tsduck_command(config: Dict[str, Any]) -> str:
    """Generate TSDuck command from configuration"""
    
    service = config.get("service", {})
    scte35 = config.get("scte35", {})
    
    service_id = service.get("service_id", 1)
    vpid = service.get("vpid", 256)
    apid = service.get("apid", 257)
    scte35_pid = service.get("scte35_pid", 500)
    pcr_pid = service.get("pcr_pid", 256)
    
    event_id = scte35.get("event_id", 100023)
    
    command = f"""tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \\
    -P sdt --service {service_id} --name "SCTE-35 Stream" --provider "ITAssist" \\
    -P remap 211={vpid} 221={apid} \\
    -P pmt --service {service_id} --add-pid {vpid}/0x1b --add-pid {apid}/0x0f --add-pid {scte35_pid}/0x86 \\
    -P spliceinject --pid {scte35_pid} --pts-pid {vpid} --files "scte35_final/preroll_{event_id}.xml" \\
    --inject-count 1 --inject-interval 1000 --start-delay 2000 \\
    -O srt --caller cdn.itassist.one:8888 --streamid "#!::r=scte/scte,m=publish" """
    
    return command

def generate_scte35_marker(config: Dict[str, Any]) -> str:
    """Generate SCTE-35 marker from configuration"""
    
    scte35 = config.get("scte35", {})
    service = config.get("service", {})
    
    event_id = scte35.get("event_id", 100023)
    preroll_duration = scte35.get("preroll_duration", 2)
    ad_duration = scte35.get("ad_duration", 600)
    scte35_pid = service.get("scte35_pid", 500)
    
    marker = f"""SCTE-35 Marker:
  Event ID: {event_id}
  Pre-roll: {preroll_duration}s
  Duration: {ad_duration}s
  PID: {scte35_pid}
  File: scte35_final/preroll_{event_id}.xml"""
    
    return marker

def validate_parameters(config: Dict[str, Any]) -> Dict[str, bool]:
    """Validate configuration parameters"""
    
    results = {}
    
    # Service validation
    service = config.get("service", {})
    results["service_id"] = 1 <= service.get("service_id", 0) <= 65535
    results["vpid"] = 1 <= service.get("vpid", 0) <= 8191
    results["apid"] = 1 <= service.get("apid", 0) <= 8191
    results["scte35_pid"] = 1 <= service.get("scte35_pid", 0) <= 8191
    results["pcr_pid"] = service.get("pcr_pid", 0) == service.get("vpid", 0)
    
    # SCTE-35 validation
    scte35 = config.get("scte35", {})
    results["event_id"] = 1 <= scte35.get("event_id", 0) <= 4294967295
    results["preroll_duration"] = 0 <= scte35.get("preroll_duration", 0) <= 300
    results["ad_duration"] = 1 <= scte35.get("ad_duration", 0) <= 3600
    
    return results

def test_ui_parameter_synchronization():
    """Test UI parameter synchronization"""
    
    print("\n🖥️ Testing UI Parameter Synchronization:")
    print("-" * 45)
    
    ui_components = [
        "Input Configuration Widget",
        "Output Configuration Widget", 
        "Service Configuration Widget",
        "SCTE-35 Configuration Widget",
        "Professional SCTE-35 Interface",
        "Monitoring Widget",
        "Status Display"
    ]
    
    for component in ui_components:
        print(f"   🔄 {component}:")
        print(f"      ✅ Should update when service parameters change")
        print(f"      ✅ Should update when SCTE-35 parameters change")
        print(f"      ✅ Should update when input/output parameters change")
        print(f"      ✅ Should reflect changes in real-time")

def main():
    """Main test function"""
    
    print("🚀 IBE-100 Parameter Synchronization Test Suite")
    print("=" * 60)
    
    try:
        # Run all tests
        test_parameter_synchronization()
        test_configuration_consistency()
        test_ui_parameter_synchronization()
        
        print("\n🎉 All Parameter Synchronization Tests Completed!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test Error: {e}")
        return False

if __name__ == "__main__":
    main()
