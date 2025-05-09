from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from utility import create_styled_lineedit, set_responsive_window

class CompanyCreateDialog(QDialog):
    def __init__(self, parent=None, on_submit_callback=None, initial_data=None):
        super().__init__(parent)
        self.setWindowTitle("Şirket Bilgilerini Güncelle" if initial_data else "Yeni Şirket Ekle")
        self.setMinimumWidth(400)
        self.on_submit_callback = on_submit_callback
        self.initial_data = initial_data  # dict: {'company_name':..., 'tax_no':..., 'representer':...}

        self.init_ui()
        set_responsive_window(self,0.3, 0.3)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Giriş alanları
        self.name_input = create_styled_lineedit("Şirket adı giriniz")
        self.tax_input = create_styled_lineedit("Vergi numarası giriniz (opsiyonel)")
        self.rep_input = create_styled_lineedit("Temsilci adı giriniz (opsiyonel)")

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

        for btn in [self.btn_cancel, self.btn_submit]:
            btn.setStyleSheet("font-size: 14px; padding: 8px 16px;")

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

        self.accept()
        
    def get_inputs(self):
        return (
            self.name_input.text().strip(),
            self.tax_input.text().strip(),
            self.rep_input.text().strip()
        )


