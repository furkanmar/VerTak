# table_config_mixin.py
from PyQt5.QtWidgets import (
    QTableWidget, QHeaderView, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QLabel
)
from functools import partial
from PyQt5.QtCore import Qt

class TableSetupMixin:
    def configure_table(
        self,
        table: QTableWidget,
        headers: list[str],
        resize_modes: list[str],  # "stretch" veya "resize"
        hidden_first_column: bool = True,
        double_click_slot=None,
        selection_changed_slot=None,
        enable_sorting: bool = True,
    ):
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setStyleSheet("font-size: 14px;")
        table.setMinimumHeight(250)
        table.setSelectionBehavior(table.SelectRows)
        table.setSelectionMode(table.SingleSelection)
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        if hidden_first_column:
            table.setColumnHidden(0, True)

        if double_click_slot:
            table.itemDoubleClicked.connect(double_click_slot)

        if selection_changed_slot:
            table.itemSelectionChanged.connect(selection_changed_slot)

        header = table.horizontalHeader()
        for i, mode in enumerate(resize_modes):
            if mode == "stretch":
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            elif mode == "resize":
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        if enable_sorting:
            table.setSortingEnabled(True)




