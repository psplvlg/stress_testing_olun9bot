import random


class Variable:
    def __init__(self, name, minVal, maxVal):
        self.name = name
        self.minVal = int(minVal)
        self.maxVal = int(maxVal)

    def generate(self):
        return random.randint(self.minVal, self.maxVal)

    def __repr__(self):
        return f"{self.name} {self.minVal} {self.maxVal}"


