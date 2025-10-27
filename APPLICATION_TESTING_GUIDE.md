# 🧪 **IBE-100 v1.5.0 Application Testing Guide**

## 📅 **Testing Information**
- **Version**: 1.5.0 (Debug)
- **Build Date**: January 25, 2025
- **Build Status**: ✅ **SUCCESSFULLY BUILT**
- **Application Status**: ✅ **RUNNING**

---

## 🎯 **Application Testing Process**

### ✅ **Application is Now Running**
- **Status**: ✅ **LAUNCHED SUCCESSFULLY**
- **Location**: `dist\IBE-100_v1.5.0\IBE-100.exe`
- **Debug Features**: ✅ **ENABLED**

---

## 🧪 **Testing Steps**

### ✅ **Step 1: Verify Application is Running**
1. **Check**: Application window should be open
2. **Verify**: Professional SCTE-35 tab is visible
3. **Status**: ✅ Application is running

### ✅ **Step 2: Generate a Marker**
1. **Navigate to**: Professional SCTE-35 tab
2. **Click**: "Quick Pre-roll 2s" button (or any template)
3. **Wait**: For marker generation to complete
4. **Check Console**: Look for debug messages

**Expected Debug Output**:
```
[INFO] New marker generated: scte35_final/preroll_10023_[timestamp].xml
[DEBUG] Signal received - storing marker: scte35_final/preroll_10023_[timestamp].xml
[DEBUG] latest_generated_marker set to: scte35_final/preroll_10023_[timestamp].xml
```

### ✅ **Step 3: Configure TSDuck Command**
1. **Navigate to**: Configuration tab
2. **Set Input**: Verify HLS input is set
3. **Set Output**: Verify SRT output is configured
4. **Click**: "Start Processing" button

**Expected Debug Output**:
```
[DEBUG] get_latest_scte35_marker called
[DEBUG] latest_generated_marker: scte35_final/preroll_10023_[timestamp].xml
[DEBUG] Using marker from Professional SCTE-35 tab: scte35_final/preroll_10023_[timestamp].xml
```

### ✅ **Step 4: Verify TSDuck Command**
1. **Check Command**: Look at the generated TSDuck command
2. **Verify**: `--files` parameter should use the generated marker
3. **Should NOT Be**: `preroll_10023.xml` (hardcoded)

**Expected Command**:
```
C:\Program Files\TSDuck\bin\tsp.EXE -I hls [input] ... --files scte35_final/preroll_10023_[timestamp].xml ...
```

---

## 🔍 **Debug Information to Report**

### ✅ **What to Look For**
1. **Widget Creation**: `[DEBUG] Professional SCTE-35 widget created and signal connected`
2. **Marker Generation**: `[INFO] New marker generated: [filename]`
3. **Signal Reception**: `[DEBUG] Signal received - storing marker: [filename]`
4. **Marker Storage**: `[DEBUG] latest_generated_marker set to: [filename]`
5. **Marker Selection**: `[DEBUG] Using marker from Professional SCTE-35 tab: [filename]`

### ✅ **What to Report**
1. **Debug Messages**: All debug messages you see in the console
2. **TSDuck Command**: The full TSDuck command that was generated
3. **Marker File Used**: The actual marker file used in the command
4. **Any Issues**: Any problems or unexpected behavior

---

## 📊 **Expected Results**

### ✅ **If Working Correctly**
- **Debug Output**: ✅ All debug messages appear
- **Marker Generation**: ✅ Marker generated successfully
- **Signal Connection**: ✅ Signal received and processed
- **TSDuck Command**: ✅ Uses generated marker (not hardcoded)
- **Example**: `--files scte35_final/preroll_10023_[timestamp].xml`

### ✅ **If Not Working**
- **No Debug Output**: ❌ Debug messages are missing
- **Hardcoded File**: ❌ TSDuck command uses `preroll_10023.xml`
- **Signal Issues**: ❌ Signal not being received/processed
- **Marker Storage**: ❌ Marker not being stored properly

---

## 🎯 **Report Format**

### ✅ **Application Status**
```
✅ Application launched successfully
✅ Professional SCTE-35 tab is visible
✅ Ready for marker generation testing
```

### ✅ **Marker Generation Test**
```
[Report whether marker was generated]
[Report debug messages seen]
```

### ✅ **TSDuck Command Test**
```
[Report the generated TSDuck command]
[Report the marker file used in --files parameter]
[Report whether it's the generated marker or hardcoded file]
```

### ✅ **Issues Found**
```
[Report any issues or unexpected behavior]
```

---

## 🚀 **Next Steps**

### ✅ **After Testing**
1. **Report Results**: Share the debug output and TSDuck command
2. **Report Issues**: Share any issues or problems found
3. **Provide Feedback**: Share whether marker selection is working correctly

### ✅ **Based on Results**
- **If Working**: Remove debug code and create final version
- **If Not Working**: Analyze debug output and fix the issue
- **If Partially Working**: Identify and fix remaining issues

---

## 🎉 **Application Ready for Testing**

### ✅ **Application Information**
- **Version**: 1.5.0 (Debug)
- **Build Status**: ✅ **SUCCESSFULLY BUILT**
- **Application Status**: ✅ **RUNNING**
- **Debug Features**: ✅ **ENABLED**

### ✅ **Testing Instructions**
- **Location**: `dist\IBE-100_v1.5.0\IBE-100.exe`
- **Status**: ✅ **READY FOR TESTING**
- **Instructions**: ✅ **PROVIDED**

**Please test the application and report the results!** 🧪

---

**Testing Guide Status**: ✅ **COMPLETE**  
**Application Status**: ✅ **RUNNING**  
**Debug Features**: ✅ **ENABLED**  
**Ready for Testing**: ✅ **YES**
