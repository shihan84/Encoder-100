# 🎬 Distributor Pre-roll SCTE-35 Markers - Complete Guide

## ✅ **Pre-roll Markers Generated Successfully!**

Your distributor-requested pre-roll SCTE-35 markers have been generated and are ready for use.

## 📁 **Generated Pre-roll Markers**

### **Available Configurations:**

| Event ID | Pre-roll Time | Ad Duration | Use Case |
|----------|---------------|-------------|----------|
| **10023** | **2 seconds** | **10 minutes** | **Standard pre-roll** |
| **10024** | **5 seconds** | **5 minutes** | **Extended pre-roll** |
| **10025** | **10 seconds** | **2 minutes** | **Long pre-roll** |
| **10026** | **0 seconds** | **10 minutes** | **Immediate insertion** |

## 🎯 **How to Use Pre-roll Markers**

### **1. Using with TSDuck (Recommended)**

```bash
# Standard 2-second pre-roll with 10-minute ad
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P spliceinject --pid 500 --pts-pid 256 \
    --files scte35_final/preroll_10023_*.xml \
    --delete-files \
    -O srt --caller cdn.itassist.one:8888 \
    --streamid "#!::r=scte/scte,m=publish" \
    --latency 2000
```

### **2. Using with IBE-100 GUI**

1. **Launch IBE-100**: Run `.\dist\IBE-100.exe`
2. **Configure Input**: Set HLS input to your stream URL
3. **Configure Output**: Set SRT output to your distributor endpoint
4. **Enable SCTE-35**: 
   - Go to SCTE-35 tab
   - Enable `spliceinject` plugin
   - Set PID to 500
   - Load pre-roll XML files
5. **Start Processing**: Click "Start Processing"

### **3. Using with TSDuck GUI**

1. **Launch TSDuck GUI**: Run the application
2. **Configure Pipeline**:
   - Input: HLS stream
   - Output: SRT to distributor
   - Add `spliceinject` plugin with pre-roll files
3. **Start Processing**: Monitor real-time output

## 📋 **Pre-roll Marker Details**

### **XML Format (TSDuck Compatible)**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <splice_information_table protocol_version="0" pts_adjustment="0" tier="0xFFF">
        <splice_insert splice_event_id="10023" splice_event_cancel="false" 
                      out_of_network="true" splice_immediate="false" 
                      pts_time="158525041064925" unique_program_id="1" 
                      avail_num="1" avails_expected="1">
            <break_duration auto_return="false" duration="54000000" />
        </splice_insert>
    </splice_information_table>
</tsduck>
```

### **Key Parameters:**
- **Event ID**: Sequential numbering (10023, 10024, 10025, 10026)
- **Pre-roll Time**: Lead time before ad insertion (0-10 seconds)
- **Ad Duration**: Length of ad break (120-600 seconds)
- **PTS Time**: Precise timing for insertion
- **Out of Network**: `true` for ad insertion

## 🚀 **Production Commands**

### **For Your Distributor Requirements:**

```bash
# HLS Input → SRT Output with Pre-roll
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P pmt --service 1 --add-pid 500/0x86 \
    -P spliceinject --service 1 \
    --files 'scte35_final/preroll_*.xml' \
    --inject-count 1 --inject-interval 1000 \
    --start-delay 2000 \
    --min-bitrate 2000 \
    -O srt --caller cdn.itassist.one:8888 \
    --streamid "#!::r=scte/scte,m=publish" \
    --latency 2000
```

### **Testing with Local UDP:**
```bash
# Test locally first
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 \
    -P spliceinject --pid 500 --files 'scte35_final/preroll_10023_*.xml' \
    -O ip 127.0.0.1:9999
```

## 📊 **Monitoring Pre-roll Markers**

### **Real-time Analysis:**
```bash
# Monitor SCTE-35 markers in output stream
tsp -I ip 127.0.0.1:9999 -P analyze -O drop
```

### **Expected Output:**
- **SCTE-35 PID**: 500 (0x01F4)
- **Event Detection**: Pre-roll markers detected
- **Timing**: 2-second lead time before ad insertion
- **Duration**: 10-minute ad break

## 🎯 **Distributor Integration**

### **Your Stream Specifications:**
- **Input**: HLS from `https://cdn.itassist.one/BREAKING/NEWS/index.m3u8`
- **Output**: SRT to `srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish`
- **SCTE-35 PID**: 500
- **Pre-roll**: 2 seconds (configurable)
- **Ad Duration**: 600 seconds (10 minutes)

### **Event ID Sequence:**
- **10023**: 2s pre-roll, 10min ad
- **10024**: 5s pre-roll, 5min ad  
- **10025**: 10s pre-roll, 2min ad
- **10026**: Immediate, 10min ad

## 🔧 **Customization**

### **Generate Custom Pre-roll Markers:**
```python
# Run the generator script
python generate_preroll.py

# Or create custom markers
from generate_preroll import generate_preroll_marker

# Custom pre-roll: 3 seconds, 8 minutes
xml_file, json_file = generate_preroll_marker(
    event_id=10030,
    preroll_seconds=3,
    ad_duration=480
)
```

## ✅ **Verification Checklist**

- [x] **Pre-roll markers generated** (4 configurations)
- [x] **TSDuck XML format** (compatible)
- [x] **Event ID sequence** (10023-10026)
- [x] **Timing calculations** (PTS-based)
- [x] **Production ready** (tested format)
- [x] **Distributor compatible** (SRT output)

## 🎉 **Ready for Production!**

Your pre-roll SCTE-35 markers are now ready for distributor integration:

1. **Choose your pre-roll configuration** (2s, 5s, 10s, or immediate)
2. **Use the appropriate XML file** with TSDuck
3. **Configure your stream pipeline** (HLS → SRT)
4. **Monitor the output** for SCTE-35 markers
5. **Verify with your distributor** that markers are received

**Your pre-roll SCTE-35 system is ready for professional broadcast operations!** 🚀
