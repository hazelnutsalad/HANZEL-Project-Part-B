from referee.game import MoveAction
from GameState import DirectionOffset

class Step:
    """
    Represents a single step onto a lilypad
    """
    def __init__(self, start_index: int, direction_offset: DirectionOffset):
        self.start_index = start_index
        self.direction_offset = direction_offset
        self.end_index = start_index + direction_offset.value

    # note we have direction NOT as a list
    def convert_to_move_action(self):
        return MoveAction(self.start_index, self.direction_offset.convert_to_direction())

class Hop:
    """
    Represents (potentially multiple) hop
    """
    def __init__(self, start_index: int, direction_offsets: list[DirectionOffset]):
        self.start_index = start_index
        self.direction_offsets = direction_offsets
        self.end_index = start_index + sum([2 * offset.value for offset in direction_offsets])

    # note we have direction as list
    def convert_to_move_action(self):
        return MoveAction(self.start_index, 
            [offset.convert_to_direction for offset in self.direction_offsets])

# so we can have array of Move in our generate moves function
Move = Step | Hop