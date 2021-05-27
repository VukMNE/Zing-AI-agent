from json import JSONEncoder
import json

class Card():
    def __init__(self, number, value, sign):
        self.number = number
        self.value = value
        self.sign = sign

    def __str__(self):
        return '[{} {}]'.format(self.value, self.sign)

    def __eq__(self, other):
        if self.number == other.number and self.value == other.value and self.sign == other.sign:
            return True
        return False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class CardEncoder(JSONEncoder):

    def default(self, object):
        if isinstance(object, Card):
            return object.__dict__

        else:
            return json.JSONEncoder.default(self, object)