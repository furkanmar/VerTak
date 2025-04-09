from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QDateTimeEdit,QCalendarWidget, QTimeEdit,QSizePolicy,QScrollArea,QToolButton,
    QMessageBox, QComboBox, QFileDialog
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QPixmap
from pdf2image import convert_from_path
import tempfile
import os
from PIL import Image
import utility
from utility import create_styled_lineedit

class TransactionCreateDialog(QDialog):
    def __init__(self, parent=None, initial_data=None):
        super().__init__(parent)
        self.setWindowTitle("İşlem Güncelle" if initial_data else "Yeni İşlem Ekle")
        self.resize(800, 600)

        self.selected_bill_path = None
        self.initial_data = initial_data
        self.pdf_images = []  # Tüm sayfalar burada tutulacak
        self.current_pdf_page = 0
        self.image_data = None  # PNG / JPEG için PIL.Image
        self.is_pdf = False
        self.zoom_level = 0.4
        self.init_ui()



    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)

        # === SOL PANEL ===
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        left_layout.setContentsMargins(20, 20, 20, 20)

        def create_label(text):
            label = QLabel(text)
            label.setStyleSheet("font-weight: bold; font-size: 13px;")
            return label

        # Tarih
        left_layout.addWidget(create_label("Tarih"))
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setSelectedDate(QDateTime.currentDateTime().date())
        left_layout.addWidget(self.calendar_widget)

        # Saat
        left_layout.addWidget(create_label("Saat"))
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(QDateTime.currentDateTime().time())
        self.time_edit.setStyleSheet(f"""
            font-size: 14px;
            padding: 6px 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        """)
        left_layout.addWidget(self.time_edit)

        # Açıklama
        left_layout.addWidget(create_label("Açıklama"))
        self.explanation_input = create_styled_lineedit("Açıklama")
        left_layout.addWidget(self.explanation_input)

        # Alacak
        left_layout.addWidget(create_label("Alacak Tutarı *"))
        self.credit_input = create_styled_lineedit("0")
        left_layout.addWidget(self.credit_input)

        # Borç
        left_layout.addWidget(create_label("Borç Tutarı *"))
        self.debit_input = create_styled_lineedit("0")
        left_layout.addWidget(self.debit_input)

        # Ödeme Türü
        left_layout.addWidget(create_label("Ödeme Türü"))
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Çek", "Nakit", "Kredi Kartı", "Havale"])
        self.payment_combo.setStyleSheet("padding: 6px; font-size: 13px;")
        left_layout.addWidget(self.payment_combo)

        # Fatura Ekle
        left_layout.addWidget(create_label("Fatura Ekle"))

        bill_layout = QHBoxLayout()
        self.bill_button = QPushButton("Fatura Seç")
        self.bill_button.setCursor(Qt.PointingHandCursor)
        self.bill_button.clicked.connect(self.select_bill_file)
        self.bill_button.setStyleSheet("padding: 8px 16px; font-size: 14px;")

        self.bill_label = QLabel("Hiçbir dosya seçilmedi")
        self.bill_label.setStyleSheet("font-style: italic; color: gray")

        bill_layout.addWidget(self.bill_button)
        bill_layout.addWidget(self.bill_label)
        left_layout.addLayout(bill_layout)

        # Ekle / İptal Butonları
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("İptal")
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Ekle")
        save_btn.clicked.connect(self.submit_form)
        save_btn.setCursor(Qt.PointingHandCursor)

        for btn in [cancel_btn, save_btn]:
            btn.setStyleSheet("padding: 8px 16px; font-size: 14px;")

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        left_layout.addLayout(button_layout)

        # === SAĞ PANEL ===
        right_layout = QVBoxLayout()

        preview_title = QLabel("Fatura Önizlemesi")
        preview_title.setAlignment(Qt.AlignCenter)
        preview_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        right_layout.addWidget(preview_title)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: 1px solid #ccc;")
        scroll_area.setWidget(self.preview_label)
        right_layout.addWidget(scroll_area, stretch=9)

        # Sayfa geçiş
        nav_layout = QHBoxLayout()
        self.prev_btn = QToolButton()
        self.prev_btn.setText("←")
        self.prev_btn.clicked.connect(self.prev_pdf_page)

        self.page_info = QLabel("0 / 0")
        self.page_info.setAlignment(Qt.AlignCenter)

        self.next_btn = QToolButton()
        self.next_btn.setText("→")
        self.next_btn.clicked.connect(self.next_pdf_page)

        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.page_info)
        nav_layout.addWidget(self.next_btn)
        right_layout.addLayout(nav_layout)

        # Zoom kontrolleri
        zoom_layout = QHBoxLayout()
        self.zoom_out_btn = QToolButton()
        self.zoom_out_btn.setText("–")
        self.zoom_out_btn.clicked.connect(self.zoom_out)

        self.zoom_in_btn = QToolButton()
        self.zoom_in_btn.setText("+")
        self.zoom_in_btn.clicked.connect(self.zoom_in)

        zoom_layout.addWidget(self.zoom_out_btn)
        zoom_layout.addWidget(QLabel("Zoom"))
        zoom_layout.addWidget(self.zoom_in_btn)
        right_layout.addLayout(zoom_layout)

        # Ana yerleşim
        main_layout.addLayout(left_layout, stretch=2)
        main_layout.addLayout(right_layout, stretch=3)
        self.setLayout(main_layout)



        if self.initial_data:
            self.explanation_input.setText(self.initial_data.get("explanation", ""))
            self.credit_input.setText(str(self.initial_data.get("credit", "0")))
            self.debit_input.setText(str(self.initial_data.get("debit", "0")))
            payment = self.initial_data.get("payment_type", "")
            if payment in ["Çek", "Nakit", "Kredi Kartı", "Havale"]:
                self.payment_combo.setCurrentText(payment)
            bill = self.initial_data.get("bill", None)
            if bill:
                self.selected_bill_path = bill
                self.bill_label.setText(bill.split("/")[-1])
            if self.initial_data.get("date"):
                dt = QDateTime.fromString(self.initial_data["date"], "yyyy-MM-dd HH:mm:ss")
                if dt.isValid():
                    self.date_time_edit.setDateTime(dt)


    def select_bill_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Fatura Dosyasını Seç",
            "",
            "Tüm Desteklenen Dosyalar (*.png *.jpg *.jpeg *.pdf);;Görseller (*.png *.jpg *.jpeg);;PDF (*.pdf);;Tüm Dosyalar (*)"
        )

        if file_path:
            self.selected_bill_path = file_path
            self.bill_label.setText(file_path.split("/")[-1])

            # Dosya içeriğini byte olarak oku
            with open(file_path, "rb") as f:
                self.selected_bill_data = f.read()

            ext = os.path.splitext(file_path)[-1].lower()

            if ext in [".png", ".jpg", ".jpeg"]:
                
                self.is_pdf = False
                self.image_data = Image.open(file_path)
                self.zoom_level = 0.4
                self.update_image_viewer()
                self.resize(1200, 800)


            elif ext == ".pdf":
                try:
                    self.is_pdf = True
                    poppler_path = r"c:\Users\Public\VerTak\VerTak\resources\poppler\bin"
                    self.pdf_images = convert_from_path(file_path, dpi=150, poppler_path=poppler_path)
                    if self.pdf_images:
                        self.current_pdf_page = 0
                        self.zoom_level = 0.4
                        self.update_pdf_viewer()
                        self.resize(1200, 800)

                    else:
                        self.preview_label.setText("PDF önizlenemedi.")
                except Exception as e:
                    self.preview_label.setText(f"PDF hatası: {str(e)}")

            else:
                self.preview_label.setText("Bu dosya türü desteklenmiyor.")

        else:
            self.selected_bill_path = None
            self.selected_bill_data = None
            self.bill_label.setText("Hiçbir dosya seçilmedi")
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


    def submit_form(self):
        credit = self.credit_input.text().strip()
        debit = self.debit_input.text().strip()

        if credit == "" or debit == "":
            QMessageBox.warning(self, "Zorunlu Alan", "Alacak ve borç alanları boş olamaz.")
            return

        try:
            self.credit_val = float(credit)
            self.debit_val = float(debit)
        except ValueError:
            QMessageBox.warning(self, "Hatalı Giriş", "Alacak ve borç tutarları sayısal olmalıdır.")
            return

        self.accept()


    def get_data(self):
        selected_date = self.calendar_widget.selectedDate()
        selected_time = self.time_edit.time()
        combined_datetime = QDateTime(selected_date, selected_time)

        return {
            "explanation": self.explanation_input.text().strip(),
            "credit": self.credit_val,
            "debit": self.debit_val,
            "payment_type": self.payment_combo.currentText(),
            "bill_added_date": utility.get_current_date() if hasattr(self, 'selected_bill_data') else None,
            "bill": self.selected_bill_data if hasattr(self, 'selected_bill_data') else None,

            "date": combined_datetime.toString("yyyy-MM-dd HH:mm:ss")
        }

