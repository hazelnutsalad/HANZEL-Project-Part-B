from enum import Enum

from referee.game import Direction


class DirectionOffset(Enum):
    """
    Enum which contains the offsets for each possible direction
    """
    UpLeft = -9
    Up = -8
    UpRight = -7
    Right = 1
    DownRight = 9
    Down = 8
    DownLeft = 7
    Left = -1

    # converts to Direction
    def convert_to_direction(self):
        match self:
            case DirectionOffset.UpLeft:
                return Direction.UpLeft
            case DirectionOffset.Up:
                return Direction.Up
            case DirectionOffset.UpRight:
                return Direction.UpRight
            case DirectionOffset.Right:
                return Direction.Right
            case DirectionOffset.DownRight:
                return Direction.DownRight
            case DirectionOffset.Down:
                return Direction.Down
            case DirectionOffset.DownLeft:
                return Direction.DownLeft
            case DirectionOffset.Left:
                return Direction.Left

    @staticmethod
    def convert_direction_to_offset(direction: Direction):
        match direction:
            case Direction.Down:
                return DirectionOffset.Down
            case Direction.DownRight:
                return DirectionOffset.DownRight
            case Direction.DownLeft:
                return DirectionOffset.DownLeft
            case Direction.Up:
                return DirectionOffset.Up
            case Direction.UpRight:
                return DirectionOffset.UpRight
            case Direction.UpLeft:
                return DirectionOffset.UpLeft
            case Direction.Right:
                return DirectionOffset.Right
            case Direction.Left:
                return DirectionOffset.Left

    def __add__(self, other: int) -> int:
        return self.value + other

    def __mul__(self, n: int) -> int:
        return n * self.value