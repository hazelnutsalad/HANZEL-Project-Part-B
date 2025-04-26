# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part B: Game Playing Agent

from agent.findmove import generate_all_moves
from referee.game import PlayerColor, Coord, Direction, \
    Action, MoveAction, GrowAction, Board


import random
    

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

        potential_moves = generate_all_moves(self.board, self._color)
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
                

                try:
                    # dirs is a list!
                    new_coordinate = coord + dirs[0]
                    is_list = True
                except TypeError:
                    # dirs is not a list!
                    new_coordinate = coord + dirs
                    is_list = False
                
                # if not hop
                if self.board._state.get(new_coordinate) == "LilyPad":
                    self.board._state[new_coordinate] = color
                    self.board._state[coord] = None
            
                # if hop
                elif self.board._state.get(new_coordinate):
                    hop_coordinate = coord
                    if is_list:
                        for direction in dirs:
                            self.board._state[hop_coordinate] = None
                            hop_coordinate = hop_coordinate + direction + direction
                    if not is_list:
                        self.board._state[hop_coordinate] = None
                        hop_coordinate = hop_coordinate + dirs + dirs
            
                    self.board._state[hop_coordinate] = color


                        


            case GrowAction():
                print(f"Testing: {color} played GROW action")
            case _:
                raise ValueError(f"Unknown action type: {action}")
