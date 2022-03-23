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

    def assert_rover_position(self, rover, expected_position):
        self.assertTrue(len(expected_position) == 2)
        self.assertEqual(expected_position[0], rover.direction.position.x)
        self.assertEqual(expected_position[1], rover.direction.position.y)

    def setUp(self):
        position = Direction(0, 0, Orientation.NORTH)
        self.planet = Planet(3, 3)
        self.rover = Rover(position, self.planet)

    def test_rover_edge_cases(self):
        self.rover.move([])

        self.assert_rover_position(self.rover, (0, 0))

    def test_rover_move_forward(self):
        moves = "f"
        expected_position = (0, 1)

        self.rover.move(moves)

        self.assert_rover_position(self.rover, expected_position)

    def test_rover_move_multiforward(self):
        # (movement, direction), expected_position
        planet = Planet(3, 3)
        test_input = [
            (("ff", Direction(0, 0, Orientation.NORTH)), (0, 2)),
            (("ff", Direction(0, 0, Orientation.EAST) ), (2, 0)),
            (("ff", Direction(0, 0, Orientation.SOUTH)), (0, 1)),
            (("ff", Direction(0, 0, Orientation.WEST) ), (1, 0)),
            (("fff", Direction(0, 0, Orientation.WEST) ), (0, 0)),
        ]
        for ((movement, direction), expected_position) in test_input:
            rover = Rover(direction, planet)
            rover.move(movement)
            self.assert_rover_position(rover, expected_position)

    def test_rover_move_backward(self):
        moves = "b"
        expected_position = (0, 2)

        self.rover.move(moves)

        self.assert_rover_position(self.rover, expected_position)

    def test_rover_str_list_types_allowed(self):
        moves = "ffff"
        self.rover.move(moves)
        self.assert_rover_position(self.rover, (0, 1))

        moves = ["b", "b", "b", "b"]
        self.rover.move(moves)
        self.assert_rover_position(self.rover, (0, 0))

    def test_rover_didnt_move(self):
        moves = "ffbb"
        self.rover.move(moves)
        self.assert_rover_position(self.rover, (0, 0))

    def test_rover_random_move(self):
        moves = "ffbfbf"
        rover = Rover(Direction(0, 0, Orientation.EAST), self.planet)
        rover.move(moves)
        self.assert_rover_position(rover, (2, 0))

        moves = "ff"
        rover = Rover(Direction(0, 0, Orientation.EAST), self.planet)
        rover.move(moves)
        self.assert_rover_position(rover, (2, 0))

    def test_rover_incorrect_arg_moves(self):
        self.assertRaises(ValueError, lambda: self.rover.move("F"))
        self.assertRaises(ValueError, lambda: self.rover.move("a"))


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


class MoveTurnRoverTestCase(unittest.TestCase):

    def assert_rover_position(self, rover, expected_position):
        self.assertTrue(len(expected_position) == 2)
        self.assertEqual(expected_position[0], rover.direction.position.x)
        self.assertEqual(expected_position[1], rover.direction.position.y)

    def assert_rover_orientation(self, rover, expected_orientation):
        self.assertTrue(rover.direction.orientation == expected_orientation)

    def setUp(self):
        planet = Planet(3, 3)
        self.rover = Rover(Direction(0, 0, Orientation.NORTH), planet)

    def test_rover_move_L(self):
        command_sequence = "frf"
        for cmd in command_sequence:
            if cmd in "lr":
                self.rover.turn(cmd)
            else:
                self.assertTrue(cmd in "fb")
                self.rover.move(cmd)

        self.assert_rover_position(self.rover, (1, 1))
        self.assert_rover_orientation(self.rover, Orientation.EAST)

    def test_rover_move_in_a_circle(self):
        command_sequence = "frfrfrfr"
        for cmd in command_sequence:
            if cmd in "lr":
                self.rover.turn(cmd)
            else:
                self.assertTrue(cmd in "fb")
                self.rover.move(cmd)

        self.assert_rover_position(self.rover, (0, 0))
        self.assert_rover_orientation(self.rover, Orientation.NORTH)

    def test_rover_move_back_and_forth(self):
        command_sequence = "fflbblffrffr"
        for cmd in command_sequence:
            if cmd in "lr":
                self.rover.turn(cmd)
            else:
                self.assertTrue(cmd in "fb")
                self.rover.move(cmd)

        self.assert_rover_position(self.rover, (0, 0))
        self.assert_rover_orientation(self.rover, Orientation.NORTH)


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

if __name__ == '__main__':
    unittest.main(verbosity=2)
