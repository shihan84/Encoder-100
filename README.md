# ITAssist Broadcast Encoder - 100 (IBE-100)

## 🎬 Professional SCTE-35 Streaming Solution

**ITAssist Broadcast Encoder - 100 (IBE-100)** is a professional TSDuck-based SCTE-35 streaming system with advanced ad insertion capabilities for live broadcast distribution.

### 🏢 Company Information

**ITAssist Broadcast Solutions**  
Professional Broadcast Technology Solutions

**📍 Global Offices:**
- **Dubai, UAE**: Middle East Operations
- **Mumbai, India**: South Asia Headquarters  
- **Gurugram, India**: Technology Development Center

**📞 Contact:** support@itassist.one | https://itassist.one

---

## ✨ Features

### 🎯 Core Capabilities
- **Professional SCTE-35 Streaming** with real-time ad insertion
- **TSDuck Integration** for broadcast-grade stream processing
- **Multi-format Support** (HLS, UDP, TCP, SRT, HTTP, DVB, ASI)
- **Real-time Monitoring** with live analytics and performance metrics
- **Enterprise Configuration** with professional GUI interface
- **Multilingual Support** (English, Hindi, Arabic)

### 📊 Professional Monitoring
- **Live Stream Analytics** with TSDuck real-time analysis
- **System Performance Monitoring** (CPU, Memory, Network)
- **SCTE-35 Detection** with live splice marker monitoring
- **Stream Health Assessment** with automated alerts
- **Professional Logging** with timestamped performance data

### 🎬 SCTE-35 Features
- **Ad Insertion Events** (CUE-OUT, CUE-IN, Crash CUE-IN, Pre-roll)
- **XML Marker Management** for professional ad breaks
- **Real-time Splice Detection** with live monitoring
- **Professional Ad Duration** configuration (0-600 seconds)
- **Event ID Management** with sequential numbering

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **TSDuck 3.30+** installed and configured
- **PyQt6** for GUI interface
- **psutil** for system monitoring (optional)

### Installation
```bash
# Clone the repository
git clone https://github.com/shihan84/Encoder-100.git
cd Encoder-100

# Install dependencies
pip install PyQt6 psutil

# Run the application
python3 tsduck_gui_simplified.py
```

### TSDuck Installation
```bash
# macOS (using Homebrew)
brew install tsduck

# Ubuntu/Debian
sudo apt-get install tsduck

# Windows
# Download from https://tsduck.io/download/
```

---

## 🎯 Usage

### 1. Configuration
- **Input Configuration**: Select input source (HLS, UDP, TCP, SRT, etc.)
- **Service Configuration**: Set service name, provider, and IDs
- **PID Configuration**: Configure Video, Audio, and SCTE-35 PIDs
- **SCTE-35 Setup**: Configure ad duration, event IDs, and pre-roll settings

### 2. Monitoring
- **Real-time Analytics**: Live stream statistics and performance
- **System Monitoring**: CPU, memory, network usage
- **Stream Health**: Automated health assessment
- **Professional Logging**: Timestamped performance logs

### 3. SCTE-35 Operations
- **Ad Break Management**: Professional ad insertion control
- **Event Monitoring**: Live SCTE-35 marker detection
- **XML Configuration**: Custom marker file management
- **Real-time Analysis**: Live splice information monitoring

---

## 📋 Supported Formats

### Input Formats
- **HLS**: HTTP Live Streaming
- **UDP**: User Datagram Protocol
- **TCP**: Transmission Control Protocol
- **SRT**: Secure Reliable Transport
- **HTTP/HTTPS**: Web-based streaming
- **DVB**: Digital Video Broadcasting
- **ASI**: Asynchronous Serial Interface
- **File**: Local file processing

### Output Formats
- **SRT**: Secure Reliable Transport with stream ID
- **UDP**: Multicast and unicast streaming
- **File**: Local file output
- **HTTP**: Web-based distribution

---

## 🔧 Configuration

### Service Information
| Parameter | Description | Default Value | Range |
|-----------|-------------|---------------|-------|
| Service Name | Broadcast service name | SCTE-35 Stream | Any text |
| Provider Name | Organization name | ITAssist | Any text |
| Service ID | Unique service identifier | 1 | 1-65535 |
| Bouquet ID | Service bouquet identifier | 1 | 1-65535 |

### PID Configuration
| PID Type | Description | Default Value | Stream Type |
|----------|-------------|---------------|-------------|
| Video PID (VPID) | Video stream PID | 256 | H.264 (0x1b) |
| Audio PID (APID) | Audio stream PID | 257 | AAC-LC (0x0f) |
| SCTE-35 PID | SCTE-35 data PID | 500 | SCTE-35 (0x86) |
| Null PID | Null stream PID | 8191 | Null (0x1f) |
| PCR PID | Program Clock Reference PID | 256 | PCR (same as video) |

### SCTE-35 Configuration
- **Ad Duration**: 600 seconds (10 minutes) default
- **Event ID**: Sequential numbering starting from 100023
- **Pre-roll Duration**: 0-10 seconds
- **SCTE-35 PID**: 500 (configurable)

---

## 📊 Professional Features

### Real-time Monitoring
- **Bitrate Monitoring**: Live bitrate analysis with thresholds
- **Continuity Checking**: Transport stream continuity error detection
- **PCR Monitoring**: Program Clock Reference jitter analysis
- **Service Discovery**: Live service detection and counting
- **SCTE-35 Detection**: Real-time splice marker monitoring

### System Performance
- **CPU Usage**: Real-time CPU monitoring
- **Memory Usage**: Live memory consumption tracking
- **Network Usage**: Streaming bandwidth monitoring
- **Process Management**: TSDuck process monitoring
- **Health Assessment**: Automated stream health evaluation

### Professional Logging
- **Performance History**: Timestamped system metrics
- **Stream Analytics**: Real-time stream statistics
- **Error Tracking**: Comprehensive error logging
- **Event Logging**: SCTE-35 event tracking

---

## 🌐 Multilingual Support

### Documentation Languages
- **English**: Complete user manual and documentation
- **Hindi (हिंदी)**: Comprehensive Hindi documentation
- **Arabic (العربية)**: Complete Arabic user manual

### Professional Localization
- **User Interface**: Multilingual GUI elements
- **Help System**: Language-specific documentation
- **Error Messages**: Localized error reporting
- **Professional Support**: Multi-language technical support

---

## 🔒 Security & Compliance

### Professional Standards
- **TSDuck Integration**: Industry-standard broadcast processing
- **SCTE-35 Compliance**: Professional ad insertion standards
- **Security Features**: Secure network connections (SRT, HTTPS)
- **Access Control**: Professional user management
- **Audit Logging**: Comprehensive activity tracking

### Best Practices
- Keep TSDuck updated for security patches
- Use secure network connections (SRT, HTTPS)
- Monitor stream access and permissions
- Regular backup of configuration files
- Professional deployment practices

---

## 📞 Support

### Technical Support
- **Email**: support@itassist.one
- **Documentation**: https://tsduck.io/
- **Community**: TSDuck User Forum
- **Professional Support**: 24/7 Technical Support

### System Requirements
- **Operating System**: macOS, Linux, Windows
- **TSDuck**: Version 3.30 or later
- **Python**: 3.8 or later
- **PyQt6**: Latest version
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 1GB free space

---

## 📄 License

**© 2024 ITAssist Broadcast Solutions**  
**All Rights Reserved | Licensed Software**

This software is proprietary to ITAssist Broadcast Solutions and is licensed for professional broadcast operations.

---

## 🏢 About ITAssist Broadcast Solutions

**Professional Broadcast Technology Solutions**

**Services:**
- Professional SCTE-35 Streaming Solutions
- Broadcast Technology Consulting
- Custom Broadcast Software Development
- Multi-format Stream Processing
- Enterprise Broadcast Infrastructure

**Global Presence:**
- **Dubai, UAE**: Middle East Operations
- **Mumbai, India**: South Asia Headquarters
- **Gurugram, India**: Technology Development Center

---

**ITAssist Broadcast Encoder - 100 (IBE-100) v1.0**  
**Professional SCTE-35 Streaming Solution**  
**© 2024 ITAssist Broadcast Solutions**