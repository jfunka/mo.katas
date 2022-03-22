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

class MovingRoverTestCase(unittest.TestCase):

    def assert_rover_position(self, expected_position, rover):
        self.assertTrue(len(expected_position) == 2)
        self.assertEqual(expected_position[0], rover.pos_x)
        self.assertEqual(expected_position[1], rover.pos_y)

    def test_rover_edge_cases(self):
        rover = Rover(0, 0, Orientation.NORTH)

        rover.move([])

        self.assert_rover_position((0, 0), rover)

    def test_rover_move_forward(self):
        rover = Rover(start_x=1, start_y=1, orientation=Orientation.NORTH)

        movements = ['f']
        expected_position = (1, 2)
        rover.move(movements)

        self.assert_rover_position(expected_position, rover)

    def test_rover_str_list_types_allowed(self):
        rover = Rover(0, 0, Orientation.NORTH)

        movs = "ffff"
        rover.move(movs)
        self.assert_rover_position((0, 4), rover)

        movs = ["b", "b", "b", "b"]
        rover.move(movs)
        self.assert_rover_position((0, 0), rover)


class TurningRoverTestCase(unittest.TestCase):

    def test_rover_edge_cases(self):
        rover = Rover(0, 0, Orientation.NORTH)
        rover.turn("")
        self.assertTrue(rover.orientation == Orientation.NORTH)

    def test_rover_random_turns(self):
        rover = Rover(0, 0, Orientation.NORTH)

        rover.turn("r")
        self.assertTrue(rover.orientation == Orientation.EAST)

        rover.turn("l")
        self.assertTrue(rover.orientation == Orientation.NORTH)

        rover.turn("lrlr")
        self.assertTrue(rover.orientation == Orientation.NORTH)

    def test_rover_circular_turns(self):
        rover = Rover(0, 0, Orientation.EAST)

        rover.turn("llll")
        self.assertTrue(rover.orientation == Orientation.EAST)

        rover.turn("rrrr")
        self.assertTrue(rover.orientation == Orientation.EAST)

    def test_rover_incorrect_arg_turns(self):
        rover = Rover(0, 0, Orientation.EAST)

        self.assertRaises(ValueError, lambda: rover.turn("L"))
        self.assertRaises(ValueError, lambda: rover.turn("a"))

        rover.turn("r")
        self.assertTrue(rover.orientation == Orientation.SOUTH)


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
        self.assertRaises(ValueError, lambda: OrientationUtils.turn_orientation("a", Orientation.NORTH))

        self.assertRaises(ValueError, lambda: OrientationUtils.turn_orientation("l", "foo"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
