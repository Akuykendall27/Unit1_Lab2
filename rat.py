class Rat():
    def __init__(self, sex:str, weight:int):
        self.sex = sex
        self.weight = weight
        self.litters = 0
    def __str__(self):
        return str(self.weight)
    def __repr__(self):
        return str(self.weight)
    def __lt__(self, other):
        return self.weight < other
    def __gt__(self, other):
        return self.weight > other
    def __le__(self, other):
        return self.weight <= other
    def __ge__(self, other):
        return self.weight >= other
    def __eq__(self, other):
        return self.weight == other
    def getWeight(self):
        return self.weight
    def getSex(self):
        return self.sex
    def canBreed(self):
        return self.litters <= 5
