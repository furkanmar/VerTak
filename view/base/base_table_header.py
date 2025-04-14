from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
import utility

class BaseTableHeaderSection:
    def create_table_header(
        self,
        title: str,
        back_btn_text: str = "← Geri",
        right_btn_text: str = None,
    ):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Üst düğme kutusu
        hbox_top = QHBoxLayout()

        self.back_button = QPushButton(back_btn_text)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setFixedHeight(36)
        self.back_button.setStyleSheet("font-size: 14px; padding: 6px 12px;")

        hbox_top.addWidget(self.back_button, alignment=Qt.AlignLeft)

        title_label = QLabel(f"🗂️ {title}")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        hbox_top.addWidget(title_label, alignment=Qt.AlignCenter)

        self.right_button = None
        if right_btn_text:
            self.right_button = QPushButton(right_btn_text)
            self.right_button.setCursor(Qt.PointingHandCursor)
            self.right_button.setFixedHeight(36)
            self.right_button.setStyleSheet("font-size: 14px; padding: 6px 12px;")
            hbox_top.addWidget(self.right_button, alignment=Qt.AlignRight)

        layout.addLayout(hbox_top)

        layout.addWidget(utility.create_horizontal_line())

        return layout, self.back_button, self.right_button
