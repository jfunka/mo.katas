
from orientation import Orientation, OrientationUtils


class Rover(object):

    pos_x = 0
    pos_y = 0
    orientation = Orientation.NORTH

    def __init__(self, start_x: int, start_y: int, orientation: Orientation):
        self.pos_x = start_x
        self.pos_y = start_y
        self.orientation = orientation

    def move(self, movs: str):
        for m in movs:
            if self.orientation == Orientation.NORTH:
                if m == "f":
                    self.pos_y = self.pos_y + 1
                else:
                    self.pos_y = self.pos_y - 1
            elif self.orientation == Orientation.SOUTH:
                if m == "f":
                    self.pos_y = self.pos_y - 1
                else:
                    self.pos_y = self.pos_y + 1
            elif self.orientation == Orientation.EAST:
                if m == "f":
                    self.pos_x = self.pos_x + 1
                else:
                    self.pos_x = self.pos_x - 1
            elif self.orientation == Orientation.WEST:
                if m == "f":
                    self.pos_x = self.pos_x - 1
                else:
                    self.pos_x = self.pos_x + 1

    def turn(self, turns: str):
        for turn in turns:
            self.orientation = OrientationUtils.turn_orientation(turn, self.orientation)