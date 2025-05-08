# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part B: Game Playing Agent

import time

from agent7.findmove import minimax_with_id_search
from agent7.GameState import *
from referee.game import Direction, \
    Action, MoveAction, GrowAction, PlayerColor
from referee.game.board import CellState


class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Freckers game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """

        ##Now using our own representation of the board instead of the referee's board class
        self.game = GameState()

        ##Convert PlayerColor to our PlayerColour enum
        self.colour = GameState.color_to_colour(color)


    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """

        # could potentially dynamically update this based on remaining time in game
        MAX_TIME_PER_MOVE = 0.3

        start = time.time()

        decision = minimax_with_id_search(self.game, self.colour, MAX_TIME_PER_MOVE)

        end = time.time()
        print(f"Move took {end-start} seconds to compute\n")

        return decision.to_action()

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after a player has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        colour = GameState.color_to_colour(color)

        match action:
            case MoveAction(coord, dirs):
                self.game.apply_move_action(colour, action)

            case GrowAction():
                self.game.apply_grow_action(colour)

            case _:
                raise ValueError(f"Unknown action type: {action}")
