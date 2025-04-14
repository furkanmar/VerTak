from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from view.base.viewer import BaseFormWithPreview  # <- senin dosya yoluna göre ayarla
import config as c

class BillViewer(QDialog, BaseFormWithPreview):
    def __init__(self, bill_bytes, parent=None):
        QDialog.__init__(self, parent)              # → QDialog kendi parent argümanını alır
        BaseFormWithPreview.__init__(self)          # → Sadece self alır
        self.setWindowTitle("Fatura Önizleme")
        self.resize(1000, 800)

        self.bill_bytes = bill_bytes
        self.init_ui()
        self.load_bill()

    def init_ui(self):
        self.preview_label, self.page_info, zoom_in, zoom_out, prev_page, next_page = self.get_preview_widgets()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.preview_label)

        nav = QHBoxLayout()
        prev_btn = QToolButton(); prev_btn.setText("←"); prev_btn.clicked.connect(prev_page)
        next_btn = QToolButton(); next_btn.setText("→"); next_btn.clicked.connect(next_page)
        zoom_out_btn = QToolButton(); zoom_out_btn.setText("–"); zoom_out_btn.clicked.connect(zoom_out)
        zoom_in_btn = QToolButton(); zoom_in_btn.setText("+"); zoom_in_btn.clicked.connect(zoom_in)

        nav.addWidget(prev_btn)
        nav.addWidget(self.page_info)
        nav.addWidget(next_btn)
        nav.addStretch()
        nav.addWidget(zoom_out_btn)
        nav.addWidget(QLabel("Zoom"))
        nav.addWidget(zoom_in_btn)

        layout = QVBoxLayout()
        layout.addWidget(scroll)
        layout.addLayout(nav)
        self.setLayout(layout)

    def load_bill(self):
        if self.bill_bytes[:4] == b'%PDF':
            self.is_pdf = True
            self.pdf_images = self._load_pdf_from_bytes(self.bill_bytes)
            self.current_pdf_page = 0
            self.zoom_level = 0.4
            self.update_pdf_viewer()
        else:
            try:
                self.is_pdf = False
                self.image_data = self._load_image_from_bytes(self.bill_bytes)
                self.zoom_level = 0.4
                self.update_image_viewer()
            except Exception as e:
                self.preview_label.setText(f"Görsel hata: {str(e)}")

    def _load_pdf_from_bytes(self, byte_data):
        from pdf2image import convert_from_bytes
        return convert_from_bytes(byte_data, dpi=150, poppler_path=c.get_poppler_path())

    def _load_image_from_bytes(self, byte_data):
        import tempfile
        from PIL import Image
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_file.write(byte_data)
        temp_file.close()
        return Image.open(temp_file.name)
