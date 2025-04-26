# Heavily adapted from our assignment 1 submission
# contains function which takes in a board state and a player color and returns a list of all possible moves for that player

from referee.game import PlayerColor, Coord, Direction, MoveAction, Board
from referee.game.board import CellState


# todo: there is a illegal moves set in game which might be useful?
VALID_MOVES_RED = [Direction.Down, Direction.DownLeft, Direction.DownRight, Direction.Left, Direction.Right]
VALID_MOVES_BLUE = [Direction.Up, Direction.UpLeft, Direction.UpRight, Direction.Left, Direction.Right]

# function which takes in a board state, and a coordinate that contains a frog and finds all of the moves for that frog
def find_moves(board: Board, starting_coordinate: Coord) -> list[MoveAction] | None:
    cell_state = board._state.get(starting_coordinate).state
    if cell_state == PlayerColor.RED:
        VALID_MOVES = VALID_MOVES_RED
    elif cell_state == PlayerColor.BLUE:
        VALID_MOVES = VALID_MOVES_BLUE
    else:
        raise Exception("Invalid starting cell state for coordinate")
    
    potential_moves = []
    
    for direction in VALID_MOVES:
        try:
            new_coordinate = starting_coordinate + direction
            # if it lands on blue or red frog we try to hop over frog
            if (board._state.get(new_coordinate).state == PlayerColor.BLUE or
                board._state.get(new_coordinate).state == PlayerColor.RED):
                hop_coordinate = new_coordinate + direction
                if board._state.get(hop_coordinate).state == "LilyPad":
                    direction_list = [direction]
                    hop(board, starting_coordinate, VALID_MOVES, potential_moves, direction_list)
            
            # if it lands on lilypad we can just move :)
            if board._state.get(new_coordinate).state == "LilyPad":
                potential_moves.append(MoveAction(starting_coordinate, direction))

        except ValueError:
            pass
    
    return potential_moves

def hop(board, starting_coordinate, VALID_MOVES, potential_moves, direction_list):
    potential_moves.append(MoveAction(starting_coordinate, direction_list))

    hop_coordinate = starting_coordinate
    for direction in direction_list:
        hop_coordinate = hop_coordinate + direction + direction

    for direction in VALID_MOVES:
        # check we aren't hopping backwards
        if direction_list[-1] == Direction.Left and direction == Direction.Right:
            pass
        elif direction_list[-1] == Direction.Right and direction == Direction.Left:
            pass

        new_coordinate = hop_coordinate + direction
        if (board._state.get(new_coordinate).state == PlayerColor.BLUE or 
            board._state.get(new_coordinate).state == PlayerColor.RED):
            hop_hop_coordinate = new_coordinate + direction
            if board._state.get(hop_hop_coordinate).state == "LilyPad":
                hop(board, starting_coordinate, VALID_MOVES, potential_moves, direction_list + [direction])

# takes in the board and player colour and outputs a list of all move_actions
def generate_all_moves(board: Board, player_colour: PlayerColor) -> list[MoveAction] | None:
    all_moves = []
    frog_locations = find_frogs(board, player_colour)
    for frog in frog_locations:
        all_moves += find_moves(board, frog)
    return all_moves

# returns a list of the coordinate of all frogs of a given colour
def find_frogs(board: Board, player_colour: PlayerColor) -> list[Coord]:

    frog_locations = []

    if player_colour == PlayerColor.RED:
        desired_cell_state = PlayerColor.RED
    else:
        desired_cell_state = PlayerColor.BLUE
    
    for coordinate, state in board._state.items():
        if state.state == desired_cell_state:
            frog_locations.append(coordinate)
    
    return frog_locations