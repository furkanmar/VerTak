# components/transaction_scene_ui.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout,QTableWidget
)
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget, QSizePolicy
from view.base.base_table_header import BaseTableHeaderSection
import utility
from view.base.table_setup_mixin import TableSetupMixin
from view.base.base_summary_section import TableSummaryButtonsMixin
from view.base.filter_bar import TableFilterBar

class TransactionView(QWidget,TableSetupMixin,TableSummaryButtonsMixin):
    
    def __init__(self,edit_func,main_window):
        super().__init__()
        self.edit_func = edit_func
        self.main_window = main_window
        self.active_filters = {}
        self.inputs = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(25)

        header_builder = BaseTableHeaderSection()
        header_layout, self.back_button, self.view_bill_btn = header_builder.create_table_header(
            title="Kayıtlı İşlemler Listesi",
            right_btn_text="Fatura Göster"
        )
        layout.addLayout(header_layout)

        # Filtre başlıkları
        headers = [
            "İşlem ID", "İşlem Tarihi", "Açıklama", "Alacak Tutar", "Borç Tutar",
            "Anlık Net Tutar", "Ödeme Türü", "Fatura Eklenme Tarihi", "Fatura Var mı?"
        ]
        filters = [f for f in headers if f != "İşlem ID"]
        self.filter_bar = TableFilterBar(filters)
        self.filter_bar.filter_changed.connect(self.apply_filter)

        layout.addWidget(self.filter_bar)

        # Tablo
        self.transaction_table = QTableWidget()
        self.configure_table(
            table=self.transaction_table,
            headers=headers,
            resize_modes=["resize", "stretch", "resize", "resize", "resize", "stretch", "resize", "resize", "resize"],
            double_click_slot=self.edit_func,
            enable_sorting=True,
        )
        layout.addWidget(self.transaction_table)
        layout.addWidget(utility.create_horizontal_line())

        # Toplamlar
        layout.addLayout(self.create_summary_and_buttons())
        self.setLayout(layout)


    def apply_filter(self, column: int, text: str):
        normalized_text = text.lower().replace(",", "").strip()

        # Filtreyi güncelle
        if normalized_text:
            self.active_filters[column] = normalized_text
        elif column in self.active_filters:
            del self.active_filters[column]

        # Her satırı kontrol et
        for row in range(self.transaction_table.rowCount()):
            visible = True  # Tüm filtrelere uyuyorsa görünür kalır

            for col, filter_text in self.active_filters.items():
                item = self.transaction_table.item(row, col)
                if item:
                    cell_text = item.text().lower().replace(",", "").strip()
                    if not cell_text.startswith(filter_text):
                        visible = False
                        break

            self.transaction_table.setRowHidden(row, not visible)

    def clear_filters(self):
        self.active_filters.clear()
        self.filter_bar.clear_all_inputs()  
        for row in range(self.transaction_table.rowCount()):
            self.transaction_table.setRowHidden(row, False)




