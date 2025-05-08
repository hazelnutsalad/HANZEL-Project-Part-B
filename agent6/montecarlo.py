from agent6.GameState import GameState, PlayerColour, Action
from agent6.findmove import Counter


class MCTnode:
        """
        Our representation of a Monte Carlo Tree Node
        """
        def __init__(self, parent):
                self.wins = 0
                self.losses = 0
                self.children = list[MCTnode]
                self.parent = parent

        def expand(self, player_colour: PlayerColour, game_state: GameState):
                child_actions = generate_all_moves(game_state, player_colour)

def monte_carlo_search(game_state: GameState, player_colour: PlayerColour, time_per_move) -> Action:
        counter = Counter(time_per_move)

        while not counter.out_of_time():




