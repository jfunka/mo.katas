
from enum import Enum
from direction import Orientation, Position, Direction
from planet import Planet


class Commands(Enum):

    MOVE_FORWARD  = "f"
    MOVE_BACKWARD = "b"

    TURN_LEFT  = "l"
    TURN_RIGHT = "r"

    def __eq__(self, other):
        # To compare value Enum.value if str
        if isinstance(other, str):
            return other == self.value
        return other.name == self.name and \
            other.value == self.value


class Rover(object):

    direction = Direction(0, 0, Orientation.NORTH)
    planet = None

    def __init__(self, direction: Direction, planet: Planet):
        self.direction = direction
        self.planet = planet

    def move(self, move_commands: str):
        for cmd in move_commands:
            if cmd == Commands.MOVE_FORWARD:
                pass
            elif cmd == Commands.MOVE_BACKWARD:
                pass
            else:
                raise ValueError(f"Invalid move command='{cmd}'.")

    def turn(self, turn_commands: str):
        for cmd in turn_commands:
            if cmd == Commands.TURN_LEFT:
                self.direction.turn_left()
            elif cmd == Commands.TURN_RIGHT:
                self.direction.turn_right()
            else:
                raise ValueError(f"Invalid turn command='{cmd}'.")