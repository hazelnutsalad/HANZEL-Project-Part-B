from enum import Enum
from referee.game import MoveAction, Direction, BOARD_N

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

    # check if move if out of bounds
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

    # returns the adjacent indices of in-bounds squares
    def get_adjacent_indices(self, index: int):
        return [index + direction.value for direction in DirectionOffset
                if not self.is_out_of_bounds(index, direction)]
    
    # returns the adjacent in-bounds squares
    def get_adjacent_squares(self, index: int):
        return [self.board[index + direction] for direction in DirectionOffset 
                if not self.is_out_of_bounds(index, direction)]
    
    # returns adjacent indices of in-bound squares restricted to certain directions
    def get_adjacent_indices_restricted(self, index: int, restricted_directions: list[DirectionOffset]):
        return [index + direction for direction in restricted_directions
                if not self.is_out_of_bounds(index, direction)]
    
    # returns adjacent in-bounds squares restricted to certain directions
    def get_adjacent_squares_restricted(self, index: int, restricted_directions: list[DirectionOffset]):
        return [self.board[index + direction] for direction in restricted_directions
                if not self.is_out_of_bounds(index, direction)]
    

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


class Frog:
    """ 
    Frog object containing a colour and position
    Contains methods to move / hop and hopefully eventually useful methods / attributes for our
    eval function
    """

    def __init__(self, location: int, colour: PlayerColour):
        self.location = location
        self.colour = colour
    
    # updates location of frog (setter for location)
    def move_frog(self, new_index: int):
        self.location = new_index


game_state = GameState()
print(game_state)
game_state.apply_grow_action(PlayerColour.RED)
print(game_state)
print(DirectionOffset.Right.convert_to_direction())
print(DirectionOffset.Left * 5 + DirectionOffset.Right.value)
print(DirectionOffset.UpRight + 21)