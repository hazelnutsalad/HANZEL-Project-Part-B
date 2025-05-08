from enum import Enum
from abc import ABC

from agent5.DirectionOffset import DirectionOffset
from referee.game import BOARD_N, Coord, MoveAction, GrowAction, PlayerColor


# defining this here and redefining later on so can compile
class Action(ABC):
    pass


class PlayerColour(Enum):
    """
    RED is truthy, BLUE is falsey
    """
    RED = 1
    BLUE = 0

    # switches colour
    def next(self):
        match self:
            case PlayerColour.RED:
                return PlayerColour.BLUE
            case PlayerColour.BLUE:
                return PlayerColour.RED


class GameState:
    """
    Our internal representation of the game state
    Contains a 8x8 character array representing the board, and 2 arrays containing the frog locations
    """

    # sets up the default board state
    def __init__(self):
        self.board = ['L', 'R', 'R', 'R', 'R', 'R', 'R', 'L',
                      '*', 'L', 'L', 'L', 'L', 'L', 'L', '*', 
                      '*', '*', '*', '*', '*', '*', '*', '*',
                      '*', '*', '*', '*', '*', '*', '*', '*',
                      '*', '*', '*', '*', '*', '*', '*', '*',
                      '*', '*', '*', '*', '*', '*', '*', '*',
                      '*', 'L', 'L', 'L', 'L', 'L', 'L', '*',
                      'L', 'B', 'B', 'B', 'B', 'B', 'B', 'L']
        
        red_frog_locations = [1, 2, 3, 4, 5, 6]
        blue_frog_locations = [57, 58, 59, 60, 61, 62]

        self.red_frogs = [Frog(index, PlayerColour.RED) for index in red_frog_locations]
        self.blue_frogs = [Frog(index, PlayerColour.BLUE) for index in blue_frog_locations]

    def __str__(self):
        string = ''
        for i in range(0, BOARD_N):
            for j in range(0, BOARD_N):
                string += self.board[i*BOARD_N + j] + ' '
            string += '\n'
        return string
        
    # convert index to Coord
    @staticmethod
    def indexToCoord(index: int):
        x = index // BOARD_N
        y = index % BOARD_N
        return Coord(x, y)

    # convert Coord to index
    @staticmethod
    def coordToIndex(coord: Coord):
        return coord.r * BOARD_N + coord.c
    
    # convert their colour to ours
    @staticmethod
    def color_to_colour(color: PlayerColor):
        match color:
            case PlayerColor.RED:
                return PlayerColour.RED
            case PlayerColor.BLUE:
                return PlayerColour.BLUE

    # check if move if out of bounds
    # TODO: replace numbers to be in terms of BOARD_N
    # TODO: also might want to change this to return the opposite of what it does currently so we
    # don't have lots of nots floating around everywhere else (i.e. change to is_in_bounds(..))
    @staticmethod
    def is_out_of_bounds(index: int, direction: DirectionOffset):
        match direction:
            case DirectionOffset.Left:
                return index % BOARD_N == 0
            case DirectionOffset.Right:
                return index % BOARD_N == 7
            case DirectionOffset.Up:
                return 0 <= index < 8
            case DirectionOffset.Down:
                return 56 <= index < 64
            case DirectionOffset.UpLeft:
                return (index % BOARD_N == 0) or (0 <= index < 8)
            case DirectionOffset.UpRight:
                return (index % BOARD_N == 7) or (0 <= index < 8)
            case DirectionOffset.DownLeft:
                return (index % BOARD_N == 0) or (56 <= index < 64)
            case DirectionOffset.DownRight:
                return (index % BOARD_N == 7) or (56 <= index < 64)

    # culls a list of DirectionOffsets to only include the ones that can form a hop (i.e 2+ away from edge)   
    # TODO: replace numbers to be in terms of BOARD_N  
    @staticmethod
    def in_bound_for_hop(index: int, directions: list[DirectionOffset]):
        in_bound_directions = []
        for direction in directions:
            match direction:
                case DirectionOffset.Up:
                    if (index >= 16):
                        in_bound_directions.append(direction)
                case DirectionOffset.Down:
                    if (index < 48):
                        in_bound_directions.append(direction)
                case DirectionOffset.Left:
                    if (index % BOARD_N >= 2):
                         in_bound_directions.append(direction)
                case DirectionOffset.Right:
                    if (index % BOARD_N < BOARD_N - 2): # gets 7 and 8?? is this right??
                        in_bound_directions.append(direction)
                
                # these are just compositions of above 4 (e.g. UpLeft is Up case and Left case)
                case DirectionOffset.UpLeft:
                    if ((index >= 16) and (index % BOARD_N >= 2)): 
                        in_bound_directions.append(direction)
                case DirectionOffset.UpRight:
                    if ((index >= 16) and (index % BOARD_N < BOARD_N - 2)):
                        in_bound_directions.append(direction)
                case DirectionOffset.DownLeft:
                    if ((index < 48) and (index % BOARD_N >= 2)):
                        in_bound_directions.append(direction)
                case DirectionOffset.DownRight:
                    if ((index < 48) and (index % BOARD_N < BOARD_N - 2)):
                        in_bound_directions.append(direction)

        return in_bound_directions

    # returns the adjacent indices of in-bounds squares
    def get_adjacent_indices(self, index: int):
        return [index + direction.value for direction in DirectionOffset
                if not self.is_out_of_bounds(index, direction)]
    
    # returns the adjacent in-bounds squares
    def get_adjacent_squares(self, index: int):
        return [self.board[index + direction.value] for direction in DirectionOffset 
                if not self.is_out_of_bounds(index, direction)]
    
    # returns adjacent indices of in-bound squares restricted to certain directions
    def get_adjacent_indices_restricted(self, index: int, restricted_directions: list[DirectionOffset]):
        return [index + direction.value for direction in restricted_directions
                if not self.is_out_of_bounds(index, direction)]
    
    # NOTE: changed this to return a dictionary of direction/state pairs for findmoves function
    # returns adjacent in-bounds squares restricted to certain directions
    def get_adjacent_squares_restricted(self, index: int, restricted_directions: list[DirectionOffset]):
        output_dict = {}
        for direction in restricted_directions:
            if not self.is_out_of_bounds(index, direction):
                output_dict[direction] = self.board[index + direction.value]
        return output_dict

    # change empty squares around index to lilypads
    def grow_around_frog(self, index: int):
        for square in self.get_adjacent_indices(index):
            if self.board[square] == '*':
                self.board[square] = 'L'

    # loops over all frogs of given colour to perform a grow action for that colour
    def apply_grow_action(self, colour: PlayerColour):
        match colour:
            case PlayerColour.RED:
                for frog in self.red_frogs:
                    self.grow_around_frog(frog.location)
            case PlayerColour.BLUE:
                for frog in self.blue_frogs:
                    self.grow_around_frog(frog.location)

    # takes in their Action (MoveAction or GrowAction) to update our board
    def update_game_state(self, colour: PlayerColour, action: MoveAction | GrowAction):
        if isinstance(action, MoveAction):
            self.apply_move_action(colour, action)
        else:
            self.apply_grow_action(colour)


    def apply_move_action(self, colour: PlayerColour, move: MoveAction):
        # converting MoveAction to our representation
        start_index = GameState.coordToIndex(move.coord)

        # first we need to determine if this is a step or hop (step is first case, hop is else)
        if len(move.directions) == 1:  # could be step or hop at this stage
            dir = DirectionOffset.convert_direction_to_offset(move.directions[0]).value
            if self.board[start_index + dir] == 'L':
                # it is a step!
                end_index = start_index + dir
            else:  # it is a hop of length one
                end_index = start_index + dir * 2
        # else it is a hop of multiple jumps
        else:
            end_index = start_index + sum(
                [DirectionOffset.convert_direction_to_offset(dir).value * 2 for dir in move.directions])

        # set current coordinate to empty
        self.board[start_index] = '*'

        # move frog to new location and update board accordingly
        match colour:
            case PlayerColour.RED:
                for frog in self.red_frogs:
                    if frog.location == start_index:
                        frog.apply_move(end_index)
                        self.board[end_index] = 'R'
            case PlayerColour.BLUE:
                for frog in self.blue_frogs:
                    if frog.location == start_index:
                        frog.apply_move(end_index)
                        self.board[end_index] = 'B'

    # take in our action to update our board (used in minimax search)
    def apply_action(self, colour: PlayerColour, action: Action):
        # move actions
        if isinstance(action, Move):
            # set current coordinate to empty
            self.board[action.start_index] = '*'

            # find frog and move it to new location
            match colour:
                case PlayerColour.RED:
                    for frog in self.red_frogs:
                        if frog.location == action.start_index:
                            frog.apply_move(action.end_index)
                            self.board[action.end_index] = 'R'
                case PlayerColour.BLUE:
                    for frog in self.blue_frogs:
                        if frog.location == action.start_index:
                            frog.apply_move(action.end_index)
                            self.board[action.end_index] = 'B'
        
        # grow action
        elif isinstance(action, Grow):
            self.apply_grow_action(colour)
        
        # for debugging: if our action is not a grow or move raise error
        else:
            print("action is not Grow or Move when trying to update board in minimax")
            exit(-1)

    def calculate_utility(self, colour: PlayerColour):
        # simple utility function that returns average distance frogs are from their starting state
        FROG_WEIGHT = 10
        LILYPAD_WEIGHT = 0

        blue_score = 0
        red_score = 0

        for i in self.red_frogs:
            red_score += FROG_WEIGHT * (i.location // BOARD_N)
        for i in self.blue_frogs:
            blue_score += FROG_WEIGHT * (8 - (i.location // BOARD_N))

        # extra term to dislike having lilypads close to their side of board 
        # only does 2 rows so we don't have to loop over entire board
        # NOTE: not sure if this makes much of a difference at all rn
        # for i in range(0, 8):
        #     if self.board[i] == '*':
        #         blue_score += 2 * LILYPAD_WEIGHT
        
        # for i in range(8, 16):
        #     if self.board[i] == '*':
        #         blue_score += LILYPAD_WEIGHT
        
        # for i in range(56, 64):
        #     if self.board[i] == '*':
        #         red_score += 2 * LILYPAD_WEIGHT
        
        # for i in range(48, 56):
        #     if self.board[i] == '*':
        #         red_score += LILYPAD_WEIGHT

        # match colour:
        #     case PlayerColour.RED:
        #         return red_score - blue_score
        #     case PlayerColour.BLUE:
        #         return blue_score - red_score


    def goal_test(self, player_colour: PlayerColour):
        goal_test = True
        if player_colour == PlayerColour.RED:
            for i in self.red_frogs:
                if i.location // BOARD_N != BOARD_N-1:
                    goal_test = False
        else:
                for i in self.blue_frogs:
                    if i.location // BOARD_N != 0:
                        goal_test = False
        return goal_test




class Frog:
    """ 
    Frog object containing a colour and position
    Contains methods to move / hop and hopefully eventually useful methods / attributes for our
    eval function
    """

    def __init__(self, location: int, colour: PlayerColour):
        self.location = location
        self.colour = colour
    
    # applies move to frog by setting location to end_index
    def apply_move(self, end_index: int):
        self.location = end_index

"""
Putting Action class stuff here to fix circular import
"""


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
    def __init__(self, colour: PlayerColour, game_state: GameState):
        self.evaluation = game_state.calculate_utility(colour)

    def to_action(self):
        return GrowAction()
    
class Move(Action):
    """
    Abstract base class for move actions with shared attributes
    """
    def __init__(self, evaluation: int):
            self.evaluation = evaluation
    
    def get_colour(self, game_state: GameState):
        match game_state.board[self.start_index]:
            case 'B':
                return PlayerColour.BLUE
            case 'R':
                return PlayerColour.RED

class Step(Move):
    """
    Represents a single step onto a lilypad
    """
    def __init__(self, start_index: int, direction_offset: DirectionOffset, game_state: GameState):
        self.start_index = start_index
        self.end_index = start_index + direction_offset.value
        self.direction_offset = direction_offset

        colour = self.get_colour(game_state)
        evaluation = game_state.calculate_utility(colour)
        super().__init__(evaluation)
        

    # note we have direction NOT as a list
    def to_action(self):
        return MoveAction(GameState.indexToCoord(self.start_index),
                           self.direction_offset.convert_to_direction())

class Hop(Move):
    """
    Represents (potentially multiple) hop
    """    
    def __init__(self, start_index: int, direction_offsets: list[DirectionOffset], game_state: GameState):
        self.start_index = start_index
        self.end_index = start_index + sum([2 * offset.value for offset in direction_offsets])
        self.direction_offsets = direction_offsets

        colour = self.get_colour(game_state)
        evaluation = game_state.calculate_utility(colour)
        super().__init__(evaluation)
        


    # note we have direction as list
    def to_action(self):
        return MoveAction(GameState.indexToCoord(self.start_index), 
                        [offset.convert_to_direction() for offset in self.direction_offsets])