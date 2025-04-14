from PyQt5.QtWidgets import (QMainWindow, QStackedWidget)

import viewmodel.login_scene as ls , viewmodel.company_scene as cs, viewmodel.transaction_scene as ts
import utility as t

class VerTakApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veresiye Takip Sistemi")

        t.set_responsive_window(self)
            
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        

        self.login_scene = ls.LoginScene(self)
        self.company_scene = cs.CompanyScene(self)
        self.transaction_scene = ts.TransactionScene(self)

        self.stacked_widget.addWidget(self.login_scene)
        self.stacked_widget.addWidget(self.company_scene)
        self.stacked_widget.addWidget(self.transaction_scene)

        self.stacked_widget.setCurrentWidget(self.login_scene)

    def switch_to_company_scene(self):

        self.company_scene.get_all_companies()
        self.company_scene.calculate_amounts()
        self.stacked_widget.setCurrentWidget(self.company_scene)


    def switch_to_transaction_scene(self,company_id):
        self.transaction_scene.set_company_id(company_id)

        self.stacked_widget.setCurrentWidget(self.transaction_scene)


    def switch_to_login_scene(self):
        self.stacked_widget.setCurrentWidget(self.login_scene)

