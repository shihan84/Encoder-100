# 🔧 TSDuck Installation and Setup Guide

## ✅ **Current Status**

**Good News!** TSDuck is already installed on your system:
- **Version**: 3.42-4421
- **Status**: Ready to use with IBE-100

## 🎯 **What is TSDuck?**

TSDuck is the **core engine** that powers the IBE-100 application. It handles:
- **Stream Processing**: HLS, SRT, UDP, TCP input/output
- **SCTE-35 Markers**: Injection and processing of ad insertion cues
- **Transport Stream Analysis**: Real-time monitoring and analysis
- **Format Conversion**: Between different streaming protocols

## 📋 **TSDuck Requirements for IBE-100**

### **✅ Already Installed**
- **TSDuck Version**: 3.42-4421 ✓
- **Command Line Tools**: `tsp`, `tsanalyze`, `tspsi` ✓
- **Plugin Support**: All required plugins ✓

### **🔧 Required TSDuck Plugins**
The following plugins are needed for IBE-100:

1. **Input Plugins**:
   - `hls` - HLS stream input
   - `ip` - UDP/TCP input
   - `file` - File input

2. **Output Plugins**:
   - `srt` - SRT streaming output
   - `ip` - UDP/TCP output
   - `file` - File output

3. **Processing Plugins**:
   - `spliceinject` - SCTE-35 marker injection
   - `analyze` - Stream analysis
   - `pmt` - Program Map Table handling
   - `services` - Service information
   - `pids` - PID management

## 🚀 **Testing TSDuck Installation**

### **Test 1: Basic TSDuck Functionality**
```cmd
tsp --version
```
**Expected Output**: `tsp: TSDuck - The MPEG Transport Stream Toolkit - version 3.42-4421`

### **Test 2: Plugin Availability**
```cmd
tsp --list-plugins
```
**Expected Output**: List of available plugins including `hls`, `srt`, `spliceinject`, etc.

### **Test 3: SCTE-35 Plugin Test**
```cmd
tsp --help | findstr spliceinject
```
**Expected Output**: Information about the spliceinject plugin

## 🔧 **TSDuck Configuration for IBE-100**

### **Required Environment Variables**
```cmd
# Set TSDuck path (if not in system PATH)
set TSDUCK_HOME=C:\Program Files\TSDuck
set PATH=%PATH%;%TSDUCK_HOME%\bin
```

### **Plugin Path Configuration**
```cmd
# Set plugin path
set TSDUCK_PLUGIN_PATH=%TSDUCK_HOME%\bin
```

## 📊 **IBE-100 Integration with TSDuck**

### **How IBE-100 Uses TSDuck**

1. **Stream Processing**:
   ```bash
   tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
       -P spliceinject --pid 500 --files 'scte35_final/preroll_*.xml' \
       -O srt --caller cdn.itassist.one:8888
   ```

2. **SCTE-35 Marker Injection**:
   - Uses `spliceinject` plugin
   - Injects XML marker files
   - Handles PID 500 for SCTE-35

3. **Stream Analysis**:
   - Uses `analyze` plugin for monitoring
   - Real-time stream statistics
   - SCTE-35 marker detection

## 🎯 **Professional SCTE-35 Workflow**

### **Step 1: Generate SCTE-35 Markers**
1. **Launch IBE-100**: `.\dist\IBE-100.exe`
2. **Go to SCTE-35 Tab**: Click "[TOOL] SCTE-35 Professional"
3. **Generate Markers**: Use Quick Actions or Professional Templates
4. **Markers Saved**: XML files in `scte35_final/` directory

### **Step 2: Use with TSDuck**
```bash
# Basic SCTE-35 injection
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P spliceinject --pid 500 --files 'scte35_final/preroll_*.xml' \
    -O srt --caller cdn.itassist.one:8888 \
    --streamid "#!::r=scte/scte,m=publish" \
    --latency 2000
```

### **Step 3: Monitor Output**
```bash
# Monitor SCTE-35 markers
tsp -I ip 127.0.0.1:9999 -P analyze -O drop
```

## 🔧 **Troubleshooting TSDuck Issues**

### **Common Issues and Solutions**

1. **"tsp is not recognized"**:
   ```cmd
   # Add TSDuck to PATH
   set PATH=%PATH%;C:\Program Files\TSDuck\bin
   ```

2. **Plugin not found**:
   ```cmd
   # Check plugin path
   tsp --list-plugins
   ```

3. **SCTE-35 injection fails**:
   ```cmd
   # Verify XML marker files
   dir scte35_final\*.xml
   ```

## 📋 **TSDuck Installation Options**

### **Option 1: Windows Installer (Recommended)**
1. **Download**: https://tsduck.io/download/tsduck/
2. **Install**: Run the Windows installer
3. **Verify**: `tsp --version`

### **Option 2: Portable Version**
1. **Download**: Portable ZIP from TSDuck website
2. **Extract**: To `C:\TSDuck\`
3. **Add to PATH**: `C:\TSDuck\bin`

### **Option 3: Build from Source**
1. **Requirements**: Visual Studio, CMake
2. **Clone**: TSDuck repository
3. **Build**: Follow build instructions

## ✅ **Verification Checklist**

- [x] **TSDuck Installed**: Version 3.42-4421 ✓
- [x] **Command Available**: `tsp --version` works ✓
- [x] **Plugins Available**: All required plugins present ✓
- [x] **IBE-100 Compatible**: Ready for integration ✓

## 🎉 **Ready for Production**

Your TSDuck installation is **ready for production use** with IBE-100:

1. **✅ TSDuck Installed**: Version 3.42-4421
2. **✅ All Plugins Available**: HLS, SRT, SCTE-35 support
3. **✅ IBE-100 Compatible**: Professional SCTE-35 interface
4. **✅ Production Ready**: Full streaming capabilities

**Your TSDuck installation is complete and ready for professional broadcast operations!** 🚀

## 🚀 **Next Steps**

1. **Launch IBE-100**: `.\dist\IBE-100.exe`
2. **Generate SCTE-35 Markers**: Use the professional interface
3. **Test with TSDuck**: Use generated markers in your stream
4. **Monitor Output**: Verify SCTE-35 markers are working

**Everything is ready for professional SCTE-35 streaming!** 🎬
