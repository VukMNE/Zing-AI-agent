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