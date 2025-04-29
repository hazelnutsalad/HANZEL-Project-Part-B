from enum import Enum

BOARD_N = 8

# enum which contains the offsets for each possible direction
class DirectionOffsets(Enum):
    UpLeft      = -9
    Up          = -8
    UpRight     = -7
    Right       = 1
    DownRight   = 9
    Down        = 8
    DownLeft    = 7
    Left        = -1

class PlayerColour(Enum):
    RED = 0
    BLUE = 1


class GameState:
    """
    Our internal representation of the game state
    Contains a 8x8 character array representing the board, and 2 arrays containing the frog locations
    """

    VALID_MOVES_RED = [DirectionOffsets.DownRight, DirectionOffsets.Down, DirectionOffsets.DownLeft, DirectionOffsets.Left, DirectionOffsets.Right]
    VALID_MOVES_BLUE = [DirectionOffsets.UpRight, DirectionOffsets.Up, DirectionOffsets.UpLeft, DirectionOffsets.Left, DirectionOffsets.Right]

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

    # return the adjacent squares to the given coordinate that are in bound
    @staticmethod
    def is_out_of_bounds(index: int, direction: DirectionOffsets):
        match direction:
            case DirectionOffsets.Left:
                return index % BOARD_N == 0
            case DirectionOffsets.Right:
                return index % BOARD_N == 7
            case DirectionOffsets.Up:
                return 0 <= index < 8
            case DirectionOffsets.Down:
                return 56 <= index < 64
            case DirectionOffsets.UpLeft:
                return (index % BOARD_N == 0) or (0 <= index < 8)
            case DirectionOffsets.UpRight:
                return (index % BOARD_N == 7) or (0 <= index < 8)
            case DirectionOffsets.DownLeft:
                return (index % BOARD_N == 0) or (56 <= index < 64)
            case DirectionOffsets.DownRight:
                return (index % BOARD_N == 7) or (56 <= index < 64)

    # returns the adjacent indicies of in-bounds squares
    def get_adjacent_indicies(self, index: int):
        return [index + direction.value for direction in DirectionOffsets if not self.is_out_of_bounds(index, direction)]
    
    # returns the adjacent in-bounds squares
    def get_adjacent_squares(self, index: int):
        return [self.board[index + direction.value] for direction in DirectionOffsets if not self.is_out_of_bounds(index, direction)]

    # change empty squares around index to lilypads
    def grow_around_frog(self, index: int):
        for square in self.get_adjacent_indicies(index):
            if self.board[square] == '*':
                self.board[square] = 'L'
    
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
    
    # move onto an adjacent lilypad
    def step(self, game_state: GameState, start_index: int, end_index: int):
        pass


game_state = GameState()
print(game_state)
game_state.apply_grow_action(PlayerColour.RED)
print(game_state)