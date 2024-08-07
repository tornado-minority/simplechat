from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Message(QWidget):
    def __init__(self, message, user_name, size, our_msg):
        super(Message, self).__init__()
        self.layout = QGridLayout()

        def chunk_string(string, length):
            return (string[0 + i:length + i] for i in range(0, len(string), length))

        self.setAttribute(Qt.WA_StyledBackground, True)

        half_w = size.width() // 2
        text_list = '\n'.join(chunk_string(message, 10))
        self.text = QLabel(text_list)

        text_alignment = Qt.AlignBottom
        self.text.setAlignment(text_alignment)
        self.text.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)

        self.username = QLabel(f'{user_name}')
        self.username.setAttribute(Qt.WA_StyledBackground, True)

        if our_msg:
            self.username.setStyleSheet('background-color: lightgreen;')

            self.layout.addItem(QSpacerItem(half_w, 0), 0, 0)
            self.layout.addWidget(self.username, 0, 1)
            self.layout.addWidget(self.text, 1, 1)
        else:
            self.username.setStyleSheet('background-color: lightblue;')

            self.layout.addItem(QSpacerItem(half_w, 0), 0, 1)
            self.layout.addWidget(self.username, 0, 0)
            self.layout.addWidget(self.text, 1, 0)
        self.setLayout(self.layout)


class Chat(QWidget):
    def __init__(self, client):
        super(Chat, self).__init__()
        self.layout = QVBoxLayout()
        self.client = client
        self.recipient = None
        self.messages = None

        self.scroll = QScrollArea()

        self.current_recipient_label = QLabel()
        self.current_recipient_label.setFixedHeight(20)

        self.input_send = QWidget()
        self.input_send.layout = QHBoxLayout()
        self.input_send.setLayout(self.input_send.layout)

        self.input_send.input = QLineEdit()
        self.input_send.input.setPlaceholderText('Введите сообщение')
        self.input_send.send = QPushButton('Отправить')
        self.input_send.send.clicked.connect(self.send_message)

        self.input_send.layout.addWidget(self.input_send.input)
        self.input_send.layout.addWidget(self.input_send.send)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)

        self.layout.addWidget(self.current_recipient_label)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.input_send)

        self.setLayout(self.layout)

    def send_message(self):
        self.client.send_message(self.recipient, self.input_send.input.text())
        self.input_send.input.setText('')

    def update_messages(self, recipient, messages, size):
        if recipient is None and messages is None:
            return None

        if self.recipient is not None:
            self.scroll.msg_box.deleteLater()

        self.recipient = recipient
        self.current_recipient_label.setText(recipient)
        self.messages = messages

        msgbox = QWidget()
        msg_layout = QVBoxLayout()
        msgbox.setLayout(msg_layout)

        # Add spacers
        if size.height() - len(messages) * 100 > 0:
            msg_layout.addItem(QSpacerItem(0, size.height() - len(messages) * 100))

        for name, message in messages:
            cur_msg = QWidget()
            stacked = QStackedLayout()
            cur_msg.setLayout(stacked)

            frame = QFrame()
            frame.setStyleSheet("""QFrame {
                                     border: 1px solid #1f178f;
                                     }""")

            message = Message(message, name, size, name == self.client.name)
            stacked.addWidget(message)
            stacked.addWidget(frame)

            msg_layout.addWidget(cur_msg)

        self.scroll.msg_box = msgbox
        self.scroll.setWidget(msgbox)
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

    def __eq__(self, other):
        return self.name == other.name

    def event(self, e):
        if e.type() in (QEvent.Show, QEvent.Resize):
            size = self.geometry()
            self.update_messages(self.recipient, self.messages, size)

        return QWidget.event(self, e)
