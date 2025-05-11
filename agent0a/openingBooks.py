from referee.game import MoveAction, GrowAction, Coord, Direction
from agent0a.GameState import PlayerColour
import random

class OpeningBooks:
    """
    Contains various sequences of opening moves and a function to return one at random given colour
    """

    # red moves

    red_moves_1 = [MoveAction(Coord(0, 3), Direction.Down), 
                        MoveAction(Coord(0, 5), Direction.Down),
                        GrowAction(),
                        MoveAction(Coord(0, 1), (Direction.Right, Direction.Down)),
                        MoveAction(Coord(0, 6), Direction.DownLeft),
                        GrowAction()]
    
    red_moves_2 = [MoveAction(Coord(0, 4), Direction.Down), 
                        MoveAction(Coord(0, 2), Direction.Down),
                        GrowAction(),
                        MoveAction(Coord(0, 6), (Direction.Left, Direction.Down)),
                        MoveAction(Coord(0, 1), Direction.DownRight),
                        GrowAction()]
    
    red_moves_3 = [MoveAction(Coord(0, 3), Direction.Down), 
                        MoveAction(Coord(0, 5), Direction.Down),
                        GrowAction(),
                        MoveAction(Coord(0, 4), Direction.DownRight),
                        MoveAction(Coord(1, 3), Direction.DownRight),
                        GrowAction()]
    
    red_moves_4 = [MoveAction(Coord(0, 4), Direction.Down), 
                        MoveAction(Coord(0, 2), Direction.Down),
                        GrowAction(),
                        MoveAction(Coord(0, 3), Direction.DownLeft),
                        MoveAction(Coord(1, 4), Direction.DownLeft),
                        GrowAction()]
    
    red_moves_5 = [MoveAction(Coord(0, 3), Direction.Down), 
                        MoveAction(Coord(0, 5), Direction.Down),
                        GrowAction(),
                        MoveAction(Coord(0, 1), (Direction.Right, Direction.Down)),
                        MoveAction(Coord(0,2), (Direction.DownRight, Direction.Left)),
                        MoveAction(Coord(0, 6), Direction.DownLeft),
                        GrowAction()]
    
    red_moves_6 = [MoveAction(Coord(0, 3), Direction.Down), 
                        MoveAction(Coord(0, 5), Direction.Down),
                        GrowAction(),
                        MoveAction(Coord(0, 1), (Direction.Right, Direction.Down))]
    
    red_moves_7 = [MoveAction(Coord(0, 2), Direction.Down),
                   MoveAction(Coord(0, 3), Direction.Down),
                   MoveAction(Coord(0, 4), Direction.Down),
                   MoveAction(Coord(0, 5), Direction.Down),
                   GrowAction()]
    
    # blue moves
    
    blue_moves_1 = [MoveAction(Coord(7, 3), Direction.Up), 
                        MoveAction(Coord(7, 5), Direction.Up),
                        GrowAction(),
                        MoveAction(Coord(7, 1), (Direction.Right, Direction.Up)),
                        MoveAction(Coord(7, 6), Direction.UpLeft),
                        GrowAction()]
    
    blue_moves_2 = [MoveAction(Coord(7, 4), Direction.Up), 
                        MoveAction(Coord(7, 2), Direction.Up),
                        GrowAction(),
                        MoveAction(Coord(7, 6), (Direction.Left, Direction.Up)),
                        MoveAction(Coord(7, 1), Direction.UpRight),
                        GrowAction()]
    
    blue_moves_3 = [MoveAction(Coord(7, 3), Direction.Up), 
                        MoveAction(Coord(7, 5), Direction.Up),
                        GrowAction(),
                        MoveAction(Coord(7, 4), Direction.UpRight),
                        MoveAction(Coord(6, 3), Direction.UpRight),
                        GrowAction()]
    
    blue_moves_4 = [MoveAction(Coord(7, 4), Direction.Up), 
                        MoveAction(Coord(7, 2), Direction.Up),
                        GrowAction(),
                        MoveAction(Coord(7, 3), Direction.UpLeft),
                        MoveAction(Coord(6, 4), Direction.UpLeft),
                        GrowAction()]
    

    # list of all books per colour
    red_books = [red_moves_1, red_moves_2, red_moves_3, red_moves_4, red_moves_5, red_moves_6]
    blue_books = [blue_moves_1, blue_moves_2, blue_moves_3, blue_moves_4]

    # methods
    @staticmethod
    def get_opening_book(colour: PlayerColour):
        match colour:
            case PlayerColour.RED:
                return OpeningBooks.red_moves_7
            case PlayerColour.BLUE:
                return random.choice(OpeningBooks.blue_books)
    