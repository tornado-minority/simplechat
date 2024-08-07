from PyQt5.QtWidgets import QPushButton, QGridLayout, QWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import ipaddress


class AddChatWindow(QWidget):
    def __init__(self, add_chat, update_chats):
        super().__init__()
        self.resize(200, 200)
        self.setWindowTitle('Добавить чат')

        readip_box = QLineEdit()
        readip_box.setAlignment(Qt.AlignRight)

        def add_ip():
            try:
                add_chat(readip_box.text())
                update_chats()
                self.close()
            except ValueError:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ошибка")
                msg.setInformativeText('Неправильный IP или порт')
                msg.setWindowTitle("Ошибка")
                msg.exec_()

        readip_button = QPushButton('Введите имя пользователя', self)
        readip_button.clicked.connect(add_ip)

        self.layout = QGridLayout()
        self.layout.addWidget(readip_box, 2, 3)
        self.layout.addWidget(readip_button, 4, 3)
        self.setLayout(self.layout)

