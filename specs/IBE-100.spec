# -*- mode: python ; coding: utf-8 -*-
"""
ITAssist Broadcast Encoder - 100 (IBE-100)
PyInstaller Spec File for Professional Packaging
Cross-platform application specification
"""

import os
import sys
from pathlib import Path

# Application Information
APP_NAME = "IBE-100"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "ITAssist Broadcast Encoder - 100 (IBE-100)"
APP_AUTHOR = "ITAssist Broadcast Solutions"

# Platform detection
PLATFORM = sys.platform.lower()

# Data files to include
data_files = [
    ('scte35_final', 'scte35_final'),
    ('README.md', '.'),
    ('LICENSE.txt', '.'),
    ('requirements.txt', '.'),
]

# TSDuck binary inclusion (platform-specific)
tsduck_files = []
if PLATFORM == "darwin":
    # macOS TSDuck paths
    tsduck_paths = [
        "/usr/local/bin/tsp",
        "/usr/bin/tsp",
        "/opt/tsduck/bin/tsp"
    ]
elif PLATFORM == "linux":
    # Linux TSDuck paths
    tsduck_paths = [
        "/usr/bin/tsp",
        "/usr/local/bin/tsp",
        "/opt/tsduck/bin/tsp"
    ]
elif PLATFORM == "win32":
    # Windows TSDuck paths
    tsduck_paths = [
        "C:\\Program Files\\TSDuck\\bin\\tsp.exe",
        "C:\\Program Files (x86)\\TSDuck\\bin\\tsp.exe",
        "C:\\tsduck\\bin\\tsp.exe"
    ]
else:
    tsduck_paths = []

# Find and include TSDuck binary
for tsduck_path in tsduck_paths:
    if os.path.exists(tsduck_path):
        tsduck_files.append((tsduck_path, 'tsduck'))
        break

# Combine all data files
all_data_files = data_files + tsduck_files

# Hidden imports for PyQt6 and dependencies
hidden_imports = [
    'PyQt6.QtCore',
    'PyQt6.QtWidgets',
    'PyQt6.QtGui',
    'PyQt6.QtOpenGL',
    'PyQt6.QtPrintSupport',
    'psutil',
    'subprocess',
    'threading',
    'queue',
    'json',
    'xml',
    'shutil',
    'platform',
    'os',
    'sys'
]

# Exclude unnecessary modules
excludes = [
    'tkinter',
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'PIL',
    'cv2',
    'tensorflow',
    'torch',
    'sklearn'
]

# Platform-specific icon
if PLATFORM == "darwin":
    icon_path = "assets/icon.icns"
elif PLATFORM == "win32":
    icon_path = "assets/icon.ico"
else:
    icon_path = "assets/icon.png"

# Main analysis
a = Analysis(
    ['tsduck_gui_simplified.py'],
    pathex=[],
    binaries=[],
    datas=all_data_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove duplicate binaries
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Platform-specific executable configuration
if PLATFORM == "darwin":
    # macOS App Bundle
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name=APP_NAME,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icon_path,
    )
    
    # Create macOS App Bundle
    app = BUNDLE(
        exe,
        name=f'{APP_NAME}.app',
        icon=icon_path,
        bundle_identifier=f'com.itassist.{APP_NAME.lower()}',
        info_plist={
            'CFBundleName': APP_NAME,
            'CFBundleDisplayName': APP_NAME,
            'CFBundleIdentifier': f'com.itassist.{APP_NAME.lower()}',
            'CFBundleVersion': APP_VERSION,
            'CFBundleShortVersionString': APP_VERSION,
            'CFBundleInfoDictionaryVersion': '6.0',
            'CFBundleExecutable': APP_NAME,
            'CFBundlePackageType': 'APPL',
            'CFBundleSignature': 'IBE1',
            'LSMinimumSystemVersion': '10.14.0',
            'NSHighResolutionCapable': True,
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleDocumentTypes': [],
            'CFBundleURLTypes': [],
            'NSHumanReadableCopyright': '© 2024 ITAssist Broadcast Solutions | Dubai • Mumbai • Gurugram'
        }
    )

elif PLATFORM == "win32":
    # Windows Executable
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name=APP_NAME,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icon_path,
        version='assets/version_info.txt'
    )

else:
    # Linux Executable
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name=APP_NAME,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icon_path,
    )

# Create directory distribution (alternative to onefile)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME
)
