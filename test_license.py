#!/usr/bin/env python3
"""
Test script for GitHub License System
"""

from github_license_manager import GitHubLicenseManager

def main():
    print("=" * 60)
    print("  IBE-100 License System - Test")
    print("=" * 60)
    print()
    
    # Initialize manager
    print("[1/4] Initializing license manager...")
    manager = GitHubLicenseManager()
    
    # Load licenses from GitHub
    print("[2/4] Loading licenses from GitHub...")
    if manager.load_licenses_from_github():
        print("   ✅ Successfully loaded licenses")
        print(f"   Found {len(manager.licenses)} license(s)\n")
    else:
        print("   ❌ Failed to load licenses")
        print("   Check your GitHub token and Gist ID in github_config.json")
        return
    
    # Test Trial License
    print("[3/4] Testing TRIAL License (TRIAL2024DEMO001)...")
    valid, message, data = manager.validate_license("TRIAL2024DEMO001")
    if valid:
        print(f"   ✅ Valid: {message}")
        print(f"   Tier: {data.get('tier', 'unknown')}")
        print(f"   Expiry: {data.get('expiry', 'none')}")
        print(f"   User: {data.get('user', 'unknown')}\n")
    else:
        print(f"   ❌ Invalid: {message}\n")
    
    # Test Unlimited License
    print("[4/4] Testing UNLIMITED License (UNLIMITED2024KARTIK)...")
    valid, message, data = manager.validate_license("UNLIMITED2024KARTIK")
    if valid:
        print(f"   ✅ Valid: {message}")
        print(f"   Tier: {data.get('tier', 'unknown')}")
        print(f"   Expiry: {data.get('expiry', 'none')}")
        print(f"   User: {data.get('user', 'unknown')}\n")
    else:
        print(f"   ❌ Invalid: {message}\n")
    
    # Test activation
    print("[BONUS] Testing license activation...")
    success, msg = manager.activate_license("TRIAL2024DEMO001", "test@example.com")
    if success:
        print(f"   ✅ {msg}")
        print(f"   License saved to: {manager.license_file}")
    else:
        print(f"   ❌ {msg}")
    
    print()
    print("=" * 60)
    print("  Test Complete!")
    print("=" * 60)
    print()
    print("Next step: Integrate into IBE-100 app")
    print()

if __name__ == "__main__":
    main()

