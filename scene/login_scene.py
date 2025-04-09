from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QLabel,QLineEdit,  QPushButton, QFormLayout)
from PyQt5.QtCore import Qt
from services import user_service as us
from PyQt5.QtGui import QPixmap
import config as c

from utility import create_styled_lineedit, create_password_lineedit  # varsa özel parola alanı

class LoginScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        


    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(15)  # spacing düşürüldü

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(c.LOGO_PATH)
        logo_label.setPixmap(pixmap)
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

        # Daha kompakt ve margin içeren açıklama
        subtitle = QLabel("Lütfen giriş bilgilerinizi giriniz")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: gray; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        # Form düzeni
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(10, 10, 10, 10)
        self.form_layout.setSpacing(12)

        self.username = create_styled_lineedit("Kullanıcı Adı")
        self.password = create_password_lineedit("Şifre")
        self.password.setEchoMode(QLineEdit.Password)

        self.form_layout.addRow(QLabel("ID:"), self.username)
        self.form_layout.addRow(QLabel("Şifre:"), self.password)

        self.enter_button = QPushButton("Giriş Yap")
        self.enter_button.clicked.connect(self.enter)
        self.enter_button.setStyleSheet("font-size: 16px; padding: 8px 20px;")
        self.enter_button.setCursor(Qt.PointingHandCursor)
        self.form_layout.addRow(self.enter_button)

        self.alert = QLabel("")
        self.alert.setStyleSheet("color: red; font-size: 13px;")
        self.alert.setVisible(False)
        self.form_layout.addRow(self.alert)

        self.form = QWidget()
        self.form.setLayout(self.form_layout)

        layout.addWidget(self.form, alignment=Qt.AlignCenter)
        self.setLayout(layout)



    def enter(self):
        username=self.username.text()
        password=self.password.text()
        if username !='' and  password !='':
            username=us.check_log_info(username=username, password=password)


            if username:
                print("Giriş başarılı")
                self.main_window.switch_to_company_scene()

            else: 
                self.alert.setText("Kullanıcı adı veya şifre hatalı!!")
                self.alert.setVisible(True)
        else:
            self.alert.setText("Kullanıcı adı ve şifrenizi giriniz!")
            self.alert.setVisible(True)
