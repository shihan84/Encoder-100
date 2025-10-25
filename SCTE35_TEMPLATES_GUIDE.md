# 📋 SCTE-35 Template System Guide

## **Overview**

The ITAssist Broadcast Encoder - 100 (IBE-100) includes a comprehensive **SCTE-35 Template System** that provides professional broadcast marker templates for different scenarios, making it easy to create consistent and reliable ad insertion markers.

---

## **🎯 Template Types**

### **📋 Standard Templates**

#### **1. Preroll Ad Break**
- **Purpose**: Ad break before main program content
- **Markers**: TIME_SIGNAL (5s warning) → CUE-OUT (ad start) → CUE-IN (return to program)
- **Duration**: 30 seconds (configurable)
- **Use Case**: Live streams, on-demand content, scheduled programming
- **Event IDs**: Base + 0, Base + 1, Base + 2

#### **2. Midroll Ad Break**
- **Purpose**: Ad break during main program content
- **Markers**: TIME_SIGNAL (10s warning) → CUE-OUT (ad start) → CUE-IN (return to program)
- **Duration**: 60 seconds (configurable)
- **Timing**: Calculated at program midpoint
- **Use Case**: Long-form content, movies, live events, sports
- **Event IDs**: Base + 0, Base + 1, Base + 2

#### **3. Postroll Ad Break**
- **Purpose**: Ad break after main program content
- **Markers**: TIME_SIGNAL (3s warning) → CUE-OUT (ad start) → CUE-IN (end of content)
- **Duration**: 30 seconds (configurable)
- **Use Case**: End of programs, credits, next program promotion
- **Event IDs**: Base + 0, Base + 1, Base + 2

#### **4. Scheduled Ad Break**
- **Purpose**: Ad break at specific scheduled time
- **Markers**: TIME_SIGNAL (15s warning) → CUE-OUT (scheduled time) → CUE-IN (return)
- **Duration**: 60 seconds (configurable)
- **Timing**: Precise scheduled time (HH:MM:SS format)
- **Use Case**: Scheduled programming, news breaks, regular intervals
- **Event IDs**: Base + 0, Base + 1, Base + 2

#### **5. Emergency Break**
- **Purpose**: Immediate emergency program interruption
- **Markers**: CRASH-OUT (immediate) → CUE-IN (return after emergency)
- **Duration**: Immediate execution
- **Use Case**: Breaking news, emergency alerts, technical issues
- **Event IDs**: Base + 0, Base + 1

#### **6. Multi-Break Template**
- **Purpose**: Multiple ad breaks at specified times
- **Markers**: 3 sets of TIME_SIGNAL → CUE-OUT → CUE-IN
- **Duration**: 30 seconds each (configurable)
- **Timing**: User-defined break times
- **Use Case**: Long-form content with multiple commercial breaks
- **Event IDs**: Base + 0-2, Base + 3-5, Base + 6-8

---

## **🚀 Getting Started**

### **1. Access Template System**
1. Launch IBE-100 application
2. Click on **"📋 SCTE-35 Templates"** tab
3. The interface will show template options

### **2. Create Standard Templates**
1. Click **"📋 Create Standard Templates"** button
2. System creates 6 standard templates automatically
3. Templates are saved in `scte35_templates/` directory

### **3. Generate from Template**
1. Go to **"📋 Standard Templates"** tab
2. Select template type from dropdown
3. Configure parameters:
   - **Base Event ID**: Starting event ID (10000-999999)
   - **Ad Duration**: Break length in seconds
   - **Scheduled Time**: For scheduled templates (HH:MM:SS)
   - **Program Duration**: For midroll templates
4. Click **"🎬 Generate from Template"**

---

## **📋 Template Parameters**

### **Common Parameters**
- **Base Event ID**: Starting event ID for the sequence
- **Ad Duration**: Length of commercial break (5-3600 seconds)
- **Description**: Human-readable template description
- **Use Case**: When to use this template

### **Template-Specific Parameters**

#### **Preroll Template**
- **Ad Duration**: 30 seconds (default)
- **Warning Time**: 5 seconds before break
- **Total Duration**: Ad duration + 5 seconds

#### **Midroll Template**
- **Ad Duration**: 60 seconds (default)
- **Program Duration**: 1800 seconds (30 minutes, default)
- **Midroll Time**: Program duration ÷ 2
- **Warning Time**: 10 seconds before break

#### **Postroll Template**
- **Ad Duration**: 30 seconds (default)
- **Warning Time**: 3 seconds before break
- **Total Duration**: Ad duration + 3 seconds

#### **Scheduled Template**
- **Scheduled Time**: 14:30:00 (default)
- **Ad Duration**: 60 seconds (default)
- **Warning Time**: 15 seconds before scheduled time
- **Time Format**: HH:MM:SS or HH:MM

#### **Emergency Template**
- **Immediate Execution**: No timing delays
- **CRASH-OUT**: Immediate program interruption
- **Return**: CUE-IN for program resumption

#### **Multi-Break Template**
- **Break Times**: [300, 900, 1500] seconds (default)
- **Ad Duration**: 30 seconds each (default)
- **Warning Time**: 5 seconds before each break
- **Total Breaks**: 3 (configurable)

---

## **🎨 Custom Templates**

### **Creating Custom Templates**
1. Go to **"🎨 Custom Templates"** tab
2. Enter template details:
   - **Template Name**: Descriptive name
   - **Scenario**: preroll, midroll, postroll, scheduled, emergency, multi_break, custom
   - **Description**: Detailed description
3. Use **Template Editor** to create JSON configuration
4. Click **"🎨 Create Custom Template"**

### **Template JSON Structure**
```json
{
  "name": "Custom Template Name",
  "description": "Template description",
  "scenario": "custom",
  "markers": [
    {
      "type": "TIME_SIGNAL",
      "event_id": 10000,
      "description": "Timing signal",
      "pts_offset": -5000,
      "purpose": "Warning signal"
    },
    {
      "type": "CUE-OUT",
      "event_id": 10001,
      "description": "Ad break start",
      "duration": 30,
      "purpose": "Start commercial content"
    },
    {
      "type": "CUE-IN",
      "event_id": 10002,
      "description": "Return to program",
      "purpose": "End commercial content"
    }
  ],
  "total_duration": 35,
  "use_case": "Custom broadcast scenario"
}
```

---

## **📚 Template Library**

### **Managing Templates**
1. Go to **"📚 Template Library"** tab
2. View all available templates in the list
3. Select template to view details
4. Use template actions:
   - **📂 Load Selected**: Load template for editing
   - **🗑️ Delete Template**: Remove template
   - **📄 View Details**: See full template configuration

### **Template Details**
- **Name**: Template display name
- **Scenario**: Template type/category
- **Description**: What the template does
- **Use Case**: When to use this template
- **Created**: Template creation timestamp
- **Markers**: List of markers in template

---

## **🔧 Advanced Features**

### **Template Validation**
- **JSON Structure**: Validates template JSON format
- **Required Fields**: Checks for required template fields
- **Marker Types**: Validates marker type values
- **Event IDs**: Ensures unique event IDs
- **Timing**: Validates timing parameters

### **Batch Operations**
- **Multiple Templates**: Generate from multiple templates
- **Sequential IDs**: Automatic event ID management
- **File Organization**: Organized output directory structure
- **Metadata Tracking**: Complete generation history

### **Integration Features**
- **TSDuck Compatibility**: Direct XML output for TSDuck
- **JSON Metadata**: Human-readable marker information
- **File Management**: Automatic file organization
- **Version Control**: Template version tracking

---

## **📊 Generated Markers Management**

### **View Generated Markers**
1. Go to **"📋 Generated Markers"** tab
2. See all markers generated from templates
3. View marker details in table format
4. Access XML and JSON files

### **Marker Operations**
- **📄 View XML**: Display XML content in dialog
- **📋 View JSON**: Display JSON metadata
- **🗑️ Delete Marker**: Remove individual markers
- **🔄 Refresh**: Update marker list

### **Marker Information**
- **Type**: Marker type (CUE-OUT, CUE-IN, etc.)
- **Event ID**: Unique identifier
- **Description**: Human-readable description
- **Purpose**: Technical purpose
- **Files**: XML and JSON file paths

---

## **🎬 Professional Use Cases**

### **Live Broadcasting**
- **Preroll**: Before live events start
- **Midroll**: During long live events
- **Emergency**: Breaking news interruptions
- **Scheduled**: Regular news breaks

### **On-Demand Content**
- **Preroll**: Before video content
- **Midroll**: During long videos
- **Postroll**: After video content
- **Multi-Break**: Multiple ad positions

### **Scheduled Programming**
- **Scheduled**: Regular commercial breaks
- **News**: Scheduled news updates
- **Sports**: Commercial timeouts
- **Events**: Scheduled event breaks

### **Emergency Situations**
- **Breaking News**: Immediate interruptions
- **Technical Issues**: Emergency program cuts
- **Alerts**: Emergency notifications
- **Updates**: Critical information

---

## **⚙️ Configuration Options**

### **Template Settings**
- **Output Directory**: Where to save generated files
- **File Naming**: Timestamp-based naming
- **Event ID Range**: 10000-999999
- **Duration Limits**: 5-3600 seconds
- **Timing Precision**: 90kHz PTS timing

### **Generation Options**
- **Sequential IDs**: Automatic event ID management
- **File Organization**: Organized directory structure
- **Metadata**: Complete marker information
- **Validation**: Template and marker validation

### **Integration Options**
- **TSDuck Format**: Direct XML compatibility
- **JSON Metadata**: Human-readable information
- **File Management**: Automatic cleanup options
- **Version Control**: Template versioning

---

## **🔍 Troubleshooting**

### **Common Issues**

#### **"Template system not available"**
- **Cause**: Template system not loaded
- **Solution**: Restart application, check imports

#### **"Failed to generate markers"**
- **Cause**: File system permissions or invalid template
- **Solution**: Check permissions, validate template

#### **"Invalid event ID"**
- **Cause**: Event ID out of range
- **Solution**: Use valid range (10000-999999)

#### **"Template not found"**
- **Cause**: Template file missing or corrupted
- **Solution**: Recreate template, check file permissions

### **Debug Information**
- **Check Console**: Look for error messages
- **Verify Files**: Check template directory
- **Permissions**: Ensure write access
- **Validation**: Use template validation

---

## **📈 Best Practices**

### **Template Design**
- **Clear Names**: Use descriptive template names
- **Proper Scenarios**: Choose appropriate scenario types
- **Complete Descriptions**: Include detailed descriptions
- **Valid Parameters**: Use proper parameter ranges

### **Event ID Management**
- **Reserve Ranges**: Plan event ID ranges for different content
- **Sequential Order**: Use sequential IDs for related markers
- **Documentation**: Keep track of used event IDs
- **Avoid Conflicts**: Don't reuse event IDs

### **Timing Coordination**
- **Preroll Signals**: Use appropriate warning times
- **Duration Accuracy**: Set exact ad break durations
- **Synchronization**: Coordinate with downstream systems
- **Testing**: Verify timing in test environments

### **File Management**
- **Regular Cleanup**: Remove old template files
- **Backup Important**: Keep copies of critical templates
- **Version Control**: Track template versions
- **Documentation**: Maintain template documentation

---

## **🚀 Future Enhancements**

### **Planned Features**
- **Template Sharing**: Export/import templates
- **Advanced Timing**: More sophisticated timing options
- **Batch Generation**: Multiple template processing
- **Integration APIs**: External system integration

### **Community Contributions**
- **Custom Scenarios**: User-defined template types
- **Industry Standards**: Broadcast industry templates
- **Validation Tools**: Enhanced template validation
- **Documentation**: Community template library

---

## **📚 Additional Resources**

### **Related Documentation**
- **SCTE-35 Generation**: `SCTE35_GENERATION_GUIDE.md`
- **Stream Processing**: `STREAM_START_FIX.md`
- **Configuration**: `AI_AGENT_INSTRUCTIONS.md`
- **Build System**: `PACKAGING_GUIDE.md`

### **External Resources**
- **SCTE-35 Standard**: Official SCTE-35 documentation
- **Broadcast Templates**: Industry template libraries
- **TSDuck Documentation**: TSDuck user guide
- **Community Support**: User forums and support

---

## **🎯 Summary**

The **SCTE-35 Template System** in IBE-100 provides:

- ✅ **Professional Templates** for all broadcast scenarios
- ✅ **Easy Configuration** with intuitive parameters
- ✅ **Custom Templates** for specific requirements
- ✅ **Template Library** for organized management
- ✅ **TSDuck Integration** for seamless processing
- ✅ **Professional Workflow** for broadcast operations

**🚀 Ready for professional broadcast operations with comprehensive SCTE-35 template support!**
