# 🎬 Stream to Distributor Endpoint Configuration

## ✅ **Working Configuration**

### **Server Details:**
- **Endpoint:** `srt://49.40.0.11:9636`
- **No Stream ID Required**
- **Mode:** CALLER (active connection)

---

## ⚙️ **IBE-100 v2.0.2 Configuration**

### **Step 1: Stream Configuration Tab**

**Input Configuration:**
- **Input Type:** HLS (HTTP Live Streaming)
- **Input URL:** `https://cdn.itassist.one/BREAKING/NEWS/index.m3u8`
  - Or your actual source URL

**Output Configuration:**
- **Output Type:** SRT
- **SRT Destination:** `49.40.0.11:9636` ← **NO srt:// prefix, NO stream ID**
- **Stream ID:** [LEAVE EMPTY]
- **Latency:** 2000 ms

**Service Configuration:**
- **Service Name:** Your service name
- **Provider:** Your provider name
- **Service ID:** 1
- **Video PID:** 256
- **Audio PID:** 257
- **SCTE-35 PID:** 500

### **Step 2: SCTE-35 Tab**

1. **Select Cue Type:** Pre-roll
2. **Configure:**
   - Pre-roll Duration: 5
   - Ad Duration: 30
   - Event ID: 10023
3. **Click "Generate"**
4. Wait for: `[INFO] Marker generated: ...`

### **Step 3: Start Stream**

1. Click **"Preview Command"** to verify
2. Should show:
   ```
   ... -O srt 49.40.0.11:9636 --caller --latency 2000
   ```
   **No `--streamid` parameter!**
3. Click **"Start Stream"**
4. Check Console for connection status

---

## 📋 **Expected Console Output**

### **Success:**
```
[INFO] Starting processing...
[INFO] Using marker: scte35_final\preroll_10023_[timestamp].xml
[TSDuck] Connecting to SRT 49.40.0.11:9636...
[TSDuck] Connected successfully
[TSDuck] Processing stream...
```

### **Connection Error:**
```
[TSDuck] * Error: srt: error during srt_connect...
```

**If you see this:**
- Server might not be accepting connections
- Check with distributor support
- Verify server is running and accessible

---

## 🔍 **Troubleshooting**

### **Error: "Connection rejected"**
- Server at 49.40.0.11:9636 not accepting connections
- Check server status with distributor
- Verify firewall allows traffic to port 9636

### **Error: "SRT IP not found"**
- Remove `srt://` prefix from address
- Use: `49.40.0.11:9636`
- Not: `srt://49.40.0.11:9636`

### **Error: "Process finished with code 1"**
- TSDuck not installed or not in PATH
- Run: `tsp --version` to verify
- Install TSDuck if missing

---

## ✅ **Working Command Structure**

The TSDuck command will be:
```
tsp -I hls <your-hls-url> \
    -P sdt --service 1 --name "Your Name" --provider "Your Provider" \
    -P remap 211=256 221=257 \
    -P pmt --service 1 --add-pid 256/0x1b --add-pid 257/0x0f --add-pid 500/0x86 \
    -P spliceinject --pid 500 --pts-pid 256 --files scte35_final\*.xml \
    --inject-count 1 --inject-interval 1000 --start-delay 2000 \
    -O srt 49.40.0.11:9636 --caller --latency 2000
```

**Key differences:**
- ✅ `49.40.0.11:9636` - direct IP:port (no srt://)
- ✅ `--caller` - active connection mode
- ✅ `--latency 2000` - 2 second latency
- ✅ NO `--streamid` parameter

---

## 🎯 **Test Your Configuration**

1. **Change Output to Distributor:**
   - Destination: `49.40.0.11:9636`
   - Stream ID: [empty]

2. **Click Preview Command:**
   - Verify no `--streamid` appears
   - Verify `--caller` is present
   - Verify `--latency 2000` is present

3. **Start Stream:**
   - Look for connection success in Console
   - Should not show "reject reason: Peer rejected"

4. **Monitor SCTE-35 Status:**
   - Should show markers injected
   - Stream markers detected

---

## 📞 **If Issues Persist**

**Contact Distributor:**
- Verify server is running on 49.40.0.11:9636
- Check if authentication required
- Verify correct IP address
- Check if firewall allows connections

**Verify Network:**
```cmd
ping 49.40.0.11
telnet 49.40.0.11 9636
```

---

**Now try the stream! The configuration should work with the distributor endpoint.**

