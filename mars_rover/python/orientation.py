
from enum import Enum


class Orientation(Enum):

    NORTH = "N"
    SOUTH = "S"
    EAST  = "E"
    WEST  = "W"


class OrientationUtils(object):
    """
    Orientation:
          N
        W   E -> NESW clockwise
          S
    """
    __orientation_order = [
        Orientation.NORTH,
        Orientation.EAST,
        Orientation.SOUTH,
        Orientation.WEST
    ]
    __orientation_size = len(__orientation_order)

    # 'l' = Left  = circular movement 'counter-clockwise'
    # 'r' = Right = circular movement 'clockwise'
    __turn_direction = {
        'l': -1,
        'r': +1
    }

    @staticmethod
    def turn_orientation(turn: str, orientation: Orientation) -> Orientation:
        """
        Modifies {orientation} in the {turn} direction defined by the {OrientationUtils.__orientation_order}.
        """
        direction = OrientationUtils.__turn_direction.get(turn, None)
        if direction is None:
            raise ValueError(f"Input turn='{turn}' not found in " \
                f"{OrientationUtils.__turn_direction.keys()}")

        try:
            orientation_ptr = OrientationUtils.__orientation_order.index(orientation)
        except ValueError:
            # Modify exception message, test isinstance(orientation, Orientation)...
            raise ValueError(f"Input orientation='{orientation}' not found in " \
                f"{OrientationUtils.__orientation_order}")

        orientation_ptr = (orientation_ptr + direction) % OrientationUtils.__orientation_size

        return OrientationUtils.__orientation_order[orientation_ptr]