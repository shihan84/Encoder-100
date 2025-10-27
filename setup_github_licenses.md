# 🔐 Setup GitHub Licenses - Step by Step

## 📋 **Quick Setup Guide**

Follow these steps to set up your license system.

---

## ✅ **Step 1: Create GitHub Personal Access Token**

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name: `IBE-100 License Manager`
4. Scopes needed:
   - ✅ `gist` - Create and update Gists
   - ✅ `repo` - Read repository data
5. Click **"Generate token"**
6. **COPY THE TOKEN** - you won't see it again!

---

## ✅ **Step 2: Create License Gist**

### **Option A: Via GitHub Website**

1. Go to https://gist.github.com
2. Click **"Create a new secret gist"**
3. Filename: `licenses.json`
4. Paste this content:

```json
{
  "TRIAL2024DEMO001": {
    "user": "Demo User",
    "email": "demo@example.com",
    "tier": "trial",
    "expiry": "2024-12-31",
    "active": true,
    "created": "2024-01-15",
    "restrictions": {
      "max_days": 7,
      "session_hours": 1,
      "features": ["basic_streaming", "limited_markers"]
    }
  },
  "UNLIMITED2024KARTIK": {
    "user": "Kartik",
    "email": "kartik@example.com",
    "tier": "unlimited",
    "expiry": "2099-12-31",
    "active": true,
    "created": "2024-01-15",
    "restrictions": {
      "max_days": null,
      "session_hours": null,
      "features": ["all_features"]
    }
  }
}
```

5. Click **"Create secret gist"**
6. **SAVE THE GIST ID** from the URL: `https://gist.github.com/your-username/GIST-ID-HERE`
   - The GIST ID is the last part of the URL

---

## ✅ **Step 3: Configure License Manager**

### **Create `github_config.json`:**

```json
{
  "token": "your-github-token-here",
  "gist_id": "your-gist-id-here"
}
```

**Example:**
```json
{
  "token": "ghp_abc123def456ghi789jkl012mno345pqr678",
  "gist_id": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
}
```

**IMPORTANT:** Keep this file **SECRET** - don't commit to GitHub!

---

## ✅ **Step 4: Add to IBE-100 App**

Update `github_license_manager.py`:

```python
def __init__(self):
    self.license_file = Path("license.json")
    self.github_token = self.get_github_token()
    self.gist_id = "YOUR-GIST-ID-HERE"  # <-- UPDATE THIS
```

---

## ✅ **Step 5: Test License System**

### **Test Script:**

Create `test_license.py`:

```python
from github_license_manager import GitHubLicenseManager

# Initialize
manager = GitHubLicenseManager()

# Test Trial License
print("\n=== Testing TRIAL License ===")
valid, message = manager.validate_license("TRIAL2024DEMO001")
print(f"Valid: {valid}")
print(f"Message: {message}")

# Test Unlimited License
print("\n=== Testing UNLIMITED License ===")
valid, message = manager.validate_license("UNLIMITED2024KARTIK")
print(f"Valid: {valid}")
print(f"Message: {message}")

# Activate a license
print("\n=== Activating License ===")
success, msg = manager.activate_license("TRIAL2024DEMO001", "test@example.com")
print(f"Success: {success}")
print(f"Message: {msg}")

print("\n✅ License system test complete!")
```

Run:
```bash
python test_license.py
```

---

## 🎫 **Creating New Licenses**

### **Trial License (7 days):**

```json
{
  "TRIAL2024DEMO002": {
    "user": "John Doe",
    "email": "john@example.com",
    "tier": "trial",
    "expiry": "2024-12-31",
    "active": true,
    "created": "2024-12-15",
    "restrictions": {
      "max_days": 7,
      "session_hours": 1,
      "features": ["basic_streaming"]
    }
  }
}
```

**License Key:** `TRIAL2024DEMO002`  
**Duration:** 7 days  
**Restrictions:**
- ⏱️ 1 hour session limit
- 🚫 Can't use after 7 days
- 📊 Limited features

---

### **Monthly License:**

```json
{
  "MONTHLY2024USER001": {
    "user": "Jane Smith",
    "email": "jane@example.com",
    "tier": "monthly",
    "expiry": "2025-01-15",
    "active": true,
    "created": "2024-12-15",
    "restrictions": {
      "max_days": 30,
      "session_hours": null,
      "features": ["all_features"]
    }
  }
}
```

**License Key:** `MONTHLY2024USER001`  
**Duration:** 30 days  
**Restrictions:**
- ⏱️ No session limit
- ✅ All features
- 🔄 Renews monthly

---

### **Unlimited License (No Restrictions):**

```json
{
  "UNLIMITED2024USER002": {
    "user": "Special User",
    "email": "special@example.com",
    "tier": "unlimited",
    "expiry": "2099-12-31",
    "active": true,
    "created": "2024-12-15",
    "restrictions": {
      "max_days": null,
      "session_hours": null,
      "features": ["all_features", "premium_support"]
    }
  }
}
```

**License Key:** `UNLIMITED2024USER002`  
**Duration:** Unlimited (until revoked)  
**Restrictions:**
- ✅ No restrictions
- ✅ All features
- ✅ Lifetime access

---

## 🔐 **Security Features**

### **Trial License Restrictions:**

1. **Time Limit:** 7 days from activation
2. **Session Limit:** 1 hour per session (app closes after 1 hour)
3. **No Advanced Features:** Limited to basic streaming
4. **Auto-Expiry:** License becomes invalid after 7 days

### **How Session Limit Works:**

- When app starts: Session timer starts
- After 1 hour: App warns user
- After 1h 5min: App forces close

**Session file:** `session_start.json` stores start time

```json
{
  "start": "2024-12-15T10:30:00"
}
```

---

## 📝 **License Key Format**

### **Recommended Format:**

```
[TYPE][YEAR][CUSTOMER][NUMBER]
```

**Examples:**
- `TRIAL2024KARTIK001` - Trial license for Kartik in 2024
- `MONTHLY2024CLIENT01` - Monthly license for Client01 in 2024
- `UNLIMITED2024DEV999` - Unlimited license for Developer in 2024

---

## 🔄 **Adding New License Steps**

1. **Edit your Gist:**
   - Go to https://gist.github.com/YOUR-USERNAME/YOUR-GIST-ID
   - Click **Edit** button
   - Add new license entry
   - Click **Update secret gist**

2. **Test the new license:**
   ```bash
   python test_license.py
   ```

3. **Send license key to customer:**
   ```
   Subject: Your IBE-100 License
   
   Your license key: TRIAL2024USER001
   Tier: Trial (7 days)
   
   Activate in the app to get started!
   ```

---

## ⚙️ **Configuration Options**

### **Environment Variable:**
```bash
export GITHUB_TOKEN="your-token-here"
```

### **Config File:**
Create `github_config.json`:
```json
{
  "token": "your-token",
  "gist_id": "your-gist-id"
}
```

### **Inline Configuration:**
Update `github_license_manager.py`:
```python
self.gist_id = "your-gist-id-here"
self.github_token = "your-token-here"
```

---

## 🧪 **Testing Checklist**

- [ ] Create GitHub token
- [ ] Create secret Gist
- [ ] Add trial license
- [ ] Add unlimited license
- [ ] Test validation
- [ ] Test activation
- [ ] Test expiry
- [ ] Test session limit
- [ ] Test restrictions

---

## ✅ **Done!**

Your license system is now set up!

**Files created:**
- ✅ `github_license_manager.py` - License manager
- ✅ `github_config.json` - Configuration
- ✅ `license.json` - Local license file
- ✅ `session_start.json` - Session timer

**Next:** Integrate into IBE-100 app!

