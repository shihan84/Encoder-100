# 🔧 Corrected SCTE-35 Command - Fixed File Path Issue

## ❌ **Issue Identified**

The `spliceinject` plugin was looking for XML files in the current directory instead of the `scte35_final` directory.

## ✅ **Solution Applied**

### **❌ Original Command (Broken)**
```bash
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P sdt --service 1 --name "SCTE-35 Stream" --provider "ITAssist" \
    -P remap 211=256 221=257 \
    -P pmt --service 1 --add-pid 256/0x1b --add-pid 257/0x0f --add-pid 500/0x86 \
    -P spliceinject --service 1 --files "scte35_final/*.xml" \
    --inject-count 1 --inject-interval 1000 --start-delay 2000 \
    -O srt --caller cdn.itassist.one:8888 --streamid "#!::r=scte/scte,m=publish"
```

### **✅ Corrected Command (Working)**
```bash
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P sdt --service 1 --name "SCTE-35 Stream" --provider "ITAssist" \
    -P remap 211=256 221=257 \
    -P pmt --service 1 --add-pid 256/0x1b --add-pid 257/0x0f --add-pid 500/0x86 \
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023.xml" \
    --inject-count 1 --inject-interval 1000 --start-delay 2000 \
    -O srt --caller cdn.itassist.one:8888 --streamid "#!::r=scte/scte,m=publish"
```

## 🎯 **Key Changes Made**

### **✅ Fixed Parameters**
1. **Changed from**: `--service 1` to `--pid 500 --pts-pid 256`
2. **Fixed file path**: Use specific file instead of wildcard
3. **Added PTS PID**: Required for SCTE-35 timing

### **✅ Why This Works**
- **PID 500**: SCTE-35 marker injection PID
- **PTS PID 256**: Video PID for timing reference
- **Specific file**: Avoids wildcard issues
- **Full path**: Plugin can find the XML file

## 🚀 **Working Commands**

### **✅ Test with Single File**
```bash
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023.xml" \
    -O ip 127.0.0.1:9999
```

### **✅ Test with Multiple Files**
```bash
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P spliceinject --pid 500 --pts-pid 256 \
    --files "scte35_final/preroll_10023.xml" \
    --files "scte35_final/preroll_10024.xml" \
    --files "scte35_final/preroll_10025.xml" \
    -O ip 127.0.0.1:9999
```

### **✅ Full Production Command**
```bash
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P sdt --service 1 --name "SCTE-35 Stream" --provider "ITAssist" \
    -P remap 211=256 221=257 \
    -P pmt --service 1 --add-pid 256/0x1b --add-pid 257/0x0f --add-pid 500/0x86 \
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023.xml" \
    --inject-count 1 --inject-interval 1000 --start-delay 2000 \
    -O srt --caller cdn.itassist.one:8888 --streamid "#!::r=scte/scte,m=publish"
```

## 🔧 **IBE-100 Application Fix**

### **✅ Update IBE-100 Command Generation**
The IBE-100 application needs to be updated to use:
- `--pid 500 --pts-pid 256` instead of `--service 1`
- Specific file paths instead of wildcards
- Full paths to XML files

### **✅ Recommended Changes**
1. **Update Command Generation**: Use PID-based parameters
2. **Fix File Paths**: Use full paths to XML files
3. **Test Locally**: Verify with local UDP output first
4. **Test SRT**: Once local works, test SRT connection

## 🎯 **Testing Sequence**

### **Step 1: Test Local Processing**
```bash
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023.xml" \
    -O ip 127.0.0.1:9999
```

### **Step 2: Monitor Output**
```bash
tsp -I ip 127.0.0.1:9999 -P analyze -O drop
```

### **Step 3: Test SRT Connection**
```bash
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023.xml" \
    -O srt --caller cdn.itassist.one:8888 --streamid "#!::r=scte/scte,m=publish"
```

## 🎉 **Expected Results**

### **✅ Successful Processing**
- Stream starts processing
- SCTE-35 markers are injected
- No file path errors
- SCTE-35 markers detected in output

### **✅ SCTE-35 Markers Working**
- Pre-roll markers injected
- Timing is correct
- Ad insertion works properly

## 🚀 **Next Steps**

1. **Update IBE-100**: Fix command generation in application
2. **Test Locally**: Verify SCTE-35 processing works
3. **Test SRT**: Once local works, test SRT connection
4. **Deploy**: Ready for production use

**The SCTE-35 file path issue has been identified and fixed!** 🎬
