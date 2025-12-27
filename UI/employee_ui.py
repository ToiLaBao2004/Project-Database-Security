from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget,
    QGridLayout, QScrollArea, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class EmployeeUI(QWidget):
    def __init__(self, conn, username, parent=None):
        super().__init__()
        self.parent = parent
        self.username = username
        self.conn = conn
        self.setWindowTitle(f"Nhân Viên - {username}")
        self.setMinimumSize(1100, 650)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= SIDEBAR =================
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #34495e;")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #2c3e50; padding: 20px;")
        header_layout = QVBoxLayout(header)
        
        logo = QLabel("👤")
        logo.setFont(QFont("Segoe UI Emoji", 32))
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("color: white;")
        
        employee_name = QLabel(f"Nhân viên: {self.username}")
        employee_name.setFont(QFont("Segoe UI", 11, QFont.Bold))
        employee_name.setAlignment(Qt.AlignCenter)
        employee_name.setStyleSheet("color: white; margin-top: 10px;")
        
        header_layout.addWidget(logo)
        header_layout.addWidget(employee_name)

        # Menu buttons
        self.btn_profile = QPushButton("👤 Thông Tin Cá Nhân")
        self.btn_activity = QPushButton("📊 Hoạt Động Của Tôi")
        self.btn_orders = QPushButton("📦 Đơn Hàng")
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
                background-color: #415b76;
            }
            QPushButton:pressed {
                background-color: #1f6fa8;
            }
        """
        
        self.btn_profile.setStyleSheet(menu_style)
        self.btn_activity.setStyleSheet(menu_style)
        self.btn_orders.setStyleSheet(menu_style)
        self.btn_logout.setStyleSheet(menu_style + "QPushButton:hover { background-color: #c0392b; }")
        
        self.btn_profile.setCursor(Qt.PointingHandCursor)
        self.btn_activity.setCursor(Qt.PointingHandCursor)
        self.btn_orders.setCursor(Qt.PointingHandCursor)
        self.btn_logout.setCursor(Qt.PointingHandCursor)

        self.btn_profile.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_activity.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_orders.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_logout.clicked.connect(self.handle_logout)

        sidebar_layout.addWidget(header)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(self.btn_profile)
        sidebar_layout.addWidget(self.btn_activity)
        sidebar_layout.addWidget(self.btn_orders)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_logout)

        # ================= CONTENT AREA =================
        self.stacked_widget = QStackedWidget()
        
        # Profile Page
        profile_page = self.create_profile_page()
        self.stacked_widget.addWidget(profile_page)
        
        # Activity Page
        activity_page = self.create_activity_page()
        self.stacked_widget.addWidget(activity_page)
        
        # Orders Page
        orders_page = self.create_orders_page()
        self.stacked_widget.addWidget(orders_page)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget)

    def create_profile_page(self):
        """Create profile information page"""
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header = QLabel("👤 THÔNG TIN CÁ NHÂN")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        # Info Card
        info_card = QFrame()
        info_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #bdc3c7;
            }
        """)
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(30, 30, 30, 30)
        info_layout.setSpacing(20)

        # Avatar and name section
        top_section = QHBoxLayout()
        avatar = QLabel("👤")
        avatar.setFont(QFont("Segoe UI Emoji", 64))
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFixedSize(100, 100)
        avatar.setStyleSheet("""
            background-color: #3498db;
            border-radius: 50px;
            color: white;
        """)

        name_section = QVBoxLayout()
        name_label = QLabel("Thông tin nhân viên")
        name_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50; border: none;")
        
        role_label = QLabel(f"🏷️ Username: {self.username}")
        role_label.setFont(QFont("Segoe UI", 12))
        role_label.setStyleSheet("color: #7f8c8d; border: none;")
        
        name_section.addWidget(name_label)
        name_section.addWidget(role_label)
        name_section.addStretch()

        top_section.addWidget(avatar)
        top_section.addSpacing(20)
        top_section.addLayout(name_section)
        top_section.addStretch()

        info_layout.addLayout(top_section)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: #ecf0f1; border: none;")
        divider.setFixedHeight(2)
        info_layout.addWidget(divider)

        # Note
        note_label = QLabel("📝 Thông tin chi tiết sẽ được load từ database khi tích hợp backend")
        note_label.setFont(QFont("Segoe UI", 10))
        note_label.setStyleSheet("color: #7f8c8d; border: none; padding: 15px;")
        note_label.setWordWrap(True)
        info_layout.addWidget(note_label)

        layout.addWidget(header)
        layout.addWidget(info_card)
        layout.addStretch()

        return page

    def create_activity_page(self):
        """Create activity log page"""
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QLabel("📊 HOẠT ĐỘNG CỦA TÔI")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        # Stats cards
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

        # Activity table
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

        # Sample activity data
        activities = [
            ["2024-12-28 14:30:22", "SELECT", "EMPLOYEES", "Xem thông tin cá nhân", "192.168.1.105"],
            ["2024-12-28 10:20:45", "SELECT", "PRODUCTS", "Xem danh sách sản phẩm", "192.168.1.105"],
        ]

        activity_table.setRowCount(len(activities))
        for row, activity in enumerate(activities):
            for col, data in enumerate(activity):
                item = QTableWidgetItem(data)
                item.setTextAlignment(Qt.AlignCenter)
                
                if col == 1:  # Action column
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
        """Create orders management page"""
        page = QWidget()
        page.setStyleSheet("background-color: #ecf0f1;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QLabel("📦 ĐƠN HÀNG CỦA TÔI")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        # Action buttons
        btn_layout = QHBoxLayout()
        
        btn_refresh = QPushButton("🔄 Làm Mới")
        btn_refresh.setFixedHeight(40)
        btn_refresh.setFont(QFont("Segoe UI", 10, QFont.Bold))
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(btn_refresh)
        btn_layout.addStretch()

        # Orders table
        orders_table = QTableWidget()
        orders_table.setColumnCount(6)
        orders_table.setHorizontalHeaderLabels(["Mã ĐH", "Khách Hàng", "Ngày Tạo", "Tổng Tiền", "Trạng Thái", "Ghi Chú"])
        orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        orders_table.setAlternatingRowColors(True)
        orders_table.setStyleSheet("""
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

        # Sample orders - empty for now
        orders_table.setRowCount(0)

        # Note
        note = QLabel("📝 Dữ liệu đơn hàng sẽ được load từ database khi tích hợp backend")
        note.setFont(QFont("Segoe UI", 10))
        note.setStyleSheet("color: #7f8c8d; padding: 10px;")
        note.setAlignment(Qt.AlignCenter)

        # Connect buttons
        btn_refresh.clicked.connect(lambda: QMessageBox.information(self, "Làm mới", "Chức năng load dữ liệu (TODO)"))

        layout.addWidget(header)
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        layout.addWidget(orders_table)
        layout.addWidget(note)

        return page

    def create_stat_card(self, icon, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border-left: 5px solid {color};
            }}
        """)
        card.setFixedHeight(120)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        icon_label.setStyleSheet(f"color: {color}; border: none;")

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 9))
        title_label.setStyleSheet("color: #7f8c8d; border: none;")

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        value_label.setStyleSheet(f"color: {color}; border: none;")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        return card

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
