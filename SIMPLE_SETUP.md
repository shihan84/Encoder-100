# ⚡ Simple Setup Guide

## **Just 3 Steps:**

### **1. Create GitHub Token** (5 minutes)
1. Go to: https://github.com/settings/tokens
2. Generate new token
3. Check `gist` scope
4. Copy token

### **2. Create Gist** (3 minutes)
1. Go to: https://gist.github.com
2. Create secret gist
3. Copy contents from `licenses_template.json`
4. Copy Gist ID from URL

### **3. Save Config**
Create `github_config.json`:

```json
{
  "token": "paste-your-token-here",
  "gist_id": "paste-your-gist-id-here"
}
```

**Done!** ✅

---

## **Test:**

```bash
python test_license.py
```

---

## **That's It!** 🎉

Now you have:
- ✅ Trial license: `TRIAL2024DEMO001` (7 days)
- ✅ Unlimited license: `UNLIMITED2024KARTIK` (unlimited)

**Next:** Integrate into IBE-100 app

