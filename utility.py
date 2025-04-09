
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLineEdit

def create_horizontal_line():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)         
    line.setFrameShadow(QFrame.Sunken)             
    line.setLineWidth(2)
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
