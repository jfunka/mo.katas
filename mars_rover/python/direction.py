
from enum import Enum


class Position(object):

    def __init__(self, x: int = 0, y: int = 0):
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

    __move_forward = {
        Orientation.NORTH: Position(0, +1),
        Orientation.SOUTH: Position(0, -1),
        Orientation.EAST:  Position(+1, 0),
        Orientation.WEST:  Position(-1, 0),
    }

    __move_backward = {
        Orientation.NORTH: Position(0, -1),
        Orientation.SOUTH: Position(0, +1),
        Orientation.EAST:  Position(-1, 0),
        Orientation.WEST:  Position(+1, 0),
    }

    __orientation_order = [
        Orientation.NORTH,
        Orientation.EAST,
        Orientation.SOUTH,
        Orientation.WEST
    ]

    # Assert size not zero
    __orientation_order_size = len(__orientation_order)

    def __init__(self, position_x: int, position_y: int, orientation: Orientation,
            limit_x: int = -1, limit_y: int = -1):
        self.position = Position(position_x, position_y)
        self.orientation = orientation
        self.__limit_x = limit_x
        self.__limit_y = limit_y

    def __move(self, move_direction_map: dict) -> Position:
        # Get move step in X and Y
        # XXX: Wrap into a function?
        next_move = move_direction_map.get(self.orientation, None)
        if next_move is None:
            raise ValueError(f"Current orientation='{self.orientation}' not found in " \
                f"'{move_direction_map.keys()}'")
        # Update
        next_position = Position()
        next_position.x = next_move.x + self.position.x
        next_position.y = next_move.y + self.position.y
        if self.__limit_x > 0:
            next_position.x = next_position.x % self.__limit_x
        if self.__limit_y > 0:
            next_position.y = next_position.y % self.__limit_y
        return next_position

    def __turn(self, turn_direction: int) -> Orientation:
        # Get next orientation in direction
        # XXX: Wrap into a function?
        try:
            orientation_index = self.__orientation_order.index(self.orientation)
        except ValueError:
            # Modify exception message, test isinstance(orientation, Orientation)...
            raise ValueError(f"Current orientation='{self.orientation}' not found in " \
                f"'{self.__orientation_order}'")
        # Update
        # XXX: Division by zero
        orientation_index = (orientation_index + turn_direction) % self.__orientation_order_size
        # XXX: 0 <= orientation_index < __orientation_order_size is asserted, but could be added
        return self.__orientation_order[orientation_index]

    def set_limit_x(self, other):
        self.__limit_x = other

    def set_limit_y(self, other):
        self.__limit_y = other

    def next_position_forward(self) -> Position:
        return self.__move(self.__move_forward)

    def next_position_backward(self) -> Position:
        return self.__move(self.__move_backward)

    def next_orientation_left(self) -> Orientation:
        return self.__turn(-1)

    def next_orientation_right(self) -> Orientation:
        return self.__turn(+1)