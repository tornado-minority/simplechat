import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer, Qt, QRect
from ..sub import from_json
from .AdditionalWindows import AddChatWindow
from .Chat import Chat


class ChatGUI(QMainWindow):
    def __init__(self, client):
        app = QApplication(sys.argv)
        super(ChatGUI, self).__init__()
        self.setWindowTitle("SimpleChat")
        self.setGeometry(500, 300, 500, 500)
        self.client = client
        self.main_widget = QWidget()
        self.chat = Chat(self.client)
        self.messages = None

        # self.client_name_label = QPushButton(self.client.name)
        self.client_name_label = QLabel(self.client.name)
        self.client_name_label.setStyleSheet("border: 1px solid black;")
        self.client_name_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.client_name_label.setFixedHeight(20)

        # Init chats list
        self.chats = QListWidget()
        for chat in client.chats:
            self.chats.addItem(chat)
        self.chats.itemClicked.connect(self.set_chat)

        # Init Update messages interval
        self.timer = QTimer()
        self.timer.timeout.connect(self.events)
        self.timer.setInterval(1000)
        self.timer.start()

        # Add toolbar
        toolbar = QToolBar("Чаты")
        self.addToolBar(toolbar)
        button_action = QAction("Добавить чат", self)
        button_action.setStatusTip("Нажмите, чтобы добавить чат")
        button_action.triggered.connect(self.add_chat_activate)
        toolbar.addAction(button_action)

        # Set status bar
        self.setStatusBar(QStatusBar(self))

        # Create chat-splitter
        self.chats_splitter = QSplitter(Qt.Horizontal)
        self.chats_splitter.addWidget(self.chats)
        self.chats_splitter.addWidget(self.chat)

        # Add layout
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.addWidget(self.client_name_label, stretch=1)
        self.layout.addWidget(self.chats_splitter)

        self.setCentralWidget(self.main_widget)

        # Show windows
        self.show()
        sys.exit(app.exec_())

    def set_chat(self, chat):
        self.client.chat = chat.text()
        self.display_messages()

    def add_chat_activate(self, s):
        add_chat_w = AddChatWindow(self.client.add_chat, self.update_chats)
        add_chat_w.show()

    def display_messages(self):
        if self.client.chat is not None:
            messages = self.client.get_messages(self.client.chat)
            if messages is not None and self.messages != messages:
                self.messages = messages
                self.chat.update_messages(self.client.chat, self.messages, self.chat.geometry())

    def get_chats(self):
        self.client.get_chats()
        self.update_chats()

    def update_chats(self):
        if self.chats.count() != len(self.client.chats):
            self.chats.clear()
            for chat in self.client.chats:
                self.chats.addItem(chat)
            self.chats.itemClicked.connect(self.set_chat)

    def events(self):
        self.display_messages()
        self.get_chats()


