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
    
    red_moves_8 = [MoveAction(Coord(0, 2), Direction.Down),
                   MoveAction(Coord(0, 5), Direction.Down),
                   MoveAction(Coord(0, 4), Direction.Down),
                   MoveAction(Coord(0, 5), Direction.Down),
                   GrowAction()]
    
    red_moves_10 = [MoveAction(Coord(0, 1), Direction.DownRight),
                    MoveAction(Coord(0, 2), Direction.DownRight),
                    MoveAction(Coord(0, 3), Direction.DownRight),
                    MoveAction(Coord(0, 4), Direction.DownRight),
                    GrowAction(),
                    MoveAction(Coord(0, 5), Direction.Down),
                    MoveAction(Coord(0, 6), Direction.DownLeft),
                    MoveAction(Coord(1, 2), Direction.Down)]
    
    red_moves_9a = [MoveAction(Coord(0, 4), Direction.Down), 
                        MoveAction(Coord(0, 2), Direction.Down),
                        GrowAction(),
                        MoveAction(Coord(0, 5), Direction.Down),
                        MoveAction(Coord(0, 1), Direction.DownRight),
                        MoveAction(Coord(0, 3), Direction.DownLeft),
                        GrowAction(),
                        MoveAction(Coord(0, 6), Direction.DownLeft)]
    
    red_moves_9b = [MoveAction(Coord(0, 3), Direction.Down), 
                        MoveAction(Coord(0, 5), Direction.Down),
                        GrowAction(),
                        MoveAction(Coord(0, 2), Direction.Down),
                        MoveAction(Coord(0, 6), Direction.DownLeft),
                        MoveAction(Coord(0, 4), Direction.DownRight),
                        GrowAction(),
                        MoveAction(Coord(0, 1), Direction.DownRight)]
    
    
    
    
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
    
    blue_moves_9a = [MoveAction(Coord(7, 4), Direction.Up), 
                        MoveAction(Coord(7, 2), Direction.Up),
                        GrowAction(),
                        MoveAction(Coord(7, 5), Direction.Up),
                        MoveAction(Coord(7, 1), Direction.UpRight),
                        MoveAction(Coord(7, 3), Direction.UpLeft),
                        GrowAction(),
                        MoveAction(Coord(7, 6), Direction.UpLeft)]
    
    blue_moves_9b = [MoveAction(Coord(7, 3), Direction.Up), 
                        MoveAction(Coord(7, 5), Direction.Up),
                        GrowAction(),
                        MoveAction(Coord(7, 2), Direction.Up),
                        MoveAction(Coord(7, 6), Direction.UpLeft),
                        MoveAction(Coord(7, 4), Direction.UpRight),
                        GrowAction(),
                        MoveAction(Coord(7, 1), Direction.UpRight)]
    

    # list of all books per colour (i believe opening 9 is the best of what we have)
    red_books = [red_moves_9a, red_moves_9b]
    blue_books = [blue_moves_9a, blue_moves_9b]

    # methods
    @staticmethod
    def get_opening_book(colour: PlayerColour):
        match colour:
            case PlayerColour.RED:
                return random.choice(OpeningBooks.red_books)
            case PlayerColour.BLUE:
                return random.choice(OpeningBooks.blue_books)
    