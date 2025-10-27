# 🧪 **IBE-100 v1.5.0 Testing Instructions**

## 📅 **Testing Information**
- **Version**: 1.5.0 (Debug)
- **Build Date**: January 25, 2025
- **Status**: ✅ **READY FOR TESTING**

---

## 🎯 **Testing Steps**

### ✅ **Step 1: Launch Application**
1. **Navigate to**: `dist\IBE-100_v1.5.0\`
2. **Run**: `IBE-100.exe`
3. **Expected**: Application window opens
4. **Check Console**: Look for debug messages about widget creation

### ✅ **Step 2: Generate Marker**
1. **Navigate to**: Professional SCTE-35 tab
2. **Select Template**: Click on "Quick Pre-roll 2s" button
3. **Expected**: Marker generation starts
4. **Check Console**: Look for debug messages about marker generation

### ✅ **Step 3: Start TSDuck Command**
1. **Navigate to**: Main Configuration tab
2. **Click**: "Start Processing" button
3. **Expected**: TSDuck command starts
4. **Check Console**: Look for debug messages about marker selection

### ✅ **Step 4: Verify TSDuck Command**
1. **Look at Command**: Check the generated TSDuck command
2. **Expected**: Command should use generated marker file
3. **Verify**: `--files` parameter should not be `preroll_10023.xml`

---

## 🔍 **Debug Messages to Look For**

### ✅ **Application Startup**
```
[DEBUG] Professional SCTE-35 widget created and signal connected
```

### ✅ **Marker Generation**
```
[INFO] New marker generated: scte35_final/preroll_10023_1761394095.xml
[DEBUG] Signal received - storing marker: scte35_final/preroll_10023_1761394095.xml
[DEBUG] latest_generated_marker set to: scte35_final/preroll_10023_1761394095.xml
```

### ✅ **TSDuck Command Building**
```
[DEBUG] get_latest_scte35_marker called
[DEBUG] latest_generated_marker: scte35_final/preroll_10023_1761394095.xml
[DEBUG] Using marker from Professional SCTE-35 tab: scte35_final/preroll_10023_1761394095.xml
```

---

## 📊 **Expected Results**

### ✅ **If Working Correctly**
- **Debug Output**: All debug messages appear in console
- **Marker Selection**: Generated marker is used in TSDuck command
- **TSDuck Command**: Uses generated marker instead of hardcoded file
- **Example**: `--files scte35_final/preroll_10023_1761394095.xml`

### ✅ **If Not Working**
- **Missing Debug Output**: Some debug messages are missing
- **Hardcoded File**: TSDuck command still uses `preroll_10023.xml`
- **No Signal**: Signal connection not working
- **No Marker Storage**: Marker not being stored properly

---

## 🐛 **Troubleshooting**

### ✅ **No Debug Output About Widget**
- **Check**: Professional SCTE-35 widget import
- **Solution**: Verify `professional_scte35_widget.py` exists

### ✅ **No Debug Output About Marker Generation**
- **Check**: Marker generation in Professional SCTE-35 tab
- **Solution**: Verify marker templates are working

### ✅ **No Debug Output About Signal Reception**
- **Check**: Signal connection
- **Solution**: Verify signal/slot communication

### ✅ **TSDuck Command Uses Hardcoded File**
- **Check**: Marker selection in `get_latest_scte35_marker()`
- **Solution**: Verify marker storage and retrieval

---

## 🎯 **Report Template**

### ✅ **Test Results**
- **Application Launch**: ✅/❌
- **Marker Generation**: ✅/❌
- **Debug Output**: ✅/❌
- **TSDuck Command**: ✅/❌

### ✅ **Debug Output Captured**
```
[Paste debug output here]
```

### ✅ **TSDuck Command**
```
[Paste TSDuck command here]
```

### ✅ **Issues Found**
- **Issue 1**: [Description]
- **Issue 2**: [Description]
- **Issue 3**: [Description]

---

## 🚀 **Application Status**

### ✅ **Ready for Testing**
- **Executable**: `dist\IBE-100_v1.5.0\IBE-100.exe`
- **Debug Features**: ✅ **ENABLED**
- **Instructions**: ✅ **PROVIDED**
- **Status**: ✅ **READY FOR TESTING**

---

**Please follow these testing steps and report the results!** 🧪
