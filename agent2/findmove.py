
from GameState import GameState, Frog, DirectionOffset, PlayerColour
from referee.game import MoveAction, Direction


VALID_MOVES_RED = [DirectionOffset.DownRight, DirectionOffset.Down, DirectionOffset.DownLeft, DirectionOffset.Left, DirectionOffset.Right]
VALID_MOVES_BLUE = [DirectionOffset.UpRight, DirectionOffset.Up, DirectionOffset.UpLeft, DirectionOffset.Left, DirectionOffset.Right]


# function which takes in a board state and a frog and finds all the moves for that frog
def find_moves(game_state: GameState, frog: Frog) -> list[MoveAction] | None:
    colour = frog.colour

    match colour:
        case PlayerColour.RED:
            VALID_MOVES = VALID_MOVES_RED
        case PlayerColour.BLUE:
            VALID_MOVES = VALID_MOVES_BLUE

    # should this even be move action???? it might be easier to just convert to move action at very
    # end (seems overcomplicated rn but probably easier when using min/max)
    # we can make our own move class? with method to convert to MoveAction?
    potential_moves = []

    for square in game_state.get_adjacent_squares_restricted(frog.location, VALID_MOVES):
        # lilypad
        if square == 'L':
            potential_moves.append()
    
    return potential_moves

def hop(board, starting_coordinate, VALID_MOVES, potential_moves, direction_list):
    potential_moves.append(MoveAction(starting_coordinate, direction_list))

    hop_coordinate = starting_coordinate
    for direction in direction_list:
        hop_coordinate = hop_coordinate + direction + direction

    for direction in VALID_MOVES:
        # check we aren't hopping backwards
        if direction_list[-1] == Direction.Left and direction == Direction.Right:
            continue
        elif direction_list[-1] == Direction.Right and direction == Direction.Left:
            continue

        new_coordinate = hop_coordinate + direction
        if (board._state.get(new_coordinate).state == CellState(PlayerColor.BLUE).state or
            board._state.get(new_coordinate).state == CellState(PlayerColor.RED).state):
            hop_hop_coordinate = new_coordinate + direction
            if board._state.get(hop_hop_coordinate).state == CellState("LilyPad").state:
                new_direction_list = direction_list + [direction]
                hop(board, starting_coordinate, VALID_MOVES, potential_moves, new_direction_list)

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
        try:
            if state.state == desired_cell_state:
                frog_locations.append(coordinate)
        except AttributeError:
            pass
    
    return frog_locations