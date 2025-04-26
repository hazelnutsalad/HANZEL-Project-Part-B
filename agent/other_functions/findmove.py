# Heavily adapted from our assignment 1 submission
# contains function which takes in a board state and a player color and returns a list of all possible moves for that player

from referee.game import PlayerColor, CellState, Coord, Direction, MoveAction, BOARD_N

# todo: there is a illegal moves set in game which might be useful?
VALID_MOVES_RED = [Direction.Down, Direction.DownLeft, Direction.DownRight, Direction.Left, Direction.Right]
VALID_MOVES_BLUE = [Direction.Up, Direction.UpLeft, Direction.UpRight, Direction.Left, Direction.Right]

