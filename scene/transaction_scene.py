from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QLabel,QDialog,  QPushButton, QHeaderView,QHBoxLayout,QTableWidget,QTableWidgetItem,QMessageBox)
from PyQt5.QtCore import Qt
from services import user_service as us, transaction_service as ts
import utility, scene.popup_dialog.transaction_create_dialog as tcd, scene.popup_dialog.bill_viewer as bv
from PyQt5.QtGui import QFont

class TransactionScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(25)

        # Geri butonu
        hbox_top = QHBoxLayout()

        back_button = QPushButton("← Geri")
        back_button.setStyleSheet("font-size: 14px; padding: 6px 12px;")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.main_window.switch_to_company_scene)
        hbox_top.addWidget(back_button, alignment=Qt.AlignLeft)
        self.view_bill_btn = QPushButton("Fatura Göster")
        self.view_bill_btn.setStyleSheet("font-size: 14px; padding: 6px 12px;")
        self.view_bill_btn.setCursor(Qt.PointingHandCursor)
        self.view_bill_btn.clicked.connect(self.open_bill_viewer)
        hbox_top.addWidget(self.view_bill_btn, alignment=Qt.AlignRight)

        layout.addLayout(hbox_top)

        # Başlık
        table_label = QLabel("🗂️ Kayıtlı İşlemler Listesi")
        table_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        table_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(table_label)
        layout.addWidget(utility.create_horizontal_line())

        # İşlem tablosu
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(9)
        self.transaction_table.setHorizontalHeaderLabels([
            "İşlem ID", "İşlem Tarihi", "Açıklama", "Alacak Tutar", "Borç Tutar","Anlık Net Tutar", "Ödeme Türü", "Fatura Eklenme Tarihi","Fatura Var mı?"
        ])
        self.transaction_table.setColumnHidden(0, True)
        self.transaction_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.transaction_table.setSelectionMode(QTableWidget.SingleSelection)
        self.transaction_table.setStyleSheet("font-size: 14px;")
        self.transaction_table.setMinimumHeight(250)

        # Header ayarları
        header = self.transaction_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)   # Tarih
        header.setSectionResizeMode(1, QHeaderView.Stretch)            # Açıklama
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)   # Alacak
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)   # Borç
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)           # Ödeme Türü
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)   # Fatura

        layout.addWidget(self.transaction_table)
        layout.addWidget(utility.create_horizontal_line())

        # Toplamlar kutusu
        hbox_balance = QHBoxLayout()

        def create_summary(title_text):
            vbox = QVBoxLayout()
            title = QLabel(title_text)
            title.setStyleSheet("font-weight: bold; font-size: 13px;")
            label = QLabel("")
            label.setFont(QFont("Arial", 20, QFont.Bold))
            vbox.addWidget(title)
            vbox.addWidget(label)
            return vbox, label

        vbox_credit, self.label_credit_value = create_summary("Toplam Alacak")
        vbox_debit, self.label_debit_value = create_summary("Toplam Borç")
        vbox_net, self.label_net_value = create_summary("Net Durum")

        hbox_balance.addLayout(vbox_credit)
        hbox_balance.addLayout(vbox_debit)
        hbox_balance.addLayout(vbox_net)
        layout.addLayout(hbox_balance)

        # Butonlar
        hbox_buttons = QHBoxLayout()
        button_style = "font-size: 14px; padding: 10px 20px;"

        self.btn_edit = QPushButton("📝 Düzenle")
        self.btn_edit.setStyleSheet(button_style)
        self.btn_edit.setCursor(Qt.PointingHandCursor)

        self.btn_delete = QPushButton("🗑️ Sil")
        self.btn_delete.setStyleSheet(button_style)
        self.btn_delete.setCursor(Qt.PointingHandCursor)

        self.btn_create = QPushButton("➕ Ekle")
        self.btn_create.setStyleSheet(button_style)
        self.btn_create.setCursor(Qt.PointingHandCursor)

        self.btn_edit.clicked.connect(self.edit_transaction)
        self.btn_delete.clicked.connect(self.delete_transaction)
        self.btn_create.clicked.connect(self.create_transaction)

        hbox_buttons.addWidget(self.btn_edit)
        hbox_buttons.addWidget(self.btn_delete)
        hbox_buttons.addWidget(self.btn_create)

        layout.addLayout(hbox_buttons)

        self.setLayout(layout)

    def set_company_id(self, company_id):
        self.company_id = company_id
        self.get_all_transaction(self.company_id)
        self.calculate_amounts()

    def edit_transaction(self):
        selected_row = self.transaction_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir işlem seçin.")
            return

        # Gizli sütundan transaction_id alınır (0. sütun)
        transaction_id_item = self.transaction_table.item(selected_row, 0)
        if not transaction_id_item:
            QMessageBox.warning(self, "Hata", "İşlem ID alınamadı.")
            return

        transaction_id = int(transaction_id_item.text())

        # ID'ye göre işlem bilgileri çekilir
        data = ts.get_transaction_by_id(transaction_id)
        if not data:
            QMessageBox.warning(self, "Hata", "İşlem bilgileri alınamadı.")
            return

        # Popup dialog açılır, veriler gönderilir
        dialog = tcd.TransactionCreateDialog(self, initial_data=data)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_data()
            ts.update_transaction(transaction_id, updated_data)
            self.refresh_page(self.company_id)

    def delete_transaction(self):
        selected_row = self.transaction_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir işlem seçin.")
            return

        transaction_id_item = self.transaction_table.item(selected_row, 0)
        if not transaction_id_item:
            QMessageBox.warning(self, "Hata", "İşlem ID alınamadı.")
            return

        transaction_id = int(transaction_id_item.text())

        reply = QMessageBox.question(
            self,
            "Silme Onayı",
            "Bu işlemi silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            ts.delete_transaction(transaction_id)
            QMessageBox.information(self, "Silindi", "İşlem başarıyla silindi.")
            self.refresh_page(self.company_id)
  
    def open_bill_viewer(self):
        selected_row = self.transaction_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir işlem seçin.")
            return

        transaction_id_item = self.transaction_table.item(selected_row, 0)
        transaction_id = int(transaction_id_item.text())

        bill_data = ts.get_bill_by_id(transaction_id)
        if bill_data:
            viewer = bv.BillViewer(bill_data)
            viewer.exec_()
        else:
            QMessageBox.information(self, "Bilgi", "Bu işlemde fatura bulunmamaktadır.")


    def create_transaction(self):
        dialog = tcd.TransactionCreateDialog(self)
        if dialog.exec_() == QDialog.Accepted:

            data = dialog.get_data()

        
            ts.add_transaction(
                company_id=self.company_id,
                date=data["date"],  # DB'de otomatik datetime('now') olacak
                explanation=data['explanation'],
                credit=data['credit'],
                debit=data['debit'],
                payment_type=data['payment_type'],
                bill_added_date=data['bill_added_date'],
                bill=data['bill'],  
            )

            self.refresh_page(company_id=self.company_id)


    def refresh_page(self,company_id):
        self.get_all_transaction(company_id=company_id)
        self.calculate_amounts()


    def get_all_transaction(self,company_id):
        transactions = ts.get_all_transaction(company_id=company_id)

        self.transaction_table.setRowCount(len(transactions))

        for row_idx, (transaction_id, transaction_date, explanation, credit_amount, debit_amount,current_balance, payment_type, bill_added_date,bill) in enumerate(transactions):
            self.transaction_table.setItem(row_idx, 0, QTableWidgetItem(str(transaction_id)))  # Gizli sütun
            self.transaction_table.setItem(row_idx, 1, QTableWidgetItem(transaction_date))
            self.transaction_table.setItem(row_idx, 2, QTableWidgetItem(explanation or "-"))
            self.transaction_table.setItem(row_idx, 3, QTableWidgetItem(f"{credit_amount:,.2f} ₺"))
            self.transaction_table.setItem(row_idx, 4, QTableWidgetItem(f"{debit_amount:,.2f} ₺"))
            self.transaction_table.setItem(row_idx, 5, QTableWidgetItem(f"{current_balance:,.2f} ₺"))
            self.transaction_table.setItem(row_idx, 6, QTableWidgetItem(payment_type or "-"))
            if bill:
                self.transaction_table.setItem(row_idx, 7, QTableWidgetItem(str(bill_added_date)))
            else:
                self.transaction_table.setItem(row_idx, 7, QTableWidgetItem("-"))
            bill_status = "var" if bill and bill.strip() != "" else "yok"

            self.transaction_table.setItem(row_idx, 8, QTableWidgetItem(bill_status))

    def calculate_amounts(self):
        company_id=self.main_window.company_scene.company_id
        amounts = ts.calculate_amounts(company_id)
        total_credit = amounts["total_credit"]
        total_debit = amounts["total_debit"]
        net_balance = amounts["net_balance"]

        self.label_credit_value.setText(f"{total_credit:,.2f} ₺")
        self.label_debit_value.setText(f"{total_debit:,.2f} ₺")
        self.label_net_value.setText(f"{net_balance:,.2f} ₺")