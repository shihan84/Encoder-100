#!/usr/bin/env python3
"""
IBE-100 Redundant Features Cleanup Script
Removes unused and redundant features to streamline the application
"""

import os
import re
from typing import List, Dict, Any

def analyze_redundant_features():
    """Analyze and identify redundant features"""
    
    print("🔍 Analyzing IBE-100 for redundant features...")
    print("=" * 60)
    
    # Files to analyze
    files_to_analyze = [
        "enc100.py",
        "professional_scte35_widget.py",
        "scte35_generation_widget.py",
        "scte35_template_widget.py",
        "tsduck_gui.py"
    ]
    
    redundant_features = []
    
    for file_path in files_to_analyze:
        if os.path.exists(file_path):
            print(f"\n📁 Analyzing {file_path}...")
            features = analyze_file_features(file_path)
            redundant_features.extend(features)
        else:
            print(f"⚠️  File not found: {file_path}")
    
    return redundant_features

def analyze_file_features(file_path: str) -> List[Dict[str, Any]]:
    """Analyze a file for redundant features"""
    
    features = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for widget classes
        widget_classes = re.findall(r'class (\w*Widget)\(', content)
        
        # Look for tab additions
        tab_additions = re.findall(r'addTab\([^,]+,\s*["\']([^"\']+)["\']', content)
        
        # Look for redundant imports
        imports = re.findall(r'from (\w+) import', content)
        
        print(f"   📊 Found {len(widget_classes)} widget classes")
        print(f"   📊 Found {len(tab_additions)} tab additions")
        print(f"   📊 Found {len(imports)} imports")
        
        # Identify potential redundancies
        for widget in widget_classes:
            if 'SCTE35' in widget and 'Professional' not in widget:
                features.append({
                    'type': 'redundant_widget',
                    'name': widget,
                    'file': file_path,
                    'reason': 'Redundant SCTE-35 widget (use Professional version)'
                })
        
        for tab in tab_additions:
            if 'TSDuck' in tab or 'TSP' in tab:
                features.append({
                    'type': 'redundant_tab',
                    'name': tab,
                    'file': file_path,
                    'reason': 'Redundant TSDuck configuration tab'
                })
        
    except Exception as e:
        print(f"   ❌ Error analyzing {file_path}: {e}")
    
    return features

def create_cleanup_plan():
    """Create a comprehensive cleanup plan"""
    
    print("\n🧹 Creating Cleanup Plan...")
    print("-" * 40)
    
    cleanup_actions = [
        {
            'action': 'remove_redundant_scte35',
            'description': 'Remove redundant SCTE-35 widget from configuration',
            'files': ['enc100.py'],
            'changes': [
                'Remove SCTE35Widget from ConfigurationWidget',
                'Keep only ProfessionalSCTE35Widget in main tabs'
            ]
        },
        {
            'action': 'remove_redundant_tsduck',
            'description': 'Remove redundant TSDuck configuration tab',
            'files': ['enc100.py'],
            'changes': [
                'Remove TSDuckConfigWidget from ConfigurationWidget',
                'Integrate TSDuck settings into main configuration'
            ]
        },
        {
            'action': 'consolidate_monitoring',
            'description': 'Consolidate monitoring features',
            'files': ['enc100.py'],
            'changes': [
                'Merge AnalyticsWidget and PerformanceWidget',
                'Create unified monitoring interface'
            ]
        },
        {
            'action': 'remove_unused_files',
            'description': 'Remove unused widget files',
            'files': [
                'scte35_generation_widget.py',
                'scte35_template_widget.py'
            ],
            'changes': [
                'Delete redundant SCTE-35 widget files',
                'Update imports in main application'
            ]
        }
    ]
    
    return cleanup_actions

def generate_cleanup_code():
    """Generate code for cleanup implementation"""
    
    print("\n🔧 Generating Cleanup Code...")
    print("-" * 40)
    
    cleanup_code = '''
# IBE-100 Redundant Features Cleanup Implementation

def cleanup_enc100():
    """Clean up enc100.py by removing redundant features"""
    
    # 1. Remove redundant SCTE-35 widget from ConfigurationWidget
    # Remove this line from ConfigurationWidget.__init__:
    # self.scte35_widget = SCTE35Widget()
    # self.config_tabs.addTab(self.scte35_widget, "🎬 SCTE-35")
    
    # 2. Remove redundant TSDuck widget from ConfigurationWidget
    # Remove this line from ConfigurationWidget.__init__:
    # self.tsduck_widget = TSDuckConfigWidget()
    # self.config_tabs.addTab(self.tsduck_widget, "[TOOL] TSDuck")
    
    # 3. Consolidate monitoring features
    # Replace separate AnalyticsWidget and PerformanceWidget with unified monitoring
    
    # 4. Update imports
    # Remove unused imports:
    # from scte35_generation_widget import SCTE35GenerationWidget
    # from scte35_template_widget import SCTE35TemplateWidget
    
    pass

def cleanup_widget_classes():
    """Remove unused widget classes"""
    
    # Remove these classes from enc100.py:
    # - SCTE35Widget (replaced by ProfessionalSCTE35Widget)
    # - TSDuckConfigWidget (integrated into main configuration)
    # - AnalyticsWidget (merged into unified monitoring)
    # - PerformanceWidget (merged into unified monitoring)
    
    pass

def update_main_interface():
    """Update main interface to use streamlined structure"""
    
    # Main tabs should be:
    # 1. ⚙️ Configuration - All configuration in one place
    # 2. 📊 Monitoring - Unified monitoring and analytics  
    # 3. 🎬 SCTE-35 Professional - Professional SCTE-35 interface
    # 4. 🛠️ Tools - Essential tools and utilities
    # 5. 📚 Help - Documentation and help
    
    pass
'''
    
    return cleanup_code

def create_optimized_structure():
    """Create optimized application structure"""
    
    print("\n🎯 Creating Optimized Structure...")
    print("-" * 40)
    
    optimized_structure = {
        'main_tabs': [
            {
                'name': '⚙️ Configuration',
                'description': 'All configuration settings in one place',
                'sub_tabs': [
                    '📥 Input - Input configuration',
                    '📤 Output - Output configuration', 
                    '📺 Service - Service and PID configuration',
                    '🔧 Advanced - Advanced settings (merged TSDuck)'
                ]
            },
            {
                'name': '📊 Monitoring',
                'description': 'Unified monitoring and analytics',
                'sub_tabs': [
                    '📺 Console - Real-time console output',
                    '📊 Analytics - Stream analytics and performance',
                    '⚡ Status - System status and health'
                ]
            },
            {
                'name': '🎬 SCTE-35 Professional',
                'description': 'Professional SCTE-35 marker management',
                'sub_tabs': [
                    'Quick Actions - Common SCTE-35 operations',
                    'Advanced Config - Advanced SCTE-35 settings',
                    'Marker Library - SCTE-35 marker library',
                    'Templates - Professional templates'
                ]
            },
            {
                'name': '🛠️ Tools',
                'description': 'Essential tools and utilities',
                'sub_tabs': [
                    '🔍 Stream Analyzer - TSAnalyzer integration',
                    '🛠️ Utilities - Utility functions'
                ]
            },
            {
                'name': '📚 Help',
                'description': 'Documentation and help system',
                'sub_tabs': [
                    '📖 User Guide - User documentation',
                    '🔧 Technical Guide - Technical documentation',
                    '❓ FAQ - Frequently asked questions'
                ]
            }
        ]
    }
    
    return optimized_structure

def main():
    """Main cleanup function"""
    
    print("🚀 IBE-100 Redundant Features Cleanup")
    print("=" * 60)
    
    # Analyze redundant features
    redundant_features = analyze_redundant_features()
    
    print(f"\n📊 Analysis Results:")
    print(f"   Found {len(redundant_features)} redundant features")
    
    for feature in redundant_features:
        print(f"   ❌ {feature['name']} - {feature['reason']}")
    
    # Create cleanup plan
    cleanup_actions = create_cleanup_plan()
    
    print(f"\n🧹 Cleanup Plan:")
    print(f"   {len(cleanup_actions)} cleanup actions identified")
    
    for action in cleanup_actions:
        print(f"   🔧 {action['description']}")
    
    # Generate cleanup code
    cleanup_code = generate_cleanup_code()
    
    # Create optimized structure
    optimized_structure = create_optimized_structure()
    
    print(f"\n🎯 Optimized Structure:")
    print(f"   {len(optimized_structure['main_tabs'])} main tabs")
    
    for tab in optimized_structure['main_tabs']:
        print(f"   📁 {tab['name']} - {tab['description']}")
        for sub_tab in tab['sub_tabs']:
            print(f"      📄 {sub_tab}")
    
    print(f"\n✅ Cleanup Analysis Complete!")
    print("=" * 60)
    
    return {
        'redundant_features': redundant_features,
        'cleanup_actions': cleanup_actions,
        'cleanup_code': cleanup_code,
        'optimized_structure': optimized_structure
    }

if __name__ == "__main__":
    main()
