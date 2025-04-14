from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from utility import create_styled_lineedit, create_bold_header_label


class TableFilterBar(QWidget):
    filter_changed = pyqtSignal(int, str)  # (column_index, filter_text)

    def __init__(self, headers: list[str], parent=None):
        super().__init__(parent)
        self.inputs = {}  

        layout = QVBoxLayout()
        header_label = create_bold_header_label("Filtreleme Seçenekleri")
        layout.addLayout(header_label)

        filters = QHBoxLayout()
        filters.setSpacing(10)
        filters.setContentsMargins(0, 0, 0, 0)

        for index, header in enumerate(headers):
            input_field = create_styled_lineedit(f"{header} filtresi")
            input_field.textChanged.connect(lambda text, idx=index: self.filter_changed.emit(idx+1, text))
            self.inputs[index] = input_field
            filters.addWidget(input_field)

        # 🔴 Filtreleri Sıfırla butonu ekle
        reset_button = QPushButton("Filtreleri Sıfırla")
        reset_button.setStyleSheet("""
            QPushButton {
                padding: 12px 12px;
                background-color: #d9534f;
                color: white;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        reset_button.setFixedHeight(38)

        reset_button.setCursor(Qt.PointingHandCursor)
        reset_button.clicked.connect(self.clear_all_inputs)
        filters.addStretch()
        filters.addWidget(reset_button)

        layout.addLayout(filters)
        self.setLayout(layout)

    def clear_all_inputs(self):
        for col_index, input_field in self.inputs.items():
            input_field.blockSignals(True)     
            input_field.clear()                
            input_field.blockSignals(False)    
            self.filter_changed.emit(col_index+1, "")
