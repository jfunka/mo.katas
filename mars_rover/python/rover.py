
def turn_orientation(turn: str, orientation: str, orientation_map: str = "NESW"):
    # check errors
    if turn not in "lr":
        print(f"Warning: input turn={turn} not in 'lr'")
        return orientation

    orientation_index = orientation_map.find(orientation)
    if orientation_index < 0:
        print(f"Warning: input orientaion={orientation} not defined in orientation_map={orientation_map}")
        return orientation

    if turn == "l":
        orientation_index = (orientation_index - 1) % len(orientation_map)
    else:
        orientation_index = (orientation_index + 1) % len(orientation_map)

    return orientation_map[orientation_index]


class Rover(object):

    x = 0
    y = 0
    orientation = 'N'

    def __init__(self, start_x, start_y, orientation):
        self.x = start_x
        self.y = start_y
        self.orientation = orientation

    def move(self, movs):
        for m in movs:
            if self.orientation == "N":
                if m == "f":
                    self.y = self.y + 1
                else:
                    self.y = self.y - 1
            elif self.orientation == "S":
                if m == "f":
                    self.y = self.y - 1
                else:
                    self.y = self.y + 1
            elif self.orientation == "E":
                if m == "f":
                    self.x = self.x + 1
                else:
                    self.x = self.x - 1
            elif self.orientation == "W":
                if m == "f":
                    self.x = self.x - 1
                else:
                    self.x = self.x + 1

    def turn(self, turns: str):
        for t in turns:
            self.orientation = turn_orientation(t, self.orientation)