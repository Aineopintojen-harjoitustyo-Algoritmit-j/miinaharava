from enum import Enum
from dataclasses import dataclass

class Action(Enum):
    QUIT = 0	# Pelin lopetus
    OPEN = 1	# Ruudun avaaminen
    FLAG = 2	# Ruudun liputus
    HINT = 3	# Anna vihjeet
    AUTO = 4	# Pelaa automaattisesti
    LEFT = 5
    RIGHT = 6
    UP = 7
    DOWN = 8

ActionKeys = {
    'w': Action.UP,	'a': Action.LEFT,	's': Action.DOWN,
    'd': Action.RIGHT,	' ': Action.OPEN,	'\n': Action.OPEN,
    'f': Action.FLAG,	'm': Action.FLAG,	'q': Action.QUIT
}


ActionEscKeys = {
    '': Action.QUIT,	'A': Action.UP,		'D': Action.LEFT,
    'C': Action.RIGHT,	'B': Action.DOWN
}

@dataclass
class TileType:
    text: str		# Teksti
    colors: []		# Lista (väri, tausta) pareja tekstille


TileTypes = {
    0:	TileType( "[ ]", [(0x7,0), (0x7,0), (0x7,0)] ),
    1:	TileType( "[1]", [(0xA,0), (0xA,0), (0xA,0)] ),
    2:	TileType( "[2]", [(0xB,0), (0xB,0), (0xB,0)] ),
    3:	TileType( "[3]", [(0xD,0), (0xD,0), (0xD,0)] ),
    4:	TileType( "[4]", [(0x9,0), (0x9,0), (0x9,0)] ),
    5:	TileType( "[5]", [(0x9,0), (0x9,0), (0x9,0)] ),
    6:	TileType( "[6]", [(0x9,0), (0x9,0), (0x9,0)] ),
    7:	TileType( "[7]", [(0x9,0), (0x9,0), (0x9,0)] ),
    8:	TileType( "[8]", [(0x9,0), (0x9,0), (0x9,0)] ),
    9:	TileType( "[¤]", [(0xF,1), (0xF,1), (0xF,1)] ),
    10:	TileType( "[#]", [(0x8,7), (0x8,7), (0x8,7)] ),
    11:	TileType( "[B]", [(0x8,7), (0x1,7), (0x8,7)] ),
    12:	TileType( "[?]", [(0x8,7), (0x3,7), (0x8,7)] )
}

class Colors:
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    GRAY = 8
    BRIGHT_RED = 9
    BRIGHT_GREEN = 0xA
    BRIGHT_YELLOW = 0xB
    BRIGHT_BLUE = 0xC
    BRIGHT_MAGENTA = 0xD
    BRIGHT_CYAN = 0xE
    BRIGHT_WHITE = 0xF