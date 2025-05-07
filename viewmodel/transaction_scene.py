from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox,QTableWidgetItem , QPushButton
from PyQt5.QtCore import Qt
from services import transaction_service as ts
import viewmodel.popup_dialog.transaction_create_dialog as tcd
import viewmodel.popup_dialog.bill_viewer as bv
from view.transaction_view import TransactionView
from utility import get_login_credentials
from services.user_service import check_log_info
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os
from services.transaction_service import get_transaction_by_id, update_transaction
from datetime import datetime

class TransactionScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ui = TransactionView(
            edit_func=self.edit_transaction,
            main_window=self.main_window
        )
        self.setLayout(self.ui.layout())

        # Event Binding
        self.ui.back_button.clicked.connect(self.main_window.switch_to_company_scene)
        self.ui.btn_edit.clicked.connect(self.edit_transaction)
        self.ui.btn_delete.clicked.connect(self.delete_transaction)
        self.ui.btn_create.clicked.connect(self.create_transaction)


    def set_company_id(self, company_id):
        self.company_id = company_id
        self.get_all_transaction()
        self.calculate_amounts()

    def refresh_page(self):
        self.get_all_transaction()
        self.calculate_amounts()

    def get_all_transaction(self):
        transactions = ts.get_all_transaction(company_id=self.company_id)
        table = self.ui.transaction_table
        table.setRowCount(len(transactions))

        for row_idx, (tid, tdate, explanation, credit, debit, net, ptype, bill_date, bill) in enumerate(transactions):
            table.setItem(row_idx, 0, QTableWidgetItem(str(tid)))
            table.setItem(row_idx, 1, QTableWidgetItem(tdate))
            table.setItem(row_idx, 2, QTableWidgetItem(explanation or "-"))
            table.setItem(row_idx, 3, QTableWidgetItem(f"{credit:,.2f} ₺"))
            table.setItem(row_idx, 4, QTableWidgetItem(f"{debit:,.2f} ₺"))
            table.setItem(row_idx, 5, QTableWidgetItem(f"{net:,.2f} ₺"))
            table.setItem(row_idx, 6, QTableWidgetItem(ptype or "-"))
            table.setItem(row_idx, 7, QTableWidgetItem(str(bill_date) if bill else "-"))
            table.setItem(row_idx, 8, QTableWidgetItem("var" if bill and bill.strip() != "" else "yok"))
            # Fatura için özel buton
            btn = QPushButton("Var" if bill and bill.strip() else "Yok")
            btn.setStyleSheet("padding: 2px; font-size: 12px;")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("transaction_id", tid)  

            if bill and bill.strip():
                btn.clicked.connect(lambda _, tid=tid: self.open_bill_viewer(int(tid)))
            else:
                btn.clicked.connect(lambda _, tid=tid: self.select_bill_file(int(tid)))

            table.setCellWidget(row_idx, 8, btn)

    def calculate_amounts(self):
        amounts = ts.calculate_amounts(self.company_id)
        self.ui.label_credit_value.setText(f"{amounts['total_credit']:,.2f} ₺")
        self.ui.label_debit_value.setText(f"{amounts['total_debit']:,.2f} ₺")
        self.ui.label_net_value.setText(f"{amounts['net_balance']:,.2f} ₺")

    def create_transaction(self):
        dialog = tcd.TransactionCreateDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            ts.add_transaction(
                company_id=self.company_id,
                date=data["date"],
                explanation=data["explanation"],
                credit=data["credit"],
                debit=data["debit"],
                payment_type=data["payment_type"],
                bill_added_date=data["bill_added_date"],
                bill=data["bill"]
            )
            self.refresh_page()

    def edit_transaction(self):
        row = self.ui.transaction_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir işlem seçin.")
            return
        tid_item = self.ui.transaction_table.item(row, 0)
        tid = int(tid_item.text())
        data = ts.get_transaction_by_id(tid)
        if not data:
            QMessageBox.warning(self, "Hata", "İşlem bulunamadı.")
            return
        dialog = tcd.TransactionCreateDialog(self, initial_data=data)
        if dialog.exec_() == QDialog.Accepted:
            ts.update_transaction(tid, dialog.get_data())
            self.refresh_page()

    def select_bill_file(self, transaction_id: int):


        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Fatura Dosyasını Seç",
            "",
            "Desteklenen Dosyalar (*.png *.jpg *.jpeg *.pdf);;Tüm Dosyalar (*)"
        )

        if not file_path:
            QMessageBox.information(self, "Bilgi", "Herhangi bir dosya seçilmedi.")
            return

        ext = os.path.splitext(file_path)[-1].lower()
        if ext not in [".png", ".jpg", ".jpeg", ".pdf"]:
            QMessageBox.warning(self, "Uyarı", "Seçilen dosya türü desteklenmiyor.")
            return

        try:
            with open(file_path, "rb") as f:
                bill_binary = f.read()

            existing_data = get_transaction_by_id(transaction_id)
            if not existing_data:
                QMessageBox.critical(self, "Hata", "İlgili işlem veritabanında bulunamadı.")
                return

            updated_data = {
                "explanation": existing_data["explanation"],
                "credit": existing_data["credit"],
                "debit": existing_data["debit"],
                "payment_type": existing_data["payment_type"],
                "bill_added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "bill": bill_binary
            }

            update_transaction(transaction_id, updated_data)

            QMessageBox.information(self, "Başarılı", f"Fatura başarıyla eklendi:\n{os.path.basename(file_path)}")
            self.get_all_transaction()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya okunurken hata oluştu:\n{str(e)}")

    def delete_transaction(self):
        row = self.ui.transaction_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir işlem seçin.")
            return
        username, password = get_login_credentials(self)
        if not username or not password:
            return
        if not check_log_info(username, password):
            QMessageBox.critical(self, "Hata", "Kullanıcı adı veya şifre hatalı!")
            return
        tid_item = self.ui.transaction_table.item(row, 0)
        tid = int(tid_item.text())
        reply = QMessageBox.question(self, "Sil", "Bu işlemi silmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            ts.delete_transaction(tid)
            QMessageBox.information(self, "Başarılı", "İşlem başarıyla silindi.")
            self.refresh_page()

    def open_bill_viewer(self,tranction_id=None):
        if tranction_id:
            tid=tranction_id
        else:
            row = self.ui.transaction_table.currentRow()
            if row == -1:
                QMessageBox.warning(self, "Uyarı", "Lütfen bir işlem seçin.")
                return
            tid = int(self.ui.transaction_table.item(row, 0).text())

        bill = ts.get_bill_by_id(tid)
        if bill:
            viewer = bv.BillViewer(bill)
            viewer.exec_()
        else:
            QMessageBox.information(self, "Bilgi", "Fatura bulunamadı.")    

