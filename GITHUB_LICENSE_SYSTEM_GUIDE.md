# 🔐 GitHub-Based License System

## 📋 **Can GitHub Manage Licenses? YES!**

GitHub can be used as a **license management system** through:
- GitHub Issues (as license store)
- GitHub Secrets (for license keys)
- GitHub Actions (for validation)
- GitHub API (to check licenses)

---

## 🎯 **Why GitHub for Licenses?**

### **Advantages:**
✅ **Free** - No cost at all  
✅ **No server needed** - Use GitHub's infrastructure  
✅ **Familiar platform** - You already use GitHub  
✅ **Automatic backups** - GitHub handles it  
✅ **Version control** - Track license changes  
✅ **Secure** - GitHub security built-in  

### **How It Works:**
1. Store licenses in GitHub **Issues** or **Projects**
2. Use **GitHub Secrets** to encrypt license keys
3. Use **GitHub Actions** to validate licenses
4. Use **GitHub API** from Python app to check licenses

---

## 🏗️ **Architecture**

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   User App  │─────────>│   GitHub    │─────────>│   Payment   │
│  (IBE-100)  │         │     API     │         │  (Stripe)   │
└─────────────┘         └─────────────┘         └─────────────┘
        │                       │                       │
        │                       │                       │
        v                       v                       v
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ License File│         │   GitHub    │         │  Webhook    │
│  (Local)    │         │  Issues/    │         │  (Action)   │
│             │         │  Secrets    │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
```

---

## 📦 **Method 1: GitHub Issues as License Store**

### **How It Works:**

Store each license as a GitHub Issue in your private repo:

```yaml
Title: "License: ABC123XYZ456"
Labels: active, professional
Body:
  email: user@example.com
  expiry: 2024-12-31
  tier: professional
  hardware_id: 00:11:22:33:44:55
```

### **Python Implementation:**

Create `github_license_manager.py`:

```python
import requests
import json
import base64
from datetime import datetime
from pathlib import Path

class GitHubLicenseManager:
    """License manager using GitHub Issues as database"""
    
    def __init__(self, github_token, repo_owner="shihan84", repo_name="Encoder-100"):
        self.github_token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.license_file = Path("license.json")
        self.license_data = None
        
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
    
    def save_local_license(self, license_data):
        """Save license to local file"""
        with open(self.license_file, 'w') as f:
            json.dump(license_data, f)
        self.license_data = license_data
    
    def validate_license(self, license_key):
        """Validate license by querying GitHub Issues"""
        try:
            # Search for issue with title containing license key
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Search issues
            url = f"{self.api_url}/issues"
            params = {'state': 'all', 'labels': 'license'}
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                return False, "GitHub API error"
            
            issues = response.json()
            
            # Find matching license
            for issue in issues:
                if license_key in issue.get('title', ''):
                    # Parse license data from issue body
                    license_data = self.parse_issue_body(issue['body'])
                    
                    # Check expiry
                    expiry_str = license_data.get('expiry')
                    if expiry_str:
                        expiry = datetime.strptime(expiry_str, '%Y-%m-%d')
                        if datetime.now() > expiry:
                            return False, "License expired"
                    
                    # Check status
                    labels = [label['name'] for label in issue.get('labels', [])]
                    if 'revoked' in labels or 'expired' in labels:
                        return False, "License revoked"
                    
                    if 'active' not in labels:
                        return False, "License not active"
                    
                    return True, license_data
            
            return False, "License not found"
            
        except Exception as e:
            print(f"[ERROR] License validation error: {e}")
            return False, str(e)
    
    def parse_issue_body(self, body):
        """Parse license data from GitHub Issue body"""
        data = {}
        for line in body.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                data[key] = value
        return data
    
    def create_license_issue(self, license_key, user_email, tier, days=30):
        """Create new license in GitHub Issues"""
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            expiry_date = datetime.now().replace(day=28).strftime('%Y-%m-%d')
            
            issue_body = f"""License Information:
email: {user_email}
expiry: {expiry_date}
tier: {tier}
created: {datetime.now().strftime('%Y-%m-%d')}
"""
            
            data = {
                'title': f'License: {license_key}',
                'body': issue_body,
                'labels': ['license', 'active', tier]
            }
            
            url = f"{self.api_url}/issues"
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error creating issue: {response.text}")
                return None
                
        except Exception as e:
            print(f"[ERROR] Create license error: {e}")
            return None
    
    def activate_license(self, license_key, user_email):
        """Activate license"""
        # Validate with GitHub
        valid, data = self.validate_license(license_key)
        
        if valid:
            # Save locally
            self.save_local_license({
                'key': license_key,
                'email': user_email,
                'activated': datetime.now().isoformat(),
                'tier': data.get('tier'),
                'expiry': data.get('expiry')
            })
            return True, "License activated"
        else:
            return False, data  # Returns error message
    
    def check_license_status(self):
        """Check if local license is still valid"""
        if not self.load_local_license():
            return False
        
        license_key = self.license_data.get('key')
        if not license_key:
            return False
        
        valid, _ = self.validate_license(license_key)
        return valid
```

---

## 🔐 **Method 2: GitHub Secrets + Actions**

### **How It Works:**

1. Store license keys in GitHub **Secrets**
2. Use **GitHub Actions** to validate
3. Call Actions from your app

### **GitHub Action Workflow:**

Create `.github/workflows/validate-license.yml`:

```yaml
name: Validate License

on:
  workflow_dispatch:
    inputs:
      license_key:
        description: 'License key to validate'
        required: true

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Check license
        uses: actions/github-script@v6
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const license = context.payload.inputs.license_key;
            
            // Check GitHub Secrets or repo
            const licenseList = [
              'ABC123XYZ456',
              'DEF789GHI012',
              // ... your license keys
            ];
            
            const valid = licenseList.includes(license);
            
            // Get license info
            if (valid) {
              // Query issue or secret for details
              const issues = await github.rest.issues.listForRepo({
                owner: context.repo.owner,
                repo: context.repo.repo,
                state: 'all',
                labels: 'license'
              });
              
              const issue = issues.data.find(i => 
                i.title.includes(license)
              );
              
              if (issue) {
                return {
                  valid: true,
                  expiry: '2024-12-31',
                  tier: 'professional'
                };
              }
            }
            
            return { valid: false };
```

### **Call from Python:**

```python
def validate_via_action(self, license_key):
    """Validate license via GitHub Action"""
    headers = {
        'Authorization': f'token {self.github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'ref': 'main',
        'inputs': {
            'license_key': license_key
        }
    }
    
    url = f"{self.api_url}/actions/workflows/validate-license.yml/dispatches"
    response = requests.post(url, headers=headers, json=data)
    
    # Get result from action
    # ... implementation
```

---

## 📂 **Method 3: GitHub Gists as License Store**

### **How It Works:**

Store all licenses in a **private GitHub Gist**:

```json
{
  "ABC123XYZ456": {
    "email": "user@example.com",
    "expiry": "2024-12-31",
    "tier": "professional",
    "active": true
  },
  "DEF789GHI012": {
    "email": "user2@example.com",
    "expiry": "2025-01-15",
    "tier": "trial",
    "active": true
  }
}
```

### **Python Implementation:**

```python
class GistLicenseManager:
    """License manager using GitHub Gist"""
    
    def __init__(self, github_token, gist_id):
        self.github_token = github_token
        self.gist_id = gist_id
        self.api_url = f"https://api.github.com/gists/{gist_id}"
        self.licenses = {}
        
    def load_licenses(self):
        """Load licenses from Gist"""
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(self.api_url, headers=headers)
            data = response.json()
            
            # Get content from first file
            file_content = list(data['files'].values())[0]['content']
            self.licenses = json.loads(file_content)
            
            return True
        except Exception as e:
            print(f"Error loading licenses: {e}")
            return False
    
    def validate_license(self, license_key):
        """Validate license from Gist"""
        if not self.licenses:
            self.load_licenses()
        
        license_data = self.licenses.get(license_key)
        
        if not license_data:
            return False, "License not found"
        
        # Check expiry
        expiry = license_data.get('expiry')
        if expiry and datetime.now() > datetime.strptime(expiry, '%Y-%m-%d'):
            return False, "License expired"
        
        # Check active
        if not license_data.get('active', False):
            return False, "License inactive"
        
        return True, license_data
    
    def update_license(self, license_key, updates):
        """Update license in Gist"""
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Get current content
            response = requests.get(self.api_url, headers=headers)
            data = response.json()
            
            # Update license
            file_name = list(data['files'].keys())[0]
            content = json.loads(list(data['files'].values())[0]['content'])
            
            if license_key in content:
                content[license_key].update(updates)
                
                # Update Gist
                update_data = {
                    'files': {
                        file_name: {
                            'content': json.dumps(content, indent=2)
                        }
                    }
                }
                
                requests.patch(self.api_url, headers=headers, json=update_data)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating license: {e}")
            return False
```

---

## 🚀 **Method 4: GitHub Releases as License Distribution**

### **How It Works:**

Create a **release asset** containing encrypted license keys:

1. Upload encrypted license file to GitHub Release
2. Download and decrypt in your app
3. Validate against file

### **Implementation:**

```python
class ReleaseLicenseManager:
    """License manager using GitHub Releases"""
    
    def download_license_file(self, release_tag="latest"):
        """Download license file from GitHub Release"""
        try:
            headers = {
                'Accept': 'application/vnd.github.v3.raw'
            }
            
            url = f"{self.api_url}/releases/{release_tag}"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                release_data = response.json()
                
                # Find license asset
                for asset in release_data.get('assets', []):
                    if 'license' in asset['name'].lower():
                        download_url = asset['browser_download_url']
                        
                        # Download file
                        file_response = requests.get(download_url)
                        
                        # Decrypt (implement decryption)
                        self.licenses = self.decrypt_licenses(file_response.content)
                        return True
            
            return False
            
        except Exception as e:
            print(f"Error downloading license file: {e}")
            return False
    
    def decrypt_licenses(self, encrypted_data):
        """Decrypt license file"""
        from cryptography.fernet import Fernet
        
        # Use your key
        key = b'your-encryption-key'
        f = Fernet(key)
        
        decrypted = f.decrypt(encrypted_data)
        return json.loads(decrypted)
```

---

## 🎯 **Recommended Approach: Issues + Gist**

### **Best of Both Worlds:**

1. **Issues** - For individual license management
2. **Gist** - For fast lookup (cache)
3. **Actions** - For automatic expiry/renewal

### **Complete Flow:**

```python
class HybridLicenseManager:
    """Combine multiple GitHub methods"""
    
    def __init__(self, github_token):
        self.issue_manager = GitHubLicenseManager(github_token)
        self.gist_manager = GistLicenseManager(github_token, "your-gist-id")
        
    def validate_license(self, license_key):
        """Validate using fastest method"""
        # Try Gist first (fast)
        if self.gist_manager.licenses:
            valid, data = self.gist_manager.validate_license(license_key)
            if valid:
                return valid, data
        
        # Fall back to Issues (complete)
        return self.issue_manager.validate_license(license_key)
```

---

## 📊 **Comparison**

| Method | Speed | Cost | Complexity | Speed |
|--------|-------|------|-----------|-------|
| Issues | ⭐⭐⭐ | Free | Easy | Medium |
| Secrets | ⭐⭐ | Free | Medium | Fast |
| Gist | ⭐⭐⭐⭐ | Free | Easy | **Very Fast** |
| Releases | ⭐⭐ | Free | Hard | Medium |

**Recommendation:** Use **GitHub Issues + Gist** for best balance.

---

## ✅ **Implementation Checklist**

- [ ] Create private repo for licenses
- [ ] Generate GitHub Personal Access Token
- [ ] Create license issues or Gist
- [ ] Implement `github_license_manager.py`
- [ ] Add to `main.py`
- [ ] Create activation dialog
- [ ] Test license validation
- [ ] Set up auto-expiry (Actions)
- [ ] Add renewal reminders

---

## 💰 **Cost: COMPLETELY FREE**

- GitHub Issues: Free (unlimited)
- GitHub Gists: Free (unlimited)
- GitHub Actions: Free (2000 min/month)
- GitHub API: Free (5000 requests/hour)

**Total Cost: $0/month**

---

## 🚀 **Quick Start**

1. **Create GitHub Personal Access Token:**
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Generate token with `repo` scope

2. **Create License Gist:**
   ```bash
   # Create gist-licenses.json with your license data
   ```

3. **Use in App:**
   ```python
   from github_license_manager import HybridLicenseManager
   
   manager = HybridLicenseManager(github_token="your-token")
   manager.validate_license("ABC123XYZ456")
   ```

---

**Want me to implement the complete GitHub license system for your app?**

