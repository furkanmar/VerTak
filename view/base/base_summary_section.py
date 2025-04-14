# view/base/table_summary_buttons_mixin.py
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class TableSummaryButtonsMixin:
    def create_summary_and_buttons(self):
        outer_layout = QVBoxLayout()

        # Toplamlar
        summary_layout = QHBoxLayout()

        def create_summary(title_text):
            vbox = QVBoxLayout()
            title = QLabel(title_text)
            title.setStyleSheet("font-weight: bold; font-size: 13px;")
            label = QLabel("")
            label.setFont(QFont("Arial", 20, QFont.Bold))
            vbox.addWidget(title)
            vbox.addWidget(label)
            return vbox, label

        vbox_credit, self.label_credit_value = create_summary("Toplam Alacak")
        vbox_debit, self.label_debit_value = create_summary("Toplam Borç")
        vbox_net, self.label_net_value = create_summary("Net Durum")

        summary_layout.addLayout(vbox_credit)
        summary_layout.addLayout(vbox_debit)
        summary_layout.addLayout(vbox_net)

        outer_layout.addLayout(summary_layout)

        # Alt Butonlar
        button_layout = QHBoxLayout()
        button_style = "font-size: 14px; padding: 10px 20px;"

        self.btn_edit = QPushButton("📝 Düzenle")
        self.btn_edit.setStyleSheet(button_style)
        self.btn_edit.setCursor(Qt.PointingHandCursor)

        self.btn_delete = QPushButton("🗑️ Sil")
        self.btn_delete.setStyleSheet(button_style)
        self.btn_delete.setCursor(Qt.PointingHandCursor)

        self.btn_create = QPushButton("➕ Ekle")
        self.btn_create.setStyleSheet(button_style)
        self.btn_create.setCursor(Qt.PointingHandCursor)

        button_layout.addWidget(self.btn_edit)
        button_layout.addWidget(self.btn_delete)
        button_layout.addWidget(self.btn_create)

        outer_layout.addLayout(button_layout)

        return outer_layout
