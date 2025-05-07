from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QLabel,QLineEdit,  QPushButton, QFormLayout)
from PyQt5.QtCore import Qt
from services import user_service as us
from PyQt5.QtGui import QPixmap
import config as c
from view.login_view import LoginView

from utility import create_styled_lineedit, create_password_lineedit  # varsa özel parola alanı

class LoginScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.init_ui()

        
    def init_ui(self):
        layout = QVBoxLayout()
        self.login_form = LoginView(on_submit_callback=self.check_login)
        layout.addWidget(self.login_form)
        self.setLayout(layout)

    def check_login(self, username, password):
        if username and password:
            user = us.check_log_info(username=username, password=password)
            if user:
                print("Giriş başarılı")
                self.login_form.clear()
                self.main_window.switch_to_company_scene()
            else:
                self.login_form.show_alert("Kullanıcı adı veya şifre hatalı!!")
        else:
            self.login_form.show_alert("Kullanıcı adı ve şifrenizi giriniz!")

