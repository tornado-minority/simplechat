import socket
from .gui.ChatGUI import ChatGUI
import json
from .sub import from_json
from time import time, sleep
from .info import info
from warnings import warn

buf_size = 1024


class Client:
    def __init__(self, name: str, server_addr: tuple):
        self.name = name
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.settimeout(1)
        self.server_addr = (server_addr[0], server_addr[1])
        self.chats = None
        self.chat = None

        info('Waiting for connection...')
        self.connect()
        while self.chats is None:
            info('Reconnecting...')
            self.connect()
            sleep(1)
        info('Connection successful!')

    def send_command(self, command: str):
        msg = bytes(command, 'utf-8')
        for pings in range(10):
            self.server.sendto(msg, self.server_addr)
            try:
                ans, addr = self.server.recvfrom(1024)
                break
            except socket.timeout:
                ans = None
                info('REQUEST TIMED OUT')
            except ConnectionResetError:
                ans = None
                warn('Cannot connect to server')
                break
        return ans

    def add_chat(self, chat: str):
        chat = str(chat.replace(' ', '').split(','))
        ans = self.send_command(f'create;{chat}')

        ID, found_users = from_json(ans)
        if ID == '-1':
            info('User not found')
        else:
            self.chats.insert(0, ', '.join(found_users))

    def send_message(self, chat_id, message):
        if self.chat is not None:
            ans = self.send_command(f'send;{chat_id};{message}')
            if ans is not None:
                info('Message sent')

    def get_messages(self, chat):
        ans = self.send_command(f'get;{str(chat)}')
        messages = from_json(ans)
        return messages

    def get_chats(self):
        ans = self.send_command(f'get_chats;')
        if ans != b'':
            self.chats = from_json(text=ans)

    def connect(self):
        ans = self.send_command(f'connect;{self.name}')
        if ans is not None:
            self.chats = from_json(text=ans)
