from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class RegisterUI(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Đăng Ký Tài Khoản")
        self.setFixedSize(720, 480)
        self.init_ui()

    def init_ui(self):
        # ================= LEFT PANEL =================
        left_panel = QFrame()
        left_panel.setFixedWidth(260)
        left_panel.setStyleSheet("background-color: #1f6fa8;")

        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignCenter)

        icon = QLabel("✨")
        icon.setFont(QFont("Segoe UI Emoji", 48))
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("color: white;")

        title1 = QLabel("TẠO TÀI KHOẢN MỚI")
        title1.setAlignment(Qt.AlignCenter)
        title1.setFont(QFont("Segoe UI", 13))
        title1.setStyleSheet("color: rgba(255,255,255,0.85);")

        title2 = QLabel("ĐĂNG KÝ")
        title2.setAlignment(Qt.AlignCenter)
        title2.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title2.setStyleSheet("color: white;")

        title3 = QLabel("QUẢN LÝ ORACLE")
        title3.setAlignment(Qt.AlignCenter)
        title3.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title3.setStyleSheet("color: #eaf6ff;")

        dev = QLabel("Đăng ký để truy cập\nHệ thống quản lý Oracle")
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
        right_layout.setContentsMargins(40, 20, 40, 20)

        title = QLabel("Đăng Ký Tài Khoản")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #155a87; margin-bottom: 5px;")

        # Full Name
        name_label = QLabel("👤 Họ và tên")
        name_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        name_label.setStyleSheet("color: #34495e;")
        
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Nhập họ và tên của bạn")
        self.txt_name.setFixedHeight(40)
        self.txt_name.setFont(QFont("Segoe UI", 11))

        # Username
        user_label = QLabel("📧 Tên đăng nhập")
        user_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        user_label.setStyleSheet("color: #34495e;")
        
        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Nhập tên đăng nhập")
        self.txt_user.setFixedHeight(40)
        self.txt_user.setFont(QFont("Segoe UI", 11))

        # Password
        pass_label = QLabel("🔒 Mật khẩu")
        pass_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        pass_label.setStyleSheet("color: #34495e;")
        
        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Nhập mật khẩu")
        self.txt_pass.setEchoMode(QLineEdit.Password)
        self.txt_pass.setFixedHeight(40)
        self.txt_pass.setFont(QFont("Segoe UI", 11))

        # Confirm Password
        confirm_label = QLabel("🔒 Xác nhận mật khẩu")
        confirm_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        confirm_label.setStyleSheet("color: #34495e;")
        
        self.txt_confirm = QLineEdit()
        self.txt_confirm.setPlaceholderText("Nhập lại mật khẩu")
        self.txt_confirm.setEchoMode(QLineEdit.Password)
        self.txt_confirm.setFixedHeight(40)
        self.txt_confirm.setFont(QFont("Segoe UI", 11))

        # Register button
        btn_register = QPushButton("ĐĂNG KÝ")
        btn_register.setFixedHeight(42)
        btn_register.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_register.setCursor(Qt.PointingHandCursor)
        btn_register.clicked.connect(self.handle_register)

        # Back to Login link
        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignCenter)
        
        back_text = QLabel("Đã có tài khoản?")
        back_text.setStyleSheet("color: #7f8c8d;")
        
        self.lbl_login = QLabel('<a href="#" style="color: #155a87; text-decoration: none; font-weight: bold;">Đăng nhập</a>')
        self.lbl_login.setOpenExternalLinks(False)
        self.lbl_login.linkActivated.connect(self.back_to_login)
        self.lbl_login.setCursor(Qt.PointingHandCursor)
        
        back_layout.addWidget(back_text)
        back_layout.addWidget(self.lbl_login)

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
        right_layout.addSpacing(15)
        right_layout.addWidget(name_label)
        right_layout.addSpacing(3)
        right_layout.addWidget(self.txt_name)
        right_layout.addSpacing(10)
        right_layout.addWidget(user_label)
        right_layout.addSpacing(3)
        right_layout.addWidget(self.txt_user)
        right_layout.addSpacing(10)
        right_layout.addWidget(pass_label)
        right_layout.addSpacing(3)
        right_layout.addWidget(self.txt_pass)
        right_layout.addSpacing(10)
        right_layout.addWidget(confirm_label)
        right_layout.addSpacing(3)
        right_layout.addWidget(self.txt_confirm)
        right_layout.addSpacing(15)
        right_layout.addWidget(btn_register)
        right_layout.addSpacing(10)
        right_layout.addLayout(back_layout)
        right_layout.addStretch()

        # ================= MAIN LAYOUT =================
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

    def handle_register(self):
        name = self.txt_name.text().strip()
        username = self.txt_user.text().strip()
        password = self.txt_pass.text()
        confirm = self.txt_confirm.text()

        if not name or not username or not password or not confirm:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin")
            return

        if password != confirm:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu phải có ít nhất 6 ký tự")
            return

        # TODO: Thêm logic đăng ký tài khoản ở đây
        QMessageBox.information(self, "Thành công", f"Đăng ký tài khoản '{username}' thành công!\n(Chưa kết nối backend)")
        print(f"Register: Name={name}, Username={username}, Password={password}")

    def back_to_login(self):
        if self.parent:
            self.parent.show()
        self.close()
