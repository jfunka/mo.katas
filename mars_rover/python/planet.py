
from typing import List

from direction import Position


Obstacle = Position

class Planet(object):

    def __init__(self, size_x: int = 0, size_y: int = 0, obstacles: List[Obstacle] = []):
        self.size_x = size_x
        self.size_y = size_y
        self.obstacles = obstacles

    def has_obstacle_at(self, test_obstacle: Obstacle) -> bool:
        # XXX: Bound checking, do we need it?
        return any([ test_obstacle == obs for obs in self.obstacles ])
