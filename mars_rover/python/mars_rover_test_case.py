import unittest

from direction import *
from rover import Rover
from planet import Planet, Obstacle

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

    def setUp(self):
        position = Direction(0, 0, Orientation.NORTH)
        planet = Planet(3, 3)
        self.rover = Rover(position, planet)

    def assert_rover_position(self, rover, expected_position):
        self.assertTrue(len(expected_position) == 2)
        self.assertEqual(expected_position[0], rover.direction.position.x)
        self.assertEqual(expected_position[1], rover.direction.position.y)

    def test_rover_edge_cases(self):
        self.rover.move([])

        self.assert_rover_position(self.rover, (0, 0))

    def test_rover_move_forward(self):
        movements = "f"
        expected_position = (0, 1)

        self.rover.move(movements)

        self.assert_rover_position(self.rover, expected_position)

    def test_rover_move_multiforward(self):
        # (movement, position), expected_position
        planet = Planet(3, 3)
        test_input = [
            (("ff", Direction(0, 0, Orientation.NORTH)), (0, 2)),
            (("ff", Direction(0, 0, Orientation.EAST) ), (2, 0)),
            (("ff", Direction(0, 0, Orientation.SOUTH)), (0, 1)),
            (("ff", Direction(0, 0, Orientation.WEST) ), (1, 0)),
            (("fff", Direction(0, 0, Orientation.WEST) ), (0, 0)),
        ]
        for ((movement, position), expected_position) in test_input:
            rover = Rover(position, planet)
            rover.move(movement)
            self.assert_rover_position(rover, expected_position)

    def test_rover_move_backward(self):
        movements = "b"
        expected_position = (0, 2)

        self.rover.move(movements)

        self.assert_rover_position(self.rover, expected_position)

    @unittest.skip("not implemented")
    def test_rover_str_list_types_allowed(self):
        movs = "ffff"
        self.rover.move(movs)
        self.assert_rover_position(self.rover, (0, 1))

        movs = ["b", "b", "b", "b"]
        self.rover.move(movs)
        self.assert_rover_position(self.rover, (0, 0))


class TurningRoverTestCase(unittest.TestCase):

    def assert_rover_orientation(self, rover, expected_orientation):
        self.assertTrue(rover.direction.orientation == expected_orientation)

    def setUp(self):
        position_north = Direction(0, 0, Orientation.NORTH)
        position_east = Direction(0, 0, Orientation.EAST)
        planet = Planet(3, 3)
        self.rover_north = Rover(position_north, planet)
        self.rover_east = Rover(position_east, planet)

    def test_rover_edge_cases(self):
        self.rover_north.turn("")
        self.assert_rover_orientation(self.rover_north, Orientation.NORTH)

    def test_rover_random_turns(self):
        self.rover_north.turn("r")
        self.assert_rover_orientation(self.rover_north, Orientation.EAST)

        self.rover_north.turn("l")
        self.assert_rover_orientation(self.rover_north, Orientation.NORTH)

        self.rover_north.turn("lrlr")
        self.assert_rover_orientation(self.rover_north, Orientation.NORTH)

    def test_rover_circular_turns(self):
        self.rover_east.turn("llll")
        self.assert_rover_orientation(self.rover_east, Orientation.EAST)

        self.rover_east.turn("rrrr")
        self.assert_rover_orientation(self.rover_east, Orientation.EAST)

    def test_rover_incorrect_arg_turns(self):
        self.assertRaises(ValueError, lambda: self.rover_east.turn("L"))
        self.assertRaises(ValueError, lambda: self.rover_east.turn("a"))

        self.rover_east.turn("r")
        self.assert_rover_orientation(self.rover_east, Orientation.SOUTH)

    def test_aaa(self):
        self.rover_east.turn("r")
        x = self.rover_east.direction.orientation
        self.assert_rover_orientation(self.rover_east, Orientation.SOUTH)


class PlanetTestCase(unittest.TestCase):

    def test_planet_constructor(self):
        planet = Planet(3, 4)

        self.assertTrue(planet.size_x == 3)
        self.assertTrue(planet.size_y == 4)
        self.assertTrue(len(planet.obstacles) == 0)

    def test_planet_with_obstacles(self):
        size_x = 3
        size_y = 4
        obstacles = []
        obstacle_coords = [ (0, 0), (2, 3) ]
        for obs_coords in obstacle_coords:
            obstacles.append(Obstacle(obs_coords[0], obs_coords[1]))

        planet = Planet(size_x, size_y, obstacles)

        for obs in obstacles:
            self.assertTrue(planet.has_obstacle_at(obs))

        for y in range(size_y):
            for x in range(size_x):
                test_obs = Obstacle(x, y)
                if (x, y) in obstacle_coords:
                    self.assertTrue(planet.has_obstacle_at(test_obs))
                else:
                    self.assertFalse(planet.has_obstacle_at(test_obs))

@unittest.skip("deprecated")
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
