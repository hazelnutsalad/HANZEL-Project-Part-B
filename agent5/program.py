# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part B: Game Playing Agent

import random
import time
import heapq

from agent5.findmove import minimax_with_id_search
from agent5.GameState import *
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
        MAX_TIME_PER_MOVE = 2

        start = time.time()

        # potential_moves = generate_all_moves(self.game, self.colour)
        decision = minimax_with_id_search(self.game, self.colour, MAX_TIME_PER_MOVE)

        end = time.time()
        print(f"Move took {end-start} seconds to compute\n")

        return decision.to_action()

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after a player has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        # There are two possible action types: MOVE and GROW. Below we check
        # which type of action was played and print out the details of the
        # action for demonstration purposes. You should replace this with your
        # own logic to update your agent's internal game state representation.

        # convert their color to our colour
        colour = GameState.color_to_colour(color)

        match action:
            case MoveAction(coord, dirs):
                # dirs_text = ", ".join([str(dir) for dir in dirs])
                # print(f"Testing: {color} played MOVE action:")
                # print(f"  Coord: {coord}")
                # print(f"  Directions: {dirs_text}")

                self.game.apply_move_action(colour, action)

                # print("what we think the board looks like")
                # print(self.game)
                # print("red frogs")
                # print([frog.location for frog in self.game.red_frogs])
                # print("blue frogs")
                # print([frog.location for frog in self.game.blue_frogs])

            case GrowAction():
                print(f"Testing: {color} played GROW action")
                
                # wow we have a function for this
                self.game.apply_grow_action(colour)

                # print("what we think the board looks like")
                # print(self.game)
                # print([frog.location for frog in self.game.red_frogs])
                # print([frog.location for frog in self.game.blue_frogs])

            case _:
                raise ValueError(f"Unknown action type: {action}")
