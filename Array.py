class Array:
    def __init__(self, name, sz, minVal, maxVal):
        self.name = name
        self.sz = sz
        self.minVal = int(minVal)
        self.maxVal = int(maxVal)

    def __repr__(self):
        return f"{self.name} {self.sz} {self.minVal} {self.maxVal}"
