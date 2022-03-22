
from obstacle import Obstacle

from typing import List


class Planet(object):

    size_x = 0
    size_y = 0
    obstacles = []

    def __init__(self, size_x, size_y, obstacles: List[Obstacle] = []):
        self.size_x = size_x
        self.size_y = size_y
        self.obstacles = obstacles

    def is_inside_bounds(self, test_x: int, test_y: int) -> bool:
        return 0 <= test_x < self.size_x and 0 <= test_y < self.size_y

    def has_obstacle_at(self, test_x: int, test_y: int) -> bool:
        return any([
            test_x == obs.pos_x and test_y == obs.pos_y \
                for obs in self.obstacles
        ])
