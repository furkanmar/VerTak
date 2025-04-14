from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

from view.base.base_table_header import BaseTableHeaderSection
from view.base.table_setup_mixin import TableSetupMixin

from view.base.base_summary_section import TableSummaryButtonsMixin
import utility
from view.base.filter_bar import TableFilterBar
class CompanyView(QWidget, TableSetupMixin, TableSummaryButtonsMixin):
    def __init__(self,open_company):
        super().__init__()
        self.open_company = open_company
        self.active_filters = {}
        self.inputs = {}
        self.layout = self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(25)

        header_builder = BaseTableHeaderSection()
        header_layout, self.back_button, self.search_button = header_builder.create_table_header(
            title="Kayıtlı Şirket Listesi",
            right_btn_text="🔍 Şirketi Aç"
        )
        layout.addLayout(header_layout)
        headers=["Şirket ID", "Şirket Adı", "Toplam Alacak", "Toplam Borç", "Net Durum", "İşlem Sayısı"]
        filters = [f for f in headers if f != "Şirket ID"]

        self.filter_bar = TableFilterBar(headers=filters)
        self.filter_bar.filter_changed.connect(self.apply_filter)

        layout.addWidget(self.filter_bar)
        self.company_table = QTableWidget()
        self.configure_table(
            table=self.company_table,
            headers=headers,
            resize_modes=["resize", "stretch", "stretch", "stretch", "stretch", "resize"],
            double_click_slot=self.open_company,
            enable_sorting=True,

        )
        layout.addWidget(self.company_table)
        layout.addWidget(utility.create_horizontal_line())

        layout.addLayout(self.create_summary_and_buttons())


        return layout

    def update_company_list(self, companies):
        self.company_table.setRowCount(len(companies))
        self.company_table.setColumnCount(6)
        self.company_table.setHorizontalHeaderLabels([
            "Şirket ID","Şirket Adı", "Toplam Alacak Tutar", "Toplam Borç Tutar", "Net Durum", "İşlem Sayısı"
        ])

        for row_idx, (company_id, company_name, credit_amount, debit_amount, net_amount, number_of_transaction) in enumerate(companies):
            self.company_table.setItem(row_idx, 0, QTableWidgetItem(str(company_id)))
            self.company_table.setItem(row_idx, 1, QTableWidgetItem(company_name))
            self.company_table.setItem(row_idx, 2, QTableWidgetItem(f"{credit_amount:,.2f} ₺"))
            self.company_table.setItem(row_idx, 3, QTableWidgetItem(f"{debit_amount:,.2f} ₺"))
            self.company_table.setItem(row_idx, 4, QTableWidgetItem(f"{net_amount:,.2f} ₺"))
            self.company_table.setItem(row_idx, 5, QTableWidgetItem(str(number_of_transaction)))

    def get_selected_company_id(self):
        selected_row = self.company_table.currentRow()
        if selected_row == -1:
            return None
        return int(self.company_table.item(selected_row, 0).text())

    def set_balance_labels(self, credit, debit, net):
        self.label_credit_value.setText(f"{credit:,.2f} ₺")
        self.label_debit_value.setText(f"{debit:,.2f} ₺")
        self.label_net_value.setText(f"{net:,.2f} ₺")

    def apply_filter(self, column: int, text: str):
        normalized_text = text.lower().replace(",", "").strip()


        if normalized_text:
            self.active_filters[column] = normalized_text
        elif column in self.active_filters:
            del self.active_filters[column]


        for row in range(self.company_table.rowCount()):
            visible = True  

            for col, filter_text in self.active_filters.items():
                item = self.company_table.item(row, col)
                if item:
                    cell_text = item.text().lower().replace(",", "").strip()
                    if not cell_text.startswith(filter_text):
                        visible = False
                        break

            self.company_table.setRowHidden(row, not visible)

    def clear_filters(self):
        self.active_filters.clear()
        self.filter_bar.clear_all_inputs()  
        for row in range(self.company_table.rowCount()):
            self.company_table.setRowHidden(row, False)