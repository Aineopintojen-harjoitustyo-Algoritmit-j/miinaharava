""" tui/static.py - Staattiset määritykset tui:ssa tarvittaville jutuille. """
from enum import Enum, IntEnum
from dataclasses import dataclass

class Action(Enum):
    """ tominnot, joita voidaan saada palautusrvona """
    QUIT = 0	# Pelin lopetus
    OPEN = 1	# Ruudun avaaminen
    FLAG = 2	# Ruudun liputus
    HINT = 3	# Anna vihjeet
    AUTO = 4	# Pelaa automaattisesti
    LEFT = 5
    RIGHT = 6
    UP = 7
    DOWN = 8
    TOP = 9
    BOTTOM = 10
    BEGIN = 11
    END = 12
    NOOP = 13

# ActionKeys - Ohjelma vertaa syötteen alkua näihin ja palauttaa ekan
ActionKeys = {
    "\033[A": Action.UP,	"\033[D": Action.LEFT,
    "\033[C": Action.RIGHT,	'\033[B': Action.DOWN,	"\033[5~": Action.TOP,
    "\033[6~": Action.BOTTOM,	"\033[7~": Action.BEGIN,"\033[8~": Action.END,
    "\033[": Action.NOOP,	"\033": Action.QUIT,
    "w": Action.UP,		"a": Action.LEFT,	"s": Action.DOWN,
    "d": Action.RIGHT,		" ": Action.OPEN,	"\n": Action.OPEN,
    "f": Action.FLAG,		"m": Action.FLAG,	"q": Action.QUIT,
}

@dataclass
class TileType:
    """ ruututyyppien tallennusmuotojen kuvaus"""
    text: str		# Teksti
    colors: []		# Lista (väri, tausta) pareja tekstin kaunistamiseen


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
    9:	TileType( "[@]", [(0xF,1), (0xF,1), (0xF,1)] ),
    10:	TileType( "[#]", [(0x8,7), (0x8,7), (0x8,7)] ),
    11:	TileType( "[B]", [(0x8,7), (0x1,7), (0x8,7)] ),
    12:	TileType( "[?]", [(0x8,7), (0x3,7), (0x8,7)] )
}

class Colors(IntEnum):
    """ ANSI värejä vastaavat lukuarvot """
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
