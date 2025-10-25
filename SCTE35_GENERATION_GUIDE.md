# 🎬 SCTE-35 Marker Generation Guide

## **Overview**

The ITAssist Broadcast Encoder - 100 (IBE-100) now includes comprehensive **SCTE-35 marker generation** capabilities, allowing you to create professional ad insertion markers for broadcast streams.

---

## **🎯 Features**

### **✅ Individual Marker Types**
- **CUE-OUT**: Program out point (start of ad break)
- **CUE-IN**: Program in point (return to program)  
- **CRASH-OUT**: Emergency program out (immediate break)
- **TIME_SIGNAL**: Timing reference signal

### **✅ Ad Break Sequences**
- **Complete Ad Break**: Preroll + CUE-OUT + CUE-IN sequence
- **Configurable Duration**: Set ad break length (1-3600 seconds)
- **Preroll Support**: Timing signals before ad breaks
- **Event ID Management**: Automatic sequential event IDs

### **✅ Professional Output**
- **TSDuck XML Format**: Direct compatibility with TSDuck
- **JSON Metadata**: Human-readable marker information
- **File Management**: Organized marker storage and cleanup
- **Real-time Generation**: Instant marker creation

---

## **🚀 Getting Started**

### **1. Access SCTE-35 Generation**
1. Launch IBE-100 application
2. Click on **"🎬 SCTE-35 Generation"** tab
3. The interface will show available marker types

### **2. Generate Individual Markers**
1. Select marker type from dropdown:
   - **CUE_OUT - Program Out Point**
   - **CUE_IN - Program In Point**
   - **CRASH_OUT - Emergency Program Out**
   - **TIME_SIGNAL - Timing Reference**
2. Set parameters:
   - **Event ID**: Unique identifier (1-999999)
   - **Duration**: Ad break length in seconds (for CUE-OUT)
   - **PTS Offset**: Timing offset in 90kHz ticks
   - **Options**: Out of network, immediate execution
3. Click **"🎬 Generate Marker"**

### **3. Generate Ad Break Sequences**
1. Go to **"📺 Ad Break Sequence"** tab
2. Configure sequence:
   - **Base Event ID**: Starting event ID
   - **Ad Duration**: Length of ad break (seconds)
   - **Preroll**: Warning time before break (seconds)
3. Click **"👁️ Preview Sequence"** to see planned markers
4. Click **"🎬 Generate Ad Break Sequence"**

---

## **📋 Marker Types Explained**

### **🎬 CUE-OUT (Program Out Point)**
- **Purpose**: Signals the start of an ad break
- **When to use**: Before playing commercial content
- **Parameters**: Event ID, duration, timing
- **Output**: XML file for TSDuck injection

### **🎬 CUE-IN (Program In Point)**
- **Purpose**: Signals return to main program
- **When to use**: After ad break ends
- **Parameters**: Event ID, timing
- **Output**: XML file for TSDuck injection

### **🚨 CRASH-OUT (Emergency Program Out)**
- **Purpose**: Immediate emergency break
- **When to use**: Breaking news, emergency situations
- **Parameters**: Event ID only
- **Output**: Immediate execution XML

### **⏰ TIME_SIGNAL (Timing Reference)**
- **Purpose**: Timing reference for synchronization
- **When to use**: Before ad breaks, timing coordination
- **Parameters**: Event ID, timing
- **Output**: Timing reference XML

---

## **🔧 Technical Details**

### **XML Format (TSDuck Compatible)**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<tsduck>
    <splice_insert>
        <splice_event_id>10021</splice_event_id>
        <splice_event_cancel_indicator>0</splice_event_cancel_indicator>
        <out_of_network_indicator>1</out_of_network_indicator>
        <program_splice_flag>1</program_splice_flag>
        <duration_flag>1</duration_flag>
        <splice_immediate_flag>0</splice_immediate_flag>
        <splice_time>
            <pts_time>158524756616182</pts_time>
        </splice_time>
        <break_duration>
            <auto_return>0</auto_return>
            <duration>2700000</duration>
        </break_duration>
        <unique_program_id>1</unique_program_id>
        <avail_num>1</avail_num>
        <avails_expected>1</avails_expected>
    </splice_insert>
</tsduck>
```

### **JSON Metadata Format**
```json
{
  "type": "CUE-OUT",
  "event_id": 10021,
  "duration_seconds": 30,
  "description": "Program out point - 30s ad break",
  "timestamp": 1761386184,
  "xml_file": "scte35_final/cue_out_10021_1761386184.xml"
}
```

### **File Organization**
```
scte35_final/
├── cue_out_10021_1761386184.xml    # TSDuck XML
├── cue_out_10021_1761386184.json   # Metadata
├── cue_in_10022_1761386184.xml     # TSDuck XML
├── cue_in_10022_1761386184.json    # Metadata
└── ...                             # More markers
```

---

## **🎬 Ad Break Sequence Example**

### **Complete Ad Break Workflow:**
1. **Preroll Signal** (Event ID: 10025)
   - TIME_SIGNAL marker
   - 2 seconds before ad break
   - Warns downstream systems

2. **Ad Break Start** (Event ID: 10026)
   - CUE-OUT marker
   - 60-second ad break
   - Out of network indicator

3. **Return to Program** (Event ID: 10027)
   - CUE-IN marker
   - Return to main program
   - End of ad break

### **Generated Files:**
- `time_signal_10025_*.xml` - Preroll timing
- `cue_out_10026_*.xml` - Ad break start
- `cue_in_10027_*.xml` - Return to program

---

## **🔧 Integration with TSDuck**

### **Automatic Integration**
The generated XML files are automatically used by IBE-100's TSDuck pipeline:

```bash
tsp -I input_source \
    -P spliceinject --service 1 \
    --files scte35_final/*.xml \
    --inject-count 1 --inject-interval 1000 \
    -O output_destination
```

### **Manual TSDuck Usage**
You can also use the generated files manually:

```bash
# Inject specific marker
tsp -I input_source \
    -P spliceinject --service 1 \
    --files scte35_final/cue_out_10021_*.xml \
    -O output_destination

# Monitor for SCTE-35 markers
tsp -I input_source \
    -P splicemonitor \
    -O output_destination
```

---

## **📊 Marker Management**

### **View Generated Markers**
1. Go to **"📋 Generated Markers"** tab
2. See all generated markers in table format
3. View XML content by clicking **"📄 View XML"**
4. View JSON metadata by clicking **"📋 View JSON"**

### **Marker Operations**
- **Delete Individual**: Select marker and click **"🗑️ Delete Marker"**
- **Clear All**: Click **"🗑️ Clear All Markers"**
- **Refresh List**: Click **"🔄 Refresh List"**

### **File Management**
- **Automatic Cleanup**: Files are organized in `scte35_final/` directory
- **Timestamp Naming**: Files include generation timestamp
- **Metadata Tracking**: JSON files contain full marker information

---

## **⚙️ Configuration Options**

### **Event ID Management**
- **Range**: 1 to 999,999
- **Sequential**: Automatic increment for sequences
- **Unique**: Each marker gets unique event ID
- **Custom**: User-defined event IDs supported

### **Timing Parameters**
- **PTS Offset**: Timing offset in 90kHz ticks
- **Duration**: Ad break length in seconds
- **Preroll**: Warning time before breaks
- **Immediate**: Execute without timing delay

### **Output Options**
- **Out of Network**: Markers indicate ad breaks
- **Program Splice**: Full program breaks
- **Duration Flag**: Include break duration
- **Auto Return**: Automatic return to program

---

## **🚀 Best Practices**

### **Event ID Planning**
- **Reserve Ranges**: Plan event ID ranges for different content
- **Sequential Order**: Use sequential IDs for related markers
- **Documentation**: Keep track of used event IDs
- **Avoid Conflicts**: Don't reuse event IDs

### **Timing Coordination**
- **Preroll Signals**: Use 2-5 seconds before ad breaks
- **Duration Accuracy**: Set exact ad break durations
- **Synchronization**: Coordinate with downstream systems
- **Testing**: Verify timing in test environments

### **File Management**
- **Regular Cleanup**: Remove old marker files
- **Backup Important**: Keep copies of critical markers
- **Version Control**: Track marker versions
- **Documentation**: Maintain marker documentation

---

## **🔍 Troubleshooting**

### **Common Issues**

#### **"Generator not available"**
- **Cause**: SCTE-35 XML generator not loaded
- **Solution**: Restart application, check imports

#### **"Failed to generate marker"**
- **Cause**: File system permissions or disk space
- **Solution**: Check write permissions, free disk space

#### **"Invalid event ID"**
- **Cause**: Event ID out of range (1-999999)
- **Solution**: Use valid event ID range

#### **"XML file not found"**
- **Cause**: Generated file was deleted or moved
- **Solution**: Regenerate marker, check file permissions

### **Debug Information**
- **Check Console**: Look for error messages in console
- **Verify Files**: Check `scte35_final/` directory exists
- **Permissions**: Ensure write access to output directory
- **Disk Space**: Verify sufficient free space

---

## **📈 Advanced Usage**

### **Custom Marker Parameters**
- **Event ID**: Set custom event IDs for specific content
- **Duration**: Configure exact ad break lengths
- **Timing**: Use PTS offsets for precise timing
- **Options**: Combine different marker options

### **Batch Generation**
- **Multiple Markers**: Generate several markers at once
- **Sequences**: Create complete ad break sequences
- **Templates**: Save common marker configurations
- **Automation**: Integrate with external systems

### **Integration Examples**
- **Live Events**: Generate markers for live broadcasts
- **Pre-recorded**: Create markers for recorded content
- **Testing**: Generate test markers for validation
- **Production**: Use for actual broadcast operations

---

## **🎉 Success Indicators**

### **✅ Generation Success**
- **Status**: "✅ SCTE-35 XML generator available"
- **Files Created**: XML and JSON files in `scte35_final/`
- **Table Updated**: Markers appear in generated markers table
- **No Errors**: No error messages in console

### **✅ Integration Success**
- **TSDuck Compatible**: XML files work with TSDuck
- **Stream Processing**: Markers injected into stream
- **Monitoring**: SCTE-35 markers detected in stream
- **Output**: Proper ad break behavior

---

## **🚀 Future Enhancements**

### **Planned Features**
- **Template System**: Save and reuse marker templates
- **Batch Operations**: Generate multiple markers at once
- **Advanced Timing**: More sophisticated timing options
- **Integration APIs**: External system integration

### **Community Contributions**
- **Custom Markers**: User-defined marker types
- **Export Formats**: Additional output formats
- **Validation Tools**: Marker validation and testing
- **Documentation**: Enhanced user guides

---

## **📚 Additional Resources**

### **Related Documentation**
- **TSDuck Guide**: `TSDUCK_SCTE35_GUIDE.md`
- **Stream Processing**: `STREAM_START_FIX.md`
- **Configuration**: `AI_AGENT_INSTRUCTIONS.md`
- **Build System**: `PACKAGING_GUIDE.md`

### **External Resources**
- **SCTE-35 Standard**: Official SCTE-35 documentation
- **TSDuck Documentation**: TSDuck user guide
- **Broadcast Standards**: Industry best practices
- **Community Support**: User forums and support

---

## **🎯 Summary**

The **SCTE-35 Marker Generation** feature in IBE-100 provides:

- ✅ **Professional marker creation** for broadcast streams
- ✅ **Complete ad break sequences** with timing coordination
- ✅ **TSDuck integration** for seamless stream processing
- ✅ **User-friendly interface** for easy marker management
- ✅ **Flexible configuration** for various broadcast scenarios

**🚀 Ready for professional broadcast operations with comprehensive SCTE-35 support!**
