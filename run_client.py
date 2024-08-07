from src.gui.ChatGUI import ChatGUI
from src.client import Client
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='SimpleChat',
        description='A chat application written with pyqt5',
        epilog='tornadominoritycode@gmail.com')

    parser.add_argument('-n', '--name', type=str, help='Your name in SimpleChat')  # option that takes a value
    parser.add_argument('-ip', default='127.0.0.1', help='Server ip address')
    parser.add_argument('-p', '--port', type=int, help='Server port',  default=12000)

    args = parser.parse_args()

    cli = Client(args.name, (args.ip, args.port))
    ChatGUI(cli)
