"""
GitHub-based License Manager for IBE-100
Manages licenses using GitHub Gist as storage
"""

import requests
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class GitHubLicenseManager:
    """Manage licenses using GitHub Gist"""
    
    def __init__(self):
        self.license_file = Path("license.json")
        self.github_token = self.get_github_token()
        self.gist_id = "your-gist-id-here"  # Update with your Gist ID
        self.api_url = f"https://api.github.com/gists/{self.gist_id}"
        self.licenses = {}
        self.license_data = None
        
    def get_github_token(self):
        """Get GitHub token from environment or config"""
        # Try environment variable first
        token = os.getenv('GITHUB_TOKEN')
        
        # Try config file
        if not token:
            config_file = Path("github_config.json")
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        token = config.get('token')
                except:
                    pass
        
        return token
    
    def load_local_license(self):
        """Load license from local file"""
        if not self.license_file.exists():
            return False
        
        try:
            with open(self.license_file, 'r') as f:
                self.license_data = json.load(f)
            return True
        except:
            return False
    
    def save_local_license(self, data):
        """Save license to local file"""
        with open(self.license_file, 'w') as f:
            json.dump(data, f, indent=2)
        self.license_data = data
    
    def load_licenses_from_github(self):
        """Load all licenses from GitHub Gist"""
        if not self.github_token:
            print("[ERROR] GitHub token not configured")
            return False
        
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(self.api_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"[ERROR] Failed to load licenses from GitHub: {response.status_code}")
                return False
            
            data = response.json()
            
            # Get content from first file
            files = data.get('files', {})
            if not files:
                print("[ERROR] No files in Gist")
                return False
            
            file_content = list(files.values())[0]['content']
            self.licenses = json.loads(file_content)
            
            print(f"[INFO] Loaded {len(self.licenses)} licenses from GitHub")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error loading licenses from GitHub: {e}")
            return False
    
    def validate_license(self, license_key, check_restrictions=True):
        """Validate license against GitHub"""
        try:
            # Load licenses if not already loaded
            if not self.licenses:
                self.load_licenses_from_github()
            
            license_data = self.licenses.get(license_key)
            
            if not license_data:
                return False, "License not found"
            
            # Check expiry
            expiry = license_data.get('expiry')
            if expiry:
                expiry_date = datetime.strptime(expiry, '%Y-%m-%d')
                if datetime.now() > expiry_date:
                    # Check if it's the first expiry day
                    if datetime.now().date() == expiry_date.date():
                        return True, "License expiring today", license_data
                    return False, "License expired"
            
            # Check active status
            if not license_data.get('active', False):
                return False, "License inactive"
            
            # Check restrictions if requested
            if check_restrictions:
                tier = license_data.get('tier', 'trial')
                
                if tier == 'trial':
                    # Trial restrictions
                    days_since_created = self.get_days_since_activation()
                    if days_since_created > 7:
                        return False, "Trial period expired (7 days)"
                    
                    # Time limit per session (e.g., 1 hour)
                    if self.check_session_time_exceeded():
                        return False, "Trial session time limit exceeded"
                
                elif tier == 'monthly':
                    # Monthly subscription
                    days_since_activated = self.get_days_since_activation()
                    if days_since_activated > 30:
                        return False, "Monthly subscription expired"
            
            return True, "License valid", license_data
            
        except Exception as e:
            print(f"[ERROR] License validation error: {e}")
            return False, f"Validation error: {e}"
    
    def get_days_since_activation(self):
        """Get days since license was activated"""
        if not self.license_data:
            self.load_local_license()
        
        if not self.license_data:
            return 999  # Very old
        
        activated_str = self.license_data.get('activated')
        if not activated_str:
            return 999
        
        try:
            activated = datetime.fromisoformat(activated_str)
            return (datetime.now() - activated).days
        except:
            return 999
    
    def check_session_time_exceeded(self):
        """Check if trial session time exceeded (1 hour limit)"""
        # For trial users, limit session to 1 hour
        session_file = Path("session_start.json")
        
        if not session_file.exists():
            # Start new session
            with open(session_file, 'w') as f:
                json.dump({'start': datetime.now().isoformat()}, f)
            return False
        
        try:
            with open(session_file, 'r') as f:
                session = json.load(f)
            
            start_time = datetime.fromisoformat(session['start'])
            elapsed = (datetime.now() - start_time).total_seconds() / 3600  # Hours
            
            # Trial: 1 hour limit per session
            if elapsed > 1:
                return True
            
            return False
            
        except:
            return False
    
    def activate_license(self, license_key, user_email):
        """Activate license"""
        valid, message, license_data = self.validate_license(license_key, check_restrictions=False)
        
        if not valid:
            return False, message
        
        # Save locally
        self.save_local_license({
            'key': license_key,
            'email': user_email,
            'activated': datetime.now().isoformat(),
            'tier': license_data.get('tier'),
            'expiry': license_data.get('expiry'),
            'user': license_data.get('user')
        })
        
        return True, "License activated successfully"
    
    def check_license_status(self):
        """Check if local license is still valid"""
        if not self.load_local_license():
            return False
        
        license_key = self.license_data.get('key')
        if not license_key:
            return False
        
        valid, _ = self.validate_license(license_key, check_restrictions=True)
        return valid
    
    def get_license_info(self):
        """Get current license information"""
        if not self.license_data:
            self.load_local_license()
        
        if not self.license_data:
            return None
        
        return {
            'email': self.license_data.get('email'),
            'tier': self.license_data.get('tier'),
            'activated': self.license_data.get('activated'),
            'expiry': self.license_data.get('expiry'),
            'days_remaining': self.get_days_remaining()
        }
    
    def get_days_remaining(self):
        """Get days until license expiry"""
        if not self.license_data:
            return 0
        
        expiry_str = self.license_data.get('expiry')
        if not expiry_str:
            return 999  # No expiry
        
        try:
            expiry = datetime.strptime(expiry_str, '%Y-%m-%d')
            remaining = expiry - datetime.now()
            return max(0, remaining.days)
        except:
            return 0
    
    def reset_session(self):
        """Reset session timer (for trial users)"""
        session_file = Path("session_start.json")
        if session_file.exists():
            session_file.unlink()
