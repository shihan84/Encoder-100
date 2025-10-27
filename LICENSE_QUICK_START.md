# 🚀 IBE-100 License System - Quick Start

## ✅ **What You Have:**

1. **Trial License:** `TRIAL2024DEMO001` (7 days)
2. **Unlimited License:** `UNLIMITED2024KARTIK` (no expiry)

---

## 🎯 **Setup (5 Minutes)**

### **1. Get GitHub Token:**
1. Go to: https://github.com/settings/tokens
2. Click: "Generate new token (classic)"
3. Check: `gist` scope
4. Copy token

### **2. Create Gist:**
1. Go to: https://gist.github.com
2. Paste contents from `licenses_template.json`
3. Create **secret** gist
4. Copy Gist ID from URL

### **3. Configure:**
Create `github_config.json`:
```json
{
  "token": "your-github-token",
  "gist_id": "your-gist-id"
}
```

### **4. Test:**
```bash
python test_license.py
```

---

## 📦 **Files Included:**

- ✅ `github_license_manager.py` - License management
- ✅ `licenses_template.json` - Sample licenses
- ✅ `github_config.json` - Your config (create this)
- ✅ `setup_github_licenses.md` - Detailed guide

---

## 🎫 **License Types:**

### **Trial (7 days):**
- ⏱️ 1 hour session limit
- 🔒 Basic features only
- ⏰ Expires after 7 days

### **Unlimited:**
- ✅ No session limit
- ✅ All features
- ✅ Never expires

---

## 🔐 **Security:**

- Licenses stored in **secret Gist**
- Validated via GitHub API
- Trial restrictions enforced
- Session timer for trials

---

## 📞 **Need Help?**

See: `setup_github_licenses.md` for detailed instructions.

