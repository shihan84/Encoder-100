# 🔧 Distributor SRT Connection Fix

## ❌ **Problem**
- **Endpoint:** `srt://49.40.0.11:9636`
- **Error:** "SRT IP not found" or "process finished with code 1"
- **No Stream ID** - Endpoint doesn't require stream ID

---

## ✅ **Solution: Correct SRT Syntax**

### **In IBE-100 v2.0.2 Configuration:**

#### **Input Configuration (if receiving from distributor):**
- **Input Type:** SRT (Secure Reliable Transport)
- **Stream URL:** `49.40.0.11:9636`  ← **NO srt:// prefix**
- **Note:** Connection will be in LISTENER mode (passive)

#### **Output Configuration (if sending to distributor):**
- **Output Type:** SRT
- **Destination:** `49.40.0.11:9636` ← **NO srt:// prefix**
- **Note:** Connection will be in CALLER mode (active)

---

## 🔧 **For IBE-100 v2.0.2:**

### **Step 1: Stream Configuration Tab**
1. **Input Type:** Your input (HLS, SRT, etc.)
2. **Output Type:** SRT
3. **Destination:** `49.40.0.11:9636` (without srt://)
4. **Latency:** 2000ms (recommended)
5. **Stream ID:** Leave empty (not required)

### **Step 2: Service Configuration**
- **Service Name:** Your service name
- **Service Provider:** Your provider
- **Service ID:** 1 (or your ID)
- **Video PID:** 256
- **Audio PID:** 257
- **SCTE-35 PID:** 500

### **Step 3: Start Stream**
- Click "Preview Command" to check syntax
- Click "Start Stream"
- Check console for connection status

---

## 📋 **Troubleshooting**

### **Error: "SRT IP not found"**
**Cause:** Invalid hostname or IP address  
**Solution:** Verify IP is correct: `49.40.0.11`

### **Error: "Connection refused"**
**Cause:** Server not accepting connections on port 9636  
**Solution:** 
- Check firewall rules
- Verify server is running
- Test with: `telnet 49.40.0.11 9636`

### **Error: "Process finished with code 1"**
**Cause:** SRT connection failure  
**Solution:**
- Run `test_distributor_srt.bat` to diagnose
- Check if server requires authentication
- Verify TSDuck is installed: `tsp --version`

---

## 🧪 **Test Connection Manually**

Run this to test the SRT connection:
```cmd
tsp -I null -O srt 49.40.0.11:9636 --caller --latency 2000
```

**Expected:** Connection establishes or shows specific error

**If connection fails:**
1. Check if server is listening on port 9636
2. Check firewall settings
3. Verify network path to server
4. Contact distributor for support

---

## 🔍 **Check Your Configuration**

### **In IBE-100 v2.0.2:**

1. **Stream Configuration Tab:**
   ```
   Output Type: SRT
   Destination: 49.40.0.11:9636
   Latency: 2000
   ```

2. **Preview Command Button:**
   Should show:
   ```
   tsp -I <input> ... -O srt 49.40.0.11:9636 --caller --latency 2000
   ```

3. **Console Output:**
   Watch for:
   ```
   Connecting to SRT server 49.40.0.11:9636...
   [OK] Connected successfully
   ```

---

## 📞 **Need More Help?**

If issues persist:
1. Run `diagnose_system.bat` from dist_final folder
2. Check console output for specific error messages
3. Contact support@itassist.one
4. Provide:
   - Exact error message
   - Network test results
   - TSDuck version: `tsp --version`

---

**Remember:** Remove `srt://` prefix when entering the address!  
Use: `49.40.0.11:9636`  
Not: `srt://49.40.0.11:9636`

