import math


class Curve:
    def __init__(self, start_value, end_value, length):
        self.frame = 0
        self.last_frame = length - 1
        self.length = length
        self.start = start_value
        self.end = end_value


class Sine(Curve):
    def __init__(self, start_value, end_value, length):
        super().__init__(start_value, end_value, length)
        self.k = 1
        self.a = 1
        self.c = 0
        self.d = 0

    def value_at(self, frame):
        inside = self.k * frame - self.d
        return self.a * math.sin(inside) + self.c

    @property
    def current_value(self):
        return self.value_at(self.frame)


class SineOut(Sine):
    def __init__(self, start_value, end_value, length):
        super().__init__(start_value, end_value, length)
        self.k = (2 * math.pi) / (length * 4)
        self.a = end_value - start_value
        self.c = start_value
