from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout, QPushButton, QLineEdit
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import config as c  
from utility import create_styled_lineedit, create_password_lineedit


class LoginView(QWidget):
    def __init__(self, on_submit_callback=None):
        super().__init__()
        self.on_submit_callback = on_submit_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(15)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(c.LOGO_PATH)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaledToWidth(150, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

        # Başlık
        title = QLabel("Veresiye Takip Sistemi")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Açıklama
        subtitle = QLabel("Lütfen giriş bilgilerinizi giriniz")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: gray; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        # Form
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(10, 10, 10, 10)
        self.form_layout.setSpacing(12)

        self.username = create_styled_lineedit("Kullanıcı Adı")
        self.password = create_password_lineedit("Şifre")
        self.password.setEchoMode(QLineEdit.Password)

        self.form_layout.addRow(QLabel("ID:"), self.username)
        self.form_layout.addRow(QLabel("Şifre:"), self.password)

        self.enter_button = QPushButton("Giriş Yap")
        self.enter_button.setStyleSheet("font-size: 16px; padding: 8px 20px;")
        self.enter_button.setCursor(Qt.PointingHandCursor)
        self.enter_button.clicked.connect(self.submit)
        self.enter_button.setDefault(True)  

        self.form_layout.addRow(self.enter_button)

        self.alert = QLabel("")
        self.alert.setStyleSheet("color: red; font-size: 13px;")
        self.alert.setVisible(False)
        self.form_layout.addRow(self.alert)

        self.form = QWidget()
        self.form.setLayout(self.form_layout)

        layout.addWidget(self.form, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def submit(self):
        if self.on_submit_callback:
            self.on_submit_callback(self.username.text(), self.password.text())

    def show_alert(self, message: str):
        self.alert.setText(message)
        self.alert.setVisible(True)

    def clear(self):
        self.username.clear()
        self.password.clear()
        self.alert.setVisible(False)
    
