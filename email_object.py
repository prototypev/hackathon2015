import json


class Email:
    def __init__(self, message_id):
        self.id = message_id

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
