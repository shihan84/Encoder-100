#!/usr/bin/env python3
"""
Optimized TSDuck GUI Launcher
Launches the TSDuck GUI with all optimizations enabled
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont

def create_splash_screen(app):
    """Create a splash screen for the application"""
    # Create a simple splash screen
    pixmap = QPixmap(400, 300)
    pixmap.fill(Qt.GlobalColor.darkBlue)
    
    splash = QSplashScreen(pixmap)
    splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
    
    # Add text to splash screen
    splash.showMessage(
        "TSDuck GUI\nLoading...",
        Qt.AlignmentFlag.AlignCenter,
        Qt.GlobalColor.white
    )
    
    return splash

def setup_application():
    """Setup the QApplication with optimizations"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("TSDuck GUI")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("TSDuck")
    
    # Set application style
    try:
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
        print("✅ Dark theme applied")
    except ImportError:
        print("⚠️  qdarkstyle not available, using default theme")
    
    # Set application font
    font = QFont("SF Pro Display", 9)
    if not font.exactMatch():
        font = QFont("Segoe UI", 9)
    if not font.exactMatch():
        font = QFont("Arial", 9)
    app.setFont(font)
    
    return app

def main():
    """Main launcher function"""
    print("🚀 TSDuck GUI - Optimized Launcher")
    print("=" * 50)
    
    # Setup application first
    app = setup_application()
    
    # Create splash screen after app is created
    splash = create_splash_screen(app)
    splash.show()
    
    # Process events to show splash screen
    QApplication.processEvents()
    
    # Update splash screen
    splash.showMessage("Loading TSDuck GUI...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
    QApplication.processEvents()
    
    # Import and create main window
    try:
        from tsduck_gui import MainWindow
        
        splash.showMessage("Initializing GUI...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
        QApplication.processEvents()
        
        # Create main window
        window = MainWindow()
        
        splash.showMessage("Finalizing...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
        QApplication.processEvents()
        
        # Show main window
        window.show()
        
        # Close splash screen
        splash.finish(window)
        
        print("✅ TSDuck GUI launched successfully")
        print("🎯 Features enabled:")
        print("   - Modern dark/light themes")
        print("   - Performance optimizations")
        print("   - Memory management")
        print("   - Keyboard shortcuts")
        print("   - Responsive layout")
        
        # Run application
        sys.exit(app.exec())
        
    except ImportError as e:
        splash.close()
        print(f"❌ Error importing TSDuck GUI: {e}")
        print("Please ensure tsduck_gui.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        splash.close()
        print(f"❌ Error launching TSDuck GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
