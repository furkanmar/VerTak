from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

class CompanyCreateDialog(QDialog):
    def __init__(self, parent=None, on_submit_callback=None, initial_data=None):
        super().__init__(parent)
        self.setWindowTitle("Şirket Bilgilerini Güncelle" if initial_data else "Yeni Şirket Ekle")
        self.setMinimumWidth(400)
        self.on_submit_callback = on_submit_callback
        self.initial_data = initial_data  # dict: {'company_name':..., 'tax_no':..., 'representer':...}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.name_input = QLineEdit()
        self.tax_input = QLineEdit()
        self.rep_input = QLineEdit()

        layout.addWidget(QLabel("Şirket Adı *"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Vergi No"))
        layout.addWidget(self.tax_input)
        layout.addWidget(QLabel("Şirket Temsilcisi"))
        layout.addWidget(self.rep_input)

        # Butonlar
        button_box = QHBoxLayout()
        self.btn_cancel = QPushButton("İptal")
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_submit = QPushButton("Kaydet" if self.initial_data else "Ekle")
        self.btn_submit.clicked.connect(self.submit_form)
        self.btn_submit.setCursor(Qt.PointingHandCursor)
        button_box.addWidget(self.btn_cancel)
        button_box.addWidget(self.btn_submit)
        layout.addLayout(button_box)

        self.setLayout(layout)

        # Eğer düzenleme yapılıyorsa inputları doldur
        if self.initial_data:
            self.name_input.setText(self.initial_data['company_name'])
            self.tax_input.setText(self.initial_data.get('tax_no', ''))
            self.rep_input.setText(self.initial_data.get('representer', ''))


    def submit_form(self):
        company_name = self.name_input.text().strip()

        if not company_name:
            QMessageBox.warning(self, "Hata", "Şirket adı zorunludur.")
            return

        tax_no = self.tax_input.text().strip()
        representer = self.rep_input.text().strip()

        if self.on_submit_callback:
            result = self.on_submit_callback(company_name, tax_no, representer)

            # Sadece gerçekten True dönerse kapat
            if result is True:
                self.accept()

