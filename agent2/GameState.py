

class GameState:
    """
    Our internal representation of the game state
    Contains a 8x8 character array representing the board, and 2 arrays containing the frog locations
    """

    # sets up the default board state
    def __init__(self):
        self.board = [['L', 'R', 'R', 'R', 'R', 'R', 'R', 'L'],
                      ['*', 'L', 'L', 'L', 'L', 'L', 'L', '*'], 
                      ['*', '*', '*', '*', '*', '*', '*', '*'],
                      ['*', '*', '*', '*', '*', '*', '*', '*'],
                      ['*', '*', '*', '*', '*', '*', '*', '*'],
                      ['*', '*', '*', '*', '*', '*', '*', '*'],
                      ['*', 'L', 'L', 'L', 'L', 'L', 'L', '*'],
                      ['L', 'B', 'B', 'B', 'B', 'B', 'B', 'L']]
        
        # i think we should make our own coord type to represent this?? since Coord is specific to
        # their board type
        
        self.red_frog_locations = []
        self.blue_frog_locations = []