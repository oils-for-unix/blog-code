#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QScrollArea, QFrame, QPushButton, QLabel, QFileDialog,
    QTextEdit, QShortcut
)
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, QEvent
from PyQt5.QtGui import QKeySequence, QFontMetrics, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView


class CommandOutput(QWidget):
    """Widget to display a command and its output"""
    
    def __init__(self, command, output, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(0)
        
        # Command label with $ prompt
        command_frame = QFrame()
        command_frame.setStyleSheet("background-color: #2E2E2E; border-top-left-radius: 5px; border-top-right-radius: 5px;")
        command_layout = QHBoxLayout(command_frame)
        command_layout.setContentsMargins(10, 5, 10, 5)
        
        prompt_label = QLabel("$")
        prompt_label.setStyleSheet("color: #00FF00; font-family: 'Courier New'; font-weight: bold;")
        command_layout.addWidget(prompt_label)
        
        cmd_label = QLabel(command)
        cmd_label.setStyleSheet("color: white; font-family: 'Courier New';")
        command_layout.addWidget(cmd_label, 1)
        
        self.layout.addWidget(command_frame)
        
        # Output with xterm.js rendering in web view
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(100)
        
        # Load xterm.js and render the output
        html_content = self._generate_xterm_html(output)
        self.web_view.setHtml(html_content)
        
        self.layout.addWidget(self.web_view)
        
        # Add copy button
        button_layout = QHBoxLayout()
        copy_button = QPushButton("Copy")
        copy_button.setMaximumWidth(80)
        copy_button.clicked.connect(self._copy_to_clipboard)
        button_layout.addStretch()
        button_layout.addWidget(copy_button)
        
        self.layout.addLayout(button_layout)
        
        # Store command and output for copying
        self.command = command
        self.output = output
    
    def _generate_xterm_html(self, output):
        """Generate HTML with xterm.js to render command output with color"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/xterm/3.14.5/xterm.min.css" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/xterm/3.14.5/xterm.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/xterm/3.14.5/addons/fit/fit.min.js"></script>
            <style>
                body, html {{ height: 100%; margin: 0; padding: 0; overflow: hidden; }}
                #terminal {{ height: 100%; background-color: #1E1E1E; padding: 5px; }}
            </style>
        </head>
        <body>
            <div id="terminal"></div>
            <script>
                Terminal.applyAddon(fit);
                const term = new Terminal({{
                    theme: {{ background: '#1E1E1E' }},
                    fontFamily: 'Courier New',
                    fontSize: 14,
                    cursorBlink: false,
                    rows: 5
                }});
                term.open(document.getElementById('terminal'));
                term.write({terminal_output});
                term.fit();
                
                // Auto-resize terminal height based on content
                function resizeTerminal() {{
                    const lines = term.buffer.active.length;
                    const newHeight = Math.max(100, lines * 20);
                    document.querySelector('#terminal').style.height = newHeight + 'px';
                    term.fit();
                    // Signal to PyQt that size changed
                    if (window.qt) {{
                        window.qt.webChannelTransport.send(JSON.stringify({{
                            type: 'resize',
                            height: newHeight
                        }}));
                    }}
                }}
                
                // Initial resize after content is loaded
                setTimeout(resizeTerminal, 100);
            </script>
        </body>
        </html>
        """
        
        # Properly escape the output for JavaScript
        escaped_output = json.dumps(output)
        
        return html_template.format(terminal_output=escaped_output)
    
    def _copy_to_clipboard(self):
        """Copy command and output to clipboard"""
        clipboard_text = f"$ {self.command}\n{self.output}"
        QApplication.clipboard().setText(clipboard_text)


class ShellGUI(QMainWindow):
    """Main window for the Unix shell GUI"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unix Shell GUI")
        self.setMinimumSize(800, 600)
        
        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Scroll area for command outputs
        scroll_widget = QWidget()
        self.command_layout = QVBoxLayout(scroll_widget)
        self.command_layout.setAlignment(Qt.AlignTop)
        self.command_layout.setSpacing(10)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, 1)
        
        # Command input layout
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(5, 5, 5, 5)
        
        prompt_label = QLabel("$")
        prompt_label.setStyleSheet("color: #00FF00; font-family: 'Courier New'; font-weight: bold;")
        input_layout.addWidget(prompt_label)
        
        self.command_input = QLineEdit()
        self.command_input.setStyleSheet("background-color: #2E2E2E; color: white; border: none; font-family: 'Courier New';")
        self.command_input.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.command_input, 1)
        
        main_layout.addWidget(input_widget)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save Session")
        save_button.clicked.connect(self.save_session)
        button_layout.addWidget(save_button)
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_session)
        button_layout.addWidget(clear_button)
        
        main_layout.addLayout(button_layout)
        
        # Set up keyboard shortcuts
        clear_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        clear_shortcut.activated.connect(self.clear_session)
        
        # Store command history for up/down keys
        self.command_history = []
        self.history_index = 0
        
        # Install event filter for up/down arrow navigation
        self.command_input.installEventFilter(self)
        
        # Track command outputs for saving session
        self.command_outputs = []
    
    def execute_command(self):
        """Execute the entered shell command and display its output"""
        command = self.command_input.text().strip()
        if not command:
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        try:
            # Execute the command using subprocess
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()
            
            # Combine stdout and stderr with proper color codes for xterm
            if stdout and stderr:
                output = stdout + "\x1b[31m" + stderr + "\x1b[0m"  # Red color for stderr
            elif stderr:
                output = "\x1b[31m" + stderr + "\x1b[0m"  # Red color for stderr
            else:
                output = stdout
            
            # Process the exit code
            exit_code = process.returncode
            if exit_code != 0:
                output += f"\n\x1b[31mExit Code: {exit_code}\x1b[0m"
            
            # Add command and output to the display
            command_output = CommandOutput(command, output)
            self.command_layout.addWidget(command_output)
            self.command_outputs.append((command, output))
            
            # Clear the input field
            self.command_input.clear()
            
            # Scroll to the bottom to show new output
            QApplication.processEvents()
            scroll_area = self.centralWidget().findChild(QScrollArea)
            scroll_bar = scroll_area.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.maximum())
            
        except Exception as e:
            error_msg = f"\x1b[31mError executing command: {str(e)}\x1b[0m"
            command_output = CommandOutput(command, error_msg)
            self.command_layout.addWidget(command_output)
            self.command_outputs.append((command, error_msg))
    
    def eventFilter(self, obj, event):
        """Handle up/down arrow keys for command history navigation"""
        if obj is self.command_input and event.type() == QEvent.KeyPress:
            key = event.key()
            
            if key == Qt.Key_Up:
                if self.command_history and self.history_index > 0:
                    self.history_index -= 1
                    self.command_input.setText(self.command_history[self.history_index])
                return True
                
            elif key == Qt.Key_Down:
                if self.history_index < len(self.command_history) - 1:
                    self.history_index += 1
                    self.command_input.setText(self.command_history[self.history_index])
                else:
                    self.history_index = len(self.command_history)
                    self.command_input.clear()
                return True
                
        return super().eventFilter(obj, event)
    
    def save_session(self):
        """Save the entire session to a text file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Session", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            with open(filename, 'w') as f:
                for command, output in self.command_outputs:
                    # Strip ANSI color codes for plain text output
                    import re
                    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                    clean_output = ansi_escape.sub('', output)
                    
                    f.write(f"$ {command}\n{clean_output}\n\n")
    
    def clear_session(self):
        """Clear all command outputs"""
        # Remove all widgets from the layout
        while self.command_layout.count():
            item = self.command_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Clear the stored outputs
        self.command_outputs = []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Apply dark theme palette
    dark_palette = app.palette()
    dark_palette.setColor(dark_palette.Window, Qt.black)
    dark_palette.setColor(dark_palette.WindowText, Qt.white)
    dark_palette.setColor(dark_palette.Base, Qt.darkGray)
    dark_palette.setColor(dark_palette.AlternateBase, Qt.darkGray)
    dark_palette.setColor(dark_palette.ToolTipBase, Qt.white)
    dark_palette.setColor(dark_palette.ToolTipText, Qt.white)
    dark_palette.setColor(dark_palette.Text, Qt.white)
    dark_palette.setColor(dark_palette.Button, Qt.darkGray)
    dark_palette.setColor(dark_palette.ButtonText, Qt.white)
    dark_palette.setColor(dark_palette.Link, Qt.blue)
    dark_palette.setColor(dark_palette.Highlight, Qt.blue)
    dark_palette.setColor(dark_palette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    
    window = ShellGUI()
    window.show()
    sys.exit(app.exec_())
