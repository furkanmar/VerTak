
from PyQt5.QtWidgets import QFrame

def create_horizontal_line():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)         
    line.setFrameShadow(QFrame.Sunken)             
    line.setLineWidth(2)
    return line