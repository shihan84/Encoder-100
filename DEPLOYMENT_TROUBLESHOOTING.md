# 🔧 IBE-100 Deployment Troubleshooting Guide

## ❌ **Common Issue: Error Code 1 on Target Systems**

### **Problem Description**
When running IBE-100 on another system, you may encounter:
```
[ERROR] Processing failed with exit code 1
Stream stops after a few seconds
```

### **Root Cause**
**Exit code 1** typically means one of these issues:
1. ❌ **TSDuck NOT installed** on the target system (MOST COMMON)
2. ❌ **TSDuck not in system PATH**
3. ❌ **Input source not accessible** (network, permissions)
4. ❌ **Output destination permissions** issues
5. ❌ **SRT connection** rejected by server
6. ❌ **Missing dependencies** (Visual C++ redistributables on Windows)

---

## ✅ **Solution: Pre-Deployment Checklist**

### **Step 1: Install TSDuck on Target System**

**For Windows:**
```cmd
# Option 1: Download installer from official site
# https://tsduck.io/download/tsduck/

# Option 2: Use winget (if available)
winget install tsduck

# Option 3: Portable version
# 1. Download portable ZIP
# 2. Extract to C:\TSDuck\
# 3. Add to PATH: set PATH=%PATH%;C:\TSDuck\bin
```

**For Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tsduck

# CentOS/RHEL
sudo yum install epel-release
sudo yum install tsduck

# Or build from source
git clone https://github.com/tsduck/tsduck.git
cd tsduck
make
sudo make install
```

**For macOS:**
```bash
# Using Homebrew
brew install tsduck

# Or build from source
git clone https://github.com/tsduck/tsduck.git
cd tsduck
make
sudo make install
```

### **Step 2: Verify TSDuck Installation**

On the target system, run this command:
```cmd
tsp --version
```

**Expected output:**
```
tsp: TSDuck - The MPEG Transport Stream Toolkit - version 3.42-4421
```

If this fails, TSDuck is NOT installed or NOT in PATH.

### **Step 3: Verify Required Plugins**

```cmd
tsp --list-plugins | findstr /i "hls srt spliceinject pmt"
```

**Required plugins:**
- ✅ `hls` - HLS input support
- ✅ `srt` - SRT streaming
- ✅ `spliceinject` - SCTE-35 injection
- ✅ `pmt` - Program Map Table handling
- ✅ `services` - Service information
- ✅ `ip` - UDP/TCP support

### **Step 4: Test Network Connectivity**

For HLS input:
```cmd
# Test if source is accessible
curl -I https://your-source-url/index.m3u8

# Or test with tsp directly
tsp -I hls https://your-source-url/index.m3u8 -O drop
```

For SRT output:
```cmd
# Test connection (replace with your SRT server)
tsp -I file input.ts -O srt srt://your-server:8888
```

### **Step 5: Check File Permissions**

Ensure the application can:
- ✅ Read from input source
- ✅ Write to output destination
- ✅ Access SCTE-35 marker files
- ✅ Create temporary files

---

## 🎯 **Troubleshooting Error Code 1**

### **Diagnostic Steps**

1. **Check TSDuck Installation:**
   ```cmd
   # On target system
   where tsp
   tsp --version
   ```

2. **Check PATH Environment:**
   ```cmd
   # On target system
   echo %PATH%
   # Make sure TSDuck bin folder is included
   ```

3. **Test Manual Command:**
   ```cmd
   # Try running tsp manually with a simple test
   tsp -I file input.ts -O drop
   ```

4. **Check Application Logs:**
   - Look for specific error messages in console output
   - Check for "tsp not found" errors
   - Look for network connection errors

5. **Test Input Source:**
   ```cmd
   # Test HLS input
   curl -I https://your-hls-url/index.m3u8
   
   # Test UDP input
   # Use appropriate tool for your platform
   ```

---

## 📋 **System Requirements**

### **Minimum Requirements for Target Systems**

**Windows:**
- ✅ Windows 10 or later
- ✅ TSDuck 3.30+ installed
- ✅ Visual C++ 2019 Redistributable
- ✅ Network connectivity for streaming
- ✅ Admin rights (may be required for certain operations)

**Linux:**
- ✅ Ubuntu 18.04+ / Debian 9+ / CentOS 7+
- ✅ TSDuck 3.30+ installed via package manager or compiled
- ✅ Network connectivity for streaming
- ✅ Permissions for network operations

**macOS:**
- ✅ macOS 10.14+ (Mojave or later)
- ✅ TSDuck installed via Homebrew or compiled
- ✅ Network connectivity for streaming

---

## 🔧 **Quick Fix Solutions**

### **Solution 1: Install TSDuck**
Most common cause is missing TSDuck.

```cmd
# Download and install TSDuck from:
https://tsduck.io/download/tsduck/

# After installation, verify:
tsp --version
```

### **Solution 2: Add TSDuck to PATH**
If TSDuck is installed but not in PATH:

**Windows:**
```cmd
# Find where tsp.exe is installed
where /R "C:\Program Files" tsp.exe

# Add to PATH permanently
setx PATH "%PATH%;C:\Program Files\TSDuck\bin"
```

**Linux/macOS:**
```bash
# Add to PATH in ~/.bashrc or ~/.zshrc
export PATH=$PATH:/usr/local/bin
# or
export PATH=$PATH:/opt/tsduck/bin
```

### **Solution 3: Use Portable TSDuck**
Include TSDuck binaries with the application distribution:

1. **Download portable TSDuck:**
   - Download from TSDuck website
   - Extract to a folder (e.g., `tsduck_portable`)

2. **Bundle with application:**
   ```
   IBE-100_v1.5.1/
   ├── IBE-100.exe
   ├── tsduck_portable/
   │   └── bin/
   │       ├── tsp.exe
   │       └── (other binaries)
   └── launch_ibe100_v1.5.1.bat
   ```

3. **Modify launch script:**
   ```batch
   @echo off
   SETLOCAL
   
   REM Set TSDuck path relative to application
   SET "TSDUCK_BIN=%~dp0tsduck_portable\bin"
   SET PATH=%PATH%;%TSDUCK_BIN%
   
   REM Launch application
   START "" "%~dp0IBE-100.exe"
   
   ENDLOCAL
   ```

### **Solution 4: Check Input Source**
Verify the input source is accessible:

```cmd
# For HLS
curl -I https://your-hls-source/index.m3u8

# For SRT (if testing receiver)
# Use appropriate SRT testing tool

# For UDP/TCP
# Use network testing tools
```

### **Solution 5: Check Output Permissions**
Ensure the application can write to output location:

```cmd
# Try manual write test
echo test > test_output.txt
del test_output.txt

# Check network permissions for SRT/UDP output
```

---

## 🛠️ **Advanced Diagnostics**

### **Enable Debug Mode**

Add debug logging to see exactly what's failing:

1. **Check TSDuck command being executed**
   - Use "Preview Command" button in GUI
   - Run the command manually in terminal

2. **Test TSDuck command directly:**
   ```cmd
   tsp -I hls https://source-url/index.m3u8 ^
       -P sdt --service 1 --name "Test" ^
       -O drop
   ```

3. **Enable verbose TSDuck output:**
   ```cmd
   tsp --verbose -I hls https://source-url/index.m3u8 ^
       -P sdt --service 1 --name "Test" ^
       -O drop
   ```

### **Common Error Messages**

**"tsp: command not found"**
- TSDuck not installed or not in PATH
- Solution: Install TSDuck or add to PATH

**"No such file or directory"**
- Input file/source not found
- Solution: Check source URL/path

**"Permission denied"**
- Insufficient permissions for output
- Solution: Run as administrator or fix permissions

**"Connection refused"**
- SRT server not accepting connections
- Solution: Check SRT server configuration

**"PID conflict"**
- Multiple streams conflicting
- Solution: Adjust PID configuration

---

## 📞 **Getting Help**

If none of these solutions work:

1. **Collect Information:**
   - Exact error message
   - TSDuck version (`tsp --version`)
   - Operating system version
   - Input source type (HLS, SRT, etc.)
   - Output destination type

2. **Test Basic TSDuck:**
   ```cmd
   tsp --version
   tsp --list-plugins
   tsp -I hls https://test-stream/index.m3u8 -O drop
   ```

3. **Contact Support:**
   - support@itassist.one
   - Include all collected information
   - Include error logs

---

## ✅ **Pre-Deployment Checklist**

Before deploying to target systems:

- [ ] TSDuck installed and verified (`tsp --version`)
- [ ] Required plugins available (`tsp --list-plugins`)
- [ ] Network connectivity tested
- [ ] Input source accessible
- [ ] Output destination accessible
- [ ] File permissions correct
- [ ] SCTE-35 marker files available
- [ ] Application starts without errors
- [ ] Test stream runs successfully for at least 1 minute
- [ ] Console shows no error messages during test

---

## 🎯 **Quick Reference: Common Exit Codes**

| Exit Code | Meaning | Solution |
|-----------|---------|----------|
| 0 | Success | Everything working correctly |
| 1 | General error | Check TSDuck installation, input source, permissions |
| 2 | Configuration error | Check application settings |
| 3 | Network error | Check network connectivity and SRT server |
| -1073741819 | Access violation | Check permissions and dependencies |

---

**Remember: Most error code 1 issues are caused by missing TSDuck installation!**

