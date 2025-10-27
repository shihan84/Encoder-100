# 🔧 SRT Connection Rejected - Error Code 3221225477

## ❌ **Problem:**
```
Error: srt: error during srt_connect: Connection setup failure: connection rejected, reject reason: Peer rejected connection
TSDuck process finished with code: 3221225477
```

## 🎯 **Root Cause:**
The SRT server at `cdn.itassist.one:8888` is **rejecting your connection**. This is a server-side issue, NOT your configuration.

---

## ✅ **Solutions:**

### **Solution 1: Check Stream ID Format**
Your stream ID might not match what the server expects:

**Current:** `#!::r=scte/scte,m=publish`  
**Try these formats:**

1. **Without prefix:**
   ```
   r=scte/scte,m=publish
   ```

2. **Simple format:**
   ```
   scte
   ```

3. **Try without stream ID:**
   - Leave Stream ID field empty
   - Remove `--streamid` parameter

### **Solution 2: Use Distributor's SRT Endpoint**
Try using your distributor's endpoint instead:
- **Server:** `49.40.0.11:9636`
- **No stream ID needed**

Change Output Configuration:
- **Destination:** `49.40.0.11:9636`  
- **Stream ID:** Leave empty

### **Solution 3: Check SRT Server Status**
The server might be:
- Not running
- Rejecting connections temporarily
- Requiring authentication
- Using different port

### **Solution 4: Test with Manual Command**
Test the connection manually:

```cmd
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O srt --caller cdn.itassist.one:8888 --latency 2000
```

Or without stream ID:
```cmd
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O srt --caller cdn.itassist.one:8888 --latency 2000
```

---

## 🔍 **Configuration Changes:**

### **In IBE-100 v2.0.2:**

1. **Change to Distributor Endpoint:**
   - Output Type: SRT
   - **SRT Destination:** `49.40.0.11:9636`  (no srt://)
   - **Stream ID:** Leave EMPTY
   - Latency: 2000

2. **Or Try Without Stream ID:**
   - If using `cdn.itassist.one:8888`
   - **Remove/clear Stream ID field**
   - Remove `--streamid` parameter

3. **Check TSDuck Command:**
   - Click "Preview Command"
   - Should show: `-O srt --caller 49.40.0.11:9636 --latency 2000`
   - **Should NOT have** `--streamid` parameter

---

## 🎯 **Recommended Configuration:**

### **For Distributor Endpoint (49.40.0.11:9636):**
```
Output Type: SRT
Destination: 49.40.0.11:9636
Stream ID: [EMPTY]
Latency: 2000
```

### **Preview Command Should Show:**
```
... -O srt --caller 49.40.0.11:9636 --latency 2000
```

**No `--streamid` parameter!**

---

## 💡 **Quick Fix:**

1. **Open IBE-100 v2.0.2**
2. **Go to Stream Configuration tab**
3. **Change Output:**
   - SRT Destination: `49.40.0.11:9636`
   - Stream ID: [Clear this field - leave empty]
4. **Click Preview to verify**
5. **Start stream**

---

## 📞 **If Still Rejected:**

- Server is rejecting for a reason (wrong stream ID, authentication, etc.)
- Contact the server administrator
- Verify the correct endpoint and parameters
- Check if server requires authentication

---

**Remember:** The SCTE-35 Status tab issue is separate - it should work after the EXE update. The main issue here is the SRT connection being rejected by the server.

