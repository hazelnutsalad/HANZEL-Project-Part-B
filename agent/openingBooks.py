from referee.game import MoveAction, GrowAction, Coord, Direction
from .GameState import PlayerColour
import random

class OpeningBooks:
    """
    Contains various sequences of opening moves and a function to return one at random given colour
    """

    # red moves

    red_moves_11 = [MoveAction(Coord(0, 3), Direction.Down),
                    MoveAction(Coord(0, 4), Direction.Down),
                    GrowAction(),
                    MoveAction(Coord(0,6), (Direction.Left, Direction.DownLeft)),
                    MoveAction(Coord(0,1), (Direction.Right, Direction.DownRight)),
                    MoveAction(Coord(0,2), Direction.DownRight),
                    MoveAction(Coord(0, 5), Direction.DownLeft)]
    
    # blue moves

    blue_moves_11 = [MoveAction(Coord(7, 3), Direction.Up),
                    MoveAction(Coord(7,4), Direction.Up),
                    GrowAction(),
                    MoveAction(Coord(7,1), (Direction.Right, Direction.UpRight)),
                    MoveAction(Coord(7,6), (Direction.Left, Direction.UpLeft)),
                    MoveAction(Coord(7,2), Direction.UpRight),
                    MoveAction(Coord(7,5), Direction.UpLeft)]
    

    # methods
    @staticmethod
    def get_opening_book(colour: PlayerColour):
        match colour:
            case PlayerColour.RED:
                return OpeningBooks.red_moves_11
            case PlayerColour.BLUE:
                return OpeningBooks.blue_moves_11
    