from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import services.company_service as cs , services.user_service as us, utility, viewmodel.popup_dialog.company_create_dialog as ccd
from view.company_view import CompanyView 
from services.user_service import check_log_info 
from utility import get_login_credentials

class CompanyScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.ui = CompanyView(
            open_company=self.open_company
        )
        self.setLayout(self.ui.layout)

        # Event binding
        self.ui.back_button.clicked.connect(self.main_window.switch_to_login_scene)
        self.ui.search_button.clicked.connect(self.open_company)
        self.ui.btn_edit.clicked.connect(self.edit_company)
        self.ui.btn_delete.clicked.connect(self.delete_company)
        self.ui.btn_create.clicked.connect(self.create_company)


    def edit_company(self):
        company_id = self.get_company_id()

        # Veritabanından tüm şirket verilerini çek
        data = cs.get_company_by_id(company_id)

        if data is None:
            QMessageBox.warning(self, "Hata", "Şirket bilgileri alınamadı.")
            return

        # Popup'u aç ve güncelleme callback'ini gönder
        dialog = ccd.CompanyCreateDialog(
            self,
            lambda name, tax, rep: self.update_company(company_id, name, tax, rep),
            initial_data={
                'company_name': data['company_name'],
                'tax_no': data['tax_no'],
                'representer': data['company_representer']
            }
        )
        dialog.exec_()

    def update_company(self, company_id, name, tax_no, representer):
        cs.update_company(company_id, name, tax_no, representer)
        QMessageBox.information(self, "Güncellendi", "Şirket bilgileri güncellendi.")
        self.refresh_page()
        return True

    def get_company_id(self):
        company_id = self.ui.get_selected_company_id()
        if company_id is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir şirket seçin.")
            return
        else :return company_id

    def delete_company(self):
        company_id = self.ui.get_selected_company_id()
        if company_id is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir şirket seçin.")
            return
        username, password = get_login_credentials(self)
        if not username or not password:
            return
        if not check_log_info(username, password):
            QMessageBox.critical(self, "Hata", "Kullanıcı adı veya şifre hatalı!")
            return
        reply = QMessageBox.question(
            self,
            "Silme Onayı",
            "Bu şirketi silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            cs.delete_company(company_id)
            QMessageBox.information(self, "Başarılı", "Şirket başarıyla silindi!")
            self.refresh_page()

    def create_company(self):
        from PyQt5.QtWidgets import QMessageBox
        from services import company_service as cs
        from viewmodel.popup_dialog.company_create_dialog import CompanyCreateDialog

        dialog = ccd.CompanyCreateDialog(self)
        if dialog.exec_():
            name, tax_no, representer = dialog.get_inputs()
            result = cs.create_company(name, tax_no, representer)

            if result == 0:
                QMessageBox.warning(self, "Kayıt Zaten Var", f"'{name}' adında bir şirket zaten kayıtlı.")
            else:
                QMessageBox.information(self, "Kayıt Başarılı", f"'{name}' şirketi başarıyla eklendi.")
                self.refresh_page()

    def refresh_page(self):
        self.get_all_companies()
        self.calculate_amounts()        

    def get_all_companies(self):

        companies = cs.get_all_company()
        self.ui.update_company_list(companies=companies)

    def calculate_amounts(self):
        amounts = cs.calculate_amounts()
        total_credit = amounts["total_credit"]
        total_debit = amounts["total_debit"]
        net_balance = amounts["net_balance"]
        self.ui.set_balance_labels(total_credit, total_debit, net_balance)

    def open_company(self):
        company_id = self.get_company_id()
        if company_id is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir şirket seçin.")
            return
        if company_id is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir şirket seçin.")
            return
        if company_id:      
            self.main_window.switch_to_transaction_scene(company_id)
        else:
            QMessageBox.warning(self, "Hata", "Seçilen şirketin verisi alınamadı.")


