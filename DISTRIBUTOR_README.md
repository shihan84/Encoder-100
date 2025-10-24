# TSDuck GUI - Distributor Streaming Configuration

## 🎯 Your Streaming Setup

This configuration is specifically designed for your distributor requirements:

- **Input**: HLS stream from `https://cdn.itassist.one/BREAKING/NEWS/index.m3u8`
- **Output**: SRT stream to `srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish`
- **SCTE-35**: Full splice information support with PID 500

## 🚀 Quick Start

### 1. Run Quick Setup
```bash
python3 quick_start.py
```

### 2. Launch Distributor Configuration
```bash
python3 launch_distributor.py
```

### 3. Configure & Start Streaming
- Click "Configure SCTE-35 & Stream Specs"
- Set your specific requirements
- Click "Launch TSDuck GUI with Configuration"
- Start processing!

## 📋 Your Distributor Specifications

### Video Requirements ✅
- **Resolution**: 1920x1080 HD
- **Codec**: H.264
- **PCR**: Video Embedded
- **Profile@Level**: High@Auto
- **GOP**: 12
- **B Frames**: 5
- **Bitrate**: 5 Mbps
- **Chroma**: 4:2:0
- **Aspect Ratio**: 16:9

### Audio Requirements ✅
- **Codec**: AAC-LC
- **Bitrate**: 128 Kbps
- **LKFS**: -20 dB
- **Sample Rate**: 48kHz

### SCTE-35 Requirements ✅
- **Data PID**: 500
- **Null PID**: 8191
- **Event ID**: 100023 (incremental)
- **Ad Duration**: 600 seconds (10 minutes)
- **Pre-roll**: 0-10 seconds
- **SRT Latency**: 2000ms (2 seconds)

### SCTE-35 Events ✅
- **CUE-OUT**: Program out point (start of ad)
- **CUE-IN**: Program in point (end of ad)
- **Crash CUE-IN**: Emergency return to program

## 🛠️ Configuration Files

### `distributor_config.json`
Your main configuration file with all settings:
```json
{
  "input": {
    "type": "hls",
    "source": "https://cdn.itassist.one/BREAKING/NEWS/index.m3u8"
  },
  "output": {
    "type": "srt", 
    "source": "srt://cdn.itassist.one:8888?streamid=#!::r=scte/scte,m=publish"
  },
  "scte35": {
    "data_pid": 500,
    "null_pid": 8191,
    "event_id": 100023,
    "ad_duration": 600
  }
}
```

## 🎮 Usage Guide

### Step 1: Launch Distributor Configuration
```bash
python3 launch_distributor.py
```

### Step 2: Configure SCTE-35
1. Click "Configure SCTE-35 & Stream Specs"
2. Set your event parameters:
   - Event ID: 100023 (or your next sequential ID)
   - Ad Duration: 600 seconds
   - SCTE Data PID: 500
   - Event Type: CUE-OUT/CUE-IN/Crash CUE-IN

### Step 3: Test Configuration
1. Click "Test Configuration"
2. Verify HLS input is accessible
3. Check SRT output connectivity

### Step 4: Launch TSDuck GUI
1. Click "Launch TSDuck GUI with Configuration"
2. All settings will be pre-configured
3. Click "Start Processing"

## 📊 Monitoring & Analysis

### Real-Time Monitoring
- **Stream Statistics**: Bitrate, packets/sec, errors
- **SCTE-35 Events**: Live splice detection and analysis
- **Service Discovery**: All services with PID mappings
- **Performance Metrics**: CPU, memory, network usage

### Source Preview
- **Stream Analysis**: Complete stream breakdown
- **Service Information**: All services and their PIDs
- **PID Analysis**: Detailed PID information
- **Table Information**: PSI/SI tables

## 🔧 Advanced Features

### Plugin Configuration
- **Analysis**: analyze, bitrate_monitor, continuity, stats
- **Processing**: filter, inject, limit, regulate, remap
- **SCTE-35**: spliceinject, splicemonitor, rmsplice
- **Tables**: pat, pmt, sdt, eit, nit, bat
- **Services**: svremove, svrename, svresync

### Configuration Management
- **Save/Load**: JSON-based configuration files
- **Presets**: Pre-configured setups for different scenarios
- **Validation**: Automatic configuration validation
- **Error Handling**: Comprehensive error reporting

## 🚨 Troubleshooting

### Common Issues

1. **HLS Input Not Accessible**
   - Check network connectivity
   - Verify HLS URL is correct
   - Test with browser or VLC

2. **SRT Output Connection Failed**
   - Verify SRT server is running
   - Check firewall settings
   - Confirm port 8888 is open

3. **SCTE-35 Events Not Working**
   - Verify PID 500 is available
   - Check event ID is unique
   - Confirm splice timing

### Debug Mode
```bash
# Run with debug output
python3 tsduck_gui.py --debug

# Test TSDuck directly
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -P analyze -O null
```

## 📈 Performance Optimization

### Recommended Settings
- **Buffer Size**: 2,000,000 packets
- **Real-time**: Enabled
- **Monitoring**: Enabled
- **Threading**: Background processing

### System Requirements
- **CPU**: Multi-core recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Network**: Stable connection for streaming
- **Storage**: SSD recommended for better performance

## 🔄 Workflow Examples

### Standard Ad Insertion
1. Configure CUE-OUT event (Event ID: 100023)
2. Set ad duration: 600 seconds
3. Start processing
4. Monitor for CUE-IN event

### Emergency Return
1. Configure Crash CUE-IN event
2. Set immediate execution
3. Send emergency return signal
4. Verify program restoration

### Pre-roll Ad
1. Configure pre-roll duration (0-10 seconds)
2. Set immediate CUE-OUT
3. Configure short duration CUE-IN
4. Start with pre-roll enabled

## 📞 Support

### Configuration Issues
- Check `distributor_config.json` syntax
- Verify all required fields are present
- Test with sample configuration

### Technical Issues
- Run `python3 test_gui.py` for diagnostics
- Check TSDuck installation: `tsp --version`
- Verify Python dependencies: `pip list`

### Stream Issues
- Use source preview to analyze input
- Check real-time monitoring for errors
- Verify SCTE-35 events in splicemonitor

## 🎯 Success Indicators

### ✅ Configuration Working
- HLS input accessible
- SRT output connected
- SCTE-35 events detected
- No continuity errors
- Stable bitrate

### ✅ SCTE-35 Working
- Events injected successfully
- Proper timing maintained
- Ad duration respected
- Clean transitions
- No splice errors

Your TSDuck GUI is now configured for professional distributor streaming with full SCTE-35 support!
