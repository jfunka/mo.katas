
from enum import Enum

from direction import Direction
from planet import Planet


class Commands(Enum):

    MOVE_FORWARD  = "f"
    MOVE_BACKWARD = "b"

    TURN_LEFT  = "l"
    TURN_RIGHT = "r"

    def __eq__(self, other: Enum):
        # To compare value Enum.value if str
        if isinstance(other, str):
            return other == self.value
        return other.name == self.name and \
            other.value == self.value


class Rover(object):

    def __init__(self, direction: Direction, planet: Planet):
        self.direction = direction
        self.planet = planet

        self.direction.set_limit_x(planet.size_x)
        self.direction.set_limit_y(planet.size_y)

    def move(self, move_commands: str):
        for cmd in move_commands:
            if cmd == Commands.MOVE_FORWARD:
                next_position = self.direction.next_position_forward()
            elif cmd == Commands.MOVE_BACKWARD:
                next_position = self.direction.next_position_backward()
            else:
                raise ValueError(f"Invalid move command='{cmd}'.")

            if self.planet.has_obstacle_at(next_position):
                print(f"Warning: Obstacle found at='{next_position}'... aborting.")
                break

            self.direction.position = next_position

    def turn(self, turn_commands: str):
        for cmd in turn_commands:
            if cmd == Commands.TURN_LEFT:
                next_orientation = self.direction.next_orientation_left()
            elif cmd == Commands.TURN_RIGHT:
                next_orientation = self.direction.next_orientation_right()
            else:
                raise ValueError(f"Invalid turn command='{cmd}'.")

            self.direction.orientation = next_orientation