class Card():
    def __init__(self, value, sign):
        self.value = value
        self.sign = sign

    def __str__(self):
        return '{}, {}'.format(self.value, self.sign)
