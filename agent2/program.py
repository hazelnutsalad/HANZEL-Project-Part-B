# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part B: Game Playing Agent

from findmove import generate_all_moves
from Move import *
from GameState import *
from referee.game import PlayerColor, Coord, Direction, \
    Action, MoveAction, GrowAction, Board


import random, time

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

        self.board = Board()

        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")



    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """

        start = time.time()

        potential_moves = generate_all_moves(self.board, self._color)

        end = time.time()
        print(f"Move took {end-start} seconds to compute\n")

        if potential_moves:
            return random.choice(potential_moves)
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

                # set current coordinate to empty
                self.board._state[action.coord] = CellState()
                new_coordinate = action.coord

            
                for direction in action.directions:
                    new_coordinate += direction
                    cell_state = self.board._state.get(new_coordinate)
                    if cell_state.state == CellState("LilyPad").state:
                        self.board._state[new_coordinate] = CellState()
                    elif cell_state.state == CellState(PlayerColor.RED).state or cell_state.state == CellState(PlayerColor.BLUE).state:
                        new_coordinate += direction
                self.board._state[new_coordinate] = CellState(color)
                # print("What we think board looks like:")
                # print(self.board.render(True, True))

            case GrowAction():
                print(f"Testing: {color} played GROW action")

                frog_locations = find_frogs(self.board, color)

                for frog in frog_locations:
                    for direction in Direction:
                        # try block handles us checking adjacent cells out of bounds
                        try:
                            new_coordinate = frog + direction
                            if self.board._state.get(new_coordinate) == CellState():
                                self.board._state[new_coordinate] = CellState("LilyPad")
                        except ValueError:
                            pass

            case _:
                raise ValueError(f"Unknown action type: {action}")
