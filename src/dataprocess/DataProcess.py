import json
import os


class DataProcess:
    def __init__(self, path: str, obj: type = None):
        if not os.path.exists(path):
            with open(path, 'w') as fp:
                json.dump(obj, fp)

        self.path = path

    def read(self) -> type:
        with open(self.path, 'r') as fp:
            data = json.load(fp)
        return data

    def save(self, data):
        with open(self.path, 'r') as fp:
            json.dump(data, fp)
