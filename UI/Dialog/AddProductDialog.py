from PySide6.QtWidgets import (
    QWidget, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QMessageBox, QGridLayout, QScrollArea, QLineEdit, QFileDialog, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
import os
import shutil
from BAL.ProductService import ProductService
from models.ProductModel import ProductModel

class AddProductDialog(QDialog):
    def __init__(self, oracleExec, parent=None):
        super().__init__(parent)
        self.oracleExec = oracleExec
        self.setWindowTitle("Thêm Sản Phẩm Mới")
        self.setMinimumSize(700, 600)
        self.input_fields = {}
        self.image_path = None
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

        # Image upload section
        image_label = QLabel("🖼️ Hình Ảnh:")
        image_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        image_label.setStyleSheet("color: #34495e;")
        image_label.setMinimumWidth(150)
        
        # Image preview container
        image_container = QFrame()
        image_container.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px dashed #bdc3c7;
                border-radius: 8px;
            }
        """)
        image_container.setFixedSize(200, 200)
        
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(10, 10, 10, 10)
        
        self.image_preview = QLabel("📷\nChưa có hình ảnh")
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setFont(QFont("Segoe UI", 10))
        self.image_preview.setStyleSheet("color: #7f8c8d; border: none; background: transparent;")
        self.image_preview.setScaledContents(False)
        
        image_layout.addWidget(self.image_preview)
        
        # Upload button
        btn_upload = QPushButton("📁 Chọn Ảnh")
        btn_upload.setFixedSize(120, 35)
        btn_upload.setFont(QFont("Segoe UI", 9, QFont.Bold))
        btn_upload.setCursor(Qt.PointingHandCursor)
        btn_upload.setStyleSheet("""
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
        btn_upload.clicked.connect(self.select_image)
        
        # Image section layout
        image_section = QHBoxLayout()
        image_section.addWidget(image_container)
        image_section.addSpacing(15)
        
        upload_layout = QVBoxLayout()
        upload_layout.addWidget(btn_upload)
        upload_layout.addStretch()
        image_section.addLayout(upload_layout)
        image_section.addStretch()
        
        grid.addWidget(image_label, 0, 0, Qt.AlignTop)
        grid.addLayout(image_section, 0, 1)

        fields = [
            ("📦 Tên Sản Phẩm:", "name", "Nhập tên sản phẩm", "text"),
            ("🏷️ Danh Mục ID:", "categoryId", "Nhập ID danh mục", "text"),
            ("💰 Giá:", "unitPrice", "Nhập giá (VND)", "text"),
            ("📊 Số Lượng:", "stockQuantity", "Nhập số lượng", "text"),
            ("🏢 Thương Hiệu ID:", "brandId", "Nhập ID thương hiệu", "text"),
            ("✅ Trạng Thái:", "active", "", "combo"),
        ]

        row = 1
        for label_text, key, placeholder, field_type in fields:
            # Label
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            label.setStyleSheet("color: #34495e;")
            label.setMinimumWidth(150)

            # Input field
            if field_type == "combo":
                input_field = QComboBox()
                input_field.addItems(["True", "False"])
                input_field.setCurrentText("True")  # Default active
                input_field.setFont(QFont("Segoe UI", 10))
                input_field.setFixedHeight(40)
                input_field.setStyleSheet("""
                    QComboBox {
                        color: #2c3e50;
                        background-color: white;
                        padding: 8px 12px;
                        border-radius: 5px;
                        border: 2px solid #e0e6ed;
                    }
                    QComboBox:focus {
                        border: 2px solid #e67e22;
                    }
                    QComboBox::drop-down {
                        border: none;
                    }
                    QComboBox::down-arrow {
                        image: url(down_arrow.png);
                        width: 12px;
                        height: 12px;
                    }
                """)
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
        btn_save.clicked.connect(self.validate_and_create)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(btn_save)

        # ================= MAIN LAYOUT =================
        main_layout.addWidget(header_frame)
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(btn_layout)

    def select_image(self):
        """Open file dialog to select image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn Hình Ảnh Sản Phẩm",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        
        if file_path:
            self.image_path = file_path
            # Update image preview
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    180, 180,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_preview.setPixmap(scaled_pixmap)
                self.image_preview.setStyleSheet("border: none; background: transparent;")
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể tải hình ảnh!")

    def save_selected_image(self):
        """Save the selected image to the images folder"""
        if not self.image_path:
            return
        
        # Create images folder if it doesn't exist
        images_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
        os.makedirs(images_dir, exist_ok=True)
        
        # Get product name for filename
        product_name = self.input_fields["name"].text().strip()
        if not product_name:
            return
        
        # Get file extension
        _, ext = os.path.splitext(self.image_path)
        
        # Create filename: product_name + ext
        filename = f"{product_name}{ext}"
        dest_path = os.path.join(images_dir, filename)
        
        try:
            shutil.copy2(self.image_path, dest_path)
            # Update image_path to the new filename (relative)
            self.image_path = filename
        except Exception as e:
            QMessageBox.warning(self, "Lỗi Lưu Ảnh", f"Không thể lưu hình ảnh: {str(e)}")

    def validate_and_create(self):
        """Validate form and accept if valid"""
        # Check if required fields are filled
        required_fields = ["name", "categoryId", "unitPrice", "stockQuantity", "brandId", "active"]
        
        for field in required_fields:
            if field == "active":
                value = self.input_fields[field].currentText()
            else:
                value = self.input_fields[field].text().strip()
            
            if not value:
                QMessageBox.warning(
                    self,
                    "Thiếu Thông Tin",
                    f"Vui lòng điền đầy đủ thông tin: {field}"
                )
                self.input_fields[field].setFocus()
                return
        
        # Validate numeric fields
        try:
            unitPrice = self.input_fields["unitPrice"].text().strip().replace(",", "")
            stockQuantity = self.input_fields["stockQuantity"].text().strip()
            categoryId = self.input_fields["categoryId"].text().strip()
            brandId = self.input_fields["brandId"].text().strip()
            
            float(unitPrice)
            int(stockQuantity)
            int(categoryId)
            int(brandId)
        except ValueError:
            QMessageBox.warning(
                self,
                "Lỗi Định Dạng",
                "Giá, Số lượng, Danh mục ID và Thương hiệu ID phải là số!"
            )
            return
        
        # If all valid, save image if selected and accept
        if self.image_path:
            self.save_selected_image()
        
        self.accept()
        
        product_data = self.get_product_data()
        try:
            product = ProductModel(
                id=0,  # Will be set by sequence
                name=product_data["name"],
                image=product_data["image"],
                unit_price=int(float(product_data["unitPrice"].replace(",", ""))),
                stock_quantity=int(product_data["stockQuantity"]),
                category_id=int(product_data["categoryId"]),
                brand_id=int(product_data["brandId"]),
                active=product_data["active"].lower() == "true"
            )
            
            service = ProductService(self.oracleExec)
            service.create_product(product)
            
            QMessageBox.information(self, "Thành Công", f"Đã thêm sản phẩm '{product_data['name']}' thành công!")
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm sản phẩm: {str(e)}")
        
    def get_product_data(self):
        """Get product data from form"""
        data = {}
        for key, field in self.input_fields.items():
            if isinstance(field, QComboBox):
                data[key] = field.currentText()
            else:
                data[key] = field.text().strip()
        data['image'] = self.image_path if self.image_path else ""
        return data