from referee.game import MoveAction, GrowAction
from agent2.GameState import DirectionOffset, GameState, PlayerColour
from abc import ABC, abstractmethod

# abstract base class for our moves, contains evaluation attribute
class Action(ABC):

    # # evaluation attribute
    # @property
    # @abstractmethod
    # def evaluation(self):
    #     pass

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
    def __init__(self):
        self.evaluation = -100
    
    # @property
    # def evaluation(self):
    #     return self._evaluation

    def to_action(self):
        return GrowAction()
    
class Move(Action):
    """
    Cannot instantiate and does nothing for now
    """

    pass

    # def __init__(self):
    #     self._evaluation = 0

    # @property
    # def evaluation(self):
    #     return self._evaluation

class Step(Move):
    """
    Represents a single step onto a lilypad
    """
    def __init__(self, start_index: int, direction_offset: DirectionOffset):
        self.evaluation = 1 + (start_index // 8)    # this only works for red
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
    def __init__(self, start_index: int, direction_offsets: list[DirectionOffset]):
        self.evaluation = 5 * (len(direction_offsets) + start_index // 8)   # this only works for red maybe
        self.start_index = start_index
        self.direction_offsets = direction_offsets
        self.end_index = start_index + sum([2 * offset.value for offset in direction_offsets])


    # note we have direction as list
    def to_action(self):
        return MoveAction(GameState.indexToCoord(self.start_index), 
                        [offset.convert_to_direction() for offset in self.direction_offsets])
