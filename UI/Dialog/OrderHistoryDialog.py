from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QPushButton, QFrame, QHeaderView, QDialogButtonBox,
    QWidget, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class OrderHistoryDialog(QDialog):
    def __init__(self, order_history, parent=None):
        super().__init__(parent)
        self.order_history = order_history
        self.parent_widget = parent
        self.setWindowTitle("📋 Lịch Sử Đơn Hàng")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("background-color: #ecf0f1;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel(f"📋 LỊCH SỬ ĐƠN HÀNG ({len(self.order_history)} đơn)")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(header)
        
        orders_table = QTableWidget()
        orders_table.setColumnCount(6)
        orders_table.setHorizontalHeaderLabels(["Mã ĐH", "Khách Hàng", "SĐT", "Thời Gian", "Tổng Tiền", "Chi Tiết"])
        
        orders_table.setColumnWidth(0, 70)
        orders_table.setColumnWidth(1, 200)
        orders_table.setColumnWidth(2, 110)
        orders_table.setColumnWidth(3, 160)
        orders_table.setColumnWidth(4, 120)
        orders_table.setColumnWidth(5, 150)
        
        # --- SỬA ĐỔI QUAN TRỌNG: Khóa chiều cao hàng ---
        # Chuyển sang chế độ Fixed để tránh bị tự động co lại
        orders_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Set chiều cao mặc định (dự phòng)
        orders_table.verticalHeader().setDefaultSectionSize(60)
        
        orders_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        orders_table.setAlternatingRowColors(True)
        orders_table.setSelectionMode(QAbstractItemView.NoSelection) # Tắt chọn ô để tránh rối mắt khi click nút
        
        orders_table.setStyleSheet("""
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
        
        orders_table.setRowCount(len(self.order_history))
        
        for row, order in enumerate(self.order_history):
            # --- SỬA ĐỔI QUAN TRỌNG: Ép chiều cao từng hàng ---
            orders_table.setRowHeight(row, 60) 

            id_item = QTableWidgetItem(f"#{order['order_id']}")
            id_item.setTextAlignment(Qt.AlignCenter)
            id_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            orders_table.setItem(row, 0, id_item)
            
            name_item = QTableWidgetItem(order['customer_name'])
            name_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            orders_table.setItem(row, 1, name_item)
            
            phone_item = QTableWidgetItem(order['customer_phone'])
            phone_item.setTextAlignment(Qt.AlignCenter)
            orders_table.setItem(row, 2, phone_item)
            
            date_item = QTableWidgetItem(order['date'])
            date_item.setTextAlignment(Qt.AlignCenter)
            orders_table.setItem(row, 3, date_item)
            
            total_item = QTableWidgetItem(f"{order['total']:,.0f} đ")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            total_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            total_item.setForeground(Qt.darkGreen)
            orders_table.setItem(row, 4, total_item)
            
            # --- Container cho nút ---
            container_widget = QWidget()
            layout_btn = QHBoxLayout(container_widget)
            layout_btn.setContentsMargins(0, 0, 0, 0)
            layout_btn.setAlignment(Qt.AlignCenter)

            btn_detail = QPushButton("🔍 Chi Tiết")
            btn_detail.setFixedSize(110, 36) # Kích thước cố định cho nút
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
            btn_detail.clicked.connect(lambda checked, o=order: self.view_order_detail(o))
            
            layout_btn.addWidget(btn_detail)
            orders_table.setCellWidget(row, 5, container_widget)
        
        layout.addWidget(orders_table)
        
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
    
    def view_order_detail(self, order):
        try:
            from UI.Dialog.OrderDetailDialog import OrderDetailDialog
            dialog = OrderDetailDialog(order, self)
            dialog.exec()
        except ImportError:
            detail_dialog = QDialog(self)
            detail_dialog.setWindowTitle(f"Chi Tiết Đơn Hàng #{order['order_id']}")
            detail_dialog.setMinimumSize(700, 500)
            detail_dialog.setStyleSheet("background-color: #ecf0f1;")
            
            layout = QVBoxLayout(detail_dialog)
            layout.setContentsMargins(25, 25, 25, 25)
            layout.setSpacing(15)
            
            header = QLabel(f"📦 CHI TIẾT ĐƠN HÀNG #{order['order_id']}")
            header.setFont(QFont("Segoe UI", 18, QFont.Bold))
            header.setStyleSheet("color: #2c3e50;")
            layout.addWidget(header)
            
            customer_card = QFrame()
            customer_card.setStyleSheet("background-color: white; border-radius: 10px; padding: 15px; border: 2px solid #3498db;")
            customer_layout = QVBoxLayout(customer_card)
            
            customer_title = QLabel("👤 THÔNG TIN KHÁCH HÀNG")
            customer_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
            customer_title.setStyleSheet("color: #3498db; border: none; background: transparent;")
            customer_layout.addWidget(customer_title)
            
            customer_info = QLabel(
                f"<b>Tên khách hàng:</b> {order['customer_name']}<br>"
                f"<b>Số điện thoại:</b> {order['customer_phone']}<br>"
                f"<b>Thời gian:</b> {order['date']}<br>"
                f"<b>Nhân viên xử lý:</b> {order.get('employee', 'N/A')}"
            )
            customer_info.setFont(QFont("Segoe UI", 10))
            customer_info.setStyleSheet("color: #2c3e50; border: none; background: transparent; padding: 5px;")
            customer_layout.addWidget(customer_info)
            
            layout.addWidget(customer_card)
            
            products_label = QLabel("🛒 SẢN PHẨM:")
            products_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            products_label.setStyleSheet("color: #2c3e50; margin-top: 10px;")
            layout.addWidget(products_label)
            
            products_table = QTableWidget()
            products_table.setColumnCount(4)
            products_table.setHorizontalHeaderLabels(["Tên Sản Phẩm", "Đơn Giá", "Số Lượng", "Thành Tiền"])
            products_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            products_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            products_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
            products_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
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
            
            products_table.setRowCount(len(order['items']))
            
            for row, item in enumerate(order['items']):
                name_item = QTableWidgetItem(item['name'])
                products_table.setItem(row, 0, name_item)
                
                price_item = QTableWidgetItem(f"{item['price']:,.0f} đ")
                price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                products_table.setItem(row, 1, price_item)
                
                qty_item = QTableWidgetItem(str(item['quantity']))
                qty_item.setTextAlignment(Qt.AlignCenter)
                products_table.setItem(row, 2, qty_item)
                
                subtotal = item['price'] * item['quantity']
                subtotal_item = QTableWidgetItem(f"{subtotal:,.0f} đ")
                subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                subtotal_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                products_table.setItem(row, 3, subtotal_item)
            
            layout.addWidget(products_table)
            
            total_frame = QFrame()
            total_frame.setStyleSheet("background-color: #2ecc71; border-radius: 10px; padding: 15px;")
            total_layout = QHBoxLayout(total_frame)
            
            total_label = QLabel("TỔNG CỘNG:")
            total_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
            total_label.setStyleSheet("color: white; border: none; background: transparent;")
            
            total_value = QLabel(f"{order['total']:,.0f} đ")
            total_value.setFont(QFont("Segoe UI", 18, QFont.Bold))
            total_value.setStyleSheet("color: white; border: none; background: transparent;")
            total_value.setAlignment(Qt.AlignRight)
            
            total_layout.addWidget(total_label)
            total_layout.addStretch()
            total_layout.addWidget(total_value)
            
            layout.addWidget(total_frame)
            
            button_box = QDialogButtonBox(QDialogButtonBox.Close)
            button_box.rejected.connect(detail_dialog.reject)
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
            
            detail_dialog.exec()