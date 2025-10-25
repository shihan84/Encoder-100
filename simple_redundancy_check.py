#!/usr/bin/env python3
"""
Simple IBE-100 Redundancy Check
Checks for redundant features without Unicode issues
"""

import os
import re

def check_redundant_features():
    """Check for redundant features in the application"""
    
    print("IBE-100 Redundancy Analysis")
    print("=" * 50)
    
    # Check main application file
    if os.path.exists("enc100.py"):
        print("\nAnalyzing enc100.py...")
        analyze_enc100()
    
    # Check for redundant SCTE-35 files
    check_scte35_redundancy()
    
    # Check for unused widgets
    check_unused_widgets()

def analyze_enc100():
    """Analyze the main application file"""
    
    try:
        with open("enc100.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count widget classes
        widget_classes = re.findall(r'class (\w*Widget)\(', content)
        print(f"Found {len(widget_classes)} widget classes:")
        for widget in widget_classes:
            print(f"  - {widget}")
        
        # Count tabs
        tabs = re.findall(r'addTab\([^,]+,\s*["\']([^"\']+)["\']', content)
        print(f"\nFound {len(tabs)} tabs:")
        for tab in tabs:
            print(f"  - {tab}")
        
        # Check for redundant SCTE-35 references
        scte35_refs = re.findall(r'SCTE35', content)
        print(f"\nFound {len(scte35_refs)} SCTE-35 references")
        
        # Check for redundant TSDuck references
        tsduck_refs = re.findall(r'TSDuck', content)
        print(f"Found {len(tsduck_refs)} TSDuck references")
        
    except Exception as e:
        print(f"Error analyzing enc100.py: {e}")

def check_scte35_redundancy():
    """Check for redundant SCTE-35 files"""
    
    print("\nChecking SCTE-35 redundancy...")
    
    scte35_files = [
        "scte35_generation_widget.py",
        "scte35_template_widget.py", 
        "professional_scte35_widget.py"
    ]
    
    for file in scte35_files:
        if os.path.exists(file):
            print(f"  Found: {file}")
        else:
            print(f"  Missing: {file}")

def check_unused_widgets():
    """Check for potentially unused widgets"""
    
    print("\nChecking for unused widgets...")
    
    # Widgets that might be redundant
    potentially_redundant = [
        "SCTE35Widget",
        "TSDuckConfigWidget", 
        "AnalyticsWidget",
        "PerformanceWidget"
    ]
    
    for widget in potentially_redundant:
        print(f"  Checking {widget}...")
        # This would need more detailed analysis
        print(f"    Status: Needs manual review")

def create_cleanup_recommendations():
    """Create cleanup recommendations"""
    
    print("\nCleanup Recommendations:")
    print("-" * 30)
    
    recommendations = [
        "1. Remove redundant SCTE-35 widget from configuration tab",
        "2. Remove separate TSDuck configuration tab", 
        "3. Consolidate monitoring features",
        "4. Remove unused widget files",
        "5. Streamline tab structure"
    ]
    
    for rec in recommendations:
        print(f"  {rec}")

def main():
    """Main function"""
    
    check_redundant_features()
    create_cleanup_recommendations()
    
    print("\nAnalysis complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
