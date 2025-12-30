from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QPushButton, QFrame, QHeaderView, QLineEdit,
    QWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from datetime import datetime

class CustomerDialog(QDialog):
    def __init__(self, oracleExec, parent=None):
        super().__init__(parent)
        self.oracleExec = oracleExec
        self.parent_widget = parent
        
        # Import service
        from BAL.CustomerService import CustomerService
        self.customerService = CustomerService(self.oracleExec)
        
        self.setWindowTitle("👥 Quản Lý Khách Hàng")
        self.setMinimumSize(1200, 700)
        self.setStyleSheet("background-color: #ecf0f1;")
        self.init_ui()
        self.load_customers()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("👥 QUẢN LÝ KHÁCH HÀNG")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Search bar
        search_frame = QFrame()
        search_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 10px;")
        search_layout = QHBoxLayout(search_frame)
        
        search_label = QLabel("🔍 Tìm kiếm:")
        search_label.setFont(QFont("Segoe UI", 11))
        search_label.setStyleSheet("color: #2c3e50;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên, số điện thoại hoặc email...")
        self.search_input.setFont(QFont("Segoe UI", 11))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.search_input.textChanged.connect(self.search_customers)
        
        btn_refresh = QPushButton("🔄 Làm mới")
        btn_refresh.setFixedSize(120, 35)
        btn_refresh.setFont(QFont("Segoe UI", 10, QFont.Bold))
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self.load_customers)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(btn_refresh)
        
        layout.addWidget(search_frame)
        
        # Customer table
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(7)
        self.customers_table.setHorizontalHeaderLabels([
            "Mã KH", "Tên Khách Hàng", "Số Điện Thoại", "Email", 
            "Ngày Sinh", "Giới Tính", "Chi Tiết"
        ])
        
        self.customers_table.setColumnWidth(0, 80)
        self.customers_table.setColumnWidth(1, 200)
        self.customers_table.setColumnWidth(2, 130)
        self.customers_table.setColumnWidth(3, 230)
        self.customers_table.setColumnWidth(4, 120)
        self.customers_table.setColumnWidth(5, 100)
        self.customers_table.setColumnWidth(6, 120)
        
        self.customers_table.verticalHeader().setDefaultSectionSize(50)
        self.customers_table.setAlternatingRowColors(True)
        self.customers_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
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
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        layout.addWidget(self.customers_table)
        
        # Footer with stats
        footer_frame = QFrame()
        footer_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 10px;")
        footer_layout = QHBoxLayout(footer_frame)
        
        self.stats_label = QLabel("Tổng số khách hàng: 0")
        self.stats_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.stats_label.setStyleSheet("color: #2c3e50;")
        
        btn_close = QPushButton("Đóng")
        btn_close.setFixedSize(100, 35)
        btn_close.setFont(QFont("Segoe UI", 10, QFont.Bold))
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(self.reject)
        
        footer_layout.addWidget(self.stats_label)
        footer_layout.addStretch()
        footer_layout.addWidget(btn_close)
        
        layout.addWidget(footer_frame)
    
    def load_customers(self):
        """Tải danh sách khách hàng từ database"""
        try:
            self.search_input.clear()
            customers = self.customerService.get_all_customers()
            self.display_customers(customers)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải danh sách khách hàng:\n{str(e)}")
    
    def search_customers(self):
        """Tìm kiếm khách hàng"""
        search_term = self.search_input.text().strip()
        
        if not search_term:
            self.load_customers()
            return
        
        try:
            customers = self.customerService.search_customers(search_term)
            self.display_customers(customers)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tìm kiếm khách hàng:\n{str(e)}")
    
    def display_customers(self, customers):
        """Hiển thị danh sách khách hàng lên bảng"""
        self.customers_table.setRowCount(0)
        self.customers_table.setRowCount(len(customers))
        
        for row, customer in enumerate(customers):
            # Mã khách hàng
            id_item = QTableWidgetItem(f"#{customer['id']}")
            id_item.setTextAlignment(Qt.AlignCenter)
            id_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self.customers_table.setItem(row, 0, id_item)
            
            # Tên khách hàng
            name_item = QTableWidgetItem(customer['name'])
            name_item.setFont(QFont("Segoe UI", 10))
            self.customers_table.setItem(row, 1, name_item)
            
            # Số điện thoại
            phone_item = QTableWidgetItem(customer['phone_number'])
            phone_item.setTextAlignment(Qt.AlignCenter)
            self.customers_table.setItem(row, 2, phone_item)
            
            # Email
            email_item = QTableWidgetItem(customer['email'])
            self.customers_table.setItem(row, 3, email_item)
            
            # Ngày sinh
            if customer['date_of_birth']:
                if isinstance(customer['date_of_birth'], str):
                    dob_str = customer['date_of_birth']
                else:
                    dob_str = customer['date_of_birth'].strftime("%d/%m/%Y")
            else:
                dob_str = "N/A"
            dob_item = QTableWidgetItem(dob_str)
            dob_item.setTextAlignment(Qt.AlignCenter)
            self.customers_table.setItem(row, 4, dob_item)
            
            # Giới tính
            gender_text = "Nam" if customer['gender'] else "Nữ"
            gender_item = QTableWidgetItem(gender_text)
            gender_item.setTextAlignment(Qt.AlignCenter)
            self.customers_table.setItem(row, 5, gender_item)
            
            # Nút chi tiết
            container_widget = QWidget()
            layout_btn = QHBoxLayout(container_widget)
            layout_btn.setContentsMargins(0, 0, 0, 0)
            layout_btn.setAlignment(Qt.AlignCenter)

            btn_detail = QPushButton("🔍 Chi Tiết")
            btn_detail.setFixedSize(100, 32)
            btn_detail.setFont(QFont("Segoe UI", 9, QFont.Bold))
            btn_detail.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border-radius: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            btn_detail.setCursor(Qt.PointingHandCursor)
            btn_detail.clicked.connect(lambda checked, c=customer: self.view_customer_detail(c))
            
            layout_btn.addWidget(btn_detail)
            self.customers_table.setCellWidget(row, 6, container_widget)
        
        # Cập nhật thống kê
        self.stats_label.setText(f"Tổng số khách hàng: {len(customers)}")
    
    def view_customer_detail(self, customer):
        """Hiển thị chi tiết khách hàng"""
        detail_dialog = QDialog(self)
        detail_dialog.setWindowTitle(f"Chi Tiết Khách Hàng #{customer['id']}")
        detail_dialog.setMinimumSize(500, 400)
        detail_dialog.setStyleSheet("background-color: #ecf0f1;")
        
        layout = QVBoxLayout(detail_dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Header
        header = QLabel(f"👤 THÔNG TIN KHÁCH HÀNG #{customer['id']}")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header.setStyleSheet("color: #2c3e50;")
        layout.addWidget(header)
        
        # Info card
        info_card = QFrame()
        info_card.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px; border: 2px solid #3498db;")
        info_layout = QVBoxLayout(info_card)
        
        # Format date of birth
        if customer['date_of_birth']:
            if isinstance(customer['date_of_birth'], str):
                dob_str = customer['date_of_birth']
            else:
                dob_str = customer['date_of_birth'].strftime("%d/%m/%Y")
        else:
            dob_str = "N/A"
        
        gender_text = "Nam" if customer['gender'] else "Nữ"
        
        info_html = f"""
        <table style='width: 100%; color: #2c3e50;'>
            <tr>
                <td style='padding: 10px; font-weight: bold; width: 40%;'>📝 Mã khách hàng:</td>
                <td style='padding: 10px;'>#{customer['id']}</td>
            </tr>
            <tr style='background-color: #f8f9fa;'>
                <td style='padding: 10px; font-weight: bold;'>👤 Tên khách hàng:</td>
                <td style='padding: 10px;'>{customer['name']}</td>
            </tr>
            <tr>
                <td style='padding: 10px; font-weight: bold;'>📞 Số điện thoại:</td>
                <td style='padding: 10px;'>{customer['phone_number']}</td>
            </tr>
            <tr style='background-color: #f8f9fa;'>
                <td style='padding: 10px; font-weight: bold;'>📧 Email:</td>
                <td style='padding: 10px;'>{customer['email']}</td>
            </tr>
            <tr>
                <td style='padding: 10px; font-weight: bold;'>🎂 Ngày sinh:</td>
                <td style='padding: 10px;'>{dob_str}</td>
            </tr>
            <tr style='background-color: #f8f9fa;'>
                <td style='padding: 10px; font-weight: bold;'>⚥ Giới tính:</td>
                <td style='padding: 10px;'>{gender_text}</td>
            </tr>
        </table>
        """
        
        info_label = QLabel(info_html)
        info_label.setFont(QFont("Segoe UI", 10))
        info_label.setStyleSheet("background: transparent; border: none;")
        info_label.setTextFormat(Qt.RichText)
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_card)
        layout.addStretch()
        
        # Close button
        btn_close = QPushButton("Đóng")
        btn_close.setFixedSize(100, 35)
        btn_close.setFont(QFont("Segoe UI", 10, QFont.Bold))
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(detail_dialog.reject)
        
        layout.addWidget(btn_close, alignment=Qt.AlignRight)
        
        detail_dialog.exec()
