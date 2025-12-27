from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget,
    QDialog, QGridLayout, QScrollArea, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from BAL.employee_service import EmployeeService

class AdminUI(QWidget):
    def __init__(self,conn, username, parent=None):
        super().__init__()
        self.parent = parent
        self.username = username
        self.setWindowTitle("Admin Dashboard - Quản Lý Hệ Thống")
        self.setMinimumSize(1200, 700)
        self.employee_service=EmployeeService(conn)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= SIDEBAR =================
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #2c3e50;")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #1a252f; padding: 20px;")
        header_layout = QVBoxLayout(header)
        
        logo = QLabel("👨‍💼")
        logo.setFont(QFont("Segoe UI Emoji", 32))
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("color: white;")
        
        admin_name = QLabel(f"Admin: {self.username}")
        admin_name.setFont(QFont("Segoe UI", 11, QFont.Bold))
        admin_name.setAlignment(Qt.AlignCenter)
        admin_name.setStyleSheet("color: white; margin-top: 10px;")
        
        header_layout.addWidget(logo)
        header_layout.addWidget(admin_name)

        # Menu buttons
        self.btn_employees = QPushButton("� Quản Lý Nhân Viên")
        self.btn_products = QPushButton("📋 Quản Lý Sản Phẩm")
        self.btn_logout = QPushButton("🚪 Đăng Xuất")

        # Style menu buttons
        menu_style = """
            QPushButton {
                background-color: transparent;
                color: #ecf0f1;
                text-align: left;
                padding: 15px 20px;
                border: none;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #1f6fa8;
            }
        """
        
        self.btn_employees.setStyleSheet(menu_style)
        self.btn_products.setStyleSheet(menu_style)
        self.btn_logout.setStyleSheet(menu_style + "QPushButton:hover { background-color: #c0392b; }")
        
        self.btn_employees.setCursor(Qt.PointingHandCursor)
        self.btn_products.setCursor(Qt.PointingHandCursor)
        self.btn_logout.setCursor(Qt.PointingHandCursor)

        self.btn_employees.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_products.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_logout.clicked.connect(self.handle_logout)

        sidebar_layout.addWidget(header)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(self.btn_employees)
        sidebar_layout.addWidget(self.btn_products)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_logout)

        # ================= CONTENT AREA =================
        self.stacked_widget = QStackedWidget()
        
        # Employee Management Page
        employee_page = self.create_employee_page()
        self.stacked_widget.addWidget(employee_page)
        
        # Product Management Page
        product_page = self.create_product_page()
        self.stacked_widget.addWidget(product_page)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget)

    def create_employee_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QLabel("👥 QUẢN LÝ NHÂN VIÊN")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        # Action buttons
        btn_layout = QHBoxLayout()
        
        btn_add = QPushButton("➕ Thêm Nhân Viên")
        btn_delete = QPushButton("🗑️ Xóa Nhân Viên")
        btn_refresh = QPushButton("🔄 Làm Mới")
        
        for btn in [btn_add, btn_delete, btn_refresh]:
            btn.setFixedHeight(40)
            btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn_layout.addWidget(btn)
        
        btn_layout.addStretch()

        # Table
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(9)
        self.employee_table.setHorizontalHeaderLabels(["id", "name", "dob","gender",
                                                       "address", "phone_number", "email",
                                                       "username", "role"])
        self.employee_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.employee_table.setAlternatingRowColors(True)
        self.employee_table.setStyleSheet("""
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
            }
            QTableCornerButton::section {
                background-color: #34495e;
                border: none;
            }
        """)
        
        # Sample data
        self.load_employee_data()

        # Connect buttons
        btn_add.clicked.connect(self.show_add_employee_form)
        btn_delete.clicked.connect(lambda: QMessageBox.information(self, "Xóa", "Chức năng xóa nhân viên (TODO)"))
        btn_refresh.clicked.connect(self.load_employee_data)
        
        # Connect cell click to show employee details
        self.employee_table.cellClicked.connect(self.show_employee_detail)

        layout.addWidget(header)
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        layout.addWidget(self.employee_table)

        return page

    def create_product_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QLabel("📦 QUẢN LÝ SẢN PHẨM")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        # Action buttons
        btn_layout = QHBoxLayout()
        
        btn_add = QPushButton("➕ Thêm Sản Phẩm")
        btn_delete = QPushButton("🗑️ Xóa Sản Phẩm")
        btn_refresh = QPushButton("🔄 Làm Mới")
        
        for btn in [btn_add, btn_delete, btn_refresh]:
            btn.setFixedHeight(40)
            btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn_layout.addWidget(btn)
        
        btn_layout.addStretch()

        # Table
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(5)
        self.product_table.setHorizontalHeaderLabels(["ID", "Tên Sản Phẩm", "Danh Mục", "Giá", "Số Lượng"])
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_table.setAlternatingRowColors(True)
        self.product_table.setStyleSheet("""
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
            }
            QTableCornerButton::section {
                background-color: #34495e;
                border: none;
            }
        """)
        
        # Sample data
        self.load_product_data()

        # Connect buttons
        btn_add.clicked.connect(self.show_add_product_form)
        btn_delete.clicked.connect(lambda: QMessageBox.information(self, "Xóa", "Chức năng xóa sản phẩm (TODO)"))
        btn_refresh.clicked.connect(self.load_product_data)
        
        # Connect cell click to show product details
        self.product_table.cellClicked.connect(self.show_product_detail)

        layout.addWidget(header)
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        layout.addWidget(self.product_table)

        return page

    def load_employee_data(self):
        employees=self.employee_service.get_all_employee_info()
        if not employees:
            self.employee_table.setRowCount(0)
            return
        
        column_headers = list(employees[0].keys())
        
        self.employee_table.setColumnCount(len(column_headers))
        self.employee_table.setHorizontalHeaderLabels([column_headers])
        
        self.employee_table.setRowCount(len(employees))
    
        for row, employee_dict in enumerate(employees):
            for col, key in enumerate(column_headers):
                data = employee_dict.get(key, "")
                item = QTableWidgetItem(str(data) if data is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                self.employee_table.setItem(row, col, item)

    def load_product_data(self):
        # Sample data - sẽ thay bằng dữ liệu từ database
        products = [
            ["1", "Laptop Dell XPS 15", "Điện tử", "25,000,000 đ", "15"],
            ["2", "iPhone 15 Pro", "Điện thoại", "30,000,000 đ", "20"],
            ["3", "Bàn làm việc gỗ", "Nội thất", "3,500,000 đ", "10"],
            ["4", "Ghế gaming DXRacer", "Nội thất", "7,000,000 đ", "8"],
            ["5", "Tai nghe Sony WH-1000XM5", "Phụ kiện", "8,500,000 đ", "25"],
        ]
        
        self.product_table.setRowCount(len(products))
        for row, product in enumerate(products):
            for col, data in enumerate(product):
                item = QTableWidgetItem(data)
                item.setTextAlignment(Qt.AlignCenter)
                self.product_table.setItem(row, col, item)

    def handle_logout(self):
        reply = QMessageBox.question(
            self,
            "Đăng Xuất",
            "Bạn có chắc chắn muốn đăng xuất?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.parent:
                self.parent.show()
            self.close()

    def show_employee_detail(self, row, col):
        """Show detailed employee information when clicking on a cell"""
        # Get employee data from the clicked row
        employee_data = {}
        for col_idx in range(self.employee_table.columnCount()):
            header = self.employee_table.horizontalHeaderItem(col_idx).text()
            item = self.employee_table.item(row, col_idx)
            employee_data[header] = item.text() if item else ""
        
        # Open detail dialog
        dialog = EmployeeDetailDialog(employee_data, self)
        dialog.exec()

    def show_add_employee_form(self):
        """Show form to add new employee"""
        dialog = AddEmployeeDialog(self)
        if dialog.exec():
            # Get the new employee data
            new_employee = dialog.get_employee_data()
            if new_employee:
                QMessageBox.information(
                    self,
                    "Thành Công",
                    f"Đã thêm nhân viên: {new_employee.get('name', 'N/A')}\n(Chức năng lưu vào database sẽ được thêm sau)"
                )
                # Reload table
                self.load_employee_data()

    def show_add_product_form(self):
        """Show form to add new product"""
        dialog = AddProductDialog(self)
        if dialog.exec():
            # Get the new product data
            new_product = dialog.get_product_data()
            if new_product:
                QMessageBox.information(
                    self,
                    "Thành Công",
                    f"Đã thêm sản phẩm: {new_product.get('name', 'N/A')}\n(Chức năng lưu vào database sẽ được thêm sau)"
                )
                # Reload table
                self.load_product_data()

    def show_product_detail(self, row, col):
        """Show detailed product information when clicking on a cell"""
        # Get product data from the clicked row
        product_data = {}
        headers = ["ID", "Tên Sản Phẩm", "Danh Mục", "Giá", "Số Lượng"]
        for col_idx in range(self.product_table.columnCount()):
            item = self.product_table.item(row, col_idx)
            product_data[headers[col_idx]] = item.text() if item else ""
        
        # Open detail dialog
        dialog = ProductDetailDialog(product_data, self)
        dialog.exec()


class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
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
            ("🏷️ Role:", "role", "EMP/MGR/ADMIN"),
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
        btn_save.clicked.connect(self.validate_and_accept)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(btn_save)

        # ================= MAIN LAYOUT =================
        main_layout.addWidget(header_frame)
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(btn_layout)

    def validate_and_accept(self):
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

    def get_employee_data(self):
        """Get employee data from form"""
        return {key: field.text().strip() for key, field in self.input_fields.items()}


class EmployeeDetailDialog(QDialog):
    def __init__(self, employee_data, parent=None):
        super().__init__(parent)
        self.employee_data = employee_data
        self.is_editing = False
        self.value_widgets = {}  # Store references to value widgets
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
        
        role_label = QLabel(f"🏷️ {self.employee_data.get('role', 'N/A')}")
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
            ("🎂 Ngày Sinh:", "dob"),
            ("⚧️ Giới Tính:", "gender"),
            ("🏠 Địa Chỉ:", "address"),
            ("📞 Số Điện Thoại:", "phone_number"),
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
        audit_table.setHorizontalHeaderLabels([
            "Thời Gian", "Hành Động", "Bảng", "Chi Tiết", "IP Address"
        ])
        audit_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        audit_table.setAlternatingRowColors(True)
        audit_table.setEditTriggers(QTableWidget.NoEditTriggers)
        audit_table.setSelectionBehavior(QTableWidget.SelectRows)
        audit_table.setMinimumHeight(300)
        audit_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e6ed;
                border-radius: 5px;
                gridline-color: #ecf0f1;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 10px;
            }
            QTableWidget::item {
                padding: 8px;
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

        # Sample audit log data - filtered by employee
        employee_id = self.employee_data.get('id', 'N/A')
        employee_name = self.employee_data.get('name', 'N/A')
        username = self.employee_data.get('username', 'N/A')
        
        audit_logs = [
            ["2024-12-28 10:30:45", "INSERT", "EMPLOYEES", f"Tạo tài khoản nhân viên ID: {employee_id}", "192.168.1.100"],
            ["2024-12-27 14:20:15", "UPDATE", "EMPLOYEES", f"Cập nhật thông tin nhân viên: {employee_name}", "192.168.1.100"],
            ["2024-12-27 09:15:30", "SELECT", "EMPLOYEES", f"Xem thông tin cá nhân", "192.168.1.105"],
            ["2024-12-26 16:45:00", "UPDATE", "EMPLOYEES", f"Thay đổi số điện thoại", "192.168.1.100"],
            ["2024-12-25 11:30:22", "SELECT", "ORDERS", f"Truy vấn đơn hàng phụ trách", "192.168.1.110"],
            ["2024-12-24 08:20:10", "INSERT", "ORDERS", f"Tạo đơn hàng mới", "192.168.1.110"],
            ["2024-12-23 15:10:05", "UPDATE", "ORDERS", f"Cập nhật trạng thái đơn hàng", "192.168.1.110"],
        ]

        audit_table.setRowCount(len(audit_logs))
        for row, log in enumerate(audit_logs):
            for col, data in enumerate(log):
                item = QTableWidgetItem(data)
                item.setTextAlignment(Qt.AlignCenter)
                
                # Color code actions
                if col == 1:  # Action column
                    if data == "INSERT":
                        item.setForeground(Qt.green)
                    elif data == "UPDATE":
                        item.setForeground(Qt.blue)
                    elif data == "DELETE":
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
            
            # Show save confirmation
            QMessageBox.information(
                self,
                "Thành Công",
                "Thông tin nhân viên đã được cập nhật!\n(Chức năng lưu vào database sẽ được thêm sau)"
            )


class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Sản Phẩm Mới")
        self.setMinimumSize(700, 500)
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
                    stop:0 #e67e22, stop:1 #d35400);
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 15, 30, 15)

        icon = QLabel("➕")
        icon.setFont(QFont("Segoe UI Emoji", 32))
        icon.setStyleSheet("color: white; background: transparent;")
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(50, 50)

        title = QLabel("THÊM SẢN PHẨM MỚI")
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
        form_title = QLabel("📋 THÔNG TIN SẢN PHẨM")
        form_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        form_title.setStyleSheet("color: #2c3e50;")
        form_layout.addWidget(form_title)

        # Form fields
        grid = QGridLayout()
        grid.setSpacing(15)
        grid.setHorizontalSpacing(20)

        fields = [
            ("📦 Tên Sản Phẩm:", "name", "Nhập tên sản phẩm"),
            ("🏷️ Danh Mục:", "category", "Nhập danh mục"),
            ("💰 Giá:", "price", "Nhập giá (VND)"),
            ("📊 Số Lượng:", "quantity", "Nhập số lượng"),
            ("📝 Mô Tả:", "description", "Nhập mô tả sản phẩm (tùy chọn)"),
        ]

        row = 0
        for label_text, key, placeholder in fields:
            # Label
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            label.setStyleSheet("color: #34495e;")
            label.setMinimumWidth(150)

            # Input field
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
                    border: 2px solid #e67e22;
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
        btn_save.clicked.connect(self.validate_and_accept)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(btn_save)

        # ================= MAIN LAYOUT =================
        main_layout.addWidget(header_frame)
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(btn_layout)

    def validate_and_accept(self):
        """Validate form and accept if valid"""
        # Check if required fields are filled
        required_fields = ["name", "category", "price", "quantity"]
        
        for field in required_fields:
            if not self.input_fields[field].text().strip():
                QMessageBox.warning(
                    self,
                    "Thiếu Thông Tin",
                    f"Vui lòng điền đầy đủ thông tin: {field}"
                )
                self.input_fields[field].setFocus()
                return
        
        # Validate price and quantity are numbers
        try:
            price = self.input_fields["price"].text().strip()
            quantity = self.input_fields["quantity"].text().strip()
            
            # Remove commas if present
            price = price.replace(",", "")
            float(price)
            int(quantity)
        except ValueError:
            QMessageBox.warning(
                self,
                "Lỗi Định Dạng",
                "Giá phải là số và Số lượng phải là số nguyên!"
            )
            return
        
        # If all valid, accept
        self.accept()

    def get_product_data(self):
        """Get product data from form"""
        return {key: field.text().strip() for key, field in self.input_fields.items()}


class ProductDetailDialog(QDialog):
    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.is_editing = False
        self.value_widgets = {}
        self.setWindowTitle(f"Chi Tiết Sản Phẩm - {product_data.get('Tên Sản Phẩm', 'N/A')}")
        self.setMinimumSize(800, 600)
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
                    stop:0 #e67e22, stop:1 #d35400);
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 15, 30, 15)

        # Product icon
        icon = QLabel("📦")
        icon.setFont(QFont("Segoe UI Emoji", 32))
        icon.setStyleSheet("color: white; background: transparent;")
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(50, 50)

        # Product name
        info_layout = QVBoxLayout()
        name_label = QLabel(self.product_data.get('Tên Sản Phẩm', 'N/A'))
        name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        name_label.setStyleSheet("color: white; background: transparent;")
        
        category_label = QLabel(f"🏷️ {self.product_data.get('Danh Mục', 'N/A')}")
        category_label.setFont(QFont("Segoe UI", 10))
        category_label.setStyleSheet("color: #ecf0f1; background: transparent;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(category_label)

        header_layout.addWidget(icon)
        header_layout.addSpacing(20)
        header_layout.addLayout(info_layout)
        header_layout.addStretch()

        # ================= CONTENT AREA =================
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

        # Product Info Section
        info_section = self.create_info_section()
        content_layout.addWidget(info_section)

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
        """Create product information section"""
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
        title = QLabel("📋 THÔNG TIN SẢN PHẨM")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; border: none; margin-bottom: 15px;")
        layout.addWidget(title)

        # Info grid
        grid = QGridLayout()
        grid.setSpacing(15)
        grid.setContentsMargins(0, 0, 0, 0)

        # Define fields to display
        fields = [
            ("🆔 ID:", "ID"),
            ("📦 Tên Sản Phẩm:", "Tên Sản Phẩm"),
            ("🏷️ Danh Mục:", "Danh Mục"),
            ("💰 Giá:", "Giá"),
            ("📊 Số Lượng:", "Số Lượng"),
        ]

        row = 0
        for label_text, key in fields:
            # Label
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            label.setStyleSheet("color: #34495e; border: none;")
            label.setMinimumWidth(150)
            
            # Value - Create QLineEdit for editing
            value = QLineEdit(self.product_data.get(key, "N/A"))
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
                if key != 'ID':  # ID should not be editable
                    widget.setReadOnly(False)
                    if first_field:
                        widget.setFocus()
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
                self.product_data[key] = widget.text()
            
            # Show save confirmation
            QMessageBox.information(
                self,
                "Thành Công",
                "Thông tin sản phẩm đã được cập nhật!\n(Chức năng lưu vào database sẽ được thêm sau)"
            )
