import unittest

from rover import Rover
from planet import Planet

"""
Mars rover moves through


                       N
        --------------------------------
        |   0,2   |   1,2   |   2,2    |
        -------------------------------- 
    W   |   0,1   |   1,1   |   2,1    |    E
        -------------------------------- 
        |   0,0   |   1,0   |   2,0    |
        --------------------------------
                       S
                   
"""


class MarsRoverTestCase(unittest.TestCase):
    def test_rover_move_forward(self):
        rover = Rover(
            start_x=1,
            start_y=1,
            orientation='N'
        )

        movements = ['f']
        expected_position = (1, 2)
        rover.move(movements)

        self.assert_rover_position(expected_position, rover)

    def assert_rover_position(self, expected_position, rover):
        self.assertEqual(expected_position[0], rover.x)
        self.assertEqual(expected_position[1], rover.y)


class PlanetTestCase(unittest.TestCase):

    def test_planet(self):
        grid = [
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.']
        ]
        planet = Planet(grid)

        self.assertEqual(planet.grid, grid)
        self.assertEqual(planet.size_x, len(grid[0]))
        self.assertEqual(planet.size_y, len(grid))

    def test_planet_with_obstacles(self):
        grid = [
            ['o', '.'],
            ['.', '.']
        ]
        planet = Planet(grid)

        self.assertTrue(planet.has_obstacle_at(0, 0))
        self.assertFalse(planet.has_obstacle_at(0, 1))

if __name__ == '__main__':
    unittest.main(verbosity=2)
