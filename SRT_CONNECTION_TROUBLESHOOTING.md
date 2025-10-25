# 🔧 SRT Connection Troubleshooting Guide

## ❌ **Connection Issue Identified**

The SRT connection to `cdn.itassist.one:8888` is being **rejected by the server**. This is a common SRT connection issue that can be resolved.

## 🎯 **Error Analysis**

### **❌ Current Error**
```
SRT.cn: @327809385: processConnectResponse: rejecting per reception of a rejection HS response: ERROR:PEER
* Error: srt: error during srt_connect: Connection setup failure: connection rejected, reject reason: Peer rejected connection
```

### **🔍 Root Causes**
1. **SRT Server Configuration**: Server may not be accepting connections
2. **Authentication Issues**: Missing or incorrect credentials
3. **Network Configuration**: Firewall or network issues
4. **SRT Parameters**: Incorrect SRT connection parameters

## 🚀 **Solution 1: Test with Local UDP First**

### **✅ Local Testing Command**
```bash
# Test locally with UDP output first
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P sdt --service 1 --name "SCTE-35 Stream" --provider "ITAssist" \
    -P remap 211=256 221=257 \
    -P pmt --service 1 --add-pid 256/0x1b --add-pid 257/0x0f --add-pid 500/0x86 \
    -P spliceinject --service 1 --files "scte35_final/*.xml" \
    --inject-count 1 --inject-interval 1000 --start-delay 2000 \
    -O ip 127.0.0.1:9999
```

### **✅ Monitor Local Output**
```bash
# Monitor the local output
tsp -I ip 127.0.0.1:9999 -P analyze -O drop
```

## 🚀 **Solution 2: SRT Connection Parameters**

### **✅ Enhanced SRT Command**
```bash
# Try with additional SRT parameters
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P sdt --service 1 --name "SCTE-35 Stream" --provider "ITAssist" \
    -P remap 211=256 221=257 \
    -P pmt --service 1 --add-pid 256/0x1b --add-pid 257/0x0f --add-pid 500/0x86 \
    -P spliceinject --service 1 --files "scte35_final/*.xml" \
    --inject-count 1 --inject-interval 1000 --start-delay 2000 \
    -O srt --caller cdn.itassist.one:8888 \
    --streamid "#!::r=scte/scte,m=publish" \
    --latency 2000 \
    --rcvbuf 10000000 \
    --sndbuf 10000000 \
    --transtype live
```

## 🚀 **Solution 3: Alternative SRT Parameters**

### **✅ Different SRT Configuration**
```bash
# Try with different SRT settings
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P sdt --service 1 --name "SCTE-35 Stream" --provider "ITAssist" \
    -P remap 211=256 221=257 \
    -P pmt --service 1 --add-pid 256/0x1b --add-pid 257/0x0f --add-pid 500/0x86 \
    -P spliceinject --service 1 --files "scte35_final/*.xml" \
    --inject-count 1 --inject-interval 1000 --start-delay 2000 \
    -O srt --caller cdn.itassist.one:8888 \
    --streamid "#!::r=scte/scte,m=publish" \
    --latency 2000 \
    --transtype file \
    --rcvbuf 1000000 \
    --sndbuf 1000000
```

## 🚀 **Solution 4: Test SRT Connection**

### **✅ Test SRT Connection First**
```bash
# Test basic SRT connection
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -O srt --caller cdn.itassist.one:8888 \
    --streamid "#!::r=scte/scte,m=publish" \
    --latency 2000
```

## 🔧 **Troubleshooting Steps**

### **Step 1: Verify SRT Server Status**
```bash
# Check if SRT server is accessible
telnet cdn.itassist.one 8888
```

### **Step 2: Test Basic SRT Connection**
```bash
# Test minimal SRT connection
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -O srt --caller cdn.itassist.one:8888
```

### **Step 3: Test with Different Parameters**
```bash
# Try different SRT parameters
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -O srt --caller cdn.itassist.one:8888 \
    --streamid "#!::r=scte/scte,m=publish" \
    --latency 2000 \
    --transtype live
```

## 🎯 **Common SRT Issues and Solutions**

### **✅ Issue 1: Connection Rejected**
**Cause**: Server not accepting connections
**Solution**: Check server status, try different parameters

### **✅ Issue 2: Authentication Required**
**Cause**: Server requires authentication
**Solution**: Add authentication parameters

### **✅ Issue 3: Network Issues**
**Cause**: Firewall or network problems
**Solution**: Check network connectivity

### **✅ Issue 4: SRT Version Mismatch**
**Cause**: Different SRT versions
**Solution**: Try different SRT parameters

## 🚀 **Recommended Testing Sequence**

### **Step 1: Test Local Output**
```bash
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P spliceinject --service 1 --files "scte35_final/*.xml" \
    -O ip 127.0.0.1:9999
```

### **Step 2: Test Basic SRT**
```bash
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -O srt --caller cdn.itassist.one:8888
```

### **Step 3: Test with SCTE-35**
```bash
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P spliceinject --service 1 --files "scte35_final/*.xml" \
    -O srt --caller cdn.itassist.one:8888 \
    --streamid "#!::r=scte/scte,m=publish"
```

## 📋 **SRT Connection Checklist**

- [ ] **Test Local Output**: Verify stream processing works locally
- [ ] **Test Basic SRT**: Verify SRT connection works
- [ ] **Test with SCTE-35**: Verify SCTE-35 injection works
- [ ] **Check Server Status**: Verify SRT server is accessible
- [ ] **Try Different Parameters**: Test various SRT configurations

## 🎉 **Expected Results**

### **✅ Successful Connection**
- Stream starts processing
- SCTE-35 markers are injected
- No connection errors

### **✅ SCTE-35 Markers Working**
- Markers are detected in output
- Pre-roll timing is correct
- Ad insertion works properly

## 🚀 **Next Steps**

1. **Test Local Output**: Verify stream processing works
2. **Test Basic SRT**: Verify SRT connection works
3. **Test with SCTE-35**: Verify SCTE-35 injection works
4. **Contact Distributor**: If SRT server issues persist

**The SRT connection issue can be resolved with proper testing and parameter adjustment!** 🎬
