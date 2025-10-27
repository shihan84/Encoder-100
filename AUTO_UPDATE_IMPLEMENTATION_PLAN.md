# 🔄 Auto-Update Implementation Plan for IBE-100

## 📋 **Overview**

Implementing automatic updates for IBE-100 v2.0.1 to keep users on the latest version with bug fixes and new features.

---

## 🎯 **Approach Options**

### **Option 1: Simple Version Check (Recommended for Start)**
**Easiest to implement, good for initial release**

#### How It Works:
1. Application checks a remote URL for latest version
2. Compares local version vs remote version
3. Shows notification if update available
4. User downloads and installs manually

#### Implementation:
```python
# In main.py - Add update checker
def check_for_updates(self):
    """Check for application updates"""
    import urllib.request
    import json
    
    try:
        # Check version from GitHub releases
        url = "https://api.github.com/repos/shihan84/Encoder-100/releases/latest"
        response = urllib.request.urlopen(url, timeout=5)
        data = json.loads(response.read())
        
        latest_version = data['tag_name']
        current_version = "2.0.1"
        
        if latest_version > current_version:
            # Show update dialog
            self.show_update_dialog(latest_version, data['html_url'])
        else:
            print("[INFO] Application is up to date")
            
    except Exception as e:
        print(f"[WARNING] Could not check for updates: {e}")
```

#### Features:
- ✅ Lightweight and fast
- ✅ No installation required
- ✅ User stays in control
- ✅ Works from first launch
- ✅ No permission issues

#### User Experience:
```
📦 Update Available!

A new version (v2.0.2) is available.
Current version: v2.0.1

Would you like to download it now?
[Download] [Later]
```

---

### **Option 2: Automatic Download & Install (Advanced)**
**More complex, seamless for users**

#### How It Works:
1. Check for updates on startup
2. Download new version in background
3. Show notification when download complete
4. Restart application with new version

#### Implementation Components:

**A. Update Checker Service**
```python
class UpdateChecker(QThread):
    """Background thread for checking updates"""
    update_available = pyqtSignal(str, str)  # version, download_url
    
    def run(self):
        # Check GitHub releases API
        latest = self.get_latest_version()
        if latest > self.current_version:
            self.update_available.emit(latest, download_url)
```

**B. Download Manager**
```python
class UpdateDownloader(QThread):
    """Download updates in background"""
    download_progress = pyqtSignal(int)  # percentage
    download_complete = pyqtSignal(str)  # file path
    
    def run(self):
        # Download to temp folder
        # Show progress bar
        # Verify file integrity
        # Signal completion
```

**C. Installation Manager**
```python
def install_update(self, update_file):
    """Install the downloaded update"""
    # Backup current version
    # Extract new version to application folder
    # Update version info
    # Restart application
```

#### Features:
- ✅ Automatic updates
- ✅ Background downloads
- ✅ Progress indication
- ✅ Resume capability
- ⚠️ Requires write permissions

---

### **Option 3: GitHub Releases Integration (Best for Production)**
**Professional, reliable, using GitHub infrastructure**

#### How It Works:
```
Application Start
    ↓
Check GitHub Releases API
    ↓
Compare version tags
    ↓
Download if newer available
    ↓
Install & Restart
```

#### Complete Implementation:

**1. Update Configuration**
```python
# config.py
UPDATE_URL = "https://api.github.com/repos/shihan84/Encoder-100/releases/latest"
CHECK_INTERVAL = 86400  # Check once per day
AUTO_DOWNLOAD = False  # Manual download for now
```

**2. Update Checker Class**
```python
class UpdateManager:
    def __init__(self, current_version):
        self.current_version = current_version
        self.latest_version = None
        self.download_url = None
    
    def check_update(self):
        """Check for available updates"""
        try:
            import urllib.request
            import json
            
            response = urllib.request.urlopen(UPDATE_URL, timeout=10)
            data = json.loads(response.read())
            
            self.latest_version = data['tag_name']
            self.download_url = data['assets'][0]['browser_download_url']
            
            return self.latest_version > self.current_version
            
        except Exception as e:
            print(f"Update check failed: {e}")
            return False
    
    def download_update(self, progress_callback=None):
        """Download update file"""
        # Implementation with progress tracking
        pass
```

**3. Update Dialog**
```python
class UpdateDialog(QDialog):
    """Dialog to prompt user about updates"""
    
    def __init__(self, version, changelog, download_url):
        super().__init__()
        self.download_url = download_url
        self.setup_ui(version, changelog)
    
    def setup_ui(self, version, changelog):
        # Title
        title = QLabel(f"Update Available: Version {version}")
        
        # Changelog
        changelog_text = QTextEdit()
        changelog_text.setPlainText(changelog)
        
        # Buttons
        download_btn = QPushButton("Download Now")
        later_btn = QPushButton("Later")
        
        download_btn.clicked.connect(self.download_update)
        later_btn.clicked.connect(self.reject)
```

**4. Main Application Integration**
```python
# In MainWindow.__init__()
def setup_auto_update(self):
    """Setup automatic update checking"""
    self.update_manager = UpdateManager("2.0.1")
    self.update_check_timer = QTimer()
    self.update_check_timer.timeout.connect(self.check_updates)
    self.update_check_timer.start(CHECK_INTERVAL * 1000)  # Convert to ms
    
    # Check once on startup
    QTimer.singleShot(5000, self.check_updates)

def check_updates(self):
    """Check for updates"""
    if self.update_manager.check_update():
        self.show_update_dialog()

def show_update_dialog(self):
    """Show update available dialog"""
    dialog = UpdateDialog(
        self.update_manager.latest_version,
        "Bug fixes and improvements",
        self.update_manager.download_url
    )
    dialog.exec()
```

---

## 🔧 **Implementation Steps**

### **Phase 1: Basic Version Check (Quick Win)**
**Time: 2-3 hours**

1. Create update configuration file
2. Add update checker function
3. Create update dialog UI
4. Integrate into main window
5. Test with mock version

### **Phase 2: Manual Download Integration**
**Time: 4-5 hours**

1. Add download functionality
2. Show download progress
3. Open download link in browser
4. User installs manually

### **Phase 3: Automatic Installation (Advanced)**
**Time: 8-10 hours**

1. Background download system
2. File integrity verification (checksums)
3. Backup current version
4. Extract and install
5. Restart application
6. Rollback capability

---

## 📊 **Recommended Approach**

### **For v2.0.1: Implement Phase 1**
**Why:**
- ✅ Simple and fast to implement
- ✅ No breaking changes
- ✅ Users stay in control
- ✅ Works immediately
- ✅ Can upgrade to Phase 2 later

### **Implementation for v2.0.1:**

```python
# Add to main.py
class UpdateChecker:
    """Simple update checker using GitHub Releases"""
    
    def __init__(self, current_version):
        self.current_version = current_version
        self.api_url = "https://api.github.com/repos/shihan84/Encoder-100/releases/latest"
    
    def check_for_updates(self):
        """Check if newer version is available"""
        try:
            import urllib.request
            import json
            from urllib.error import URLError
            
            req = urllib.request.Request(self.api_url)
            req.add_header('User-Agent', 'IBE-100/2.0.1')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                latest_version = data['tag_name']
                download_url = data['html_url']
                
                if latest_version != self.current_version:
                    return {
                        'available': True,
                        'version': latest_version,
                        'url': download_url,
                        'notes': data.get('body', '')
                    }
                
                return {'available': False}
                
        except Exception as e:
            print(f"[INFO] Could not check for updates: {e}")
            return {'available': False, 'error': str(e)}
```

**Add to MainWindow:**
```python
def show_update_notification(self):
    """Check and show update notification"""
    checker = UpdateChecker("2.0.1")
    result = checker.check_for_updates()
    
    if result.get('available'):
        self.show_update_dialog(
            result['version'],
            result['url'],
            result['notes']
        )

def show_update_dialog(self, version, url, notes):
    """Show update available dialog"""
    from PyQt6.QtWidgets import QMessageBox, QTextEdit
    
    msg = QMessageBox(self)
    msg.setWindowTitle("Update Available")
    msg.setText(f"<b>IBE-100 Version {version} is available!</b>")
    msg.setInformativeText(f"Current version: 2.0.1")
    
    details = QTextEdit()
    details.setPlainText(notes[:500])  # Limit to 500 chars
    details.setReadOnly(True)
    details.setMaximumHeight(150)
    msg.layout().addWidget(details, 1, 1, 1, 3)
    
    download_btn = msg.addButton("Download", QMessageBox.ButtonRole.AcceptRole)
    later_btn = msg.addButton("Later", QMessageBox.ButtonRole.RejectRole)
    
    msg.exec()
    
    if msg.clickedButton() == download_btn:
        import webbrowser
        webbrowser.open(url)
```

---

## 🎯 **Features**

### **What Gets Included:**

1. **Update Check on Startup**
   - Checks GitHub releases API
   - Compares version numbers
   - Shows notification if update available

2. **Manual Update Dialog**
   - Shows current vs latest version
   - Displays release notes
   - "Download" button opens GitHub releases page

3. **Configurable Checking**
   - Check on startup (default: enabled)
   - Check interval (default: once per day)
   - Skip notification option

4. **User Preferences**
   - Enable/disable auto-check
   - Check frequency
   - Show changelog option

---

## ⚙️ **Configuration Menu Addition**

Add to Settings/Preferences:
```python
# Update Settings Section
update_group = QGroupBox("Update Settings")
update_layout = QVBoxLayout()

auto_check = QCheckBox("Check for updates on startup")
auto_check.setChecked(True)
update_layout.addWidget(auto_check)

check_frequency = QComboBox()
check_frequency.addItems(["Daily", "Weekly", "Never"])
update_layout.addWidget(check_frequency)

update_group.setLayout(update_layout)
```

---

## 📝 **User Experience Flow**

### **First Launch:**
1. App checks for updates (silently in background)
2. If update found, shows notification
3. User clicks "Download"
4. Browser opens to GitHub releases
5. User downloads and installs

### **Subsequent Launches:**
1. If auto-check enabled, checks on startup
2. Only shows notification if update available
3. User can check manually from Help menu
4. Update notification appears as needed

### **Manual Check:**
1. User clicks "Check for Updates" in Help menu
2. Shows checking indicator
3. Displays result (up to date or update available)
4. Opens download page if update found

---

## ✅ **Benefits**

### **For Users:**
- ✅ Always know about new versions
- ✅ Easy access to updates
- ✅ Can see what's new in updates
- ✅ Stay current with bug fixes

### **For Developers:**
- ✅ Push updates easily
- ✅ Users notified automatically
- ✅ Track adoption rate
- ✅ Reduce support requests

---

## 🚀 **Next Steps**

1. **Implement Basic Checker** (2-3 hours)
2. **Add Update Dialog** (1 hour)
3. **Test with GitHub Releases** (1 hour)
4. **Add to Settings Menu** (1 hour)
5. **Release as v2.0.2**

**Total Implementation Time: 5-6 hours**

---

Would you like me to implement this for v2.0.2?

