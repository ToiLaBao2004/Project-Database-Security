import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QVBoxLayout, QFrame,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from BAL.LoginService import login
from UI.MainForm import MainForm

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.oracle_app = None
        self.setWindowTitle("Login")
        self.setFixedSize(720, 380)
        self.init_ui()

    def init_ui(self):
        # ================= LEFT PANEL =================
        left_panel = QFrame()
        left_panel.setFixedWidth(260)
        left_panel.setStyleSheet("background-color: #1f6fa8;")

        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)

        icon = QLabel("⚽")
        icon.setFont(QFont("Segoe UI Emoji", 48))
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("color: white;")

        title1 = QLabel("CHÀO MỪNG ĐẾN VỚI")
        title1.setAlignment(Qt.AlignCenter)
        title1.setFont(QFont("Segoe UI", 13))
        title1.setStyleSheet("color: rgba(255,255,255,0.85);")

        title2 = QLabel("HỆ THỐNG")
        title2.setAlignment(Qt.AlignCenter)
        title2.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title2.setStyleSheet("color: white;")

        title3 = QLabel("QUẢN LÝ CỬA HÀNG THỂ THAO")
        title3.setAlignment(Qt.AlignCenter)
        title3.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title3.setStyleSheet("color: #eaf6ff;")

        dev = QLabel("Hệ thống quản lý\nKết nối Oracle chuyên nghiệp")
        dev.setAlignment(Qt.AlignCenter)
        dev.setStyleSheet("color: rgba(255,255,255,0.7);")
        dev.setFont(QFont("Segoe UI", 8))

        left_layout.addStretch()
        left_layout.addWidget(icon)
        left_layout.addSpacing(25)
        left_layout.addWidget(title1)
        left_layout.addSpacing(8)
        left_layout.addWidget(title2)
        left_layout.addWidget(title3)
        left_layout.addSpacing(20)
        left_layout.addWidget(dev)
        left_layout.addStretch()

        # ================= RIGHT PANEL =================
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #f7f7f7;")

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("Đăng Nhập Hệ Thống")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #155a87; margin-bottom: 5px;")

        # Username
        user_label = QLabel("👤 Tên đăng nhập")
        user_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        user_label.setStyleSheet("color: #34495e;")
        
        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Nhập tên đăng nhập của bạn")
        self.txt_user.setFixedHeight(42)
        self.txt_user.setFont(QFont("Segoe UI", 11))

        # Password
        pass_label = QLabel("🔒 Mật khẩu")
        pass_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        pass_label.setStyleSheet("color: #34495e;")
        
        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Nhập mật khẩu của bạn")
        self.txt_pass.setEchoMode(QLineEdit.Password)
        self.txt_pass.setFixedHeight(42)
        self.txt_pass.setFont(QFont("Segoe UI", 11))

        # Login button
        btn_login = QPushButton("ĐĂNG NHẬP")
        btn_login.setFixedHeight(42)
        btn_login.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.clicked.connect(self.handle_login)

        # Style
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e6ed;
                border-radius: 8px;
                padding: 8px 15px;
                background-color: #f8f9fa;
                font-size: 12px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border: 2px solid #1f6fa8;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #bdc3c7;
            }
            QPushButton {
                background-color: #155a87;
                color: black;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #0e4a6b;
            }
            QPushButton:pressed {
                background-color: #0a3a52;
            }
        """)

        right_layout.addWidget(title)
        right_layout.addSpacing(25)
        right_layout.addWidget(user_label)
        right_layout.addSpacing(5)
        right_layout.addWidget(self.txt_user)
        right_layout.addSpacing(15)
        right_layout.addWidget(pass_label)
        right_layout.addSpacing(5)
        right_layout.addWidget(self.txt_pass)
        right_layout.addSpacing(20)
        right_layout.addWidget(btn_login)
        right_layout.addStretch()

        # ================= MAIN LAYOUT =================
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

    def handle_login(self):
        username = self.txt_user.text().strip()
        password = self.txt_pass.text()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        try:
            oracleExec = login(username, password)
            self.hide()
            mainForm = MainForm(oracleExec, username)
            mainForm.show()
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi đăng nhập", str(e)) 

        print("Login attempt:", username)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginForm()
    window.show()
    sys.exit(app.exec())
    