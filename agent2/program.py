# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part B: Game Playing Agent


"""
TO-DO:
    1. Fix update method to reflect new representation of game (No longer using Board Class, but optimised GameState Class
"""

import random
import time

from agent2.findmove import generate_all_moves
from agent2.GameState import *
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
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
                self.colour = PlayerColour.RED
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")
                self.colour = PlayerColour.BLUE



    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """

        start = time.time()

        potential_moves = generate_all_moves(self.game, self.colour)

        end = time.time()
        print(f"Move took {end-start} seconds to compute\n")

        if potential_moves:
            return random.choice(potential_moves).convert_to_move_action()
        else:
            return GrowAction()

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after a player has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        # There are two possible action types: MOVE and GROW. Below we check
        # which type of action was played and print out the details of the
        # action for demonstration purposes. You should replace this with your
        # own logic to update your agent's internal game state representation.
        match action:
            case MoveAction(coord, dirs):
                dirs_text = ", ".join([str(dir) for dir in dirs])
                print(f"Testing: {color} played MOVE action:")
                print(f"  Coord: {coord}")
                print(f"  Directions: {dirs_text}")

                index = GameState.coordToIndex(action.coord)

                # set current coordinate to empty
                self.game.board[index] = '*'
                
                # TODO: could make a function to convert MoveAction to Move so we can find end index easily
                # currently need to convert each direction to directionOffset??
                # trace move to find end index
                new_coordinate = index
                for direction in action.directions:
                    new_coordinate += direction.value

                match self.colour:
                    case PlayerColour.RED:
                        self.game.board[new_coordinate] = 'R'
                    case PlayerColour.BLUE:
                        self.game.board[new_coordinate] = 'B'
                    case _:
                        Exception("Invalid player colour in update")


                # print("What we think board looks like:")
                # print(self.board.render(True, True))

            case GrowAction():
                print(f"Testing: {color} played GROW action")
                
                # wow we have a function for this
                self.game.apply_grow_action(self.colour)

            case _:
                raise ValueError(f"Unknown action type: {action}")
