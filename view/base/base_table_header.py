from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
import utility

class BaseTableHeaderSection:
    def create_table_header(
        self,
        title: str,
        back_btn_text: str = "← Geri",
        right_btn_text: str = None,
        return_right_button: bool = True  
    ):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        vbox_title= QVBoxLayout()
        title_label = QLabel(f"🗂️ {title}")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        vbox_title.addWidget(title_label, alignment=Qt.AlignCenter)

        # Üst düğme kutusu
        hbox_top = QHBoxLayout()
        self.back_button = QPushButton(back_btn_text)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setFixedHeight(36)
        self.back_button.setStyleSheet("font-size: 14px; padding: 6px 12px;")

        hbox_top.addWidget(self.back_button, alignment=Qt.AlignLeft)
        right_button_instance = None
        if right_btn_text and return_right_button:
            right_button_instance = QPushButton(right_btn_text)
            right_button_instance.setCursor(Qt.PointingHandCursor)
            right_button_instance.setFixedHeight(36)
            right_button_instance.setStyleSheet("font-size: 14px; padding: 6px 12px;")
            hbox_top.addWidget(right_button_instance, alignment=Qt.AlignRight)

        layout.addLayout(vbox_title)
        layout.addLayout(hbox_top)
        layout.addWidget(utility.create_horizontal_line())

        return layout, self.back_button, right_button_instance
