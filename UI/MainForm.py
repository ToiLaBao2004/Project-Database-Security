from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget,
    QGridLayout, QScrollArea, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from BAL.UserService import UserService
from BAL.ProductService import ProductService

from UI.Dialog.EmployeeDialog import EmployeeDetailDialog
from UI.Dialog.AddEmployeeDialog import AddEmployeeDialog
from UI.Dialog.AddProductDialog import AddProductDialog
from UI.Dialog.ProductDetailDialog import ProductDetailDialog

class MainForm(QWidget):
    def __init__(self, oracleExec, username=None, parent=None):
        super().__init__()
        self.parent = parent
        self.oracleExec = oracleExec
        self.username = username
        self.userService = UserService(self.oracleExec)
        self.productService = ProductService(self.oracleExec)
        self.setWindowTitle(f"Main Form - {self.username}")
        self.setMinimumSize(1100, 650)            
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
        
        name_label = QLabel(f"Người dùng: {self.username}")
        name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: white; margin-top: 10px;")
        
        header_layout.addWidget(logo)
        header_layout.addWidget(name_label)

        # Menu buttons based on role
        self.btn_employees = QPushButton("👥 Quản Lý Nhân Viên")
        self.btn_products = QPushButton("📋 Quản Lý Sản Phẩm")
        self.btn_logout = QPushButton("🚪 Đăng Xuất")
        self.btn_profile = QPushButton("👤 Thông Tin Cá Nhân")
        self.btn_activity = QPushButton("📊 Hoạt Động Của Tôi")
        self.btn_orders = QPushButton("📦 Đơn Hàng")
        menu_buttons = [self.btn_profile, self.btn_activity, self.btn_orders, self.btn_employees, self.btn_products, self.btn_logout]

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
                background-color: #415b76;
            }
            QPushButton:pressed {
                background-color: #1f6fa8;
            }
        """
        
        for btn in menu_buttons:
            btn.setStyleSheet(menu_style)
            btn.setCursor(Qt.PointingHandCursor)
        
        self.btn_logout.setStyleSheet(menu_style + "QPushButton:hover { background-color: #c0392b; }")
        self.btn_logout.setCursor(Qt.PointingHandCursor)

        # Connect buttons
        self.btn_employees.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_products.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_profile.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_activity.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_orders.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_logout.clicked.connect(self.handle_logout)

        sidebar_layout.addWidget(header)
        sidebar_layout.addSpacing(20)
        for btn in menu_buttons:
            sidebar_layout.addWidget(btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_logout)

        # ================= CONTENT AREA =================
        self.stacked_widget = QStackedWidget()
        
        employee_page = self.create_employee_page()
        self.stacked_widget.addWidget(employee_page)
            
        product_page = self.create_product_page()
        self.stacked_widget.addWidget(product_page)

        profile_page = self.create_profile_page()
        self.stacked_widget.addWidget(profile_page)
            
        activity_page = self.create_activity_page()
        self.stacked_widget.addWidget(activity_page)
            
        orders_page = self.create_orders_page()
        self.stacked_widget.addWidget(orders_page)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget)

    def create_profile_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header = QLabel("👤 THÔNG TIN CÁ NHÂN")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        info_card = QFrame()
        info_card.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #bdc3c7;")
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(30, 30, 30, 30)
        info_layout.setSpacing(20)

        top_section = QHBoxLayout()
        avatar = QLabel("👤")
        avatar.setFont(QFont("Segoe UI Emoji", 64))
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFixedSize(100, 100)
        avatar.setStyleSheet("background-color: #3498db; border-radius: 50px; color: white;")

        name_section = QVBoxLayout()
        name_label = QLabel("Thông tin nhân viên")
        name_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        
        role_label = QLabel(f"🏷️ Username: {self.username}")
        role_label.setFont(QFont("Segoe UI", 12))
        role_label.setStyleSheet("color: #7f8c8d;")
        
        name_section.addWidget(name_label)
        name_section.addWidget(role_label)
        name_section.addStretch()

        top_section.addWidget(avatar)
        top_section.addSpacing(20)
        top_section.addLayout(name_section)
        top_section.addStretch()

        info_layout.addLayout(top_section)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: #ecf0f1;")
        divider.setFixedHeight(2)
        info_layout.addWidget(divider)

        note_label = QLabel("📝 Thông tin chi tiết sẽ được load từ database khi tích hợp backend")
        note_label.setFont(QFont("Segoe UI", 10))
        note_label.setStyleSheet("color: #7f8c8d; padding: 15px;")
        note_label.setWordWrap(True)
        info_layout.addWidget(note_label)

        layout.addWidget(header)
        layout.addWidget(info_card)
        layout.addStretch()

        return page

    def create_activity_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        header = QLabel("📊 HOẠT ĐỘNG CỦA TÔI")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        stats = [
            ("📝", "Đơn Hàng Xử Lý", "0", "#3498db"),
            ("✅", "Hoàn Thành", "0", "#27ae60"),
            ("⏳", "Đang Xử Lý", "0", "#f39c12"),
        ]

        for icon, title, value, color in stats:
            card = self.create_stat_card(icon, title, value, color)
            stats_layout.addWidget(card)

        activity_table = QTableWidget()
        activity_table.setColumnCount(5)
        activity_table.setHorizontalHeaderLabels(["Thời Gian", "Hành Động", "Bảng", "Chi Tiết", "IP Address"])
        activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        activity_table.setAlternatingRowColors(True)
        activity_table.setStyleSheet("""
            QTableWidget { background-color: white; border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #ecf0f1; }
            QHeaderView::section { background-color: #34495e; color: white; padding: 10px; border: none; font-weight: bold; }
            QTableWidget::item { padding: 8px; }
            QTableCornerButton::section { background-color: #34495e; border: none; }
        """)

        activities = [
            ["2024-12-28 14:30:22", "SELECT", "EMPLOYEES", "Xem thông tin cá nhân", "192.168.1.105"],
            ["2024-12-28 10:20:45", "SELECT", "PRODUCTS", "Xem danh sách sản phẩm", "192.168.1.105"],
        ]

        activity_table.setRowCount(len(activities))
        for row, activity in enumerate(activities):
            for col, data in enumerate(activity):
                item = QTableWidgetItem(data)
                item.setTextAlignment(Qt.AlignCenter)
                
                if col == 1:
                    if data == "INSERT":
                        item.setForeground(Qt.green)
                    elif data == "UPDATE":
                        item.setForeground(Qt.blue)
                    elif data == "DELETE":
                        item.setForeground(Qt.red)
                
                activity_table.setItem(row, col, item)

        layout.addWidget(header)
        layout.addLayout(stats_layout)
        layout.addSpacing(20)
        layout.addWidget(activity_table)

        return page

    def create_orders_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        header = QLabel("📦 ĐƠN HÀNG CỦA TÔI")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        btn_layout = QHBoxLayout()
        btn_refresh = QPushButton("🔄 Làm Mới")
        btn_refresh.setFixedHeight(40)
        btn_refresh.setFont(QFont("Segoe UI", 10, QFont.Bold))
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(btn_refresh)
        btn_layout.addStretch()

        orders_table = QTableWidget()
        orders_table.setColumnCount(6)
        orders_table.setHorizontalHeaderLabels(["Mã ĐH", "Khách Hàng", "Ngày Tạo", "Tổng Tiền", "Trạng Thái", "Ghi Chú"])
        orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        orders_table.setAlternatingRowColors(True)
        orders_table.setStyleSheet("""
            QTableWidget { background-color: white; border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #ecf0f1; }
            QHeaderView::section { background-color: #34495e; color: white; padding: 10px; border: none; font-weight: bold; }
            QTableWidget::item { padding: 8px; }
            QTableCornerButton::section { background-color: #34495e; border: none; }
        """)
        orders_table.setRowCount(0)

        note = QLabel("📝 Dữ liệu đơn hàng sẽ được load từ database khi tích hợp backend")
        note.setFont(QFont("Segoe UI", 10))
        note.setStyleSheet("color: #7f8c8d; padding: 10px;")
        note.setAlignment(Qt.AlignCenter)

        btn_refresh.clicked.connect(lambda: QMessageBox.information(self, "Làm mới", "Chức năng load dữ liệu (TODO)"))

        layout.addWidget(header)
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        layout.addWidget(orders_table)
        layout.addWidget(note)

        return page

    def create_employee_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        header = QLabel("👥 QUẢN LÝ NHÂN VIÊN")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

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

        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(9)
        self.employee_table.setHorizontalHeaderLabels(["id", "name", "dob", "gender", "address", "phone_number", "email", "username", "role"])
        self.employee_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.employee_table.setAlternatingRowColors(True)
        self.employee_table.setStyleSheet("""
            QTableWidget { background-color: white; border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #ecf0f1; }
            QHeaderView::section { background-color: #34495e; color: white; padding: 10px; border: none; font-weight: bold; }
            QTableWidget::item { padding: 8px; }
            QTableCornerButton::section { background-color: #34495e; border: none; }
        """)

        self.load_employee_data()

        btn_add.clicked.connect(self.show_add_employee_form)
        btn_delete.clicked.connect(lambda: QMessageBox.information(self, "Xóa", "Chức năng xóa nhân viên (TODO)"))
        btn_refresh.clicked.connect(self.load_employee_data)
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

        header = QLabel("📦 QUẢN LÝ SẢN PHẨM")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

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

        self.product_table = QTableWidget()
        self.product_table.setColumnCount(5)
        self.product_table.setHorizontalHeaderLabels(["ID", "Tên Sản Phẩm", "Danh Mục", "Giá", "Số Lượng"])
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_table.setAlternatingRowColors(True)
        self.product_table.setStyleSheet("""
            QTableWidget { background-color: white; border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #ecf0f1; }
            QHeaderView::section { background-color: #34495e; color: white; padding: 10px; border: none; font-weight: bold; }
            QTableWidget::item { padding: 8px; }
            QTableCornerButton::section { background-color: #34495e; border: none; }
        """)

        self.load_product_data()

        btn_add.clicked.connect(self.show_add_product_form)
        btn_delete.clicked.connect(lambda: QMessageBox.information(self, "Xóa", "Chức năng xóa sản phẩm (TODO)"))
        btn_refresh.clicked.connect(self.load_product_data)
        self.product_table.cellClicked.connect(self.show_product_detail)

        layout.addWidget(header)
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        layout.addWidget(self.product_table)

        return page

    def create_stat_card(self, icon, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"background-color: white; border-radius: 10px; border-left: 5px solid {color};")
        card.setFixedHeight(120)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        icon_label.setStyleSheet(f"color: {color};")

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 9))
        title_label.setStyleSheet("color: #7f8c8d;")

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        return card

    def load_employee_data(self):
        if not self.userService:
            self.employee_table.setRowCount(0)
            return
            
        employees = self.userService.get_all_employee_info()
        if not employees:
            self.employee_table.setRowCount(0)
            return
        
        # Lấy danh sách các key từ nhân viên đầu tiên
        column_headers = list(employees[0].keys())
        
        self.employee_table.setColumnCount(len(column_headers))
        self.employee_table.setHorizontalHeaderLabels(column_headers)
        
        self.employee_table.setRowCount(len(employees))
        
        for row, employee_dict in enumerate(employees):
            for col, key in enumerate(column_headers):
                data = employee_dict.get(key, "")
                item = QTableWidgetItem(str(data) if data is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                self.employee_table.setItem(row, col, item)

    def load_product_data(self):
        if not self.productService:
            self.product_table.setRowCount(0)
            return

        products = self.productService.get_all_products()
        if not products:
            self.product_table.setRowCount(0)
            return
        
        # Lấy danh sách các key từ sản phẩm đầu tiên
        column_headers = list(products[0].keys())

        self.product_table.setColumnCount(len(column_headers))
        self.product_table.setHorizontalHeaderLabels(column_headers)

        self.product_table.setRowCount(len(products))
        
        for row, product_dict in enumerate(products):
            for col, key in enumerate(column_headers):
                data = product_dict.get(key, "")
                item = QTableWidgetItem(str(data) if data is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                self.product_table.setItem(row, col, item)
                
    def handle_logout(self):
        reply = QMessageBox.question(self, "Đăng Xuất", "Bạn có chắc chắn muốn đăng xuất?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.parent:
                self.parent.show()
            self.close()

    def show_employee_detail(self, row, col):
        if EmployeeDetailDialog is None:
            QMessageBox.warning(self, "Lỗi", "Chưa import được dialog chi tiết nhân viên")
            return
            
        employee_data = {}
        for col_idx in range(self.employee_table.columnCount()):
            header = self.employee_table.horizontalHeaderItem(col_idx).text()
            item = self.employee_table.item(row, col_idx)
            employee_data[header] = item.text() if item else ""
        
        dialog = EmployeeDetailDialog(employee_data, self)
        dialog.exec()

    def show_add_employee_form(self):
        if AddEmployeeDialog is None:
            QMessageBox.warning(self, "Lỗi", "Chưa import được form thêm nhân viên")
            return
            
        dialog = AddEmployeeDialog(self)
        if dialog.exec():
            new_employee = dialog.get_employee_data()
            if new_employee:
                QMessageBox.information(self, "Thành Công",
                    f"Đã thêm nhân viên: {new_employee.get('name', 'N/A')}\n(Chức năng lưu vào database sẽ được thêm sau)")
                self.load_employee_data()

    def show_add_product_form(self):
        if AddProductDialog is None:
            QMessageBox.warning(self, "Lỗi", "Chưa import được form thêm sản phẩm")
            return
            
        dialog = AddProductDialog(self)
        if dialog.exec():
            new_product = dialog.get_product_data()
            if new_product:
                QMessageBox.information(self, "Thành Công",
                    f"Đã thêm sản phẩm: {new_product.get('name', 'N/A')}\n(Chức năng lưu vào database sẽ được thêm sau)")
                self.load_product_data()

    def show_product_detail(self, row, col):
        if ProductDetailDialog is None:
            QMessageBox.warning(self, "Lỗi", "Chưa import được dialog chi tiết sản phẩm")
            return
            
        product_data = {}
        headers = ["ID", "NAME", "IMAGE", "UNITPRICE", "STOCKQUANTITY", "CATEGORYID", "BRANDID", "ACTIVE"]
        for col_idx in range(self.product_table.columnCount()):
            item = self.product_table.item(row, col_idx)
            product_data[headers[col_idx]] = item.text() if item else ""
        
        dialog = ProductDetailDialog(product_data, self)
        dialog.exec()