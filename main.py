import sys
import services.db_setup as db_setup 
import scene.app as main_app

from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    db_setup.setup_database()
    app = QApplication(sys.argv)
    main_window = main_app.VerTakApp()
    main_window.show()
    sys.exit(app.exec_())
