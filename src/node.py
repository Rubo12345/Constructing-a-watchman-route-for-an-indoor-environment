import math


class Node:
    def __init__(self, x, y, inside, h):
        self.x = x
        self.y = y
        self.inside = inside
        self.h = h
        self.g = math.inf
        self.cost = None
        self.parent = None