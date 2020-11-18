import random

from enum import Enum


class Complexity:
    level: int
    width: int
    points: int
    curves: int

    def __init__(self, level, points, curves, width):
        self.level = level
        self.width = width
        self.points = points
        self.curves = curves + int(curves / random.randint(level, points))

    def __str__(self):
        return f"D{self.level}_{self.points}"


class TrackComplexity(Enum):
    D1 = Complexity(level=1, points=3, curves=5, width=10)
    D2 = Complexity(level=2, points=4, curves=10, width=10)
    D3 = Complexity(level=3, points=6, curves=20, width=8)

    @staticmethod
    def list():
        return list(map(lambda c: c, TrackComplexity))
