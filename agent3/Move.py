# from abc import ABC, abstractmethod

# from referee.game import MoveAction, GrowAction, BOARD_N
# from agent3.GameState import GameState, PlayerColour
# from agent3.DirectionOffset import DirectionOffset


# # abstract base class for our moves, contains evaluation attribute
# class Action(ABC):

#     # abstract method to convert to their action
#     @abstractmethod
#     def to_action(self):
#         pass

#     # compare dunder method
#     def __lt__(self, other):
#         return self.evaluation > other.evaluation


# class Grow(Action):
#     """
#     Represents a grow action, for now we set evaluation to zero
#     """
#     def __init__(self, colour: PlayerColour, game_state: GameState):
#         if colour == PlayerColour.RED:
#             start_index = game_state.red_frogs[0].location
#         else:
#             start_index = game_state.blue_frogs[0].location
#         self.evaluation = game_state.calculate_utility()

#     def to_action(self):
#         return GrowAction()
    
# class Move(Action):
#     """
#     Abstract base class for move actions with shared attributes
#     """
#     def __init__(self, start_index: int, end_index: int, evaluation: int):
#             self.start_index = start_index
#             self.end_index = end_index
#             self.evaluation = evaluation

# class Step(Move):
#     """
#     Represents a single step onto a lilypad
#     """
#     def __init__(self, start_index: int, direction_offset: DirectionOffset, game_state: GameState):
#         end_index = start_index + direction_offset.value

#         # self.evaluation = 1 + (start_index // 8)    # this only works for red
#         evaluation = game_state.calculate_utility()
#         super().__init__(start_index, end_index, evaluation)
#         self.direction_offset = direction_offset

#     # note we have direction NOT as a list
#     def to_action(self):
#         return MoveAction(GameState.indexToCoord(self.start_index),
#                            self.direction_offset.convert_to_direction())

# class Hop(Move):
#     """
#     Represents (potentially multiple) hop
#     """    
#     def __init__(self, start_index: int, direction_offsets: list[DirectionOffset], board: GameState):
#         end_index = start_index + sum([2 * offset.value for offset in direction_offsets])
#         #self.evaluation = 5 * (len(direction_offsets) + start_index // 8)   # this only works for red maybe
#         evaluation = board.calculate_utility()
#         super().__init__(start_index, end_index, evaluation)
#         self.direction_offsets = direction_offsets


#     # note we have direction as list
#     def to_action(self):
#         return MoveAction(GameState.indexToCoord(self.start_index), 
#                         [offset.convert_to_direction() for offset in self.direction_offsets])
