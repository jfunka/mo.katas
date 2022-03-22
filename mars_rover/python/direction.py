
from enum import Enum


class Position(object):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return isinstance(other, Position) and \
            self.x == other.x and self.y == other.y


class Orientation(Enum):

    NORTH = "N"
    SOUTH = "S"
    EAST  = "E"
    WEST  = "W"


class Direction(object):

    __orientation_order = [
        Orientation.NORTH,
        Orientation.EAST,
        Orientation.SOUTH,
        Orientation.WEST
    ]

    __orientation_order_size = len(__orientation_order)

    def __init__(self, position_x: int, position_y: int, orientation: Orientation):
        self.position = Position(position_x, position_y)
        self.orientation = orientation

    def __get_orientation_index(self):
        try:
            orientation_ptr = self.__orientation_order.index(self.orientation)
        except ValueError:
            # Modify exception message, test isinstance(orientation, Orientation)...
            raise ValueError(f"Current orientation='{self.orientation}' not found in " \
                f"{self.__orientation_order}")
        return orientation_ptr

    def __turn(self, orientation_index: int, turn_direction: int) -> Orientation:
        # XXX: Division by zero
        orientation_index = (orientation_index + turn_direction) % self.__orientation_order_size
        return self.__orientation_order[orientation_index]

    def __move(self, move_x: int, move_y: int, clamp_x: int, clamp_y: int):
        pass

    def move_forward(self):
        pass

    def move_backward(self):
        pass

    def turn_left(self):
        # Gets the current orientation and turns it.
        # Leave the exception raised.
        self.orientation = self.__turn(self.__get_orientation_index(), -1)

    def turn_right(self):
        # Same as {turn_left}
        self.orientation = self.__turn(self.__get_orientation_index(), +1)
