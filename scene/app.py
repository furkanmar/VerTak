from PyQt5.QtWidgets import (QMainWindow, QStackedWidget,QDesktopWidget)

import scene.login_scene as ls , scene.company_scene as cs, scene.transaction_scene as ts

class VerTakApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veresiye Takip Sistemi")

        # Ekran boyutunu al
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Pencere boyutunu ekranın %60'ı yap (ortalamaya uygun bir oran)
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)

        # Ortalamak için sol üst köşe koordinatlarını hesapla
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        # Ayarla
        self.setGeometry(x, y, window_width, window_height)
            
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
        self.stacked_widget.setCurrentWidget(self.company_scene)
        self.company_scene.get_all_companies()
        self.company_scene.calculate_amounts()

        

    def switch_to_transaction_scene(self,company_id):
        self.transaction_scene.get_all_transaction(company_id)        
        self.transaction_scene.set_company_id(company_id)

        self.stacked_widget.setCurrentWidget(self.transaction_scene)


    def switch_to_login_scene(self):
        self.stacked_widget.setCurrentWidget(self.login_scene)

