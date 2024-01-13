import termios, fcntl, sys, os
from time import sleep
from tui.static import Action, ActionKeys, ActionEscKeys, Colors, TileTypes


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
        if color >= 0 and color < 16:
            print(end=f"\033[{'1;' if color//8 else ''}3{color%8}m")

    def set_bg(self, color):
        if color >= 0 and color < 8:
            print(end=f"\033[4{color}m")

    def cursor_up(self, lines):
        print(end=f"\033[{lines}F")

    def reset_color(self):
        print(end="\033[0m")

    def draw_tile(self, tile, hilighted):
        for i in range(len(TileTypes[tile].text)):
            color, bg = TileTypes[tile].colors[i]
            self.set_color(Colors.BLACK if hilighted else color)
            self.set_bg(Colors.CYAN if hilighted else bg)
            print(end=TileTypes[tile].text[i])
            self.reset_color()

    def draw_matrix(self, matrix, hx, hy):
        self.cursor_up(len(matrix[0]))
        for y in range(len(matrix[0])):
            for x in range(len(matrix)):
                self.draw_tile(matrix[x][y],
                               x == hx and y == hy)
            print()

    def read_action(self):
        escape = 0
        while True:
            try:
                # Ehkä riittää jos näppäimiä luetaan 200x sekunnissa
                sleep(0.005)
                c = sys.stdin.read(1)
            except:
                continue
            if escape:
                if c in "[0123456789":
                    continue
                if c in ActionEscKeys:
                    return ActionEscKeys[c]
                escape = 0
                continue
            else:
                if c == '\033':
                    escape = 1
                    continue
                if c in ActionKeys:
                    return ActionKeys[c]

    def matrix_selector(self, matrix, x, y):
        self.draw_matrix(matrix, x, y)
        while True:
            action = self.read_action()
            match action:
                case Action.QUIT:
                    return (action, x, y)
                case Action.OPEN | Action.FLAG:
                    if matrix[x][y] >= 10:
                        return (action, x, y)
                case Action.UP:
                    y = y-1 if y > 0 else 0
                case Action.LEFT:
                    x = x-1 if x > 0 else 0
                case Action.DOWN:
                    y = y+1 if y < len(matrix[0])-1 else y
                case Action.RIGHT:
                    x = x+1 if x < len(matrix)-1 else x
            self.draw_matrix(matrix, x, y)
