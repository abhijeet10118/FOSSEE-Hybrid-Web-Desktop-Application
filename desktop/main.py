import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog
from api_client import ApiClient


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")

    client = ApiClient()
    login = LoginDialog(client)
    if not login.exec_():
        sys.exit(0)

    win = MainWindow(client)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
