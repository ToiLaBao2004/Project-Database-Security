from PySide6.QtWidgets import (
    QWidget, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QMessageBox, QGridLayout, QScrollArea, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


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
