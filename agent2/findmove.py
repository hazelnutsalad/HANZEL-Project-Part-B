
from agent2.GameState import GameState, Frog, DirectionOffset, PlayerColour
from agent2.Move import *


VALID_MOVES_RED = [DirectionOffset.DownRight, DirectionOffset.Down, DirectionOffset.DownLeft, DirectionOffset.Left, DirectionOffset.Right]
VALID_MOVES_BLUE = [DirectionOffset.UpRight, DirectionOffset.Up, DirectionOffset.UpLeft, DirectionOffset.Left, DirectionOffset.Right]


# appends possible moves one step away from this index given a list of allowable directions
def get_adjacent_moves(game_state: GameState, index: int, 
                       restricted_directions: list[DirectionOffset], move_list: list[Move]):
    
    adjacent_squares = game_state.get_adjacent_squares_restricted(index, restricted_directions)

    # if no moves can be made from this index exit function here
    if not adjacent_squares:
        return

    for direction, square in adjacent_squares.items():
        # lilypad
        if square == 'L':
            move_list.append(Step(index, direction))

        # hop
        if square == 'B' or square == 'R':
            # check if next square is also in-bound
            if not game_state.is_out_of_bounds(index + direction.value, direction):
                if game_state.board[index + direction * 2] == 'L':
                    start_hop(game_state, index, direction, move_list, restricted_directions)

# first time hopping we have as separate func since logic is a bit different
def start_hop(game_state: GameState, start_index: int, start_direction: DirectionOffset,
              move_list: list[Move], restricted_directions: list[DirectionOffset]):
    # note we check that we land on lilypad before calling this so we know it is valid hop
    hop_history = [start_direction]
    move_list.append(Hop(start_index, hop_history))
    hop(game_state, start_index, move_list, restricted_directions, hop_history)

# now we need to look for multiple directions when hopping, and have to keep track of dirs we hop
def hop(game_state: GameState, start_index: int, move_list: list[Move], 
        restricted_directions: list[DirectionOffset], hop_history: list[DirectionOffset]):
    # NOTE: this breaks if we change how we add things to move_list so be careful!!
    # but saves us from having to recompute this (could also just add it to signature ??)
    current_index = move_list[-1].end_index
    last_direction = hop_history[-1]

    # trims down our restricted_directions to only include those at least 2 squares away from edge
    potential_hops = game_state.in_bound_for_hop(current_index, restricted_directions)
    for direction in potential_hops:
        # check we haven't gone backwards (left -> right or right -> left)
        if direction + last_direction.value != 0:
            # now we check if the adjacent square is a frog
            square = game_state.board[current_index + direction.value]
            if (square == 'B' or square == 'R'):
                # now we check that the square past the frog is a lilypad
                if game_state.board[current_index + 2 * direction.value] == 'L':
                    # we have a valid hop so can add it to move_list and try to hop from new square
                    hop2_history = hop_history + [direction]    # new list for recursion
                    move_list.append(Hop(start_index, hop2_history))
                    hop(game_state, start_index, move_list, restricted_directions, hop2_history)

# takes in the board and player colour and outputs a list of all move_actions
def generate_all_moves(game_state: GameState, player_colour: PlayerColour) -> list[MoveAction] | None:
    all_moves = []

    match player_colour: 
        case PlayerColour.RED:
            frogs = game_state.red_frogs
            VALID_MOVES = VALID_MOVES_RED
        case PlayerColour.BLUE:
            frogs = game_state.blue_frogs
            VALID_MOVES = VALID_MOVES_BLUE
        case _:
            raise ValueError("Unexpected player colour")

    for frog in frogs:
        get_adjacent_moves(game_state, frog.location, VALID_MOVES, all_moves)

    return all_moves