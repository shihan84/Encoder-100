# TSDuck GUI Installation Guide

This guide provides detailed installation instructions for TSDuck GUI on different operating systems.

## Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+, CentOS 7+, etc.)
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: At least 1GB free space
- **Network**: Internet connection for downloading dependencies

### Required Software
1. **TSDuck**: The MPEG Transport Stream Toolkit
2. **Python 3.8+**: Python interpreter and pip package manager
3. **Git**: For cloning the repository (optional)

## Installation Methods

### Method 1: Quick Installation (Recommended)

1. **Clone or download the repository**:
   ```bash
   git clone https://github.com/tsduck-gui/tsduck-gui.git
   cd tsduck-gui
   ```

2. **Run the launcher script**:
   ```bash
   python launch.py
   ```
   
   The launcher will automatically:
   - Check Python version
   - Verify TSDuck installation
   - Install missing dependencies
   - Launch the application

### Method 2: Manual Installation

#### Step 1: Install TSDuck

**macOS (using Homebrew)**:
```bash
brew install tsduck
```

**Windows (using winget)**:
```cmd
winget install tsduck
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install tsduck
```

**Linux (CentOS/RHEL/Fedora)**:
```bash
# For CentOS/RHEL
sudo yum install tsduck

# For Fedora
sudo dnf install tsduck
```

#### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Install the Application

```bash
python setup.py install
```

#### Step 4: Run the Application

```bash
python tsduck_gui.py
```

### Method 3: Development Installation

For developers who want to modify the code:

```bash
# Clone the repository
git clone https://github.com/tsduck-gui/tsduck-gui.git
cd tsduck-gui

# Install in development mode
pip install -e ".[dev]"

# Run tests
make test

# Run the application
make run
```

## Platform-Specific Instructions

### Windows

#### Prerequisites
- Windows 10 or later
- Python 3.8+ from [python.org](https://python.org)
- Visual Studio Build Tools (for some Python packages)

#### Installation Steps

1. **Install Python**:
   - Download Python from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **Install TSDuck**:
   ```cmd
   winget install tsduck
   ```

3. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```cmd
   python tsduck_gui.py
   ```

#### Troubleshooting Windows Issues

- **"tsp is not recognized"**: Add TSDuck to your PATH environment variable
- **PyQt6 installation fails**: Install Visual Studio Build Tools
- **Permission errors**: Run Command Prompt as Administrator

### macOS

#### Prerequisites
- macOS 10.14 (Mojave) or later
- Xcode Command Line Tools
- Homebrew (recommended)

#### Installation Steps

1. **Install Xcode Command Line Tools**:
   ```bash
   xcode-select --install
   ```

2. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Install TSDuck**:
   ```bash
   brew install tsduck
   ```

4. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python3 tsduck_gui.py
   ```

#### Troubleshooting macOS Issues

- **"tsp: command not found"**: Ensure Homebrew is in your PATH
- **PyQt6 issues**: Install with `pip3 install PyQt6`
- **Permission errors**: Use `pip3 install --user` for user-only installation

### Linux

#### Ubuntu/Debian

1. **Update package list**:
   ```bash
   sudo apt-get update
   ```

2. **Install dependencies**:
   ```bash
   sudo apt-get install python3 python3-pip python3-venv build-essential
   ```

3. **Install TSDuck**:
   ```bash
   sudo apt-get install tsduck
   ```

4. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python3 tsduck_gui.py
   ```

#### CentOS/RHEL/Fedora

1. **Install dependencies**:
   ```bash
   # CentOS/RHEL
   sudo yum install python3 python3-pip gcc gcc-c++ make
   
   # Fedora
   sudo dnf install python3 python3-pip gcc gcc-c++ make
   ```

2. **Install TSDuck**:
   ```bash
   # CentOS/RHEL
   sudo yum install tsduck
   
   # Fedora
   sudo dnf install tsduck
   ```

3. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python3 tsduck_gui.py
   ```

#### Troubleshooting Linux Issues

- **"tsp: command not found"**: Add TSDuck to your PATH or install from source
- **PyQt6 issues**: Install system packages: `sudo apt-get install python3-pyqt6`
- **Permission errors**: Use virtual environment or `pip3 install --user`

## Docker Installation

### Using Docker (Alternative Method)

1. **Build the Docker image**:
   ```bash
   docker build -t tsduck-gui .
   ```

2. **Run the container**:
   ```bash
   # For Linux
   docker run -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY tsduck-gui
   
   # For macOS (with XQuartz)
   docker run -it --rm -e DISPLAY=host.docker.internal:0 tsduck-gui
   
   # For Windows (with X11 server)
   docker run -it --rm -e DISPLAY=host.docker.internal:0 tsduck-gui
   ```

## Verification

After installation, verify that everything is working:

1. **Check TSDuck**:
   ```bash
   tsp --version
   ```

2. **Check Python dependencies**:
   ```bash
   python -c "import PyQt6; print('PyQt6: OK')"
   python -c "import numpy; print('NumPy: OK')"
   python -c "import matplotlib; print('Matplotlib: OK')"
   ```

3. **Run the application**:
   ```bash
   python tsduck_gui.py
   ```

## Uninstallation

### Remove Python Package
```bash
pip uninstall tsduck-gui
```

### Remove Dependencies (Optional)
```bash
pip uninstall PyQt6 numpy matplotlib psutil requests pyqtgraph qdarkstyle
```

### Remove TSDuck
```bash
# macOS
brew uninstall tsduck

# Windows
winget uninstall tsduck

# Linux
sudo apt-get remove tsduck  # Ubuntu/Debian
sudo yum remove tsduck      # CentOS/RHEL
sudo dnf remove tsduck      # Fedora
```

## Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'PyQt6'"
**Solution**: Install PyQt6:
```bash
pip install PyQt6
```

### Issue: "tsp: command not found"
**Solution**: 
1. Verify TSDuck is installed: `which tsp`
2. Add TSDuck to your PATH
3. Restart your terminal

### Issue: "Permission denied" errors
**Solution**: 
1. Use virtual environment: `python -m venv venv && source venv/bin/activate`
2. Or install with user flag: `pip install --user -r requirements.txt`

### Issue: GUI doesn't start
**Solution**:
1. Check if you have a display server running (X11, Wayland, etc.)
2. For remote connections, enable X11 forwarding: `ssh -X user@host`
3. Check if PyQt6 is properly installed

### Issue: "TSDuck Python bindings not available"
**Solution**: This is not critical - the application will use subprocess mode instead

## Getting Help

If you encounter issues:

1. **Check the logs**: Look for error messages in the console output
2. **Verify installation**: Run `make check` to verify all components
3. **Check dependencies**: Run `make check-deps` to verify Python packages
4. **Check TSDuck**: Run `make check-tsduck` to verify TSDuck installation
5. **Search issues**: Check the GitHub issues page for similar problems
6. **Create issue**: If the problem persists, create a new issue with:
   - Operating system and version
   - Python version
   - TSDuck version
   - Complete error message
   - Steps to reproduce

## Next Steps

After successful installation:

1. **Read the documentation**: See README.md for usage instructions
2. **Try examples**: Check the examples/ directory for sample configurations
3. **Explore features**: Start with basic analysis and work up to advanced features
4. **Join community**: Participate in discussions and report issues

## Support

For additional support:
- **Documentation**: README.md and inline help
- **Issues**: GitHub Issues page
- **Community**: TSDuck community forums
- **Email**: Contact the maintainers
