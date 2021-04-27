class Card():
    def __init__(self, number, value, sign):
        self.number = number
        self.value = value
        self.sign = sign

    def __str__(self):
        return '[{} {}]'.format(self.value, self.sign)
