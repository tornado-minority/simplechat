from datetime import datetime


def info(msg):
    print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} {msg}')
