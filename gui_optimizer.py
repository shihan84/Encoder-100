#!/usr/bin/env python3
"""
GUI Optimizer for TSDuck GUI
Implements performance optimizations, modern styling, and enhanced UX
"""

import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from typing import Dict, List, Any, Optional

class OptimizedStyleSheet:
    """Modern, optimized stylesheet for TSDuck GUI"""
    
    @staticmethod
    def get_dark_theme() -> str:
        """Get modern dark theme stylesheet"""
        return """
        /* Modern Dark Theme */
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            font-family: 'SF Pro Display', 'Segoe UI', 'Roboto', sans-serif;
            font-size: 9pt;
        }
        
        /* Group Boxes */
        QGroupBox {
            font-weight: bold;
            border: 2px solid #404040;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: #353535;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #64b5f6;
            font-size: 10pt;
            font-weight: 600;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #404040;
            border: 1px solid #555555;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 500;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #4a4a4a;
            border-color: #64b5f6;
        }
        
        QPushButton:pressed {
            background-color: #2a2a2a;
        }
        
        QPushButton:disabled {
            background-color: #2a2a2a;
            color: #666666;
            border-color: #333333;
        }
        
        /* Primary Action Buttons */
        QPushButton[class="primary"] {
            background-color: #1976d2;
            border-color: #1976d2;
            color: white;
        }
        
        QPushButton[class="primary"]:hover {
            background-color: #1565c0;
        }
        
        QPushButton[class="success"] {
            background-color: #388e3c;
            border-color: #388e3c;
            color: white;
        }
        
        QPushButton[class="success"]:hover {
            background-color: #2e7d32;
        }
        
        QPushButton[class="warning"] {
            background-color: #f57c00;
            border-color: #f57c00;
            color: white;
        }
        
        QPushButton[class="warning"]:hover {
            background-color: #ef6c00;
        }
        
        QPushButton[class="danger"] {
            background-color: #d32f2f;
            border-color: #d32f2f;
            color: white;
        }
        
        QPushButton[class="danger"]:hover {
            background-color: #c62828;
        }
        
        /* Input Fields */
        QLineEdit, QSpinBox, QComboBox {
            background-color: #404040;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 6px 8px;
            selection-background-color: #64b5f6;
        }
        
        QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
            border-color: #64b5f6;
            border-width: 2px;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #ffffff;
            margin-right: 5px;
        }
        
        /* Text Areas */
        QTextEdit, QPlainTextEdit {
            background-color: #1e1e1e;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 8px;
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
            font-size: 9pt;
        }
        
        /* Tables */
        QTableWidget {
            background-color: #2b2b2b;
            alternate-background-color: #353535;
            selection-background-color: #64b5f6;
            gridline-color: #404040;
            border: 1px solid #555555;
            border-radius: 4px;
        }
        
        QTableWidget::item {
            padding: 6px;
            border: none;
        }
        
        QTableWidget::item:selected {
            background-color: #64b5f6;
            color: #000000;
        }
        
        QHeaderView::section {
            background-color: #404040;
            color: #ffffff;
            padding: 8px;
            border: none;
            border-right: 1px solid #555555;
            border-bottom: 1px solid #555555;
            font-weight: 600;
        }
        
        /* Tabs */
        QTabWidget::pane {
            border: 1px solid #555555;
            border-radius: 4px;
            background-color: #2b2b2b;
        }
        
        QTabBar::tab {
            background-color: #404040;
            color: #ffffff;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #2b2b2b;
            border-bottom: 2px solid #64b5f6;
        }
        
        QTabBar::tab:hover {
            background-color: #4a4a4a;
        }
        
        /* Progress Bars */
        QProgressBar {
            border: 1px solid #555555;
            border-radius: 4px;
            text-align: center;
            background-color: #404040;
        }
        
        QProgressBar::chunk {
            background-color: #64b5f6;
            border-radius: 3px;
        }
        
        /* Checkboxes */
        QCheckBox {
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #555555;
            border-radius: 3px;
            background-color: #404040;
        }
        
        QCheckBox::indicator:checked {
            background-color: #64b5f6;
            border-color: #64b5f6;
        }
        
        /* Scrollbars */
        QScrollBar:vertical {
            background-color: #404040;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #666666;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #777777;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        /* Status Bar */
        QStatusBar {
            background-color: #353535;
            border-top: 1px solid #555555;
            color: #ffffff;
        }
        
        /* Menu Bar */
        QMenuBar {
            background-color: #353535;
            color: #ffffff;
            border-bottom: 1px solid #555555;
        }
        
        QMenuBar::item {
            padding: 6px 12px;
            background-color: transparent;
        }
        
        QMenuBar::item:selected {
            background-color: #4a4a4a;
        }
        
        QMenu {
            background-color: #404040;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 4px;
        }
        
        QMenu::item {
            padding: 6px 20px;
        }
        
        QMenu::item:selected {
            background-color: #64b5f6;
            color: #000000;
        }
        
        /* Tooltips */
        QToolTip {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 4px;
        }
        """
    
    @staticmethod
    def get_light_theme() -> str:
        """Get modern light theme stylesheet"""
        return """
        /* Modern Light Theme */
        QMainWindow {
            background-color: #fafafa;
            color: #212121;
        }
        
        QWidget {
            background-color: #fafafa;
            color: #212121;
            font-family: 'SF Pro Display', 'Segoe UI', 'Roboto', sans-serif;
            font-size: 9pt;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: #ffffff;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #1976d2;
            font-size: 10pt;
            font-weight: 600;
        }
        
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 500;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #f5f5f5;
            border-color: #1976d2;
        }
        
        QPushButton:pressed {
            background-color: #eeeeee;
        }
        
        QLineEdit, QSpinBox, QComboBox {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 6px 8px;
            selection-background-color: #1976d2;
        }
        
        QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
            border-color: #1976d2;
            border-width: 2px;
        }
        
        QTextEdit, QPlainTextEdit {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 8px;
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
            font-size: 9pt;
        }
        
        QTableWidget {
            background-color: #ffffff;
            alternate-background-color: #f8f9fa;
            selection-background-color: #1976d2;
            gridline-color: #e0e0e0;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        
        QHeaderView::section {
            background-color: #f5f5f5;
            color: #212121;
            padding: 8px;
            border: none;
            border-right: 1px solid #e0e0e0;
            border-bottom: 1px solid #e0e0e0;
            font-weight: 600;
        }
        """

class PerformanceOptimizer:
    """Performance optimization utilities"""
    
    @staticmethod
    def optimize_table(table: QTableWidget):
        """Optimize table widget performance"""
        # Disable sorting for better performance
        table.setSortingEnabled(False)
        
        # Set alternating row colors
        table.setAlternatingRowColors(True)
        
        # Disable word wrap
        table.setWordWrap(False)
        
        # Set selection behavior
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Optimize header
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)
        
        # Set edit triggers
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Enable smooth scrolling
        table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
    
    @staticmethod
    def optimize_text_widget(widget: QTextEdit):
        """Optimize text widget performance"""
        # Set monospace font
        font = QFont("Monaco", 9)
        if not font.exactMatch():
            font = QFont("Consolas", 9)
        if not font.exactMatch():
            font = QFont("Courier New", 9)
        widget.setFont(font)
        
        # Set read-only for output widgets
        widget.setReadOnly(True)
        
        # Enable line wrap
        widget.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        
        # Set maximum block count to prevent memory issues
        widget.document().setMaximumBlockCount(10000)
    
    @staticmethod
    def optimize_tree_widget(tree: QTreeWidget):
        """Optimize tree widget performance"""
        # Set alternating row colors
        tree.setAlternatingRowColors(True)
        
        # Disable sorting for better performance
        tree.setSortingEnabled(False)
        
        # Set selection behavior
        tree.setSelectionBehavior(QTreeWidget.SelectionBehavior.SelectRows)
        
        # Enable smooth scrolling
        tree.setVerticalScrollMode(QTreeWidget.ScrollMode.ScrollPerPixel)
        tree.setHorizontalScrollMode(QTreeWidget.ScrollMode.ScrollPerPixel)

class ResponsiveLayout:
    """Responsive layout utilities"""
    
    @staticmethod
    def create_responsive_splitter(orientation=Qt.Orientation.Horizontal) -> QSplitter:
        """Create a responsive splitter"""
        splitter = QSplitter(orientation)
        splitter.setChildrenCollapsible(False)
        splitter.setHandleWidth(8)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #555555;
                border: 1px solid #666666;
            }
            QSplitter::handle:hover {
                background-color: #64b5f6;
            }
        """)
        return splitter
    
    @staticmethod
    def create_scrollable_widget(widget: QWidget) -> QScrollArea:
        """Create a scrollable wrapper for a widget"""
        scroll_area = QScrollArea()
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        return scroll_area

class KeyboardShortcuts:
    """Keyboard shortcuts manager"""
    
    @staticmethod
    def setup_shortcuts(window: QMainWindow):
        """Setup keyboard shortcuts for the main window"""
        shortcuts = {
            'Ctrl+N': 'New Configuration',
            'Ctrl+O': 'Open Configuration',
            'Ctrl+S': 'Save Configuration',
            'Ctrl+R': 'Start Processing',
            'Ctrl+E': 'Stop Processing',
            'Ctrl+P': 'Preview Source',
            'F1': 'Help',
            'F5': 'Refresh',
            'Ctrl+Q': 'Quit'
        }
        
        for key, description in shortcuts.items():
            action = QAction(description, window)
            action.setShortcut(QKeySequence(key))
            window.addAction(action)
        
        return shortcuts

class ThemeManager:
    """Theme management utilities"""
    
    def __init__(self, app: QApplication):
        self.app = app
        self.current_theme = "dark"
    
    def apply_theme(self, theme: str = "dark"):
        """Apply theme to the application"""
        self.current_theme = theme
        
        if theme == "dark":
            stylesheet = OptimizedStyleSheet.get_dark_theme()
        elif theme == "light":
            stylesheet = OptimizedStyleSheet.get_light_theme()
        else:
            return
        
        self.app.setStyleSheet(stylesheet)
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new_theme)
        return new_theme

class MemoryOptimizer:
    """Memory optimization utilities"""
    
    @staticmethod
    def clear_text_widget(widget: QTextEdit, max_lines: int = 1000):
        """Clear old content from text widget to prevent memory issues"""
        document = widget.document()
        if document.blockCount() > max_lines:
            # Keep only the last max_lines
            cursor = widget.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            cursor.movePosition(QTextCursor.MoveOperation.Down, 
                              QTextCursor.MoveMode.KeepAnchor, 
                              document.blockCount() - max_lines)
            cursor.removeSelectedText()
    
    @staticmethod
    def optimize_table_memory(table: QTableWidget, max_rows: int = 10000):
        """Optimize table memory usage"""
        if table.rowCount() > max_rows:
            # Remove old rows
            rows_to_remove = table.rowCount() - max_rows
            for i in range(rows_to_remove):
                table.removeRow(0)

class LoadingIndicator:
    """Loading indicator widget"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.indicator = None
    
    def show_loading(self, message: str = "Loading..."):
        """Show loading indicator"""
        if self.indicator is None:
            self.indicator = QProgressDialog(message, "Cancel", 0, 0, self.parent)
            self.indicator.setWindowModality(Qt.WindowModality.WindowModal)
            self.indicator.setCancelButton(None)  # Disable cancel button
            self.indicator.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.indicator.setLabelText(message)
        self.indicator.show()
        QApplication.processEvents()
    
    def hide_loading(self):
        """Hide loading indicator"""
        if self.indicator:
            self.indicator.hide()

def optimize_main_window(window: QMainWindow):
    """Apply all optimizations to main window"""
    # Apply performance optimizations
    for widget in window.findChildren(QTableWidget):
        PerformanceOptimizer.optimize_table(widget)
    
    for widget in window.findChildren(QTextEdit):
        PerformanceOptimizer.optimize_text_widget(widget)
    
    for widget in window.findChildren(QTreeWidget):
        PerformanceOptimizer.optimize_tree_widget(widget)
    
    # Setup keyboard shortcuts
    KeyboardShortcuts.setup_shortcuts(window)
    
    # Apply modern styling
    theme_manager = ThemeManager(QApplication.instance())
    theme_manager.apply_theme("dark")
    
    # Set window properties
    window.setWindowFlags(Qt.WindowType.Window)
    window.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
    window.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
    
    return theme_manager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create test window
    window = QMainWindow()
    window.setWindowTitle("TSDuck GUI - Optimized")
    window.setMinimumSize(1200, 800)
    
    # Apply optimizations
    theme_manager = optimize_main_window(window)
    
    # Create test content
    central_widget = QWidget()
    layout = QVBoxLayout()
    
    # Test buttons with different styles
    button_layout = QHBoxLayout()
    
    primary_btn = QPushButton("Primary Action")
    primary_btn.setProperty("class", "primary")
    button_layout.addWidget(primary_btn)
    
    success_btn = QPushButton("Success")
    success_btn.setProperty("class", "success")
    button_layout.addWidget(success_btn)
    
    warning_btn = QPushButton("Warning")
    warning_btn.setProperty("class", "warning")
    button_layout.addWidget(warning_btn)
    
    danger_btn = QPushButton("Danger")
    danger_btn.setProperty("class", "danger")
    button_layout.addWidget(danger_btn)
    
    layout.addLayout(button_layout)
    
    # Test table
    table = QTableWidget(5, 3)
    table.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
    PerformanceOptimizer.optimize_table(table)
    layout.addWidget(table)
    
    # Test text area
    text_area = QTextEdit()
    text_area.setPlainText("This is a test of the optimized text widget with monospace font.")
    PerformanceOptimizer.optimize_text_widget(text_area)
    layout.addWidget(text_area)
    
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    
    # Theme toggle button
    theme_btn = QPushButton("Toggle Theme")
    theme_btn.clicked.connect(lambda: theme_manager.toggle_theme())
    window.statusBar().addWidget(theme_btn)
    
    window.show()
    sys.exit(app.exec())
