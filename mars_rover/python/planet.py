
from typing import List


class Planet(object):

    __OBSTACLE = "o"

    size_x = 0
    size_y = 0
    grid = None

    def __init__(self, grid: List[List[str]]):
        self.size_x = len(grid[0])
        self.size_y = len(grid)
        self.grid = grid

    def is_inside_bounds(self, test_x: int, test_y: int) -> bool:
        return 0 <= test_x < self.size_x and 0 <= test_y < self.size_y

    def has_obstacle_at(self, test_x: int, test_y: int) -> bool:
        if not self.is_inside_bounds(test_x, test_y):
            return False
        return self.grid[test_y][test_x] == self.__OBSTACLE
