from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget,
    QLineEdit, QComboBox, QSpinBox, 
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from datetime import date, datetime

from BAL.UserService import UserService
from BAL.ProductService import ProductService
from BAL.OrderService import OrderService
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
        
        # Khởi tạo service nếu import thành công
        self.userService = UserService(self.oracleExec) if UserService else None
        self.productService = ProductService(self.oracleExec) if ProductService else None
        self.orderService = OrderService(self.oracleExec) if OrderService else None
        
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
        logo.setStyleSheet("color: white; border: none;")
        
        name_label = QLabel(f"Người dùng: {self.username}")
        name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: white; margin-top: 10px; border: none;")
        
        header_layout.addWidget(logo)
        header_layout.addWidget(name_label)

        # Menu buttons based on role
        self.btn_employees = QPushButton("👥 Quản Lý Nhân Viên")
        self.btn_products = QPushButton("📋 Quản Lý Sản Phẩm")
        
        
        self.btn_profile = QPushButton("👤 Thông Tin Cá Nhân")
        self.btn_activity = QPushButton("📊 Hoạt Động Của Tôi")
        self.btn_orders = QPushButton("📦 Đơn Hàng")
        
        self.btn_logout = QPushButton("🚪 Đăng Xuất")
        menu_buttons = [self.btn_employees, self.btn_products, self.btn_profile, self.btn_activity, self.btn_orders, self.btn_logout]

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
        self.btn_profile.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_activity.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.btn_orders.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
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

        activity_table = QTableWidget()
        activity_table.setColumnCount(5)
        activity_table.setHorizontalHeaderLabels(["Thời Gian", "Hành Động", "Bảng", "Chi Tiết", "IP Address"])
        activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        activity_table.setAlternatingRowColors(True)
        activity_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                gridline-color: #ecf0f1;
                outline: none;
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
                outline: none;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTableWidget::item:focus {
                outline: none;
                border: none;
            }
            QTableCornerButton::section {
                background-color: #34495e;
                border: none;
            }
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
        layout.addWidget(activity_table)

        return page

    def create_orders_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header with view orders button
        header_layout = QHBoxLayout()
        header = QLabel("🛒 TẠO ĐƠN HÀNG")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        
        btn_view_orders = QPushButton("📋 Xem Lịch Sử Đơn Hàng")
        btn_view_orders.setFixedHeight(40)
        btn_view_orders.setFont(QFont("Segoe UI", 10, QFont.Bold))
        btn_view_orders.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border-radius: 8px;
                padding: 0 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        btn_view_orders.setCursor(Qt.PointingHandCursor)
        btn_view_orders.clicked.connect(self.view_order_history)
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(btn_view_orders)
        main_layout.addLayout(header_layout)

        # Content layout - 2 columns
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # ============= LEFT SIDE: PRODUCT LIST =============
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #bdc3c7;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(15)

        # Product list header
        product_header = QLabel("📦 DANH SÁCH SẢN PHẨM")
        product_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        product_header.setStyleSheet("color: #2c3e50;")
        left_layout.addWidget(product_header)

        # Search for products
        search_layout = QHBoxLayout()
        self.order_product_search = QLineEdit()
        self.order_product_search.setPlaceholderText("🔍 Tìm kiếm sản phẩm...")
        self.order_product_search.setFixedHeight(35)
        self.order_product_search.setStyleSheet("""
            QLineEdit {
                background-color: #f8f9fa;
                border: 2px solid #e0e6ed;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 11px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.order_product_search.textChanged.connect(self.search_order_products)
        search_layout.addWidget(self.order_product_search)

        # Refresh button
        btn_refresh_products = QPushButton("🔄")
        btn_refresh_products.setFixedSize(35, 35)
        btn_refresh_products.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_refresh_products.setCursor(Qt.PointingHandCursor)
        btn_refresh_products.clicked.connect(self.load_order_products)
        search_layout.addWidget(btn_refresh_products)
        
        left_layout.addLayout(search_layout)

        # Product table
        self.order_product_table = QTableWidget()
        self.order_product_table.setColumnCount(5)
        self.order_product_table.setHorizontalHeaderLabels(["ID", "Tên Sản Phẩm", "Giá", "Tồn Kho", ""])
        self.order_product_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.order_product_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.order_product_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.order_product_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.order_product_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.order_product_table.setAlternatingRowColors(True)
        self.order_product_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.order_product_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #ecf0f1;
                border: none;
                outline: none;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 5px;
                color: #2c3e50;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        left_layout.addWidget(self.order_product_table)

        # ============= RIGHT SIDE: SHOPPING CART =============
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #bdc3c7;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(15)

        # Cart header
        cart_header = QLabel("🛒 GIỎ HÀNG")
        cart_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        cart_header.setStyleSheet("color: #2c3e50;")
        right_layout.addWidget(cart_header)

        # Customer info section
        customer_frame = QFrame()
        customer_frame.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; padding: 10px;")
        customer_layout = QVBoxLayout(customer_frame)
        customer_layout.setSpacing(10)
        
        # Customer name
        name_layout = QHBoxLayout()
        name_label = QLabel("👤 Tên khách hàng:")
        name_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50; background: transparent; border: none;")
        name_label.setMinimumWidth(140)
        name_label.setWordWrap(False)
        
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("Nhập tên khách hàng...")
        self.customer_name_input.setFixedHeight(32)
        self.customer_name_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #e0e6ed;
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 11px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.customer_name_input)
        customer_layout.addLayout(name_layout)
        
        # Customer phone
        phone_layout = QHBoxLayout()
        phone_label = QLabel("📱 Số điện thoại:")
        phone_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        phone_label.setStyleSheet("color: #2c3e50; background: transparent; border: none;")
        phone_label.setMinimumWidth(140)
        phone_label.setWordWrap(False)
        
        self.customer_phone_input = QLineEdit()
        self.customer_phone_input.setPlaceholderText("Nhập số điện thoại...")
        self.customer_phone_input.setFixedHeight(32)
        self.customer_phone_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #e0e6ed;
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 11px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.customer_phone_input)
        customer_layout.addLayout(phone_layout)
        
        right_layout.addWidget(customer_frame)

        # Cart table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["Tên SP", "Đơn Giá", "SL", "Thành Tiền", ""])
        
        # Enable horizontal scrollbar
        self.cart_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.cart_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        
        # Set column widths to show all content
        self.cart_table.horizontalHeader().setMinimumSectionSize(80)
        self.cart_table.setColumnWidth(0, 150)  # Tên SP - wider
        self.cart_table.setColumnWidth(1, 100)  # Đơn Giá
        self.cart_table.setColumnWidth(2, 70)   # SL
        self.cart_table.setColumnWidth(3, 110)  # Thành Tiền
        self.cart_table.setColumnWidth(4, 50)   # Delete button
        
        self.cart_table.setAlternatingRowColors(True)
        self.cart_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #ecf0f1;
                border: none;
                outline: none;
            }
            QHeaderView::section {
                background-color: #27ae60;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 5px;
                color: #2c3e50;
            }
        """)
        self.cart_table.setRowCount(0)
        right_layout.addWidget(self.cart_table)

        # Total section
        total_frame = QFrame()
        total_frame.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; padding: 15px;")
        total_layout = QVBoxLayout(total_frame)
        
        total_label_layout = QHBoxLayout()
        total_text = QLabel("TỔNG CỘNG:")
        total_text.setFont(QFont("Segoe UI", 12, QFont.Bold))
        total_text.setStyleSheet("color: #2c3e50;")
        
        self.total_amount_label = QLabel("0 đ")
        self.total_amount_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.total_amount_label.setStyleSheet("color: #e74c3c;")
        self.total_amount_label.setAlignment(Qt.AlignRight)
        
        total_label_layout.addWidget(total_text)
        total_label_layout.addStretch()
        total_label_layout.addWidget(self.total_amount_label)
        total_layout.addLayout(total_label_layout)
        
        right_layout.addWidget(total_frame)

        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_clear_cart = QPushButton("🗑️ Xóa Giỏ Hàng")
        btn_clear_cart.setFixedHeight(40)
        btn_clear_cart.setFont(QFont("Segoe UI", 10, QFont.Bold))
        btn_clear_cart.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_clear_cart.setCursor(Qt.PointingHandCursor)
        btn_clear_cart.clicked.connect(self.clear_cart)
        
        btn_create_order = QPushButton("✅ Tạo Đơn Hàng")
        btn_create_order.setFixedHeight(40)
        btn_create_order.setFont(QFont("Segoe UI", 10, QFont.Bold))
        btn_create_order.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        btn_create_order.setCursor(Qt.PointingHandCursor)
        btn_create_order.clicked.connect(self.create_order)
        
        btn_layout.addWidget(btn_clear_cart)
        btn_layout.addWidget(btn_create_order)
        right_layout.addLayout(btn_layout)

        # Add panels to content layout
        content_layout.addWidget(left_panel, 3)  # 60% width
        content_layout.addWidget(right_panel, 2)  # 40% width

        main_layout.addLayout(content_layout)

        # Initialize cart data
        self.cart_items = []  # List to store cart items: [{"id": ..., "name": ..., "price": ..., "quantity": ...}]
        self.order_history = []  # List to store completed orders
        
        # Load products
        self.load_order_products()

        return page

    def create_employee_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        header = QLabel("👥 QUẢN LÝ NHÂN VIÊN")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        # Search section
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        search_label = QLabel("🔍 Tìm kiếm:")
        search_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        search_label.setStyleSheet("color: #2c3e50;")
        
        self.employee_search_combo = QComboBox()
        self.employee_search_combo.addItems(["Tất cả", "Tên", "Email", "Số điện thoại", "Username", "Chức vụ"])
        self.employee_search_combo.setFixedHeight(40)
        self.employee_search_combo.setFixedWidth(180)
        self.employee_search_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 11px;
                color: #2c3e50;
            }
            QComboBox:hover {
                border: 2px solid #3498db;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #2c3e50;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                color: black;
                selection-background-color: #3498db;
            }
        """)
        
        self.employee_search_input = QLineEdit()
        self.employee_search_input.setPlaceholderText("Nhập từ khóa tìm kiếm...")
        self.employee_search_input.setFixedHeight(40)
        self.employee_search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 11px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.employee_search_input.textChanged.connect(self.search_employees)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.employee_search_combo)
        search_layout.addWidget(self.employee_search_input)
        search_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("➕ Thêm Nhân Viên")
        btn_delete = QPushButton("🗑️ Xóa Nhân Viên")
        btn_refresh = QPushButton("🔄 Làm Mới")
        
        btn_add.setStyleSheet("color: black; font-weight: bold;")
        btn_delete.setStyleSheet("color: black; font-weight: bold;")
        btn_refresh.setStyleSheet("color: black; font-weight: bold;")
        
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
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                gridline-color: #ecf0f1;
                outline: none;
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
                outline: none;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTableWidget::item:focus {
                outline: none;
                border: none;
            }
            QTableCornerButton::section {
                background-color: #34495e;
                border: none;
            }
        """)

        self.load_employee_data()

        btn_add.clicked.connect(self.show_add_employee_form)
        btn_delete.clicked.connect(self.delete_employee)
        btn_refresh.clicked.connect(self.load_employee_data)
        self.employee_table.cellClicked.connect(self.show_employee_detail)

        layout.addWidget(header)
        layout.addLayout(search_layout)
        layout.addSpacing(10)
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

        # Search section
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        search_label = QLabel("🔍 Tìm kiếm:")
        search_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        search_label.setStyleSheet("color: #2c3e50;")
        
        self.product_search_combo = QComboBox()
        self.product_search_combo.addItems(["Tất cả", "Tên sản phẩm", "ID", "Danh mục", "Thương hiệu"])
        self.product_search_combo.setFixedHeight(40)
        self.product_search_combo.setFixedWidth(180)
        self.product_search_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 11px;
                color: #2c3e50;
            }
            QComboBox:hover {
                border: 2px solid #3498db;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #2c3e50;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                color: black;
                selection-background-color: #3498db;
            }
        """)
        
        self.product_search_input = QLineEdit()
        self.product_search_input.setPlaceholderText("Nhập từ khóa tìm kiếm...")
        self.product_search_input.setFixedHeight(40)
        self.product_search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 11px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.product_search_input.textChanged.connect(self.search_products)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.product_search_combo)
        search_layout.addWidget(self.product_search_input)
        search_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("➕ Thêm Sản Phẩm")
        btn_delete = QPushButton("🗑️ Xóa Sản Phẩm")
        btn_refresh = QPushButton("🔄 Làm Mới")
        
        btn_add.setStyleSheet("color: black; font-weight: bold;")
        btn_delete.setStyleSheet("color: black; font-weight: bold;")
        btn_refresh.setStyleSheet("color: black; font-weight: bold;")
        
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
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                gridline-color: #ecf0f1;
                outline: none;
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
                outline: none;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTableWidget::item:focus {
                outline: none;
                border: none;
            }
            QTableCornerButton::section {
                background-color: #34495e;
                border: none;
            }
        """)

        self.load_product_data()

        btn_add.clicked.connect(self.show_add_product_form)
        btn_delete.clicked.connect(self.handle_delete_product)
        btn_refresh.clicked.connect(self.load_product_data)
        self.product_table.cellClicked.connect(self.show_product_detail)

        layout.addWidget(header)
        layout.addLayout(search_layout)
        layout.addSpacing(10)
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        layout.addWidget(self.product_table)

        return page

    # =========================================================================
    # PHẦN ĐÃ SỬA LỖI (FIXED)
    # =========================================================================
    def create_stat_card(self, icon, title, value, color):
        card = QFrame()
        # 1. Đặt ID cho thẻ để dùng selector
        card.setObjectName("statCard")
        
        # 2. Sử dụng selector #statCard để style KHÔNG ảnh hưởng đến con bên trong
        card.setStyleSheet(f"""
            #statCard {{
                background-color: white; 
                border-radius: 10px; 
                border-left: 5px solid {color};
            }}
        """)
        card.setFixedHeight(130)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Icon container
        icon_container = QFrame()
        icon_container.setFixedSize(60, 60)
        # Style cụ thể cho icon container
        icon_container.setStyleSheet(
            f"""
            QFrame {{
                background-color: {color}; 
                border-radius: 30px;
                border: none;
            }}
            """
        )
        icon_container_layout = QVBoxLayout(icon_container)
        icon_container_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 28))
        # Set background transparent và border none
        icon_label.setStyleSheet("color: white; background: transparent; border: none;")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_container_layout.addWidget(icon_label)

        # Text info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10))
        # Đảm bảo không dính border
        title_label.setStyleSheet("color: #7f8c8d; border: none; background: transparent;")

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        # Đảm bảo không dính border
        value_label.setStyleSheet(f"color: {color}; border: none; background: transparent;")

        info_layout.addWidget(title_label)
        info_layout.addWidget(value_label)
        info_layout.addStretch()

        layout.addWidget(icon_container)
        layout.addLayout(info_layout)
        layout.addStretch()

        return card

    def load_employee_data(self, keyword=None, type_search=None):
            
        employees = self.userService.get_all_employee_info(keyword=keyword, type_search=type_search)
        
        self.employee_table.setRowCount(0)
        
        if not employees:
            return
        
        column_headers = list(employees[0].keys())
        
        self.employee_table.setColumnCount(len(column_headers))
        self.employee_table.setHorizontalHeaderLabels(column_headers)
        
        self.employee_table.setRowCount(len(employees))
        
        for row, employee_dict in enumerate(employees):
            for col, key in enumerate(column_headers):
                data = employee_dict.get(key, "")
                
                if isinstance(data, (date, datetime)):
                    display_text = data.strftime('%Y-%m-%d')
                elif data is None:
                    display_text = ""
                else:
                    display_text = str(data)
                
                item = QTableWidgetItem(display_text)
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
        
        dialog = EmployeeDetailDialog(employee_data, self.oracleExec, self)
        dialog.exec()

    def show_add_employee_form(self):
        if AddEmployeeDialog is None:
            QMessageBox.warning(self, "Lỗi", "Chưa import được form thêm nhân viên")
            return

        dialog = AddEmployeeDialog(self.oracleExec, self)
        if dialog.exec():
            new_employee = dialog.get_employee_data()
            if new_employee:
                QMessageBox.information(self, "Thành Công",
                    f"Đã thêm nhân viên: {new_employee.get('name', 'N/A')}\n")
                self.load_employee_data()
                
    def delete_employee(self):
        selected_row=self.employee_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self,"Cảnh báo", "Vui lòng chọn một nhân viên để xóa")
            return
        
        username=self.employee_table.item(selected_row,7).text()
        reply = QMessageBox.question(self, "Xác Nhận",
                                     f"Bạn có chắc chắn muốn xóa nhân viên {username}?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.userService.deactive_employee(username)
                QMessageBox.information(self, "Thành Công", f"Đã xóa nhân viên {username}")
                self.load_employee_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa: {str(e)}")
        
    def show_add_product_form(self):
        if AddProductDialog is None:
            QMessageBox.warning(self, "Lỗi", "Chưa import được form thêm sản phẩm")
            return
            
        dialog = AddProductDialog(self.oracleExec, self)
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
        
        dialog = ProductDetailDialog(product_data, self.oracleExec, self)
        dialog.exec()
        
    def handle_delete_product(self):
        selected_items = self.product_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Chưa Chọn", "Vui lòng chọn sản phẩm để xóa.")
            return
        
        selected_row = selected_items[0].row()
        product_id_item = self.product_table.item(selected_row, 0)
        if not product_id_item:
            QMessageBox.warning(self, "Lỗi", "Không thể lấy ID sản phẩm.")
            return
        
        product_id = int(product_id_item.text())
        
        reply = QMessageBox.question(self, "Xác Nhận Xóa",
                                     f"Bạn có chắc chắn muốn xóa sản phẩm ID {product_id}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.productService.deactivate_product(product_id)
                QMessageBox.information(self, "Thành Công", f"Đã xóa sản phẩm ID {product_id}.")
                self.load_product_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa sản phẩm: {str(e)}")
    
    def search_employees(self):
        keyword = self.employee_search_input.text().strip()
        search_type_vn = self.employee_search_combo.currentText()
        
        column_map = {
            "Tên": "name",
            "Email": "email",
            "Số điện thoại": "phonenumber",
            "Username": "username",
            "Chức vụ": "emp_role"
        }
        
        type_search = column_map.get(search_type_vn) if search_type_vn != "Tất cả" else None
        
        self.load_employee_data(keyword=keyword, type_search=type_search)
        
    def search_products(self):
        """Tìm kiếm sản phẩm theo từ khóa và thuộc tính đã chọn"""
        search_text = self.product_search_input.text().strip().lower()
        search_type = self.product_search_combo.currentText()
        
        # Nếu không có từ khóa, hiển thị tất cả các hàng
        if not search_text:
            for row in range(self.product_table.rowCount()):
                self.product_table.setRowHidden(row, False)
            return
        
        # Map thuộc tính tìm kiếm với tên cột trong database
        column_map = {
            "Tên sản phẩm": "name",
            "ID": "id",
            "Danh mục": "categoryid",
            "Thương hiệu": "brandid"
        }
        
        # Ẩn tất cả các hàng trước
        for row in range(self.product_table.rowCount()):
            self.product_table.setRowHidden(row, True)
        
        # Hiển thị các hàng phù hợp với tìm kiếm
        for row in range(self.product_table.rowCount()):
            match = False
            
            if search_type == "Tất cả":
                # Tìm kiếm trên tất cả các cột
                for col in range(self.product_table.columnCount()):
                    item = self.product_table.item(row, col)
                    if item and search_text in item.text().lower():
                        match = True
                        break
            else:
                # Tìm kiếm trên cột cụ thể
                col_name = column_map.get(search_type)
                if col_name:
                    # Tìm index của cột
                    for col in range(self.product_table.columnCount()):
                        header = self.product_table.horizontalHeaderItem(col)
                        if header and header.text().lower() == col_name:
                            item = self.product_table.item(row, col)
                            if item and search_text in item.text().lower():
                                match = True
                            break
            
            if match:
                self.product_table.setRowHidden(row, False)
    
    # =========================================================================
    # ORDER / CART FUNCTIONS
    # =========================================================================
    def load_order_products(self):
        """Load danh sách sản phẩm vào bảng order"""
        if not self.productService:
            self.order_product_table.setRowCount(0)
            return

        try:
            products = self.productService.get_all_products()
            if not products:
                self.order_product_table.setRowCount(0)
                return
            
            self.order_product_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                # ID
                id_item = QTableWidgetItem(str(product.get('id', '')))
                id_item.setTextAlignment(Qt.AlignCenter)
                self.order_product_table.setItem(row, 0, id_item)
                
                # Name
                name_item = QTableWidgetItem(str(product.get('name', '')))
                self.order_product_table.setItem(row, 1, name_item)
                
                # Price
                price = product.get('unitprice', 0)
                price_item = QTableWidgetItem(f"{price:,.0f} đ")
                price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.order_product_table.setItem(row, 2, price_item)
                
                # Stock
                stock = product.get('stockquantity', 0)
                stock_item = QTableWidgetItem(str(stock))
                stock_item.setTextAlignment(Qt.AlignCenter)
                self.order_product_table.setItem(row, 3, stock_item)
                
                # Add button
                btn_add = QPushButton("➕ Thêm")
                btn_add.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border-radius: 5px;
                        padding: 5px 10px;
                        font-weight: bold;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                btn_add.setCursor(Qt.PointingHandCursor)
                btn_add.clicked.connect(lambda checked, r=row: self.add_to_cart(r))
                self.order_product_table.setCellWidget(row, 4, btn_add)
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể load sản phẩm: {str(e)}")
    
    def search_order_products(self):
        """Tìm kiếm sản phẩm trong bảng order"""
        search_text = self.order_product_search.text().strip().lower()
        
        if not search_text:
            for row in range(self.order_product_table.rowCount()):
                self.order_product_table.setRowHidden(row, False)
            return
        
        for row in range(self.order_product_table.rowCount()):
            match = False
            for col in range(self.order_product_table.columnCount() - 1):  # Skip button column
                item = self.order_product_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.order_product_table.setRowHidden(row, not match)
    
    def add_to_cart(self, row):
        """Thêm sản phẩm vào giỏ hàng"""
        try:
            # Get product info from table
            product_id = int(self.order_product_table.item(row, 0).text())
            product_name = self.order_product_table.item(row, 1).text()
            price_text = self.order_product_table.item(row, 2).text().replace(' đ', '').replace(',', '')
            product_price = float(price_text)
            stock = int(self.order_product_table.item(row, 3).text())
            
            if stock <= 0:
                QMessageBox.warning(self, "Hết Hàng", f"Sản phẩm '{product_name}' đã hết hàng!")
                return
            
            # Check if product already in cart
            for item in self.cart_items:
                if item['id'] == product_id:
                    if item['quantity'] < stock:
                        item['quantity'] += 1
                        self.update_cart_display()
                        return
                    else:
                        QMessageBox.warning(self, "Vượt Quá Tồn Kho", 
                                          f"Không thể thêm. Tồn kho chỉ còn {stock} sản phẩm!")
                        return
            
            # Add new item to cart
            self.cart_items.append({
                'id': product_id,
                'name': product_name,
                'price': product_price,
                'quantity': 1,
                'stock': stock
            })
            
            self.update_cart_display()
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể thêm vào giỏ hàng: {str(e)}")
    
    def update_cart_display(self):
        """Cập nhật hiển thị giỏ hàng"""
        self.cart_table.setRowCount(len(self.cart_items))
        total = 0
        
        for row, item in enumerate(self.cart_items):
            # Product name
            name_item = QTableWidgetItem(item['name'])
            self.cart_table.setItem(row, 0, name_item)
            
            # Price
            price_item = QTableWidgetItem(f"{item['price']:,.0f} đ")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 1, price_item)
            
            # Quantity spinbox
            quantity_spin = QSpinBox()
            quantity_spin.setMinimum(1)
            quantity_spin.setMaximum(item['stock'])
            quantity_spin.setValue(item['quantity'])
            quantity_spin.setAlignment(Qt.AlignCenter)
            
            quantity_spin.setStyleSheet("color: black")
            
            quantity_spin.valueChanged.connect(lambda val, r=row: self.update_cart_quantity(r, val))
            self.cart_table.setCellWidget(row, 2, quantity_spin)
            
            # Subtotal
            subtotal = item['price'] * item['quantity']
            total += subtotal
            subtotal_item = QTableWidgetItem(f"{subtotal:,.0f} đ")
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            subtotal_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            
            subtotal_item.setForeground(QColor("black"))
            
            self.cart_table.setItem(row, 3, subtotal_item)
            
            # Remove button
            btn_remove = QPushButton("🗑️")
            btn_remove.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            btn_remove.setCursor(Qt.PointingHandCursor)
            btn_remove.clicked.connect(lambda checked, r=row: self.remove_from_cart(r))
            self.cart_table.setCellWidget(row, 4, btn_remove)
        
        # Update total
        self.total_amount_label.setText(f"{total:,.0f} đ")
    
    def update_cart_quantity(self, row, quantity):
        """Cập nhật số lượng sản phẩm trong giỏ"""
        if 0 <= row < len(self.cart_items):
            self.cart_items[row]['quantity'] = quantity
            self.update_cart_display()
    
    def remove_from_cart(self, row):
        """Xóa sản phẩm khỏi giỏ hàng"""
        if 0 <= row < len(self.cart_items):
            product_name = self.cart_items[row]['name']
            reply = QMessageBox.question(self, "Xác Nhận", 
                                        f"Xóa '{product_name}' khỏi giỏ hàng?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.cart_items.pop(row)
                self.update_cart_display()
    
    def clear_cart(self):
        """Xóa toàn bộ giỏ hàng"""
        if not self.cart_items:
            QMessageBox.information(self, "Thông Báo", "Giỏ hàng đang trống!")
            return
        
        reply = QMessageBox.question(self, "Xác Nhận", 
                                    "Bạn có chắc muốn xóa toàn bộ giỏ hàng?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cart_items.clear()
            self.update_cart_display()
            QMessageBox.information(self, "Thành Công", "Đã xóa giỏ hàng!")
    
    def create_order(self):
        """Tạo đơn hàng từ giỏ hàng"""
        if not self.cart_items:
            QMessageBox.warning(self, "Giỏ Hàng Trống", "Vui lòng thêm sản phẩm vào giỏ hàng!")
            return
        
        # Validate customer info
        customer_name = self.customer_name_input.text().strip()
        customer_phone = self.customer_phone_input.text().strip()
        
        if not customer_name:
            QMessageBox.warning(self, "Thiếu Thông Tin", "Vui lòng nhập tên khách hàng!")
            self.customer_name_input.setFocus()
            return
        
        if not customer_phone:
            QMessageBox.warning(self, "Thiếu Thông Tin", "Vui lòng nhập số điện thoại!")
            self.customer_phone_input.setFocus()
            return
        
        total = sum(item['price'] * item['quantity'] for item in self.cart_items)
        
        # Create order summary
        summary = "CHI TIẾT ĐƠN HÀNG:\n\n"
        summary += f"👤 Khách hàng: {customer_name}\n"
        summary += f"📱 Số điện thoại: {customer_phone}\n\n"
        summary += "DANH SÁCH SẢN PHẨM:\n"
        for item in self.cart_items:
            subtotal = item['price'] * item['quantity']
            summary += f"• {item['name']}\n"
            summary += f"  {item['quantity']} x {item['price']:,.0f} đ = {subtotal:,.0f} đ\n\n"
        summary += f"TỔNG CỘNG: {total:,.0f} đ"
        
        reply = QMessageBox.question(self, "Xác Nhận Đơn Hàng", 
                                    summary + "\n\nXác nhận tạo đơn hàng?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # Save order to history
                from datetime import datetime
                order = {
                    'order_id': len(self.order_history) + 1,
                    'customer_name': customer_name,
                    'customer_phone': customer_phone,
                    'items': [item.copy() for item in self.cart_items],
                    'total': total,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'employee': self.username
                }
                self.order_history.append(order)
                
                # TODO: Gọi API lưu đơn hàng vào database
                # self.orderService.create_order(order)
                
                QMessageBox.information(self, "Thành Công", 
                                      f"Đã tạo đơn hàng #{order['order_id']} thành công!\n"
                                      f"Khách hàng: {customer_name}\n"
                                      f"Tổng tiền: {total:,.0f} đ\n\n"
                                      f"(Chức năng lưu vào database sẽ được thêm sau)")
                
                # Clear cart and customer info
                self.cart_items.clear()
                self.customer_name_input.clear()
                self.customer_phone_input.clear()
                self.update_cart_display()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể tạo đơn hàng: {str(e)}")
    
    def view_order_history(self):
        """Xem lịch sử đơn hàng đã tạo"""
        if not self.order_history:
            QMessageBox.information(self, "Lịch Sử Đơn Hàng", "Chưa có đơn hàng nào được tạo!")
            return
        
        # Open OrderHistoryDialog
        from UI.Dialog.OrderHistoryDialog import OrderHistoryDialog
        dialog = OrderHistoryDialog(self.order_history, self)
        dialog.exec()
