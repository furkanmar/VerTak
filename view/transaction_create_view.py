from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCalendarWidget, QTimeEdit,
    QComboBox, QScrollArea, QWidget, QToolButton
)
from PyQt5.QtCore import Qt, QDateTime
from utility import create_styled_lineedit

class TransactionFormUI:
    def __init__(self, parent):
        self.parent = parent
        self.layout = self.create_layout()

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; font-size: 13px;")
        return label

    def create_layout(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)

        # === SOL PANEL ===
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        left_layout.setContentsMargins(20, 20, 20, 20)

        left_layout.addWidget(self.create_label("Tarih"))
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setSelectedDate(QDateTime.currentDateTime().date())
        left_layout.addWidget(self.calendar_widget)

        left_layout.addWidget(self.create_label("Saat"))
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(QDateTime.currentDateTime().time())
        self.time_edit.setStyleSheet("font-size: 14px; padding: 6px 10px; border: 1px solid #ccc; border-radius: 5px;")
        left_layout.addWidget(self.time_edit)

        left_layout.addWidget(self.create_label("Açıklama"))
        self.explanation_input = create_styled_lineedit("Açıklama")
        left_layout.addWidget(self.explanation_input)

        left_layout.addWidget(self.create_label("Alacak Tutarı *"))
        self.credit_input = create_styled_lineedit("0")
        left_layout.addWidget(self.credit_input)

        left_layout.addWidget(self.create_label("Borç Tutarı *"))
        self.debit_input = create_styled_lineedit("0")
        left_layout.addWidget(self.debit_input)

        left_layout.addWidget(self.create_label("Ödeme Türü"))
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Çek", "Nakit", "Kredi Kartı", "Havale"])
        self.payment_combo.setStyleSheet("padding: 6px; font-size: 13px;")
        left_layout.addWidget(self.payment_combo)

        left_layout.addWidget(self.create_label("Fatura Ekle"))
        bill_layout = QHBoxLayout()
        self.bill_button = QPushButton("Fatura Seç")
        self.bill_button.setCursor(Qt.PointingHandCursor)
        self.bill_button.clicked.connect(self.parent.select_bill_file)
        self.bill_button.setStyleSheet("padding: 8px 16px; font-size: 14px;")

        self.bill_label = QLabel("Hiçbir dosya seçilmedi")
        self.bill_label.setStyleSheet("font-style: italic; color: gray")

        bill_layout.addWidget(self.bill_button)
        bill_layout.addWidget(self.bill_label)
        left_layout.addLayout(bill_layout)

        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("İptal")
        cancel_btn.clicked.connect(self.parent.reject)
        save_btn = QPushButton("Ekle")
        save_btn.clicked.connect(self.parent.submit_form)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setDefault(True)

        for btn in [cancel_btn, save_btn]:
            btn.setStyleSheet("padding: 8px 16px; font-size: 14px;")

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        left_layout.addLayout(button_layout)

        # === SAĞ PANEL ===
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Fatura Önizlemesi"))
        self.preview_label, self.page_info, zoom_in, zoom_out, prev_page, next_page = self.parent.get_preview_widgets()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.preview_label)
        right_layout.addWidget(scroll_area, stretch=9)

        nav_layout = QHBoxLayout()
        prev_btn = QToolButton(); prev_btn.setText("←"); prev_btn.clicked.connect(prev_page)
        next_btn = QToolButton(); next_btn.setText("→"); next_btn.clicked.connect(next_page)
        nav_layout.addWidget(prev_btn)
        nav_layout.addWidget(self.page_info)
        nav_layout.addWidget(next_btn)
        right_layout.addLayout(nav_layout)

        zoom_layout = QHBoxLayout()
        zoom_out_btn = QToolButton(); zoom_out_btn.setText("–"); zoom_out_btn.clicked.connect(zoom_out)
        zoom_in_btn = QToolButton(); zoom_in_btn.setText("+"); zoom_in_btn.clicked.connect(zoom_in)
        zoom_layout.addWidget(zoom_out_btn)
        zoom_layout.addWidget(QLabel("Zoom"))
        zoom_layout.addWidget(zoom_in_btn)
        right_layout.addLayout(zoom_layout)

        main_layout.addLayout(left_layout, stretch=2)
        main_layout.addLayout(right_layout, stretch=3)

        scroll_container = QWidget()
        scroll_container.setLayout(main_layout)

        full_scroll_area = QScrollArea()
        full_scroll_area.setWidgetResizable(True)
        full_scroll_area.setWidget(scroll_container)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(full_scroll_area)

        return outer_layout
