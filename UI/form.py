import sys
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from BAL.employee_service import get_current_user_info

class OracleApp(QDialog):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.conn = conn
        self.setWindowTitle("User info")
        self.resize(650, 300)

        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True) 
        layout.addWidget(self.table)

    def load_data(self):
        try:
            columns, rows = get_current_user_info(self.conn)

            self.table.setColumnCount(len(columns))
            self.table.setHorizontalHeaderLabels(columns)
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch) 

            self.table.setRowCount(0)

            self.table.setRowCount(len(rows))
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value)) 
                    self.table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        event.accept() 