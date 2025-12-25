from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class AdminUI(QWidget):
    def __init__(self, parent=None, username="admin"):
        super().__init__()
        self.parent = parent
        self.username = username
        self.setWindowTitle("Admin Dashboard - Quản Lý Hệ Thống")
        self.setMinimumSize(1200, 700)
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
        btn_edit = QPushButton("✏️ Sửa Nhân Viên")
        btn_delete = QPushButton("🗑️ Xóa Nhân Viên")
        btn_refresh = QPushButton("🔄 Làm Mới")
        
        for btn in [btn_add, btn_edit, btn_delete, btn_refresh]:
            btn.setFixedHeight(40)
            btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn_layout.addWidget(btn)
        
        btn_layout.addStretch()

        # Table
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(5)
        self.employee_table.setHorizontalHeaderLabels(["ID", "Họ và Tên", "Email", "Số Điện Thoại", "Chức Vụ"])
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
        btn_add.clicked.connect(lambda: QMessageBox.information(self, "Thêm", "Chức năng thêm nhân viên (TODO)"))
        btn_edit.clicked.connect(lambda: QMessageBox.information(self, "Sửa", "Chức năng sửa nhân viên (TODO)"))
        btn_delete.clicked.connect(lambda: QMessageBox.information(self, "Xóa", "Chức năng xóa nhân viên (TODO)"))
        btn_refresh.clicked.connect(self.load_employee_data)

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
        btn_edit = QPushButton("✏️ Sửa Sản Phẩm")
        btn_delete = QPushButton("🗑️ Xóa Sản Phẩm")
        btn_refresh = QPushButton("🔄 Làm Mới")
        
        for btn in [btn_add, btn_edit, btn_delete, btn_refresh]:
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
        btn_add.clicked.connect(lambda: QMessageBox.information(self, "Thêm", "Chức năng thêm sản phẩm (TODO)"))
        btn_edit.clicked.connect(lambda: QMessageBox.information(self, "Sửa", "Chức năng sửa sản phẩm (TODO)"))
        btn_delete.clicked.connect(lambda: QMessageBox.information(self, "Xóa", "Chức năng xóa sản phẩm (TODO)"))
        btn_refresh.clicked.connect(self.load_product_data)

        layout.addWidget(header)
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        layout.addWidget(self.product_table)

        return page

    def load_employee_data(self):
        # Sample data - sẽ thay bằng dữ liệu từ database
        employees = [
            ["1", "Nguyễn Văn A", "nguyenvana@email.com", "0912345678", "Nhân viên"],
            ["2", "Trần Thị B", "tranthib@email.com", "0923456789", "Quản lý"],
            ["3", "Lê Văn C", "levanc@email.com", "0934567890", "Nhân viên"],
            ["4", "Phạm Thị D", "phamthid@email.com", "0945678901", "Trưởng phòng"],
            ["5", "Hoàng Văn E", "hoangvane@email.com", "0956789012", "Nhân viên"],
        ]
        
        self.employee_table.setRowCount(len(employees))
        for row, employee in enumerate(employees):
            for col, data in enumerate(employee):
                item = QTableWidgetItem(data)
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
