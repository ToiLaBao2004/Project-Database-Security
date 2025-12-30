from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QPushButton, QFrame, QHeaderView, QDialogButtonBox,
    QWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from BAL.OrderService import OrderService

class OrderDetailDialog(QDialog):
    def __init__(self, order_service: OrderService, order_id, parent=None):
        super().__init__(parent)
        self.order_service = order_service
        self.order_id = order_id
        self.parent_widget = parent
        self.order_details = []
        self.setWindowTitle(f"📋 Chi Tiết Đơn Hàng #{order_id}")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #ecf0f1;")
        self.load_order_details_data()
        self.init_ui()
    
    def load_order_details_data(self):
        """Load order details from OrderService"""
        try:
            details_data = self.order_service.load_orders_detail(self.order_id)
            if details_data:
                for detail in details_data:
                    self.order_details.append({
                        'id': detail["id"],
                        'order_id': detail["order_id"],
                        'product_name': detail["product_name"],
                        'unit_price': detail["unit_price"],
                        'quantity': detail["quantity"],
                        'subtotal': detail["subtotal"]
                    })
            else:
                QMessageBox.warning(self, "Thông báo", f"Không có chi tiết cho đơn hàng #{self.order_id}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tải chi tiết đơn hàng: {str(e)}")
    
    def init_ui(self):
        """Initialize UI for order detail display"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        header = QLabel(f"📦 CHI TIẾT ĐƠN HÀNG #{self.order_id}")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setStyleSheet("color: #2c3e50;")
        layout.addWidget(header)
        
        products_label = QLabel("🛒 CHI TIẾT SẢN PHẨM:")
        products_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        products_label.setStyleSheet("color: #2c3e50; margin-top: 10px;")
        layout.addWidget(products_label)
        
        products_table = QTableWidget()
        products_table.setColumnCount(6)
        products_table.setHorizontalHeaderLabels(["Mã Chi Tiết", "Mã ĐH", "Tên Sản Phẩm", "Đơn Giá", "Số Lượng", "Thành Tiền"])
        products_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        products_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        products_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        products_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        products_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        products_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        products_table.setAlternatingRowColors(True)
        products_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                gridline-color: #ecf0f1;
            }
            QHeaderView::section {
                background-color: #27ae60;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                color: #2c3e50;
            }
        """)
        
        products_table.setRowCount(len(self.order_details))
        
        total_amount = 0
        for row, detail in enumerate(self.order_details):
            id_item = QTableWidgetItem(str(detail['id']))
            id_item.setTextAlignment(Qt.AlignCenter)
            products_table.setItem(row, 0, id_item)
            
            order_id_item = QTableWidgetItem(str(detail['order_id']))
            order_id_item.setTextAlignment(Qt.AlignCenter)
            products_table.setItem(row, 1, order_id_item)
            
            name_item = QTableWidgetItem(detail['product_name'])
            products_table.setItem(row, 2, name_item)
            
            price_item = QTableWidgetItem(f"{detail['unit_price']:,.0f} đ")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            products_table.setItem(row, 3, price_item)
            
            qty_item = QTableWidgetItem(str(detail['quantity']))
            qty_item.setTextAlignment(Qt.AlignCenter)
            products_table.setItem(row, 4, qty_item)
            
            subtotal_item = QTableWidgetItem(f"{detail['subtotal']:,.0f} đ")
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            subtotal_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            products_table.setItem(row, 5, subtotal_item)
            
            total_amount += detail['subtotal']
        
        layout.addWidget(products_table)
        
        total_frame = QFrame()
        total_frame.setStyleSheet("background-color: #2ecc71; border-radius: 10px; padding: 15px;")
        total_layout = QHBoxLayout(total_frame)
        
        total_label = QLabel("TỔNG CỘNG:")
        total_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        total_label.setStyleSheet("color: white; border: none; background: transparent;")
        
        total_value = QLabel(f"{total_amount:,.0f} đ")
        total_value.setFont(QFont("Segoe UI", 18, QFont.Bold))
        total_value.setStyleSheet("color: white; border: none; background: transparent;")
        total_value.setAlignment(Qt.AlignRight)
        
        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(total_value)
        
        layout.addWidget(total_frame)
        
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