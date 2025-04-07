from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QToolButton, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pdf2image import convert_from_bytes
from PIL import Image
import tempfile

class BillViewer(QDialog):
    def __init__(self, bill_bytes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fatura Önizleme")
        self.resize(1000, 800)

        self.bill_bytes = bill_bytes
        self.pdf_images = []
        self.image_data = None
        self.current_page = 0
        self.zoom_level = 1.0
        self.is_pdf = False

        self.init_ui()
        self.load_bill()

    def init_ui(self):
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.preview_label)

        self.page_info = QLabel("")

        self.prev_btn = QToolButton()
        self.prev_btn.setText("←")
        self.prev_btn.clicked.connect(self.prev_page)

        self.next_btn = QToolButton()
        self.next_btn.setText("→")
        self.next_btn.clicked.connect(self.next_page)

        self.zoom_in_btn = QToolButton()
        self.zoom_in_btn.setText("+")
        self.zoom_in_btn.clicked.connect(self.zoom_in)

        self.zoom_out_btn = QToolButton()
        self.zoom_out_btn.setText("–")
        self.zoom_out_btn.clicked.connect(self.zoom_out)

        nav = QHBoxLayout()
        nav.addWidget(self.prev_btn)
        nav.addWidget(self.page_info)
        nav.addWidget(self.next_btn)
        nav.addStretch()
        nav.addWidget(self.zoom_out_btn)
        nav.addWidget(QLabel("Zoom"))
        nav.addWidget(self.zoom_in_btn)

        layout = QVBoxLayout()
        layout.addWidget(scroll)
        layout.addLayout(nav)

        self.setLayout(layout)

    def load_bill(self):
        if self.bill_bytes[:4] == b'%PDF':
            self.is_pdf = True
            self.pdf_images = convert_from_bytes(self.bill_bytes, dpi=150, poppler_path=r"c:\Users\Public\VerTak\VerTak\resources\poppler\bin")
            self.current_page = 0
            self.zoom_level = 0.4
            self.update_pdf_viewer()
        else:
            try:
                self.is_pdf = False
                # Önce geçici dosyaya yaz
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                temp_file.write(self.bill_bytes)
                temp_file.close()

                self.image_data = Image.open(temp_file.name)
                self.zoom_level = 0.4
                self.update_image_viewer()
            except Exception as e:
                self.preview_label.setText(f"Görsel hata: {str(e)}")

    def update_pdf_viewer(self):
        if not self.pdf_images:
            return
        img = self.pdf_images[self.current_page]
        self._show_image(img)
        self.page_info.setText(f"{self.current_page + 1} / {len(self.pdf_images)}")

    def update_image_viewer(self):
        if not self.image_data:
            return
        self._show_image(self.image_data)
        self.page_info.setText("Görsel")

    def _show_image(self, pil_img):
        w = int(pil_img.width * self.zoom_level)
        h = int(pil_img.height * self.zoom_level)
        resized = pil_img.resize((w, h))
        path = tempfile.mktemp(suffix=".png")
        resized.save(path)
        self.preview_label.setPixmap(QPixmap(path))

    def prev_page(self):
        if self.is_pdf and self.current_page > 0:
            self.current_page -= 1
            self.update_pdf_viewer()

    def next_page(self):
        if self.is_pdf and self.current_page < len(self.pdf_images) - 1:
            self.current_page += 1
            self.update_pdf_viewer()

    def zoom_in(self):
        self.zoom_level += 0.1
        if self.is_pdf:
            self.update_pdf_viewer()
        else:
            self.update_image_viewer()

    def zoom_out(self):
        self.zoom_level = max(0.1, self.zoom_level - 0.1)
        if self.is_pdf:
            self.update_pdf_viewer()
        else:
            self.update_image_viewer()
