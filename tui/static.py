""" tui/static.py - Staattiset määritykset tui:ssa tarvittaville jutuille. """
from enum import Enum
from dataclasses import dataclass
from board import Tile

class Action(Enum):
    """ tominnot, joita voidaan saada palautusrvona """
    QUIT = 0	# Pelin lopetus
    OPEN = 1	# Ruudun avaaminen
    FLAG = 2	# Ruudun liputus
    HINT = 3	# Anna vihjeet
    AUTO = 4	# Pelaa automaattisesti
    LEFT = 5	# Liikkumiset...
    RIGHT = 6
    UP = 7
    DOWN = 8
    TOP = 9
    BOTTOM = 10
    BEGIN = 11
    END = 12
    NOOP = 13	# ei mitään - tarvitaan, ettei mätsää ansikoodeja esciin
    MINE = 14	# merkkaa pommi
    SAFE = 15	# merkkaa turvallinen

# ActionKeys - Ohjelma vertaa syötteen alkua näihin ja palauttaa ekan
ActionKeys = {
    "\033[A": Action.UP,	"\033[D": Action.LEFT,
    "\033[C": Action.RIGHT,	'\033[B': Action.DOWN,	"\033[5~": Action.TOP,
    "\033[6~": Action.BOTTOM,	"\033[7~": Action.BEGIN,"\033[8~": Action.END,
    "\033[": Action.NOOP,	"\033": Action.QUIT,	"t": Action.SAFE,
    "w": Action.UP,		"a": Action.LEFT,	"s": Action.DOWN,
    "d": Action.RIGHT,		" ": Action.OPEN,	"\n": Action.OPEN,
    "l": Action.QUIT,		"?": Action.HINT,	"b": Action.HINT,
    "f": Action.FLAG,		"q": Action.QUIT,	"m": Action.MINE,
    "\t": Action.FLAG,		"9": Action.MINE,	"0": Action.SAFE
}

KEY_DESCRIPTIONS = """Näppäinasettelu:

  YLÖS, ALAS, VASEN, OIKEA, PGDN, PGUP, HOME, END, w, a, s, d
                       Kursorin liikuttaminen pelilaudalla
  
  ENTER, SPACE         Avaa laatta
  
  f, TAB               Vaihda laatan merkintää
  m, 9                 Merkitse miinaksi
  t, 0                 Merkitse turvalliseksi
  
  ?, b                 Vihje tekoälyltä

  l, q, ESC            Pelin lopetus
"""

@dataclass
class TileType:
    """ ruututyyppien tallennusmuotojen kuvaus"""
    text: str		# Teksti
    colors: []		# Lista (väri, tausta) pareja tekstin kaunistamiseen


TileTypes = {
    Tile.BLANK:		TileType( "[ ]", [(0x7,0), (0x7,0), (0x7,0)] ),
    Tile.ONE:		TileType( "[1]", [(0xA,0), (0xA,0), (0xA,0)] ),
    Tile.TWO:		TileType( "[2]", [(0xB,0), (0xB,0), (0xB,0)] ),
    Tile.THREE:		TileType( "[3]", [(0xD,0), (0xD,0), (0xD,0)] ),
    Tile.FOUR:		TileType( "[4]", [(0x9,0), (0x9,0), (0x9,0)] ),
    Tile.FIVE:		TileType( "[5]", [(0x9,0), (0x9,0), (0x9,0)] ),
    Tile.SIX:		TileType( "[6]", [(0x9,0), (0x9,0), (0x9,0)] ),
    Tile.SEVEN:		TileType( "[7]", [(0x9,0), (0x9,0), (0x9,0)] ),
    Tile.EIGHT:		TileType( "[8]", [(0x9,0), (0x9,0), (0x9,0)] ),
    Tile.MINE:		TileType( "[@]", [(0xF,1), (0xF,1), (0xF,1)] ),
    Tile.FLAG_MINE:	TileType( "[×]", [(0x8,7), (0x1,7), (0x8,7)] ),
    Tile.FLAG_FREE:	TileType( "[•]", [(0x8,7), (0x2,7), (0x8,7)] ),
    Tile.UNOPENED:	TileType( "[#]", [(0x8,7), (0x8,7), (0x8,7)] ),
    Tile.FLAG_UNKNOWN:	TileType( "[?]", [(0x8,7), (0x0,7), (0x8,7)] )
}
