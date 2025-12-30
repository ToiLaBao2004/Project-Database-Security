from PySide6.QtWidgets import (
    QWidget, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QGridLayout, QScrollArea, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from BAL.UserService import UserService
from models.EmployeeModel import EmployeeModel
from BAL.AuditSerice import AuditService

class EmployeeDetailDialog(QDialog):
    def __init__(self, employee_data, oracleExec,parent=None):
        super().__init__(parent)
        self.employee_data = employee_data
        self.is_editing = False
        self.value_widgets = {}
        self.auditService=AuditService(oracleExec)
        self.userService=UserService(oracleExec)
        
        self.setWindowTitle(f"Chi Tiết Nhân Viên - {employee_data.get('name', 'N/A')}")
        self.setMinimumSize(900, 700)
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
                    stop:0 #2c3e50, stop:1 #1f6fa8);
                border-bottom: 3px solid #155a87;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 20, 30, 20)

        # Avatar
        avatar = QLabel("👤")
        avatar.setFont(QFont("Segoe UI Emoji", 48))
        avatar.setStyleSheet("color: white; background: transparent;")
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFixedSize(80, 80)

        # Employee name and role
        info_layout = QVBoxLayout()
        name_label = QLabel(self.employee_data.get('name', 'N/A'))
        name_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        name_label.setStyleSheet("color: white; background: transparent;")
        
        role_label = QLabel(f"🏷️ {self.employee_data.get('emp_role', 'N/A')}")
        role_label.setFont(QFont("Segoe UI", 12))
        role_label.setStyleSheet("color: #ecf0f1; background: transparent;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(role_label)

        header_layout.addWidget(avatar)
        header_layout.addSpacing(20)
        header_layout.addLayout(info_layout)
        header_layout.addStretch()

        # ================= CONTENT AREA WITH SCROLL =================
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #ecf0f1;
            }
        """)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # ================= EMPLOYEE INFO SECTION =================
        info_section = self.create_info_section()
        content_layout.addWidget(info_section)

        # ================= AUDIT LOG SECTION =================
        audit_section = self.create_audit_section()
        content_layout.addWidget(audit_section)

        content_layout.addStretch()
        scroll_area.setWidget(content_widget)

        # ================= BUTTONS =================
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(30, 15, 30, 15)
        
        self.btn_edit = QPushButton("✏️ Chỉnh Sửa")
        self.btn_edit.setFixedSize(140, 40)
        self.btn_edit.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.btn_edit.clicked.connect(self.toggle_edit_mode)
        
        btn_close = QPushButton("✖ Đóng")
        btn_close.setFixedSize(120, 40)
        btn_close.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #a93226;
            }
            QPushButton:pressed {
                background-color: #922b21;
            }
        """)
        btn_close.clicked.connect(self.close)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(btn_close)

        # ================= MAIN LAYOUT =================
        main_layout.addWidget(header_frame)
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(btn_layout)

    def create_info_section(self):
        """Create employee information section"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #bdc3c7;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)

        # Section title
        title = QLabel("📋 THÔNG TIN NHÂN VIÊN")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; border: none; margin-bottom: 15px;")
        layout.addWidget(title)

        # Info grid
        grid = QGridLayout()
        grid.setSpacing(15)
        grid.setContentsMargins(0, 0, 0, 0)

        # Define fields to display
        fields = [
            ("👤 ID:", "id"),
            ("👤 Họ và Tên:", "name"),
            ("🎂 Ngày Sinh:", "dateofbirth"),
            ("⚧️ Giới Tính:", "gender"),
            ("🏠 Địa Chỉ:", "address"),
            ("📞 Số Điện Thoại:", "phonenumber"),
            ("📧 Email:", "email"),
            ("🔑 Username:", "username"),
        ]

        row = 0
        for label_text, key in fields:
            # Label
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            label.setStyleSheet("color: #34495e; border: none;")
            label.setMinimumWidth(150)
            
            # Value - Create QLineEdit for editing
            value = QLineEdit(self.employee_data.get(key, "N/A"))
            value.setFont(QFont("Segoe UI", 10))
            value.setStyleSheet("""
                QLineEdit {
                    color: #2c3e50;
                    background-color: #f8f9fa;
                    padding: 8px 12px;
                    border-radius: 5px;
                    border: 1px solid #e0e6ed;
                }
                QLineEdit:focus {
                    border: 2px solid #3498db;
                    background-color: white;
                }
                QLineEdit:read-only {
                    background-color: #f8f9fa;
                    color: #2c3e50;
                }
            """)
            value.setReadOnly(True)  # Start in read-only mode
            
            # Store reference
            self.value_widgets[key] = value
            
            grid.addWidget(label, row, 0, Qt.AlignTop)
            grid.addWidget(value, row, 1)
            row += 1

        layout.addLayout(grid)
        return section

    def create_audit_section(self):
        """Create audit log section"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #bdc3c7;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)

        # Section title
        title = QLabel("📊 LỊCH SỬ AUDIT LOG")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; border: none; margin-bottom: 15px;")
        layout.addWidget(title)

        # Audit table
        audit_table = QTableWidget()
        audit_table.setColumnCount(5)
        audit_table.setHorizontalHeaderLabels(["Tài Khoản", "Thời gian", "Hành động", "Bảng", "Hoàn thành"])
        audit_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        audit_table.setAlternatingRowColors(True)
        audit_table.setEditTriggers(QTableWidget.NoEditTriggers)
        audit_table.setSelectionBehavior(QTableWidget.SelectRows)
        audit_table.setMinimumHeight(300)
        audit_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                gridline-color: #ecf0f1;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                color: #2c3e50;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTableCornerButton::section {
                background-color: #34495e;
                border: none;
            }
        """)
        
        audit_logs = []
        current_user=self.userService.get_user_session()["username"]
        if "MGR" in current_user:
            try:
                audit_logs = self.auditService.get_user_audit(self.employee_data["username"])
            except Exception as e:
                QMessageBox.critical(self, "Lỗi audit", f"{str(e)}")

        audit_table.setRowCount(len(audit_logs))
        
        keys = ['username', 'event_timestamp', 'action_name', 'object_name', 'return_code']

        for row, log in enumerate(audit_logs):
            for col, key in enumerate(keys):
                val = log.get(key, "")
                
                if key == 'event_timestamp' and val:
                    display_text = val.strftime("%d/%m/%Y %H:%M:%S")
                else:
                    display_text = str(val)

                item = QTableWidgetItem(display_text)
                item.setTextAlignment(Qt.AlignCenter)
                
                if key == 'action_name':
                    if val == "INSERT":
                        item.setForeground(Qt.green)
                        item.setFont(QFont("Segoe UI", weight=QFont.Bold))
                    elif val == "UPDATE":
                        item.setForeground(Qt.blue)
                    elif val == "DELETE":
                        item.setForeground(Qt.red)
                    elif val == "SELECT":
                        item.setForeground(Qt.darkGray)
                
                if key == 'return_code':
                    if val != 0:
                        item.setForeground(Qt.red)

                audit_table.setItem(row, col, item)

        layout.addWidget(audit_table)
        return section

    def toggle_edit_mode(self):
        """Toggle between view and edit mode"""
        self.is_editing = not self.is_editing
        
        if self.is_editing:
            # Enable editing
            self.btn_edit.setText("💾 Lưu")
            self.btn_edit.setStyleSheet("""
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
            
            # Make fields editable (except ID)
            first_field = True
            for key, widget in self.value_widgets.items():
                if key != 'id':  # ID should not be editable
                    widget.setReadOnly(False)
                    if first_field:
                        widget.setFocus()  # Focus first editable field
                        first_field = False
        else:
            # Save and disable editing
            self.btn_edit.setText("✏️ Chỉnh Sửa")
            self.btn_edit.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #21618c;
                }
            """)
            
            # Make fields read-only and save data
            for key, widget in self.value_widgets.items():
                widget.setReadOnly(True)
                self.employee_data[key] = widget.text()
            
            try:
                employee=EmployeeModel(id=self.employee_data["id"],
                                       address=self.employee_data["address"],
                                       phonenumber=self.employee_data["phonenumber"],
                                       email=self.employee_data["email"])
                
                self.userService.update_employee(employee)
                QMessageBox.information(
                    self,
                    "Thành Công",
                    "Thông tin nhân viên đã được cập nhật!"
                )
                
            except Exception as e:
                self.is_editing = True
                for key, widget in self.value_widgets.items():
                    if key != 'id':
                        widget.setReadOnly(False)
                
                QMessageBox.critical(self,"Lỗi Cập Nhật",f"{str(e)}"
                )