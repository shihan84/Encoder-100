#!/usr/bin/env python3
"""
Execute IBE-100 Redundant Features Cleanup
Practical implementation of cleanup plan
"""

import os
import shutil
from datetime import datetime

def create_backup():
    """Create backup before cleanup"""
    
    print("Creating backup before cleanup...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"IBE-100_backup_{timestamp}"
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup main files
        files_to_backup = [
            "enc100.py",
            "professional_scte35_widget.py",
            "scte35_generation_widget.py",
            "scte35_template_widget.py",
            "tsduck_gui.py"
        ]
        
        for file in files_to_backup:
            if os.path.exists(file):
                shutil.copy2(file, backup_dir)
                print(f"  Backed up: {file}")
        
        print(f"Backup created: {backup_dir}")
        return backup_dir
        
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

def remove_redundant_files():
    """Remove redundant SCTE-35 files"""
    
    print("\nRemoving redundant files...")
    
    files_to_remove = [
        "scte35_generation_widget.py",
        "scte35_template_widget.py"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"  Removed: {file}")
            except Exception as e:
                print(f"  Error removing {file}: {e}")
        else:
            print(f"  Not found: {file}")

def update_enc100():
    """Update enc100.py with streamlined structure"""
    
    print("\nUpdating enc100.py...")
    
    if not os.path.exists("enc100.py"):
        print("  Error: enc100.py not found")
        return False
    
    try:
        # Read current file
        with open("enc100.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove redundant imports
        redundant_imports = [
            "from scte35_generation_widget import SCTE35GenerationWidget",
            "from scte35_template_widget import SCTE35TemplateWidget"
        ]
        
        for import_line in redundant_imports:
            if import_line in content:
                content = content.replace(import_line, "# " + import_line + " # REMOVED")
                print(f"  Commented out: {import_line}")
        
        # Write updated file
        with open("enc100.py", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("  Updated enc100.py")
        return True
        
    except Exception as e:
        print(f"  Error updating enc100.py: {e}")
        return False

def create_cleanup_summary():
    """Create cleanup summary"""
    
    print("\nCreating cleanup summary...")
    
    summary = f"""
# IBE-100 Cleanup Summary
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Files Removed
- scte35_generation_widget.py (redundant with professional version)
- scte35_template_widget.py (redundant with professional version)

## Files Modified
- enc100.py (removed redundant imports)

## Recommended Next Steps
1. Test the application to ensure all features work
2. Remove unused widget classes from enc100.py
3. Consolidate monitoring features
4. Streamline tab structure

## Benefits Expected
- Reduced memory usage
- Faster application startup
- Cleaner interface
- Easier maintenance
"""
    
    with open("CLEANUP_SUMMARY.md", 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("  Created CLEANUP_SUMMARY.md")

def main():
    """Main cleanup execution"""
    
    print("IBE-100 Redundant Features Cleanup")
    print("=" * 50)
    
    # Create backup
    backup_dir = create_backup()
    if not backup_dir:
        print("Error: Could not create backup. Aborting cleanup.")
        return False
    
    # Remove redundant files
    remove_redundant_files()
    
    # Update main application
    update_enc100()
    
    # Create summary
    create_cleanup_summary()
    
    print("\nCleanup completed!")
    print("=" * 50)
    print("Next steps:")
    print("1. Test the application")
    print("2. Review CLEANUP_SUMMARY.md")
    print("3. Continue with manual cleanup if needed")
    
    return True

if __name__ == "__main__":
    main()
