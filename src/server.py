from .dataprocess.DataProcess import DataProcess
from typing import Tuple, List, Dict
from info import info
import socket
import json
import os


ChatId = int
ChatList = List[ChatId]
UserName = str
Users = Dict[UserName, ChatList]
BytesChatList = lambda chat_list: bytes(chat_list, 'utf-8')
Messages = list
LastChatID = 0
AuthorMessage = List[UserName, str]
Chat = List[AuthorMessage]


class Server:
    def __init__(self, chats_names_path: str, users_path: str, chats_path: str, port: int = 12000, buf_size: int = 1024):
        self.server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('', port))

        self.chat_names: DataProcess = DataProcess(chats_names_path, [])
        self.users: DataProcess = DataProcess(users_path, {})
        self.chats_path = chats_path
        self.chats: List[DataProcess] = [DataProcess(os.path.join(chats_path, chat_i))
                                         for chat_i in sorted(os.listdir(chats_path))]

        self.buf_size: int = buf_size
        self.current_connections: Dict[str, bytes] = {}
        self.chat_ids: Dict[int, str] = {}

    def receive_packet(self) -> Tuple[str, bytes]:
        """
        Receive packet from client with declared buffer size

        :return: utf-8 message, bytes address
        """
        message, address = self.server_socket.recvfrom(self.buf_size)
        message = message.decode('utf-8')
        return message, address

    @staticmethod
    def get_command(message: str) -> Tuple[str, str]:
        """
        Split message by command and sub-info

        :return: utf-8 command, utf-8 sub-info
        """
        return message.split(';', maxsplit=1)

    def chat_names_by_ids(self, name: str) -> List[str]:
        """
        Get given user chat names by ids and saves it in current chat ids

        :param name: Name of user
        :return: List of chat names
        """
        chat_names = self.chat_names.read()
        users = self.users.read()

        user_chat_names = [', '.join(chat_names[ID]) for ID in users[name]]
        self.chat_ids = dict(zip(user_chat_names, users[name]))
        return user_chat_names

    def append_chat(self):
        """
        Appends new chat
        """
        chat_path = os.path.join(self.chats_path, str(len(self.chats)))
        self.chats.append(DataProcess(chat_path, Messages()))

    def connect(self, name: str, address: bytes):
        info(f'Connected with ip: {address}')

        # Add user to current connections
        self.current_connections[address] = name
        users: dict = self.users.read()
        if name not in users:
            info(f'User {name} is not found')

            # Add new user
            cur_chat_list = ChatList()
            users.update({name: cur_chat_list})
            self.users.save(users)

            info(f'User {name} added to database')

            # Make response
            cur_chats_names = BytesChatList(cur_chat_list)
        else:
            info(f'User {name} loaded from database')

            # Get chat names that will show in GUI by IDS
            user_chat_names = self.chat_names_by_ids(name)
            cur_chats_names = BytesChatList(str(user_chat_names))

            info(f'User {name} chats extracted')

        # Send chat names
        self.server_socket.sendto(cur_chats_names, address)

        info(f'Current chats sent to user: {name}')

    def create(self, message: str, address: bytes):
        # Get current connection
        name = self.current_connections[address]
        info(f'Create, user name {name}: command recieved')

        # Find given users in server data
        got_users = json.loads(message.replace("'", '"'))
        users: Dict[str, List[]] = self.users.read()
        found_users = [chat_user for chat_user in got_users if chat_user in users]
        info(f'Create, user name {name}: Found users {str(found_users)}')
        if found_users:
            found_users.append(name)

            # Dump new chat to server data
            chat_names: list = self.chat_names.read()
            chat_names.append(found_users)
            self.chat_names.save(chat_names)
            self.append_chat()
            info(f'Command - create: user name {name} - with users {str(found_users)}')

            # Dump new chat to users
            chat_id = chat_names[found_users]
            for user in users.values():
                user.insert(LastChatID, chat_id)
            self.

            info(f'Create, user name {name}: chat id {str(chat_id)} dumped to users {str(found_users)}')

            chat_ids[name] = {', '.join(chats[int(ID)]): str(ID) for ID in users[name]}
            for found_user in found_users:
                chat_ids[found_user] = {', '.join(chats[int(ID)]): str(ID) for ID in users[found_user]}

            answer = bytes(str([chat_id, found_users]), 'utf-8')
            server_socket.sendto(answer, address)
        else:
            answer = bytes(str(['-1', '']), 'utf-8')
            server_socket.sendto(answer, address)
            info(f'Create, user name {name}: participants not found sent to user')

    def run(self):
        info('Server started!')
        while True:
            message, address = self.receive_packet()

            command, other = Server.get_command(message)
            if command == 'connect':
                self.connect(other, address)
            elif command == 'create':
                self.create(other, address)
            elif command == 'send':
                name = current_connections[address]

                chat, message = other.split(';', maxsplit=1)
                chat = chat_ids[name][chat]
                chat_path = os.path.join(SERVER_DATA, chat)

                if os.path.exists(chat_path):
                    with open(chat_path, 'r') as fp:
                        messages = json.load(fp)
                    messages.append((name, message))
                    with open(chat_path, 'w') as fp:
                        json.dump(messages, fp)
                else:
                    messages = [(name, message)]
                    with open(chat_path, 'w') as fp:
                        json.dump(messages, fp)

                server_socket.sendto(b'', address)
            elif command == 'get':
                name = current_connections[address]

                chat = chat_ids[name][other]
                chat_path = os.path.join(SERVER_DATA, chat)
                if os.path.exists(chat_path):
                    with open(chat_path, 'r') as fp:
                        messages = fp.read()

                    messages = bytes(str(messages), 'utf-8')
                    server_socket.sendto(messages, address)
                else:
                    server_socket.sendto(b'', address)
            elif command == 'get_chats':
                name = current_connections[address]

                with open(USERS, 'r') as fp:
                    users = json.load(fp)

                if name in chat_ids:
                    chat_ids[name] = {', '.join(chats[int(ID)]): str(ID) for ID in users[name]}
                    cur_chats = bytes(str(list(chat_ids[name].keys())), 'utf-8')
                    info(f'User {name} chats extracted')

                    server_socket.sendto(cur_chats, address)
                else:
                    server_socket.sendto(b'', address)


