
from agent0c.GameState import *
from agent0c.DirectionOffset import DirectionOffset
import copy
import time

VALID_MOVES_RED = [DirectionOffset.DownRight, DirectionOffset.Down, DirectionOffset.DownLeft, DirectionOffset.Left, DirectionOffset.Right]
VALID_MOVES_BLUE = [DirectionOffset.UpRight, DirectionOffset.Up, DirectionOffset.UpLeft, DirectionOffset.Left, DirectionOffset.Right]

class Counter:
    def __init__(self, time_per_move):
        self.remaining_time = time_per_move
        self.time_last_updated = time.time()
    
    def update(self):
        self.remaining_time -= time.time() - self.time_last_updated
        self.time_last_updated = time.time()
    
    def out_of_time(self):
        return self.remaining_time < 0

# appends possible moves one step away from this index given a list of allowable directions
def get_adjacent_moves(game_state: GameState, index: int, restricted_directions: list[DirectionOffset],
                        step_list: list[Action], hop_list: list[Action]):
    
    adjacent_squares = game_state.get_adjacent_squares_restricted(index, restricted_directions)

    # if no moves can be made from this index exit function here
    if not adjacent_squares:
        return

    for direction, square in adjacent_squares.items():
        # lilypad
        if square == 'L':
            step_list.append(Step(index, direction, game_state))

        # hop
        if square == 'B' or square == 'R':
            # check if next square is also in-bound
            if not game_state.is_out_of_bounds(index + direction.value, direction):
                if game_state.board[index + direction * 2] == 'L':
                    start_hop(game_state, index, direction, hop_list, restricted_directions)

# first time hopping we have as separate func since logic is a bit different
def start_hop(game_state: GameState, start_index: int, start_direction: DirectionOffset,
              move_list: list[Move], restricted_directions: list[DirectionOffset]):
    # note we check that we land on lilypad before calling this so we know it is valid hop
    hop_history = [start_direction]
    move_list.append(Hop(start_index, hop_history, game_state))
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
                    move_list.append(Hop(start_index, hop2_history, game_state))
                    hop(game_state, start_index, move_list, restricted_directions, hop2_history)

# takes in the board and player colour and outputs a list of all move_actions
def generate_all_moves(game_state: GameState, player_colour: PlayerColour) -> list[Action] | None:
    step_list = []
    hop_list = []

    match player_colour: 
        case PlayerColour.RED:
            frogs = game_state.red_frogs
            VALID_MOVES = VALID_MOVES_RED
            # goal_index = BOARD_N - 1
        case PlayerColour.BLUE:
            frogs = game_state.blue_frogs
            VALID_MOVES = VALID_MOVES_BLUE
            # goal_index = 0
        case _:
            raise ValueError("Unexpected player colour")

    for frog in frogs:
        if not frog.at_goal:
            get_adjacent_moves(game_state, frog.location, VALID_MOVES, step_list, hop_list)
    
    all_moves = []
    all_moves.extend(hop_list)
    all_moves.extend(step_list)
    all_moves.append(Grow(player_colour, game_state))
    return all_moves

#Mini Max
def minimax_decision(game_state: GameState, player_colour: PlayerColour, search_depth: int, counter) -> Action:

    potential_actions = generate_all_moves(game_state, player_colour)

    # print(f"remaining time for depth {search_depth} is {counter.remaining_time}")

    ##Initialising values
    best_action = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for action in potential_actions:
        #Making a deep copy so that changed board does not influence original board
        modified_game_state = copy.deepcopy(game_state)
        modified_game_state.apply_action(player_colour, action)
        
        action_value = minimax_value(modified_game_state, player_colour, search_depth - 1, alpha, beta, player_colour, counter)

        ##Update based on result
        if action_value > best_value:
            best_value = action_value
            best_action = action

    return best_action
    
# player_colour is maximising player would be start true and alternate each time probably
def minimax_value(game_state: GameState, player_colour: PlayerColour, search_depth, alpha, beta, maximising_player: bool, counter) -> int:
    counter.update()

    # terminate if we run out of time or reach depth 0
    if counter.out_of_time() or search_depth == 0:
        return game_state.calculate_utility(player_colour)
    
    # dumb way to make it like winning
    if game_state.goal_test(player_colour):
        return game_state.calculate_utility(player_colour) * 100
    
    
    # if playing MAX
    if maximising_player:
        max_value = float('-inf')
        # generate all children of this board state
        for action in generate_all_moves(game_state, player_colour):
            # copy board and apply this action to it
            modified_game_state = copy.deepcopy(game_state)
            modified_game_state.apply_action(player_colour, action)
            
            value = minimax_value(modified_game_state, player_colour, search_depth - 1, alpha, beta, False, counter)
            max_value = max(max_value, value)

            # set alpha to the new maximum value for this branch
            alpha = max(alpha, max_value)
            # beta cut off
            if beta <= alpha:
                break
        
        return max_value
    
    else:
        min_value = float('inf')
        for action in generate_all_moves(game_state, player_colour.next()):
            # copy board and apply action
            modified_game_state = copy.deepcopy(game_state)
            modified_game_state.apply_action(player_colour.next(), action)

            value = minimax_value(modified_game_state, player_colour, search_depth - 1, alpha, beta, True, counter)
            min_value = min(min_value, value)

            # set beta to new minimum value for this branch
            beta = min(beta, min_value)
            # alpha cut off
            if beta <= alpha:
                break

        return min_value

# updated version of minimax_decision that uses iterative deepening search with a time limit
# NOTE: need to order moves to make this much much more useful
def minimax_with_id_search(game_state: GameState, player_colour: PlayerColour, time_per_move) -> Action:
    counter = Counter(time_per_move)
    depth = 1
    while not counter.out_of_time():

        # run minimax search with this depth
        decision = minimax_decision(game_state, player_colour, depth, counter)

        # increment depth
        depth += 1
    
    # print the maximum depth we got to in this search
    print(f"searched to a depth of {depth-1}")
    
    return decision


