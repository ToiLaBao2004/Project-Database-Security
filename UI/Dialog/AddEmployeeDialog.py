from PySide6.QtWidgets import (
    QWidget, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QGridLayout, QScrollArea, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from BAL.UserService import UserService
from models.EmployeeModel import EmployeeModel
import datetime
class AddEmployeeDialog(QDialog):
    def __init__(self, oracleExec, parent=None):
        super().__init__(parent)
        self.oracleExec = oracleExec
        self.userService = UserService(self.oracleExec)
        self.setWindowTitle("Thêm Nhân Viên Mới")
        self.setMinimumSize(700, 600)
        self.input_fields = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= HEADER =================
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27ae60, stop:1 #16a085);
                border-bottom: 3px solid #1e8449;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 15, 30, 15)

        icon = QLabel("➕")
        icon.setFont(QFont("Segoe UI Emoji", 32))
        icon.setStyleSheet("color: white; background: transparent;")
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(50, 50)

        title = QLabel("THÊM NHÂN VIÊN MỚI")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")

        header_layout.addWidget(icon)
        header_layout.addSpacing(20)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # ================= FORM CONTENT =================
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #ecf0f1;
            }
        """)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(40, 30, 40, 30)
        form_layout.setSpacing(20)

        # Form title
        form_title = QLabel("📋 THÔNG TIN NHÂN VIÊN")
        form_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        form_title.setStyleSheet("color: #2c3e50;")
        form_layout.addWidget(form_title)

        # Form fields
        grid = QGridLayout()
        grid.setSpacing(15)
        grid.setHorizontalSpacing(20)

        fields = [
            ("👤 Họ và Tên:", "name", "Nhập họ và tên đầy đủ"),
            ("🎂 Ngày Sinh:", "dob", "YYYY-MM-DD"),
            ("⚧️ Giới Tính:", "gender", "True/False"),
            ("🏠 Địa Chỉ:", "address", "Nhập địa chỉ"),
            ("📞 Số Điện Thoại:", "phone_number", "Nhập số điện thoại"),
            ("📧 Email:", "email", "example@email.com"),
            ("🔑 Username:", "username", "Nhập username"),
            ("🔒 Password:", "password", "Nhập mật khẩu"),
            ("🏷️ Role:", "role", "EMP/MGR"),
        ]

        row = 0
        for label_text, key, placeholder in fields:
            # Label
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            label.setStyleSheet("color: #34495e;")
            label.setMinimumWidth(150)

            # Input field
            if key == "password":
                input_field = QLineEdit()
                input_field.setEchoMode(QLineEdit.Password)
            else:
                input_field = QLineEdit()
            
            input_field.setPlaceholderText(placeholder)
            input_field.setFont(QFont("Segoe UI", 10))
            input_field.setFixedHeight(40)
            input_field.setStyleSheet("""
                QLineEdit {
                    color: #2c3e50;
                    background-color: white;
                    padding: 8px 12px;
                    border-radius: 5px;
                    border: 2px solid #e0e6ed;
                }
                QLineEdit:focus {
                    border: 2px solid #27ae60;
                }
            """)

            self.input_fields[key] = input_field

            grid.addWidget(label, row, 0)
            grid.addWidget(input_field, row, 1)
            row += 1

        form_layout.addLayout(grid)
        form_layout.addStretch()
        scroll_area.setWidget(form_widget)

        # ================= BUTTONS =================
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(30, 15, 30, 15)
        btn_layout.addStretch()

        btn_cancel = QPushButton("✖ Hủy")
        btn_cancel.setFixedSize(120, 45)
        btn_cancel.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7a7b;
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_save = QPushButton("💾 Lưu")
        btn_save.setFixedSize(120, 45)
        btn_save.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        btn_layout.addWidget(btn_save)
        btn_save.clicked.connect(self.validate_and_create)

        # ================= MAIN LAYOUT =================
        main_layout.addWidget(header_frame)
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(btn_layout)

    def validate_and_create(self):
        """Validate form and accept if valid"""
        # Check if all required fields are filled
        required_fields = ["name", "dob", "gender", "address", "phone_number", "email", "username", "password", "role"]
        
        for field in required_fields:
            if not self.input_fields[field].text().strip():
                QMessageBox.warning(
                    self,
                    "Thiếu Thông Tin",
                    f"Vui lòng điền đầy đủ thông tin: {field}"
                )
                self.input_fields[field].setFocus()
                return
        
        # If all valid, accept
        self.accept()
        
        data = self.get_employee_data()
        try:
            employee = EmployeeModel(
                name=data["name"],
                dateofbirth= datetime.datetime.strptime(data["dob"],"%Y-%m-%d").date(),
                gender=data["gender"],
                address=data["address"],
                phonenumber=data["phone_number"],
                email=data["email"],
                username=data["username"],
                password=data["password"],
                emp_role=data["role"]
            )
            
            self.userService.create_employee(employee)
            
            QMessageBox.information(self, "Thành Công", f"Đã thêm nhân viên {data['name']} với ID {employee.id}")
            return employee  # Trả về model để parent sử dụng nếu cần
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm nhân viên: {str(e)}")
            return None

    def get_employee_data(self):
        """Get employee data from form"""
        return {key: field.text().strip() for key, field in self.input_fields.items()}