from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QPushButton, QFrame, QHeaderView, QDialogButtonBox,
    QWidget, QMessageBox, QAbstractItemView, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from BAL.OrderService import OrderService

class OrderHistoryDialog(QDialog):
    def __init__(self, order_service: OrderService, parent=None):
        super().__init__(parent)
        self.order_service = order_service
        self.parent_widget = parent
        self.order_history = []
        self.filtered_orders = []  # Danh sách đơn hàng sau khi lọc
        self.setWindowTitle("📋 Lịch Sử Đơn Hàng")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("background-color: #ecf0f1;")
        self.load_orders_data()
        self.init_ui()
    
    def load_orders_data(self):
        try:
            orders_data = self.order_service.load_orders()
            if orders_data:
                for order in orders_data:
                    self.order_history.append({
                        'order_id': order["id"],
                        'customer_name': order["customer_name"],
                        'customer_phone': order["customer_phone"],
                        'order_date': order["order_date"], 
                        'employee_name': order["employee_name"],
                        "employee_username": order["employee_username"],
                        "total": order["total"]
                    })
                self.filtered_orders = self.order_history.copy()  # Khởi tạo danh sách lọc
            else:
                QMessageBox.warning(self, "Thông báo", "Không có dữ liệu đơn hàng")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tải dữ liệu đơn hàng: {str(e)}")
    
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel(f"📋 LỊCH SỬ ĐƠN HÀNG ({len(self.order_history)} đơn)")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Thêm thanh tìm kiếm
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Tìm kiếm:")
        search_label.setFont(QFont("Segoe UI", 11))
        search_label.setStyleSheet("color: #2c3e50;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên khách hàng, SĐT, nhân viên hoặc mã đơn hàng...")
        self.search_input.setFont(QFont("Segoe UI", 10))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.search_input.textChanged.connect(self.filter_orders)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Bảng đơn hàng
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(8)
        self.orders_table.setHorizontalHeaderLabels(["Mã ĐH", "Khách Hàng", "SĐT", "Thời Gian", "Nhân Viên", "Username", "Tổng Tiền", "Chi Tiết"])
        
        self.orders_table.setColumnWidth(0, 70)
        self.orders_table.setColumnWidth(1, 160)
        self.orders_table.setColumnWidth(2, 100)
        self.orders_table.setColumnWidth(3, 140)
        self.orders_table.setColumnWidth(4, 140)
        self.orders_table.setColumnWidth(5, 120)
        self.orders_table.setColumnWidth(6, 100)
        self.orders_table.setColumnWidth(7, 90)
        
        # --- SỬA ĐỔI QUAN TRỌNG: Khóa chiều cao hàng ---
        # Chuyển sang chế độ Fixed để tránh bị tự động co lại
        self.orders_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Set chiều cao mặc định (dự phòng)
        self.orders_table.verticalHeader().setDefaultSectionSize(60)
        
        self.orders_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.orders_table.setAlternatingRowColors(True)
        self.orders_table.setSelectionMode(QAbstractItemView.NoSelection) # Tắt chọn ô để tránh rối mắt khi click nút
        
        self.orders_table.setStyleSheet("""
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
                border-bottom: 1px solid #ecf0f1;
            }
        """)
        
        self.populate_table()  # Gọi hàm populate table
        
        layout.addWidget(self.orders_table)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        button_box.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        layout.addWidget(button_box)
    
    def populate_table(self):
        """Điền dữ liệu vào bảng từ filtered_orders"""
        self.orders_table.setRowCount(len(self.filtered_orders))
        
        for row, order in enumerate(self.filtered_orders):
            self.orders_table.setRowHeight(row, 60) 
            
            id_val = order["order_id"]
            id_item = QTableWidgetItem(f"#{id_val}")
            id_item.setTextAlignment(Qt.AlignCenter)
            id_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self.orders_table.setItem(row, 0, id_item)

            name_item = QTableWidgetItem(order["customer_name"])
            name_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.orders_table.setItem(row, 1, name_item)
            
            phone_item = QTableWidgetItem(order["customer_phone"])
            phone_item.setTextAlignment(Qt.AlignCenter)
            self.orders_table.setItem(row, 2, phone_item)
            
            raw_date = order["order_date"]
            date_str = raw_date.strftime("%d/%m/%Y %H:%M:%S")
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignCenter)
            self.orders_table.setItem(row, 3, date_item)
            
            employee_item = QTableWidgetItem(order["employee_name"])
            employee_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.orders_table.setItem(row, 4, employee_item)
            
            username_item = QTableWidgetItem(order["employee_username"])
            username_item.setTextAlignment(Qt.AlignCenter)
            self.orders_table.setItem(row, 5, username_item)

            total_val = order.get('total') or 0
            total_item = QTableWidgetItem(f"{float(total_val):,.0f} đ")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            total_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            total_item.setForeground(Qt.darkGreen)
            self.orders_table.setItem(row, 6, total_item)
            
            # --- Container cho nút ---
            container_widget = QWidget()
            layout_btn = QHBoxLayout(container_widget)
            layout_btn.setContentsMargins(0, 0, 0, 0)
            layout_btn.setAlignment(Qt.AlignCenter)

            btn_detail = QPushButton("🔍 Chi Tiết")
            btn_detail.setFixedSize(90, 36) # Kích thước cố định cho nút
            btn_detail.setFont(QFont("Segoe UI", 9, QFont.Bold))
            btn_detail.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border-radius: 6px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #1f618d;
                }
            """)
            btn_detail.setCursor(Qt.PointingHandCursor)
            btn_detail.clicked.connect(lambda checked, o=order: self.view_order_detail(o['order_id']))
            
            layout_btn.addWidget(btn_detail)
            self.orders_table.setCellWidget(row, 7, container_widget)
    
    def filter_orders(self):
        """Lọc đơn hàng dựa trên từ khóa tìm kiếm"""
        search_text = self.search_input.text().lower().strip()
        
        if not search_text:
            # Nếu không có từ khóa, hiển thị tất cả
            self.filtered_orders = self.order_history.copy()
        else:
            # Lọc đơn hàng theo từ khóa
            self.filtered_orders = []
            for order in self.order_history:
                # Tìm kiếm trong tên khách hàng, SĐT, nhân viên, username, mã đơn hàng
                if (search_text in order["customer_name"].lower() or
                    search_text in order["customer_phone"].lower() or
                    search_text in order["employee_name"].lower() or
                    search_text in order["employee_username"].lower() or
                    search_text in str(order["order_id"]).lower()):
                    self.filtered_orders.append(order)
        
        # Cập nhật lại bảng
        self.populate_table()
    
    def view_order_detail(self, order_id):
        """View details of a specific order"""
        try:
            from UI.Dialog.OrderDetailDialog import OrderDetailDialog
            dialog = OrderDetailDialog(self.order_service, order_id, self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi mở chi tiết đơn hàng: {str(e)}")