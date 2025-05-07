from PyQt5.QtWidgets import QDialog, QDesktopWidget
from PyQt5.QtCore import Qt, QDateTime
from view.base.viewer import BaseFormWithPreview
from utility import center_and_resize_dialog
from view.transaction_create_view import TransactionFormUI  # yeni component dosyası


class TransactionCreateDialog(QDialog, BaseFormWithPreview):

    def __init__(self, parent=None, initial_data=None):
        QDialog.__init__(self, parent)
        BaseFormWithPreview.__init__(self)

        self.initial_data = initial_data
        self.setWindowTitle("İşlem Güncelle" if initial_data else "Yeni İşlem Ekle")

        self.setWindowFlags(self.windowFlags() & ~Qt.MSWindowsFixedSizeDialogHint)
        self.setSizeGripEnabled(True)

        screen = QDesktopWidget().availableGeometry(self)
        self.setMaximumHeight(int(screen.height() * 0.9))

        center_and_resize_dialog(self, 0.5, 0.6)

        self.form_ui = TransactionFormUI(self)
        self.setLayout(self.form_ui.layout)
        self.set_bill_label(lambda text: self.form_ui.bill_label.setText(text))

        if self.initial_data:

            self.form_ui.explanation_input.setText(self.initial_data.get("explanation", ""))
            self.form_ui.credit_input.setText(str(self.initial_data.get("credit", "0")))
            self.form_ui.debit_input.setText(str(self.initial_data.get("debit", "0")))
            payment = self.initial_data.get("payment_type", "")
            if payment in ["Çek", "Nakit", "Kredi Kartı", "Havale"]:
                self.form_ui.payment_combo.setCurrentText(payment)
            bill_bytes = self.initial_data.get("bill")
            if bill_bytes:
                self.selected_bill_data = bill_bytes
                self.load_bill_from_bytes(self.selected_bill_data)
                self.form_ui.bill_label.setText("Yüklü fatura (veritabanından)")
            if self.initial_data.get("date"):
                dt = QDateTime.fromString(self.initial_data["date"], "yyyy-MM-dd HH:mm:ss")
                if dt.isValid():
                    self.form_ui.calendar_widget.setSelectedDate(dt.date())
                    self.form_ui.time_edit.setTime(dt.time())

    def submit_form(self):
        credit = self.form_ui.credit_input.text().strip()
        debit = self.form_ui.debit_input.text().strip()

        if credit == "" and debit == "":
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Zorunlu Alan", "Alacak ve borç alanları boş olamaz.")
            return
        elif credit == "":
            credit = "0"
        elif debit == "":
            debit = "0"
        try:
            self.credit_val = float(credit)
            self.debit_val = float(debit)
        except ValueError:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Hatalı Giriş", "Alacak ve borç tutarları sayısal olmalıdır.")
            return
        self.accept()

    def get_data(self):
        selected_date = self.form_ui.calendar_widget.selectedDate()
        selected_time = self.form_ui.time_edit.time()
        combined_datetime = QDateTime(selected_date, selected_time)

        bill_info = self.get_bill_data()

        return {
            "explanation": self.form_ui.explanation_input.text().strip(),
            "credit": self.credit_val,
            "debit": self.debit_val,
            "payment_type": self.form_ui.payment_combo.currentText(),
            "bill_added_date": bill_info["bill_added_date"],
            "bill": bill_info["bill"],
            "date": combined_datetime.toString("yyyy-MM-dd HH:mm:ss")
        }
    
    def get_preview_widgets(self):
        return BaseFormWithPreview.get_preview_widgets(self)