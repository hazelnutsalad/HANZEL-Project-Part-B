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
        
        # i think we should make our own coord type to represent this?? since Coord is specific to
        # their board type

        # we could just have a single size 64 array so we don't need coord type???
        # e.g. board[1, 3] -> board[12]
        # then we calculate the moves based on offsets if we are at board[12] and we want to move
        # right it would be board[12+1] or move down is board[12+8]???
        # might be faster and probably not that annoying to implement if we put a bunch of functions
        # in the board class???

        self.red_frog_locations = [1, 2, 3, 4, 5, 6]
        self.blue_frog_locations = [57, 58, 59, 60, 61, 62]

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

    # returns the adjacent in-bounds squares
    def get_adjacent_indicies(self, index: int):
        return [index + direction.value for direction in DirectionOffsets if not self.is_out_of_bounds(index, direction)]
    
    def get_adjacent_squares(self, index: int):
        

board = GameState()
print(board.get_adjacent_squares(8))