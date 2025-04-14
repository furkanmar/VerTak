from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QCalendarWidget, QTimeEdit, QScrollArea, QToolButton, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QPixmap
from utility import create_styled_lineedit
from PIL import Image
from pdf2image import convert_from_path
import os, tempfile
import config as c
from utility import get_current_date


class BaseFormWithPreview(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_bill_path = None
        self.selected_bill_data = None
        self.pdf_images = []
        self.current_pdf_page = 0
        self.image_data = None
        self.is_pdf = False
        self.zoom_level = 0.4
        self.preview_label = QLabel()
        self.page_info = QLabel("0 / 0")

    def select_bill_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Fatura Dosyasını Seç", "",
            "Tüm Desteklenen Dosyalar (*.png *.jpg *.jpeg *.pdf);;Görseller (*.png *.jpg *.jpeg);;PDF (*.pdf);;Tüm Dosyalar (*)")

        if file_path:
            self.selected_bill_path = file_path

            if hasattr(self, "_external_bill_label"):
                self._external_bill_label(os.path.basename(file_path))  # 💡 Burada setText yerine direkt çağırıyoruz

            with open(file_path, "rb") as f:
                self.selected_bill_data = f.read()

            ext = os.path.splitext(file_path)[-1].lower()

            if ext in [".png", ".jpg", ".jpeg"]:
                self.is_pdf = False
                self.image_data = Image.open(file_path)
                self.zoom_level = 0.4
                self.update_image_viewer()

            elif ext == ".pdf":
                try:
                    self.is_pdf = True
                    poppler_path = c.get_poppler_path()
                    self.pdf_images = convert_from_path(file_path, dpi=150, poppler_path=poppler_path)
                    if self.pdf_images:
                        self.current_pdf_page = 0
                        self.zoom_level = 0.4
                        self.update_pdf_viewer()
                    else:
                        self.preview_label.setText("PDF önizlenemedi.")
                except Exception as e:
                    self.preview_label.setText(f"PDF hatası: {str(e)}")
            else:
                self.preview_label.setText("Bu dosya türü desteklenmiyor.")
        else:
            self.selected_bill_path = None
            self.selected_bill_data = None
            if hasattr(self, "_external_bill_label"):
                self._external_bill_label("Hiçbir dosya seçilmedi")
            self.preview_label.clear()

    def update_image_viewer(self):
        if self.image_data is None:
            return
        width = int(self.image_data.width * self.zoom_level)
        height = int(self.image_data.height * self.zoom_level)
        resized = self.image_data.resize((width, height))

        temp_img_path = tempfile.mktemp(suffix=".png")
        resized.save(temp_img_path, 'PNG')

        pixmap = QPixmap(temp_img_path)
        self.preview_label.setPixmap(pixmap)
        self.page_info.setText("Resim")

    def update_pdf_viewer(self):
        if not self.pdf_images:
            return

        image = self.pdf_images[self.current_pdf_page]
        width = int(image.width * self.zoom_level)
        height = int(image.height * self.zoom_level)
        image = image.resize((width, height))

        temp_img_path = tempfile.mktemp(suffix=".png")
        image.save(temp_img_path, 'PNG')

        pixmap = QPixmap(temp_img_path)
        self.preview_label.setPixmap(pixmap)
        self.page_info.setText(f"{self.current_pdf_page + 1} / {len(self.pdf_images)}")

    def prev_pdf_page(self):
        if self.current_pdf_page > 0:
            self.current_pdf_page -= 1
            self.update_pdf_viewer()

    def next_pdf_page(self):
        if self.current_pdf_page < len(self.pdf_images) - 1:
            self.current_pdf_page += 1
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

    def get_bill_data(self):
        return {
            "bill_added_date": get_current_date() if self.selected_bill_data else None,
            "bill": self.selected_bill_data
        }
    
    def set_bill_label(self, label_widget):
        self._external_bill_label = label_widget

    def load_bill_from_bytes(self, bill_bytes):
        from pdf2image import convert_from_bytes
        import tempfile
        from PIL import Image

        if bill_bytes[:4] == b'%PDF':
            self.is_pdf = True
            self.pdf_images = convert_from_bytes(bill_bytes, dpi=150, poppler_path=c.get_poppler_path())
            self.current_pdf_page = 0
            self.zoom_level = 0.4
            self.update_pdf_viewer()
        else:
            self.is_pdf = False
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            temp_file.write(bill_bytes)
            temp_file.close()
            self.image_data = Image.open(temp_file.name)
            self.zoom_level = 0.4
            self.update_image_viewer()

    def reset_preview(self):
        self.selected_bill_path = None
        self.selected_bill_data = None
        self.preview_label.clear()
        self.page_info.setText("0 / 0")

    def get_preview_widgets(self):
        return (
            self.preview_label,
            self.page_info,
            self.zoom_in,
            self.zoom_out,
            self.prev_pdf_page,
            self.next_pdf_page
        )
