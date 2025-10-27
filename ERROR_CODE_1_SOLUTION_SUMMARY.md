# 🔧 Error Code 1 Solution Summary

## Problem
When running IBE-100 on another system, you get **Error Code 1** and the stream stops.

Since TSDuck is already installed on your system, the issue is likely one of these:

## Most Common Causes (with TSDuck installed)

### 1. **TSDuck Not in System PATH on Target System**
The target system may have TSDuck installed but not in the PATH, so the app can't find `tsp.exe`.

**Solution:**
```cmd
# On the target system, check:
tsp --version

# If it fails, add to PATH:
set PATH=%PATH%;C:\Program Files\TSDuck\bin

# Or permanently add via:
# Control Panel → System → Environment Variables → PATH
```

### 2. **Input Source Not Accessible**
The HLS/network source might not be reachable from the target system.

**Solution:**
```cmd
# Test connectivity from target system:
curl -I https://your-source-url/index.m3u8

# Or test with TSDuck:
tsp -I hls https://your-source/index.m3u8 -O drop
```

### 3. **SRT Connection Issues**
If using SRT output, the server might be rejecting connections.

**Solution:**
```cmd
# Verify SRT server is accessible:
# Check firewall rules
# Verify SRT server is running
# Test with manual command:
tsp -I file input.ts -O srt srt://your-server:port
```

### 4. **Missing Configuration Files**
The `gui_working_config.json` or `scte35_final` folder might be missing.

**Solution:**
- First run of IBE-100 creates these automatically
- If missing, run the GUI once and configure

### 5. **Firewall/Antivirus Blocking**
Security software might be blocking TSDuck connections.

**Solution:**
- Add exception for TSDuck in Windows Defender
- Add exception for IBE-100.exe
- Check firewall rules for network ports

## New Tools I Created

### 1. **diagnose_system.bat** ✅
**Location:** `dist/IBE-100_v1.5.1/diagnose_system.bat`

Quick Windows batch file to check:
- ✅ TSDuck installation
- ✅ Python installation
- ✅ SCTE-35 folder
- ✅ Network connectivity
- ✅ Configuration files

**How to use:**
```cmd
cd dist\IBE-100_v1.5.1
diagnose_system.bat
```

### 2. **diagnose_error.py** ✅
**Location:** Root directory (`diagnose_error.py`)

Detailed Python diagnostic that checks:
- ✅ TSDuck in PATH
- ✅ TSDuck execution
- ✅ Input source configuration
- ✅ SCTE-35 markers
- ✅ Network connectivity
- ✅ Output configuration

**How to use:**
```cmd
python diagnose_error.py
```

### 3. **check_system_requirements.py** ✅
**Location:** Root directory (`check_system_requirements.py`)

Comprehensive requirements checker that verifies:
- ✅ Python version
- ✅ TSDuck installation
- ✅ All required plugins
- ✅ Network connectivity
- ✅ File permissions
- ✅ SCTE-35 configuration

**How to use:**
```cmd
python check_system_requirements.py
```

### 4. **Updated launch_ibe100_v1.5.1.bat** ✅
**Location:** `dist/IBE-100_v1.5.1/launch_ibe100_v1.5.1.bat`

Now includes:
- ✅ Pre-launch TSDuck check
- ✅ Warning if TSDuck not found
- ✅ Helpful error messages
- ✅ System requirements verification

### 5. **README_DEPLOYMENT.md** ✅
**Location:** `dist/IBE-100_v1.5.1/README_DEPLOYMENT.md`

Complete deployment guide with:
- ✅ Troubleshooting steps
- ✅ Common solutions
- ✅ Diagnostic procedures
- ✅ Quick reference

### 6. **DEPLOYMENT_TROUBLESHOOTING.md** ✅
**Location:** Root directory (`DEPLOYMENT_TROUBLESHOOTING.md`)

Comprehensive troubleshooting guide with:
- ✅ Detailed error analysis
- ✅ Pre-deployment checklist
- ✅ Platform-specific instructions
- ✅ Quick fix solutions
- ✅ Advanced diagnostics

## How to Use These Tools

### On the Original System (Development)
1. ✅ Run diagnostics to verify everything works
2. ✅ Check TSDuck is properly installed
3. ✅ Test a sample stream to ensure functionality

### On the Target System (Deployment)
1. **Before First Launch:**
   ```cmd
   # Copy these files to target system:
   - diagnose_system.bat
   - README_DEPLOYMENT.md
   - check_system_requirements.py
   - diagnose_error.py
   ```

2. **Run Diagnostics:**
   ```cmd
   # Quick check:
   diagnose_system.bat
   
   # Detailed check (if Python available):
   python diagnose_error.py
   python check_system_requirements.py
   ```

3. **Fix Issues Found:**
   - Install TSDuck if missing
   - Add to PATH if needed
   - Fix network connectivity
   - Configure firewall

4. **Launch Application:**
   ```cmd
   launch_ibe100_v1.5.1.bat
   ```

## Step-by-Step Troubleshooting

### Step 1: Check TSDuck
```cmd
# On target system:
tsp --version

# Expected: Shows TSDuck version
# If fails: Install TSDuck from https://tsduck.io/download/
```

### Step 2: Check TSDuck in PATH
```cmd
# On target system:
where tsp

# Expected: Shows path to tsp.exe
# If fails: Add TSDuck to PATH
```

### Step 3: Test Basic TSDuck
```cmd
# Test with a simple command:
tsp --version

# Should work without errors
```

### Step 4: Test Input Source
```cmd
# Test if your HLS source works:
curl -I https://your-source/index.m3u8

# Or test with TSDuck:
tsp -I hls https://your-source/index.m3u8 -O drop
```

### Step 5: Check Network
```cmd
# Check internet connectivity:
ping 8.8.8.8

# Check DNS:
ping google.com

# Test specific server:
ping your-srt-server.com
```

### Step 6: Check Configuration
```cmd
# Verify config file exists:
dir gui_working_config.json

# Verify SCTE-35 folder:
dir scte35_final
```

### Step 7: Launch with Diagnostics
```cmd
# Launch the app:
launch_ibe100_v1.5.1.bat

# Watch console output for errors
# Look for specific error messages
```

## Common Error Messages

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `tsp: command not found` | TSDuck not in PATH | Add TSDuck to PATH |
| `Connection refused` | Server not accepting | Check firewall/rules |
| `No such file or directory` | Source not found | Check URL/path |
| `Permission denied` | Missing permissions | Run as admin |
| `Exit code 1` | Various | Run diagnose_error.py |

## Quick Reference

### Check if TSDuck is Working:
```cmd
tsp --version
tsp --list-plugins
tsp -I file input.ts -O drop
```

### Install TSDuck:
- **Windows:** Download from https://tsduck.io/download/
- **Linux:** `sudo apt-get install tsduck`
- **macOS:** `brew install tsduck`

### Add TSDuck to PATH:
```cmd
# Windows:
set PATH=%PATH%;C:\Program Files\TSDuck\bin

# Linux/macOS:
export PATH=$PATH:/usr/local/bin
```

## Contact Support

If none of these solutions work:
- 📧 Email: support@itassist.one
- 🌐 Website: https://itassist.one
- 📋 Include: Error messages, diagnostic report, system info

## Summary

✅ I've created comprehensive diagnostic tools to help identify the exact cause of error code 1
✅ The launch script now checks for TSDuck before starting
✅ Multiple troubleshooting guides provide step-by-step solutions
✅ Diagnostic tools help pinpoint the specific issue

**Most likely cause:** TSDuck not in PATH on target system
**Quick fix:** Add TSDuck bin folder to system PATH
**Best tool:** Run `diagnose_system.bat` on target system

