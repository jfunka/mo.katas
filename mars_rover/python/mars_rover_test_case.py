import unittest

from orientation import Orientation, OrientationUtils
from rover import Rover
from planet import Planet
from obstacle import Obstacle

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

    def test_planet_constructor(self):
        planet = Planet(3, 4)

        self.assertTrue(planet.size_x == 3)
        self.assertTrue(planet.size_y == 4)
        self.assertTrue(len(planet.obstacles) == 0)

    def test_planet_bounds(self):
        planet = Planet(3, 4)

        self.assertTrue(planet.is_inside_bounds(0, 0))
        self.assertTrue(planet.is_inside_bounds(0, 3))
        self.assertFalse(planet.is_inside_bounds(0, 4))
        self.assertFalse(planet.is_inside_bounds(3, 4))
        self.assertFalse(planet.is_inside_bounds(-1, 0))

    def test_planet_with_obstacles(self):
        size_x = 3
        size_y = 4
        obstacles = []
        obstacle_coords = [ (0, 0), (2, 3) ]
        for obs_coords in obstacle_coords:
            obstacles.append(Obstacle(obs_coords[0], obs_coords[1]))

        planet = Planet(size_x, size_y, obstacles)

        for obs in obstacles:
            self.assertTrue(planet.has_obstacle_at(obs.pos_x, obs.pos_y))

        for y in range(size_y):
            for x in range(size_x):
                if (x, y) in obstacle_coords:
                    self.assertTrue(planet.has_obstacle_at(x, y))
                else:
                    self.assertFalse(planet.has_obstacle_at(x, y))


class OrientationUtilsTestCase(unittest.TestCase):

    def test_single_turn(self):
        new_orientation = OrientationUtils.turn_orientation("l", Orientation.NORTH)
        self.assertTrue(new_orientation == Orientation.WEST)

    def test_all_possible_turns(self):
        test_input = [
            # ( (input_turn, input_orientation), expected_orientation )
            (("r", Orientation.NORTH), Orientation.EAST),
            (("r", Orientation.EAST), Orientation.SOUTH),
            (("r", Orientation.SOUTH), Orientation.WEST),
            (("r", Orientation.WEST), Orientation.NORTH),
            #
            (("l", Orientation.NORTH), Orientation.WEST),
            (("l", Orientation.WEST), Orientation.SOUTH),
            (("l", Orientation.SOUTH), Orientation.EAST),
            (("l", Orientation.EAST), Orientation.NORTH),
        ]
        for ((input_turn, input_orientation), expected_orientation) in test_input:
            new_orientation = OrientationUtils.turn_orientation(input_turn, input_orientation)
            self.assertTrue(new_orientation == expected_orientation)

    def test_incorrect_input_format(self):
        # lr is expected as turn
        # Orientation.obj is expected as orientation
        OrientationUtils.turn_orientation("a", "aa")
        self.assertRaises(ValueError, lambda: OrientationUtils.turn_orientation("a", Orientation.NORTH))

        self.assertRaises(ValueError, lambda: OrientationUtils.turn_orientation("l", "foo"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
