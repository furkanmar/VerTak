from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QLabel,QLineEdit,  QPushButton, QFormLayout)
from PyQt5.QtCore import Qt
from services import user_service as us

class LoginScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(20)

        # Başlıklar
        title = QLabel("Veresiye Takip Sistemi")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        subtitle = QLabel("Lütfen giriş bilgilerinizi giriniz")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: gray;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Form düzeni
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(20, 20, 20, 20)
        self.form_layout.setSpacing(15)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Kullanıcı Adı")
        self.username.setFixedHeight(35)
        self.username.setStyleSheet("font-size: 16px; padding: 5px;")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Şifre")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedHeight(35)
        self.password.setStyleSheet("font-size: 16px; padding: 5px;")

        self.form_layout.addRow(QLabel("ID:"), self.username)
        self.form_layout.addRow(QLabel("Şifre:"), self.password)

        self.enter_button = QPushButton("Giriş Yap")
        self.enter_button.clicked.connect(self.enter)
        self.enter_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.enter_button.setCursor(Qt.PointingHandCursor)
        self.form_layout.addRow(self.enter_button)

        self.alert = QLabel("")
        self.alert.setStyleSheet("color: red; font-size: 14px;")
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
