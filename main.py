import sys
import os
import json
import ctypes
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QListWidget, 
                             QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator, QIcon

APP_DIR = os.path.join(os.getenv('APPDATA'), 'SecureDnsChanger')
DATA_FILE = os.path.join(APP_DIR, 'dns_data.json')

def load_dns_list():
    """Loads the DNS list from AppData as raw JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def save_dns_list(data):
    """Saves the DNS list to AppData in raw JSON format."""
    if not os.path.exists(APP_DIR):
        os.makedirs(APP_DIR)
        
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

def execute_as_admin(ps_command):
    """Prompts for Admin access and executes a PowerShell command."""
    full_command = f"-NoProfile -WindowStyle Hidden -Command \"{ps_command}\""
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", full_command, None, 0)
    
    if result <= 32:
        return False
    return True

class DnsChangerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.dns_data = load_dns_list()
        self.init_ui()
        self.populate_list()

    def init_ui(self):
        self.setWindowTitle("Legion DNS")
        self.setFixedSize(450, 600) 
        self.setWindowIcon(QIcon(resource_path('icon1.ico')))
        
        self.setStyleSheet("""
            QWidget { background-color: #1e1e2e; color: #cdd6f4; font-family: 'Segoe UI', sans-serif; }
            QLabel { font-size: 14px; font-weight: bold; }
            QLineEdit { background-color: #313244; border: 1px solid #45475a; border-radius: 5px; padding: 8px; font-size: 13px; }
            QLineEdit:focus { border: 1px solid #89b4fa; }
            QPushButton { background-color: #89b4fa; color: #11111b; border: none; border-radius: 5px; padding: 10px; font-size: 14px; font-weight: bold; }
            QPushButton:hover { background-color: #b4befe; }
            QPushButton:pressed { background-color: #74c7ec; }
            QPushButton#btn_toggle { background-color: #45475a; color: #cdd6f4; font-size: 12px; padding: 5px; }
            QPushButton#btn_toggle:hover { background-color: #585b70; }
            QPushButton#btn_unset { background-color: #f38ba8; }
            QPushButton#btn_unset:hover { background-color: #eba0ac; }
            QPushButton#btn_delete { background-color: #fab387; }
            QPushButton#btn_delete:hover { background-color: #f9e2af; }
            QPushButton#btn_flush { background-color: #a6e3a1; }
            QPushButton#btn_flush:hover { background-color: #94e2d5; }
            QListWidget { background-color: #313244; border: 1px solid #45475a; border-radius: 5px; padding: 5px; font-size: 14px; }
            QListWidget::item { padding: 8px; border-bottom: 1px solid #45475a; }
            QListWidget::item:selected { background-color: #45475a; border-radius: 4px; }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("🌐 IPv4 DNS Manager")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.btn_toggle_form = QPushButton("▶ Show Add Form")
        self.btn_toggle_form.setObjectName("btn_toggle")
        self.btn_toggle_form.clicked.connect(self.toggle_form)
        layout.addWidget(self.btn_toggle_form)

        self.form_widget = QWidget()

        self.form_widget.setVisible(False) 
        
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(10)

        ip_regex = QRegExp(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        ip_validator = QRegExpValidator(ip_regex)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Profile Name (e.g., Google DNS)")
        form_layout.addWidget(self.input_name)

        self.input_primary = QLineEdit()
        self.input_primary.setPlaceholderText("Primary DNS (e.g., 8.8.8.8)")
        self.input_primary.setValidator(ip_validator)
        form_layout.addWidget(self.input_primary)

        self.input_secondary = QLineEdit()
        self.input_secondary.setPlaceholderText("Secondary DNS (Optional, e.g., 8.8.4.4)")
        self.input_secondary.setValidator(ip_validator)
        form_layout.addWidget(self.input_secondary)

        btn_add = QPushButton("➕ Add to List")
        btn_add.clicked.connect(self.add_dns)
        form_layout.addWidget(btn_add)

        self.form_widget.setLayout(form_layout)
        layout.addWidget(self.form_widget)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #45475a;")
        layout.addWidget(line)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        action_layout1 = QHBoxLayout()
        
        btn_set = QPushButton("🚀 Set DNS")
        btn_set.clicked.connect(self.set_dns)
        action_layout1.addWidget(btn_set)

        btn_unset = QPushButton("🔄 Unset (Auto)")
        btn_unset.setObjectName("btn_unset")
        btn_unset.clicked.connect(self.unset_dns)
        action_layout1.addWidget(btn_unset)

        action_layout2 = QHBoxLayout()
        
        btn_flush = QPushButton("🧹 Flush DNS")
        btn_flush.setObjectName("btn_flush")
        btn_flush.clicked.connect(self.flush_dns)
        action_layout2.addWidget(btn_flush)

        btn_delete = QPushButton("🗑️ Delete")
        btn_delete.setObjectName("btn_delete")
        btn_delete.clicked.connect(self.delete_dns)
        action_layout2.addWidget(btn_delete)

        layout.addLayout(action_layout1)
        layout.addLayout(action_layout2)
        
        self.setLayout(layout)

    def toggle_form(self):
        """Hides or shows the 'Add DNS' form."""
        if self.form_widget.isVisible():
            self.form_widget.setVisible(False)
            self.btn_toggle_form.setText("▶ Show Add Form")
        else:
            self.form_widget.setVisible(True)
            self.btn_toggle_form.setText("▼ Hide Add Form")

    def populate_list(self):
        self.list_widget.clear()
        for item in self.dns_data:
            sec = item.get('secondary', '')
            display_text = f"{item['name']} - {item['primary']}"
            if sec:
                display_text += f", {sec}"
            self.list_widget.addItem(display_text)

    def add_dns(self):
        name = self.input_name.text().strip()
        primary = self.input_primary.text().strip()
        secondary = self.input_secondary.text().strip()

        if not name or not primary:
            QMessageBox.warning(self, "Input Error", "Profile Name and Primary DNS are required.")
            return

        new_entry = {"name": name, "primary": primary, "secondary": secondary}
        self.dns_data.append(new_entry)
        save_dns_list(self.dns_data)
        
        self.populate_list()
        self.input_name.clear()
        self.input_primary.clear()
        self.input_secondary.clear()

    def delete_dns(self):
        selected_row = self.list_widget.currentRow()
        if selected_row >= 0:
            del self.dns_data[selected_row]
            save_dns_list(self.dns_data)
            self.populate_list()
        else:
            QMessageBox.information(self, "Selection Error", "Please select a DNS profile to delete.")

    def set_dns(self):
        selected_row = self.list_widget.currentRow()
        if selected_row < 0:
            QMessageBox.information(self, "Selection Error", "Please select a DNS profile to set.")
            return

        profile = self.dns_data[selected_row]
        primary = profile['primary']
        secondary = profile.get('secondary', '')

        if secondary:
            dns_servers = f'"{primary}","{secondary}"'
        else:
            dns_servers = f'"{primary}"'

        ps_script = (
            f"Get-NetAdapter | Where-Object {{ $_.Status -eq 'Up' -and $_.Virtual -eq $False }} | "
            f"Set-DnsClientServerAddress -ServerAddresses {dns_servers}"
        )

        reply = QMessageBox.question(self, 'Admin Access Required', 
                                     f"Setting DNS to {primary}. This requires Administrator privileges.\n\nProceed?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            success = execute_as_admin(ps_script)
            if not success:
                QMessageBox.warning(self, "Failed", "Administrator access was denied or the command failed.")

    def unset_dns(self):
        ps_script = (
            "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' -and $_.Virtual -eq $False } | "
            "Set-DnsClientServerAddress -ResetServerAddresses"
        )

        reply = QMessageBox.question(self, 'Admin Access Required', 
                                     "Resetting DNS to Automatic (DHCP). This requires Administrator privileges.\n\nProceed?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            success = execute_as_admin(ps_script)
            if not success:
                QMessageBox.warning(self, "Failed", "Administrator access was denied or the command failed.")

    def flush_dns(self):
        """Silently executes ipconfig /flushdns in the background."""
        try:
            subprocess.run(["ipconfig", "/flushdns"], creationflags=0x08000000)
            QMessageBox.information(self, "Success", "DNS Cache has been flushed successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not flush DNS cache.\n{str(e)}")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    try:
        myappid = 'legion.dns.manager.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    
    app.setWindowIcon(QIcon(resource_path('icon1.ico')))
    
    window = DnsChangerApp()
    window.show()
    sys.exit(app.exec_())
