import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QScrollArea,
                             QLabel, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class TerminalWidget(QWidget):
    """Widget to display the command and its output"""
    
    def __init__(self, command, parent=None):
        super().__init__(parent)
        
        # Set up the layout
        layout = QVBoxLayout(self)
        
        # Command label
        cmd_label = QLabel(f"<b>$ {command}</b>")
        cmd_label.setStyleSheet("color: #00FF00; background-color: #000000; padding: 5px;")
        layout.addWidget(cmd_label)
        
        # Output text area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier New", 10))
        self.output.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        layout.addWidget(self.output)
        
        # Set some sensible minimum size
        self.setMinimumHeight(150)
        
        # Execute the command and display output
        self.execute_command(command)
    
    def execute_command(self, command):
        try:
            # Execute the command and capture output
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()
            
            # Display output (or error if something went wrong)
            if stdout:
                self.output.append(stdout)
            if stderr:
                self.output.append(f"<span style='color: #FF0000;'>{stderr}</span>")
                
            # Display return code if non-zero
            if process.returncode != 0:
                self.output.append(f"<span style='color: #FF0000;'>Command returned non-zero exit status {process.returncode}</span>")
                
        except Exception as e:
            self.output.append(f"<span style='color: #FF0000;'>Error executing command: {str(e)}</span>")


class TerminalApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terminal Command GUI")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create input area
        input_layout = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command (e.g. 'ls /tmp')")
        self.command_input.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.command_input)
        
        execute_button = QPushButton("Execute")
        execute_button.clicked.connect(self.execute_command)
        input_layout.addWidget(execute_button)
        
        main_layout.addLayout(input_layout)
        
        # Create scrollable area for terminal outputs
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)
        
        # Container for terminal widgets
        self.terminal_container = QWidget()
        self.terminal_layout = QVBoxLayout(self.terminal_container)
        self.terminal_layout.addStretch(1)  # Push widgets to the top
        
        scroll_area.setWidget(self.terminal_container)
    
    def execute_command(self):
        # Get command from input
        command = self.command_input.text().strip()
        if not command:
            return
        
        # Create new terminal widget for this command
        terminal = TerminalWidget(command)
        
        # Add to layout (at position 0 to keep newest at top)
        self.terminal_layout.insertWidget(0, terminal)
        
        # Clear the input field
        self.command_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TerminalApp()
    window.show()
    sys.exit(app.exec_())
