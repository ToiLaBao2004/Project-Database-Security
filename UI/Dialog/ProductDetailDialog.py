from PySide6.QtWidgets import (
    QWidget, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QMessageBox, QGridLayout, QScrollArea, QLineEdit, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from BAL.ProductService import ProductService
from models.ProductModel import ProductModel
import shutil
import os  # Added for path handling

class ProductDetailDialog(QDialog):
    def __init__(self, product_data, oracle_exec, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.is_editing = False
        self.value_widgets = {}
        self.image_path = None  # Store selected image path
        self.oracle_exec = oracle_exec
        self.setWindowTitle(f"Chi Tiết Sản Phẩm - {product_data.get('NAME', 'N/A')}")
        self.setMinimumSize(800, 600)
        self.init_ui()
        self.load_initial_image()  # Load initial image after UI is set up

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
        name_label = QLabel(self.product_data.get('NAME', 'N/A'))
        name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        name_label.setStyleSheet("color: white; background: transparent;")
        
        category_label = QLabel(f"🏷️ {self.product_data.get('CATEGORYID', 'N/A')}")
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

        # Add image preview section at the top
        image_label = QLabel("Hình Ảnh Sản Phẩm:")
        image_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        image_label.setStyleSheet("color: #34495e; border: none;")
        
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
        self.btn_upload = QPushButton("📁 Chọn Ảnh")
        self.btn_upload.setFixedSize(120, 35)
        self.btn_upload.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.btn_upload.setCursor(Qt.PointingHandCursor)
        self.btn_upload.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.btn_upload.clicked.connect(self.select_image)
        self.btn_upload.setEnabled(False)  # Disabled until edit mode
        
        # Image section layout
        image_section = QHBoxLayout()
        image_section.addWidget(image_container)
        image_section.addSpacing(15)
        
        upload_layout = QVBoxLayout()
        upload_layout.addWidget(self.btn_upload)
        upload_layout.addStretch()
        image_section.addLayout(upload_layout)
        image_section.addStretch()
        
        grid.addWidget(image_label, 0, 0, Qt.AlignTop)
        grid.addLayout(image_section, 0, 1)

        # Define fields to display - sử dụng đúng key từ product_data
        fields = [
            ("🆔 ID:", "ID"),
            ("📦 Tên Sản Phẩm:", "NAME"),
            ("🖼️ Đường Dẫn Ảnh:", "IMAGE"),
            ("💰 Giá:", "UNITPRICE"),
            ("📊 Số Lượng:", "STOCKQUANTITY"),
            ("🏷️ Danh Mục ID:", "CATEGORYID"),
            ("🏢 Thương Hiệu ID:", "BRANDID"),
            ("✅ Trạng Thái:", "ACTIVE"),
        ]

        row = 1  # Start from row 1 since row 0 is for image
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

    def load_initial_image(self):
        """Load initial image from product_data['IMAGE'] if available"""
        image_key = self.product_data.get('IMAGE', None)
        if image_key and image_key != 'N/A':
            script_dir = os.path.dirname(os.path.abspath(__file__))
            #lùi về 1 thư mục để đến thư mục gốc
            script_dir = os.path.dirname(script_dir)
            images_dir = os.path.join(script_dir, 'images')
            image_path = os.path.join(images_dir, image_key)
            # Check if file exists
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        180, 180,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self.image_preview.setPixmap(scaled_pixmap)
                    self.image_preview.setStyleSheet("border: none; background: transparent;")
                    self.image_path = image_path  # Store absolute path
                else:
                    self.image_preview.setText("📷\nKhông thể tải hình ảnh")
                    QMessageBox.warning(self, "Lỗi", f"Không thể tải hình ảnh từ đường dẫn: {image_path}")
            else:
                self.image_preview.setText("📷\nFile không tồn tại")
                QMessageBox.warning(self, "Lỗi", f"File không tồn tại tại đường dẫn: {image_path}")

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
                
                # Update IMAGE field with filename (assuming it will be copied to images/ later)
                filename = os.path.basename(file_path)
                if 'IMAGE' in self.value_widgets:
                    self.value_widgets['IMAGE'].setText(filename)
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể tải hình ảnh!")

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
            
            # Enable upload button
            self.btn_upload.setEnabled(True)
            
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
            
            # Disable upload button
            self.btn_upload.setEnabled(False)
            
            # Make fields read-only and save data
            for key, widget in self.value_widgets.items():
                widget.setReadOnly(True)
                self.product_data[key] = widget.text()
            
            # Call ProductService to update product
            try:
                productService = ProductService(self.oracle_exec)
                
                # Save new image to images folder if selected
                if self.image_path:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    script_dir = os.path.dirname(script_dir)
                    images_dir = os.path.join(script_dir, 'images')
                    os.makedirs(images_dir, exist_ok=True)
                    
                    filename = os.path.basename(self.image_path)
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    dest_path = os.path.join(images_dir, filename)
                    
                    # Avoid overwriting existing files
                    while os.path.exists(dest_path):
                        new_filename = f"{base}_{counter}{ext}"
                        dest_path = os.path.join(images_dir, new_filename)
                        filename = new_filename
                        counter += 1
                    
                    try:
                        shutil.copy2(self.image_path, dest_path)
                        self.product_data['IMAGE'] = filename
                    except Exception as e:
                        QMessageBox.warning(self, "Lỗi Lưu Ảnh", f"Không thể lưu hình ảnh: {str(e)}")
                
                # Parse ACTIVE field (handle boolean/int values)
                active_value = self.product_data['ACTIVE'].strip().lower()
                active = 1 if active_value in ('1', 'true', 'yes') else 0
                
                product = ProductModel(id=int(self.product_data['ID']),
                                       name=self.product_data['NAME'],
                                       image=self.product_data['IMAGE'],
                                       unit_price=float(self.product_data['UNITPRICE']),
                                       stock_quantity=int(self.product_data['STOCKQUANTITY']),
                                       category_id=int(self.product_data['CATEGORYID']),
                                       brand_id=int(self.product_data['BRANDID']),
                                       active=active)
                productService.update_product(product)
                
                QMessageBox.information(
                    self,
                    "Thành Công",
                    "Thông tin sản phẩm đã được cập nhật!"
                )
            except ValueError as e:
                QMessageBox.critical(
                    self,
                    "Lỗi Dữ Liệu",
                    f"Vui lòng kiểm tra dữ liệu:\n- Giá phải là số\n- Số lượng phải là số nguyên\n- ID danh mục/thương hiệu phải là số nguyên\n\nLỗi: {str(e)}"
                )
                self.is_editing = True
                self.toggle_edit_mode()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Lỗi",
                    f"Không thể cập nhật sản phẩm: {str(e)}"
                )
                # Restore editing mode if save fails
                self.is_editing = True
                self.toggle_edit_mode()