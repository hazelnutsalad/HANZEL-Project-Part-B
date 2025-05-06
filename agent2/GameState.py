from enum import Enum
from referee.game import MoveAction, Direction, BOARD_N, Coord

class DirectionOffset(Enum):
    """
    Enum which contains the offsets for each possible direction
    """
    UpLeft      = -9
    Up          = -8
    UpRight     = -7
    Right       = 1
    DownRight   = 9
    Down        = 8
    DownLeft    = 7
    Left        = -1

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

class PlayerColour(Enum):
    RED = 0
    BLUE = 1


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
                    if not (0 <= index < 16):
                        in_bound_directions.append(direction)
                case DirectionOffset.Down:
                    if not (48 <= index < 64):
                        in_bound_directions.append(direction)
                case DirectionOffset.Left:
                    if not (index % BOARD_N < 2):
                         in_bound_directions.append(direction)
                case DirectionOffset.Right:
                    if not (index % BOARD_N > BOARD_N - 2):
                        in_bound_directions.append(direction)
                
                # these are just compositions of above 4 (e.g. UpLeft is Up case and Left case)
                case DirectionOffset.UpLeft:
                    if not ((0 <= index < 16) or (index % BOARD_N < 2)): 
                        in_bound_directions.append(direction)
                case DirectionOffset.UpRight:
                    if not ((0 <= index < 16) or (index % BOARD_N > BOARD_N - 2)):
                        in_bound_directions.append(direction)
                case DirectionOffset.DownLeft:
                    if not ((48 <= index < 64) or (index % BOARD_N < 2)):
                        in_bound_directions.append(direction)
                case DirectionOffset.DownRight:
                    if not ((48 <= index < 64) or (index % BOARD_N > BOARD_N - 2)):
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
    
    def apply_move_action(self, colour: PlayerColour, move: MoveAction):
        # converting MoveAction to our representation
        start_index = GameState.coordToIndex(move.coord)
        
        # first we need to determine if this is a step or hop (step is first case, hop is else)
        if len(move.directions) == 1:   # could be step or hop at this stage
            dir = DirectionOffset.convert_direction_to_offset(move.directions[0]).value
            if self.board[start_index + dir] == 'L':
                # it is a step!
                end_index = start_index + dir
            else:   # it is a hop of length one
                end_index = start_index + dir * 2
        # else it is a hop of multiple jumps
        else:
            end_index = start_index + sum([DirectionOffset.convert_direction_to_offset(dir).value * 2 for dir in move.directions])

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