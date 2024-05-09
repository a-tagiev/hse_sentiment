import random


class Model:
    def __init__(self):
        ...

    def predict(self, text: str) -> int:
        return random.randint(-1, 1)


model = Model()
