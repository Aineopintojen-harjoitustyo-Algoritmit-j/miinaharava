""" board/static.py - määrittelyjä pelilaudan muuttumattomille asoille """

from enum import Enum, IntEnum

class Level(Enum):
    """ vaikeustasot """
    BEGINNER = 0
    INTERMEDIATE = 1
    EXPERT = 2


class Tile(IntEnum):
    """ alueiden selitteet """
    BLANK = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    BOMB = 9
    FLAG_BOMB = 10
    FLAG_FREE = 11
    UNOPENED = 12
    FLAG_UNKNOWN = 13


LevelSpecs = {
    Level.BEGINNER:	(  9,  9, 10 ),
    Level.INTERMEDIATE:	( 15, 15, 40 ),
    Level.EXPERT:	( 30, 16, 99 )
}
