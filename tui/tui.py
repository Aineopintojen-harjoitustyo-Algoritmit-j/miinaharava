import termios, fcntl, sys, os
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
            
    
@dataclass
class TileType:
    text: str		# Teksti
    colors: []		# Lista (väri, tausta) pareja tekstille


tile_types = {
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


class Tui():
    def __init__(self):
        # Vaatii hieman terminaaliasetusten muokkaamista jotta yksittäiset
        # napin painallukset voidaan lukea
        # https://stackoverflow.com/questions/983354/how-do-i-wait-for-a-pressed-key
        fd = sys.stdin.fileno()
        self.oldterm = termios.tcgetattr(fd)
        
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        
        self.oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)
        

    def __del__(self):
        # palautetaan terminaali takaisin alkupetäiseen uskoon
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSAFLUSH, self.oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, self.oldflags)
        

    def set_color(self, color):
        if color>=0 and color<16:
            print(end=f"\033[{'1;' if color//8 else ''}3{color%8}m")


    def set_bg(self, color):
        if color>=0 and color<8:
            print(end=f"\033[4{color}m")


    def cursor_up(self, lines):
        print(end=f"\033[{lines}F")


    def reset_color(self):
        print(end="\033[0m")
        

    def draw_tile(self, tile, hilighted):
        for i in range(len(tile_types[tile].text)):
            color, bg = tile_types[tile].colors[i]
            self.set_color(Colors.BLACK if hilighted else color)
            self.set_bg(Colors.CYAN if hilighted else bg)
            print(end=tile_types[tile].text[i])
            self.reset_color()
        

    def draw_matrix(self, matrix, hx, hy ):
        self.cursor_up(len(matrix[0]))
        for y in range(len(matrix[0])):
            for x in range(len(matrix)):
                self.draw_tile( matrix[x][y], 
                        x == hx and y == hy )
            print()
            
    
    def read_action(self):
        actions = {
            'w': Action.UP,	'a': Action.LEFT,	's': Action.DOWN,
            'd': Action.RIGHT,	' ': Action.OPEN,	'\n': Action.OPEN,
            'f': Action.FLAG,	'm': Action.FLAG,	'q': Action.QUIT
        }
        esc_actions = {
            '': Action.QUIT,	'A': Action.UP,		'D': Action.LEFT,
            'C': Action.RIGHT,	'B': Action.DOWN
        }
        escape = 0
        while True:
            try:
                c = sys.stdin.read(1)
            except:
                continue
            if escape:
                if c in "[0123456789":
                    continue
                if c in esc_actions:
                    return esc_actions[c]
                escape = 0
                continue
            else:
                if c == '\033':
                    escape = 1
                    continue
                if c in actions:
                    return actions[c]
    
                

    def matrix_selector(self, matrix, x, y ):
        self.draw_matrix(matrix, x, y)
        while True:
            action = self.read_action()
            match action:
                case Action.QUIT:
                    return (action,x,y)
                case Action.OPEN | Action.FLAG:
                    if matrix[x][y]>=10:
                        return (action,x,y)
                case Action.UP:
                    y = y-1 if y>0 else 0
                case Action.LEFT:
                    x = x-1 if x>0 else 0
                case Action.DOWN:
                    y = y+1 if y<len(matrix[0])-1 else y
                case Action.RIGHT:
                    x = x+1 if x<len(matrix)-1 else x
            self.draw_matrix(matrix, x, y)
        