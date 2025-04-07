from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import services.company_service as cs , services.user_service as us, utility, scene.popup_dialog.company_create_dialog as ccd

class CompanyScene(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.rating = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(25)

        # Geri ve Şirket Aç butonları
        hbox_top = QHBoxLayout()

        back_button = QPushButton("← Geri")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.setFixedHeight(36)
        back_button.setStyleSheet("font-size: 14px; padding: 6px 12px;")
        back_button.clicked.connect(self.main_window.switch_to_login_scene)

        self.search_button = QPushButton("🔍 Şirketi Aç")
        self.search_button.setCursor(Qt.PointingHandCursor)
        self.search_button.setEnabled(False)
        self.search_button.setFixedHeight(36)
        self.search_button.setStyleSheet("font-size: 14px; padding: 6px 12px;")
        self.search_button.clicked.connect(self.OpenCompany)

        hbox_top.addWidget(back_button, alignment=Qt.AlignLeft)
        hbox_top.addWidget(self.search_button, alignment=Qt.AlignRight)
        layout.addLayout(hbox_top)

        # Başlık
        table_label = QLabel("🗂️ Kayıtlı Şirket Listesi")
        table_label.setAlignment(Qt.AlignLeft)
        table_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(table_label)
        layout.addWidget(utility.create_horizontal_line())

        from PyQt5.QtWidgets import QHeaderView

        # Şirket tablosu
        self.company_table = QTableWidget()
        self.company_table.setColumnCount(6)
        self.company_table.setHorizontalHeaderLabels([
            "Şirket ID", "Şirket Adı", "Toplam Alacak", "Toplam Borç", "Net Durum", "İşlem Sayısı"
        ])
        self.company_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.company_table.setSelectionMode(QTableWidget.SingleSelection)
        self.company_table.setStyleSheet("font-size: 14px;")
        self.company_table.setMinimumHeight(250)
        self.company_table.itemSelectionChanged.connect(self.enable_search_button_if_selected)

        header = self.company_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  


        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  
        header.setSectionResizeMode(1, QHeaderView.Stretch)           
        header.setSectionResizeMode(2, QHeaderView.Stretch)           
        header.setSectionResizeMode(3, QHeaderView.Stretch)           
        header.setSectionResizeMode(4, QHeaderView.Stretch)           
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  

        layout.addWidget(self.company_table)


        layout.addWidget(utility.create_horizontal_line())

        # Toplam Alacak/Borç/Net Durum kutuları
        hbox_balance = QHBoxLayout()

        def create_summary_box(title_text, label_attr):
            vbox = QVBoxLayout()
            title = QLabel(title_text)
            title.setStyleSheet("font-weight: bold; font-size: 13px;")
            label = QLabel("")
            label.setFont(QFont("Arial", 20, QFont.Bold))
            setattr(self, label_attr, label)
            vbox.addWidget(title)
            vbox.addWidget(label)
            return vbox

        hbox_balance.addLayout(create_summary_box("Toplam Alacak", "label_credit_value"))
        hbox_balance.addLayout(create_summary_box("Toplam Borç", "label_debit_value"))
        hbox_balance.addLayout(create_summary_box("Net Durum", "label_net_value"))

        layout.addLayout(hbox_balance)

        # Ekle/Sil/Düzenle butonları
        hbox_buttons = QHBoxLayout()
        button_style = "font-size: 16px; padding: 10px 20px;"

        self.btn_edit = QPushButton("📝 Düzenle")
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.btn_edit.setStyleSheet(button_style)

        self.btn_delete = QPushButton("🗑️ Sil")
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.setStyleSheet(button_style)

        self.btn_create = QPushButton("➕ Ekle")
        self.btn_create.setCursor(Qt.PointingHandCursor)
        self.btn_create.setStyleSheet(button_style)

        self.btn_create.clicked.connect(self.open_create_dialog)
        self.btn_create.setFixedHeight(50)
        self.btn_edit.clicked.connect(self.edit_company)
        self.btn_edit.setFixedHeight(50)
        self.btn_delete.clicked.connect(self.delete_company)
        self.btn_delete.setFixedHeight(50)

        hbox_buttons.addWidget(self.btn_edit)
        hbox_buttons.addWidget(self.btn_delete)
        hbox_buttons.addWidget(self.btn_create)

        layout.addLayout(hbox_buttons)

        self.setLayout(layout)

    def edit_company(self):
        selected_row = self.company_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir şirket seçin.")
            return

        # Sadece ID alınır
        company_id = int(self.company_table.item(selected_row, 0).text())

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

    def delete_company(self):
        selected_row = self.company_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir şirket seçin.")
            return

        company_id = int(self.company_table.item(selected_row, 0).text())
        company_name = self.company_table.item(selected_row, 1).text()

        reply = QMessageBox.question(
            self,
            "Silme Onayı",
            f"'{company_name}' şirketini silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            cs.delete_company(company_id)
            QMessageBox.information(self, "Silindi", f"'{company_name}' başarıyla silindi.")
            self.refresh_page()


    def open_create_dialog(self):
        dialog = ccd.CompanyCreateDialog(self, self.create_company)
        dialog.exec_()
    
    def create_company(self, name, tax_no, representer):
        result = cs.create_company(name, tax_no, representer)

        if result == 0:
            QMessageBox.warning(self, "Kayıt Zaten Var", f"'{name}' adında bir şirket zaten kayıtlı.")
            return False
        else:
            QMessageBox.information(self, "Kayıt Başarılı", f"'{name}' şirketi başarıyla eklendi.")
            self.refresh_page()
            return True

    def refresh_page(self):
        self.get_all_companies()
        self.calculate_amounts()        


    def get_all_companies(self):

        companies = cs.get_all_company()

        self.company_table.setRowCount(len(companies))
        self.company_table.setColumnCount(6)
        self.company_table.setHorizontalHeaderLabels(["Şirket ID","Şirket Adı", "Toplam Alacak Tutar", "Toplam Borç Tutar","Net Durum" ,"İşlem sayısı"])

        for row_idx, (company_id, company_name, credit_amount, debit_amount, net_amount, number_of_transaction) in enumerate(companies):
            self.company_table.setItem(row_idx, 0, QTableWidgetItem(str(company_id)))
            self.company_table.setItem(row_idx, 1, QTableWidgetItem(company_name))
            self.company_table.setItem(row_idx, 2, QTableWidgetItem(f"{credit_amount:,.2f} ₺"))
            self.company_table.setItem(row_idx, 3, QTableWidgetItem(f"{debit_amount:,.2f} ₺"))
            self.company_table.setItem(row_idx, 4, QTableWidgetItem(f"{net_amount:,.2f} ₺"))
            self.company_table.setItem(row_idx, 5, QTableWidgetItem(str(number_of_transaction)))


        
    def enable_search_button_if_selected(self):
        selected_row = self.company_table.currentRow()
        self.search_button.setEnabled(selected_row != -1)

    def calculate_amounts(self):
        amounts = cs.calculate_amounts()
        total_credit = amounts["total_credit"]
        total_debit = amounts["total_debit"]
        net_balance = amounts["net_balance"]

        self.label_credit_value.setText(f"{total_credit:,.2f} ₺")
        self.label_debit_value.setText(f"{total_debit:,.2f} ₺")
        self.label_net_value.setText(f"{net_balance:,.2f} ₺")



    def OpenCompany(self):
        selected_row = self.company_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir şirket seçin.")
            return

        company_id_str = self.company_table.item(selected_row, 0)  
        if company_id_str:
            self.company_id = company_id_str.text()
            self.main_window.switch_to_transaction_scene(self.company_id)
        else:
            QMessageBox.warning(self, "Hata", "Seçilen şirketin verisi alınamadı.")


