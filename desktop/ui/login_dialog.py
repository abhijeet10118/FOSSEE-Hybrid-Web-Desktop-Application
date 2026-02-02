from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
)
from PyQt5.QtCore import Qt


class LoginDialog(QDialog):
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self.client = client
        self.setWindowTitle("Sign in")
        self.setFixedSize(320, 180)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Password")
        form.addRow("Username:", self.username)
        form.addRow("Password:", self.password)
        layout.addLayout(form)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setWordWrap(True)
        layout.addWidget(self.error_label)
        btn = QPushButton("Sign in")
        btn.clicked.connect(self.do_login)
        layout.addWidget(btn)

    def do_login(self):
        username = self.username.text().strip()
        password = self.password.text()
        self.error_label.setText("")
        if not username or not password:
            self.error_label.setText("Enter username and password.")
            return
        try:
            self.client.login(username, password)
            self.accept()
        except Exception as e:
            self.error_label.setText(str(e)[:80])
