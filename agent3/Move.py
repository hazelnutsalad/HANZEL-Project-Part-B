from referee.game import MoveAction, GrowAction, BOARD_N
from agent3.GameState import DirectionOffset, GameState, PlayerColour
from abc import ABC, abstractmethod



# abstract base class for our moves, contains evaluation attribute
class Action(ABC):

    # abstract method to convert to their action
    @abstractmethod
    def to_action(self):
        pass

    # compare dunder method
    def __lt__(self, other):
        return self.evaluation > other.evaluation


class Grow(Action):
    """
    Represents a grow action, for now we set evaluation to zero
    """
    def __init__(self, colour: PlayerColour, board: GameState):
        if colour == PlayerColour.RED:
            start_index = board.red_frogs[0].location
        else:
            start_index = board.blue_frogs[0].location
        self.evaluation = board.calculate_utility(start_index)

    def to_action(self):
        return GrowAction()
    
class Move(Action):
    """
    Cannot instantiate and does nothing for now
    """
    pass

class Step(Move):
    """
    Represents a single step onto a lilypad
    """
    def __init__(self, start_index: int, direction_offset: DirectionOffset, board: GameState):
        #self.evaluation = 1 + (start_index // 8)    # this only works for red
        self.evaluation = board.calculate_utility(start_index)
        self.start_index = start_index
        self.direction_offset = direction_offset
        self.end_index = start_index + direction_offset.value

    # note we have direction NOT as a list
    def to_action(self):
        return MoveAction(GameState.indexToCoord(self.start_index),
                           self.direction_offset.convert_to_direction())

class Hop(Move):
    """
    Represents (potentially multiple) hop
    """    
    def __init__(self, start_index: int, direction_offsets: list[DirectionOffset], board: GameState):
        #self.evaluation = 5 * (len(direction_offsets) + start_index // 8)   # this only works for red maybe
        self.evaluation = board.calculate_utility(start_index)
        self.start_index = start_index
        self.direction_offsets = direction_offsets
        self.end_index = start_index + sum([2 * offset.value for offset in direction_offsets])


    # note we have direction as list
    def to_action(self):
        return MoveAction(GameState.indexToCoord(self.start_index), 
                        [offset.convert_to_direction() for offset in self.direction_offsets])
