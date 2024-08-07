import json


def from_json(text):
    text = text.decode('utf-8').replace("'", '"')
    text = json.loads(text)
    return text

