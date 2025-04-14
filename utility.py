
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDesktopWidget,QInputDialog,QLabel,QVBoxLayout
from PyQt5.QtCore import Qt
def create_horizontal_line():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)         
    line.setFrameShadow(QFrame.Sunken)             
    line.setLineWidth(1)
    return line

def get_current_date():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")

def create_styled_lineedit(placeholder="", height=38, font_size=14):
    line_edit = QLineEdit()
    line_edit.setPlaceholderText(placeholder)
    line_edit.setFixedHeight(height)
    line_edit.setStyleSheet(f"""
        font-size: {font_size}px;
        padding: 6px 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    """)
    return line_edit

def create_password_lineedit(placeholder="", height=38, font_size=14):
    line_edit = create_styled_lineedit(placeholder, height, font_size)
    line_edit.setEchoMode(QLineEdit.Password)
    return line_edit

def create_bold_header_label(text, font_size=16):
    title_box=QVBoxLayout()
    title_label = QLabel(text)
    title_label.setAlignment(Qt.AlignLeft)
    title_label.setStyleSheet(f"""font-weight: bold; font-size: {font_size}px;""")
    title_label_underline = create_horizontal_line()
    title_box.addWidget(title_label)
    title_box.addWidget(title_label_underline)
    return title_box

def set_responsive_window(window, width_ratio=0.7, height_ratio=0.75):
    """
    Verilen pencereyi ekranın ortasına yerleştirir ve belirtilen oranlarda boyutlandırır.
    :param window: QMainWindow veya QWidget
    :param width_ratio: Ekran genişliğine göre pencere genişlik oranı (varsayılan 0.7)
    :param height_ratio: Ekran yüksekliğine göre pencere yükseklik oranı (varsayılan 0.75)
    """
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()

    window_width = int(screen_width * width_ratio)
    window_height = int(screen_height * height_ratio)

    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)

    window.setGeometry(x, y, window_width, window_height)

def get_login_credentials(parent=None):
    username, ok1 = QInputDialog.getText(parent, "Kimlik Doğrulama", "Kullanıcı adınızı girin:")
    if not ok1 or not username:
        return None, None

    password, ok2 = QInputDialog.getText(parent, "Kimlik Doğrulama", "Şifrenizi girin:", QLineEdit.Password)
    if not ok2 or not password:
        return None, None

    return username, password

def center_and_resize_dialog(dialog, width_ratio=0.5, height_ratio=0.6):
    screen = QDesktopWidget().availableGeometry()  # Ekranda kullanılabilir alan
    screen_width = screen.width()
    screen_height = screen.height()

    window_width = int(screen_width * width_ratio)
    window_height = int(screen_height * height_ratio)

    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)

    dialog.setGeometry(x, y, window_width, window_height)
