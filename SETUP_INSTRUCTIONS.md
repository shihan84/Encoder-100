# 🚀 IBE-100 License System - Setup Instructions

## **Quick Setup (Interactive Script)**

### **Method 1: Automated Setup (Easiest)**

Run the automated setup script:

```bash
python setup_license_system.py
```

This will:
1. ✅ Open GitHub token page
2. ✅ Open Gist creation page
3. ✅ Save your configuration
4. ✅ Test the license system

**Just follow the prompts!**

---

## **Manual Setup**

### **Step 1: Get GitHub Token**

1. Go to: https://github.com/settings/tokens
2. Click: **"Generate new token (classic)"**
3. Fill:
   - **Note:** `IBE-100 License Manager`
   - **Scopes:** Check `gist`
4. Click: **"Generate token"**
5. **COPY THE TOKEN** - you won't see it again!

---

### **Step 2: Create Gist**

1. Go to: https://gist.github.com
2. Click: **"Create a new secret gist"**
3. Fill:
   - **Description:** `IBE-100 Licenses`
   - **Filename:** `licenses.json`
   - **Content:** Copy from `licenses_template.json`
4. Click: **"Create secret gist"**
5. **COPY THE GIST ID** from the URL

---

### **Step 3: Create Config File**

Create `github_config.json`:

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

---

### **Step 4: Test**

```bash
python test_license.py
```

Expected output:
```
✅ Licenses loaded successfully
✅ TRIAL License: Valid
✅ UNLIMITED License: Valid
```

---

## **Ready to Use**

Your license system is now configured!

**Licenses available:**
- `TRIAL2024DEMO001` - 7 days trial
- `UNLIMITED2024KARTIK` - Unlimited access

**Next:** Integrate into IBE-100 app

---

## **Need Help?**

See:
- `setup_license_system.py` - Interactive setup
- `test_license.py` - Test script
- `NEXT_STEPS_DETAILED.md` - Detailed instructions

