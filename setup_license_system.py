#!/usr/bin/env python3
"""
Interactive setup script for IBE-100 License System
Guides you through GitHub token and Gist creation
"""

import json
from pathlib import Path
import webbrowser

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(num, total, text):
    print(f"[{num}/{total}] {text}")

def wait_for_input(prompt):
    input(f"\n{prompt}\nPress Enter when done...")

def main():
    print_header("IBE-100 License System Setup")
    print("This script will help you set up the GitHub-based license system.")
    print()
    
    # Step 1: GitHub Token
    print_step(1, 4, "Get GitHub Personal Access Token")
    print("\nFollow these steps:")
    print("1. A browser window will open to GitHub token settings")
    print("2. Click 'Generate new token (classic)'")
    print("3. Name it: 'IBE-100 License Manager'")
    print("4. Check the 'gist' scope")
    print("5. Click 'Generate token'")
    print("6. COPY THE TOKEN - you won't see it again!")
    
    input("\nPress Enter to open GitHub token settings...")
    webbrowser.open("https://github.com/settings/tokens")
    
    github_token = input("\n📋 Paste your GitHub token here: ").strip()
    
    if not github_token:
        print("❌ Token is required!")
        return
    
    print("✅ GitHub token saved")
    
    # Step 2: Create Gist
    print_step(2, 4, "Create GitHub Gist")
    print("\nFollow these steps:")
    print("1. A browser window will open to create a new Gist")
    print("2. Click 'Create a new secret gist'")
    print("3. Description: 'IBE-100 Licenses'")
    print("4. Filename: 'licenses.json'")
    print("5. Paste the license content")
    print("6. Click 'Create secret gist'")
    print("7. COPY THE GIST ID from the URL")
    
    input("\nPress Enter to open Gist creation...")
    webbrowser.open("https://gist.github.com")
    
    print("\n📋 After creating the Gist, copy the Gist ID from the URL")
    print("   Example URL: https://gist.github.com/YOU/a1b2c3d4e5f6g7h8...")
    print("   Gist ID is: a1b2c3d4e5f6g7h8...")
    
    gist_id = input("\n📋 Paste your Gist ID here: ").strip()
    
    if not gist_id:
        print("❌ Gist ID is required!")
        return
    
    print("✅ Gist ID saved")
    
    # Step 3: Create Config File
    print_step(3, 4, "Create Configuration File")
    
    config = {
        "token": github_token,
        "gist_id": gist_id
    }
    
    config_file = Path("github_config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created: {config_file}")
    
    # Step 4: Test License System
    print_step(4, 4, "Test License System")
    
    print("\nTesting license system...")
    
    try:
        from github_license_manager import GitHubLicenseManager
        
        manager = GitHubLicenseManager()
        
        print("Loading licenses from GitHub...")
        if manager.load_licenses_from_github():
            print(f"✅ Successfully loaded {len(manager.licenses)} license(s)")
            
            # Test Trial
            print("\nTesting TRIAL license...")
            valid, msg, data = manager.validate_license("TRIAL2024DEMO001")
            if valid:
                print(f"   ✅ {msg}")
                print(f"   Tier: {data.get('tier')}")
            else:
                print(f"   ❌ {msg}")
            
            # Test Unlimited
            print("\nTesting UNLIMITED license...")
            valid, msg, data = manager.validate_license("UNLIMITED2024KARTIK")
            if valid:
                print(f"   ✅ {msg}")
                print(f"   Tier: {data.get('tier')}")
            else:
                print(f"   ❌ {msg}")
            
            print("\n✅ License system is working!")
            
        else:
            print("❌ Failed to load licenses")
            print("Please check:")
            print("  - GitHub token is correct")
            print("  - Gist ID is correct")
            print("  - Gist is set to 'secret'")
            return
    
    except Exception as e:
        print(f"❌ Error testing license system: {e}")
        print("\nPlease check:")
        print("  - github_license_manager.py exists")
        print("  - python -m pip install requests")
        return
    
    # Summary
    print_header("Setup Complete!")
    print("\n✅ License system is configured and working!")
    print(f"\nConfig file: {config_file}")
    print(f"Licenses in Gist: https://gist.github.com/{gist_id}")
    print(f"\nLicense keys:")
    print(f"  - TRIAL2024DEMO001 (7 days, 1h session)")
    print(f"  - UNLIMITED2024KARTIK (unlimited)")
    print("\nNext step: Integrate into IBE-100 app")
    print()

if __name__ == "__main__":
    main()

