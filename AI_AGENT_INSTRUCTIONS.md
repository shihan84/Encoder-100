# 🤖 AI Agent Instructions - ITAssist Broadcast Encoder - 100 (IBE-100)

## 📋 **Project Overview**

**Project Name**: ITAssist Broadcast Encoder - 100 (IBE-100) v2.0.4  
**Repository**: https://github.com/shihan84/Encoder-100.git  
**Main Application**: `IBE-100_v2.0_CLEAN/main.py`  
**Build Scripts**: `IBE-100_v2.0_CLEAN/build_config.py`  
**Distribution**: `IBE-100_v2.0_CLEAN/dist_final/` folder with executables  
**Latest Release**: v2.0.4 "Profile-Based Output Folders & Multiple Instance Support" (January 2025)

---

## 🎯 **Project Status: PRODUCTION READY WITH SCTE-35**

### **✅ All Major Issues Resolved**
- **Windows Dark Theme**: Consistent theming across all platforms
- **Stream Start Issues**: Real-time output display and proper error handling
- **Smart PID Remapping**: No more "PID present both in input and remap" errors
- **Connection Testing**: Pre-flight validation for network outputs
- **Enhanced Error Handling**: Specific guidance for different failure types

### **🎬 NEW: SCTE-35 Professional Features**
- **Complete SCTE-35 System**: Professional marker generation for broadcast streams
- **Template System**: 6 standard broadcast templates (Preroll, Midroll, Postroll, Scheduled, Emergency, Multi-Break)
- **Enhanced UI**: New tabs for SCTE-35 Generation and Templates
- **TSDuck Integration**: Direct XML output for professional stream processing
- **Professional Workflows**: Live broadcasting, on-demand content, scheduled programming

### **📦 Distribution Files Available**
- **IBE-100**: 26MB standalone executable for macOS (v1.1.0)
- **IBE-100-1.0.0.dmg**: 26MB macOS installer package
- **IBE-100.app**: macOS application bundle
- **Windows Executable**: Enhanced Windows build script available
- **Documentation**: Complete usage guides and SCTE-35 documentation

---

## 🔧 **Technical Architecture**

### **Core Components**
1. **Main Application**: `enc100.py` - PyQt6 GUI application
2. **TSDuck Integration**: Professional stream processing
3. **SCTE-35 System**: Complete marker generation and template system
4. **Multi-Platform**: Windows, macOS, Linux support
5. **Build System**: Professional build scripts with PyInstaller

### **🎬 SCTE-35 Components (NEW)**
1. **Marker Generation**: `scte35_xml_generator.py` - Core XML generation
2. **Generation Widget**: `scte35_generation_widget.py` - GUI for marker creation
3. **Template System**: `scte35_templates.py` - Professional broadcast templates
4. **Template Widget**: `scte35_template_widget.py` - GUI for template management
5. **Advanced Generator**: `scte35_marker_generator.py` - Advanced marker creation
6. **Simple Generator**: `scte35_simple_generator.py` - Simplified generation

### **Key Features**
- **Input Support**: HLS, SRT, UDP, TCP, File, HTTP/HTTPS
- **Output Support**: SRT, UDP, TCP, File with user-defined parameters
- **SCTE-35 System**: Complete marker generation and template system
- **Professional Templates**: 6 standard broadcast templates
- **Marker Types**: CUE-OUT, CUE-IN, CRASH-OUT, TIME_SIGNAL
- **Monitoring**: Real-time analytics and stream analysis
- **Theme**: Professional dark theme with Windows consistency

---

## 📊 **Project Progress Tracking**

### **Phase 1: Initial Development ✅ COMPLETED**
- [x] Basic GUI application structure
- [x] TSDuck integration
- [x] Input/output configuration
- [x] SCTE-35 support implementation

### **Phase 2: Issue Resolution ✅ COMPLETED**
- [x] **Windows Dark Theme Issue**: Fixed inconsistent theming
  - **Problem**: Dark theme not applied consistently on Windows
  - **Solution**: Platform detection + Fusion style + comprehensive CSS
  - **Files Modified**: `enc100.py` (main function)
  - **Result**: Consistent dark theme across all platforms

- [x] **Stream Start Issues**: Fixed output capture and display
  - **Problem**: Streams appeared to not start (no output visible)
  - **Solution**: Real-time output capture with threading
  - **Files Modified**: `enc100.py` (TSDuckProcessor class)
  - **Result**: Real-time output display in GUI console

- [x] **Smart PID Remapping**: Fixed PID conflicts
  - **Problem**: "PID present both in input and remap" errors
  - **Solution**: Smart conflict detection and conditional remapping
  - **Files Modified**: `enc100.py` (build_command method)
  - **Result**: No PID conflicts, SRT inputs work without remap

- [x] **Connection Testing**: Added pre-flight validation
  - **Problem**: Network issues not detected early
  - **Solution**: Connection testing before stream start
  - **Files Modified**: `enc100.py` (test_connection method)
  - **Result**: Early detection of network issues

### **Phase 3: Build & Distribution ✅ COMPLETED**
- [x] **Professional Build Scripts**: Enhanced build.sh and build.bat
- [x] **Cross-Platform Support**: Windows, macOS, Linux builds
- [x] **Distribution Files**: Standalone executables created
- [x] **GitHub Integration**: All files uploaded to repository
- [x] **Documentation**: Comprehensive README and usage guides

### **Phase 4: SCTE-35 Professional System ✅ COMPLETED**
- [x] **SCTE-35 Marker Generation**: Complete marker creation system
  - **Problem**: Need for professional SCTE-35 marker generation
  - **Solution**: XML generator with TSDuck compatibility
  - **Files Created**: `scte35_xml_generator.py`, `scte35_generation_widget.py`
  - **Result**: Professional marker generation with GUI interface

- [x] **Template System**: Professional broadcast templates
  - **Problem**: Need for standardized broadcast workflows
  - **Solution**: 6 standard templates for all broadcast scenarios
  - **Files Created**: `scte35_templates.py`, `scte35_template_widget.py`
  - **Result**: Professional template system with GUI management

- [x] **Enhanced User Interface**: New tabs for SCTE-35 functionality
  - **Problem**: Need for dedicated SCTE-35 interface
  - **Solution**: New tabs in main application
  - **Files Modified**: `enc100.py` (added new tabs)
  - **Result**: Integrated SCTE-35 generation and template management

- [x] **Professional Workflows**: Broadcast-ready capabilities
  - **Problem**: Need for professional broadcast workflows
  - **Solution**: Complete SCTE-35 system with templates
  - **Features**: Live broadcasting, on-demand content, scheduled programming
  - **Result**: Production-ready broadcast streaming solution

---

## 🎯 **Current Status Summary**

### **✅ Production Ready Features (v2.0.4)**
1. **Professional GUI**: Modern dark theme with consistent styling
2. **Stream Processing**: Real-time output with TSDuck integration
3. **Smart PID Handling**: Automatic conflict detection and resolution
4. **Connection Validation**: Pre-flight testing for network outputs
5. **Error Handling**: Comprehensive guidance for troubleshooting
6. **Multi-Platform**: Windows, macOS, Linux support
7. **Distribution**: Ready-to-use executables available
8. **Profile Management**: Save/load/delete stream configurations
9. **Continuous Streaming**: Auto-reconnect on disconnection
10. **Profile-Based Output Folders**: Automatic folder organization per profile
11. **Multiple Instance Support**: Run multiple app instances concurrently
12. **DASH/MPD Support**: Full DASH streaming with SCTE-35 markers

### **🎬 SCTE-35 Professional Features**
1. **Complete SCTE-35 System**: Professional marker generation for broadcast streams
2. **Marker Types**: Pre-roll, CUE-OUT, CUE-IN, Time Signal
3. **TSDuck Integration**: Direct XML output for professional stream processing
4. **Professional Workflows**: Live broadcasting, on-demand content, scheduled programming
5. **File Management**: Organized marker storage in `scte35_final/` directory

### **📁 v2.0.4 New Features**
1. **Profile-Based Output Folders**: 
   - Output folders automatically named after profile (e.g., `output/ProfileName/hls`)
   - Prevents conflicts when running multiple instances
   - Easy identification of output files per profile
   - Auto-directory creation when starting streams

2. **Multiple Instance Support**:
   - Each profile uses its own isolated output directory
   - No file conflicts between different profiles
   - Perfect for running multiple streams simultaneously

3. **Web Server Improvements**:
   - Auto-creates serving directory if missing
   - Works seamlessly with profile-based folders
   - Prevents "Directory not found" errors

4. **DASH/MPD Support**:
   - Full DASH streaming with `.mpd` manifest files
   - SCTE-35 markers included in DASH streams
   - CORS support for web players
   - Complete documentation (`DASH_MPD_GUIDE.md`)

### **🔧 Technical Implementation**
- **Language**: Python 3.9+ with PyQt6
- **Stream Processing**: TSDuck integration
- **Build System**: PyInstaller with professional scripts
- **Distribution**: Standalone executables with all dependencies
- **Documentation**: Comprehensive user guides and technical docs

### **📦 Available Distributions**
- **Standalone Executable**: `releases/IBE-100` (25MB)
- **macOS Installer**: `releases/IBE-100-1.0.0.dmg` (25MB)
- **Application Bundle**: `releases/IBE-100.app`
- **Source Code**: Complete repository with build scripts

---

## 🚀 **Future Development Guidelines**

### **When Adding New Features**
1. **Maintain Compatibility**: Ensure all platforms work
2. **Test Thoroughly**: Verify with different input/output types
3. **Update Documentation**: Keep README and guides current
4. **Rebuild Distribution**: Update executables after changes
5. **GitHub Sync**: Push all changes to repository

### **When Fixing Issues**
1. **Identify Root Cause**: Use console output and error messages
2. **Test Solution**: Verify fix works across all platforms
3. **Update Build**: Rebuild executables with fixes
4. **Document Changes**: Update relevant documentation
5. **GitHub Update**: Push fixes to repository

### **When Building/Deploying**
1. **Run Build Script**: Use `./build.sh onefile` or `build.bat onefile`
2. **Test Executables**: Verify all distributions work
3. **Update Releases**: Copy new files to `releases/` folder
4. **GitHub Push**: Upload all changes to repository
5. **Documentation**: Update version information

---

## 📋 **Key Files Reference**

### **Core Application**
- `enc100.py` - Main application with SCTE-35 integration
- `requirements.txt` - Python dependencies (includes threefive)
- `README.md` - Project documentation

### **🎬 SCTE-35 System**
- `scte35_xml_generator.py` - Core XML generation system
- `scte35_generation_widget.py` - GUI widget for marker creation
- `scte35_template_widget.py` - GUI widget for template management
- `scte35_templates.py` - Professional template system
- `scte35_marker_generator.py` - Advanced marker generation
- `scte35_simple_generator.py` - Simplified generation system

### **Build System**
- `build.sh` - macOS/Linux build script
- `build.bat` - Windows build script
- `IBE-100.spec` - PyInstaller specification

### **Distribution**
- `releases/IBE-100` - Standalone executable
- `releases/IBE-100-1.0.0.dmg` - macOS installer
- `releases/IBE-100.app` - Application bundle
- `releases/README.md` - Distribution documentation

### **Documentation**
- `WINDOWS_DARK_THEME_FIX.md` - Theme fix documentation
- `STREAM_START_FIX.md` - Stream processing fix documentation
- `SCTE35_GENERATION_GUIDE.md` - Complete SCTE-35 generation guide
- `SCTE35_TEMPLATES_GUIDE.md` - Professional template system guide
- `RELEASE_NOTES_v1.1.0.md` - Comprehensive release notes
- `AI_AGENT_INSTRUCTIONS.md` - This file

---

## 🔍 **Troubleshooting Guide**

### **Common Issues & Solutions**

#### **Stream Not Starting**
- **Check**: Console output for error messages
- **Verify**: Input source accessibility
- **Test**: Connection to output destination
- **Solution**: Use connection testing feature

#### **PID Remapping Conflicts**
- **Check**: Input type (SRT inputs skip remap automatically)
- **Verify**: Target PIDs don't conflict with input
- **Solution**: Smart remapping logic handles this automatically

#### **Theme Issues**
- **Check**: Platform detection working correctly
- **Verify**: qdarkstyle or fallback CSS applied
- **Solution**: Force Fusion style on Windows

#### **Build Issues**
- **Check**: PyInstaller installation
- **Verify**: All dependencies available
- **Solution**: Use `python3 -m PyInstaller` instead of `pyinstaller`

#### **SCTE-35 Generation Issues**
- **Check**: Template system availability
- **Verify**: threefive library installed
- **Solution**: Install threefive with `pip install threefive>=2.3.0`

#### **Template System Issues**
- **Check**: Template files in `scte35_templates/` directory
- **Verify**: JSON template format
- **Solution**: Recreate standard templates using template widget

---

## 📊 **Performance Metrics**

### **Build Results**
- **Executable Size**: 25MB (includes all dependencies)
- **Build Time**: ~2-3 minutes on macOS
- **Platform Support**: Windows, macOS, Linux
- **Dependencies**: All included in executable

### **Application Performance**
- **Startup Time**: <5 seconds
- **Memory Usage**: ~100MB base
- **Stream Processing**: Real-time with TSDuck
- **GUI Responsiveness**: Smooth with dark theme

---

## 🎯 **Success Criteria Met**

### **✅ Functional Requirements**
- [x] Professional GUI with dark theme
- [x] Multi-input support (HLS, SRT, UDP, TCP, File)
- [x] Multi-output support (SRT, UDP, TCP, File)
- [x] SCTE-35 ad insertion
- [x] Real-time monitoring and analytics
- [x] Cross-platform compatibility

### **✅ Technical Requirements**
- [x] TSDuck integration
- [x] Smart PID remapping
- [x] Connection testing
- [x] Error handling
- [x] Professional build system
- [x] Distribution packages

### **✅ Quality Requirements**
- [x] Consistent theming across platforms
- [x] Real-time output display
- [x] Comprehensive error guidance
- [x] Professional documentation
- [x] Production-ready executables

---

## 🚀 **Next Steps for AI Agent**

### **When Continuing Development**
1. **Review Current Status**: Check this file for latest progress
2. **Identify Issues**: Use console output and user feedback
3. **Implement Fixes**: Follow established patterns
4. **Test Thoroughly**: Verify across all platforms
5. **Update Documentation**: Keep this file current
6. **Rebuild & Deploy**: Update distribution files

### **When Helping Users**
1. **Check Documentation**: Refer to `releases/README.md`
2. **Verify Setup**: Ensure TSDuck and dependencies available
3. **Test Configuration**: Use connection testing features
4. **Provide Guidance**: Use specific error messages
5. **Update Instructions**: Improve documentation as needed

---

## 📝 **Version History**

### **v2.0.4 - Profile-Based Output Folders (January 2025)**
- ✅ Profile-based output folder organization
- ✅ Multiple instance support (no file conflicts)
- ✅ Auto-directory creation for output folders
- ✅ Web server directory auto-creation fix
- ✅ DASH/MPD support confirmed with SCTE-35
- ✅ Complete DASH/MPD documentation
- ✅ Profile name sanitization for filesystem compatibility

### **v2.0.3 - Profile Management & Continuous Streaming (January 2025)**
- ✅ Profile management system (save/load/delete)
- ✅ Editable profile combo box
- ✅ Profile persistence in JSON format
- ✅ Continuous streaming with auto-reconnect
- ✅ Exponential backoff retry logic
- ✅ Graceful shutdown handling

### **v2.0.2 - Auto-Update & License System (January 2025)**
- ✅ GitHub release checking for updates
- ✅ Update notification dialog
- ✅ GitHub-based license management
- ✅ Trial and unlimited license support
- ✅ Deployment troubleshooting tools

### **v2.0.1 - Clean Rebuild (December 2024)**
- ✅ Complete application rebuild from scratch
- ✅ Fixed SRT input configuration
- ✅ Fixed XML marker format (TSDuck compatible)
- ✅ Fixed PID conflict handling
- ✅ Fixed console window visibility
- ✅ Integrated web server for HLS/DASH

### **v1.1.0 - SCTE-35 Professional (October 25, 2024)**
- ✅ Complete SCTE-35 marker generation system
- ✅ Professional template system (6 standard templates)
- ✅ Enhanced user interface with new tabs
- ✅ TSDuck integration for broadcast streams
- ✅ Professional workflows for live broadcasting
- ✅ Marker types: CUE-OUT, CUE-IN, CRASH-OUT, TIME_SIGNAL
- ✅ Template scenarios: Preroll, Midroll, Postroll, Scheduled, Emergency, Multi-Break
- ✅ Comprehensive SCTE-35 documentation
- ✅ Enhanced build system with Windows support

### **v1.0.0 - Production Release (October 25, 2024)**
- ✅ Windows dark theme consistency fixed
- ✅ Stream start issues resolved with real-time output
- ✅ Smart PID remapping prevents conflicts
- ✅ Connection testing for network outputs
- ✅ Enhanced error handling with specific guidance
- ✅ Professional build system with distribution files
- ✅ Complete documentation and user guides

---

## 🎉 **Project Success Summary**

**The ITAssist Broadcast Encoder - 100 (IBE-100) v2.0.4 is now a fully functional, production-ready application with:**

- **Professional GUI**: Modern dark theme with consistent styling
- **Advanced Stream Processing**: TSDuck integration with smart PID handling
- **Complete SCTE-35 System**: Professional marker generation with multiple cue types
- **Profile Management**: Save/load/delete stream configurations
- **Continuous Streaming**: Auto-reconnect with exponential backoff
- **Profile-Based Output Folders**: Automatic folder organization per profile
- **Multiple Instance Support**: Run multiple app instances without conflicts
- **DASH/MPD Support**: Full DASH streaming with SCTE-35 markers
- **HLS Support**: Complete HLS streaming with SCTE-35 markers
- **Auto-Update System**: GitHub release checking
- **License Management**: GitHub-based license system (ready for integration)
- **Integrated Web Server**: Built-in server for HLS/DASH testing
- **Multi-Platform Support**: Windows, macOS, Linux compatibility
- **Production Distribution**: Ready-to-use executables available
- **Comprehensive Documentation**: Complete user guides and technical documentation
- **GitHub Integration**: All code and distributions available online

**🚀 Ready for professional broadcast operations with comprehensive SCTE-35 support and multi-instance capabilities!**
