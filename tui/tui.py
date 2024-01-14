""" tui/tui.py - teksikäyttöliittymä """
# pylint: disable = multiple-imports
import termios, fcntl, sys, os
from time import sleep
from tui.static import Action, ActionKeys, TileTypes
from tui.ansi import Ansi


class Tui():
    """ Tui - Luokka käyttäjän interaktiota varten """
    def __init__(self, bot = None):
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

        self.bot = bot


    def __del__(self):
        # palautetaan terminaali takaisin alkupetäiseen uskoon
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSAFLUSH, self.oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, self.oldflags)
        print()


    def draw_tile(self, tile, hilighted):
        """ "piirtää" yhden ruudun """
        for ch, colors in zip(TileTypes[tile].text, TileTypes[tile].colors):
            color, bg = colors
            Ansi.color(Ansi.BLACK if hilighted else color)
            Ansi.bg(Ansi.CYAN if hilighted else bg)
            print(end=ch)
            Ansi.reset()


    def draw_matrix(self, matrix, hx, hy):
        """ "piirtää" ruudukon """
        Ansi.cup(len(matrix[0]))
        # pylint: disable=consider-using-enumerate
        for y in range(len(matrix[0])):
            for x in range(len(matrix)):
                hilight = matrix[x][y] != 9 and x == hx and y == hy
                self.draw_tile(matrix[x][y], hilight)
            print()


    def read_action(self):
        """ lukee näppäimistölä käyttäjän toiminnon """
        while True:
            # Ehkä riittää jos näppäimiä luetaan 50x sekunnissa
            sleep(0.02)
            try:
                keycode = sys.stdin.read(16)
            except KeyboardInterrupt:
                return Action.QUIT
            if keycode:
                for key, action in ActionKeys.items():
                    if keycode.startswith(key):
                        return action


    def matrix_selector(self, matrix, x, y):
        """ piirtää ruudukon ja antaa käyttäjän valita nuolinäppäimillä """
        self.draw_matrix(matrix, x, y)
        while True:
            action = self.read_action()
            match action:
                case Action.QUIT:
                    return (action, x, y)
                case Action.OPEN | Action.FLAG | Action.BOMB | Action.SAFE:
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
                case Action.TOP:
                    y = 0
                case Action.BOTTOM:
                    y = len(matrix[0])-1
                case Action.BEGIN:
                    x = 0
                case Action.END:
                    x = len(matrix)-1
                case Action.HINT:
                    if self.bot is not None:
                        return (Action.BOMB, 0, 0)
            self.draw_matrix(matrix, x, y)


    def show_board_with_text(self, matrix, x, y, text):
        """ näyttää laudan, tekstin alla ja jää odottelemaan nappia """
        self.draw_matrix(matrix, x, y)
        print(text)
        Ansi.cup(1)
        self.read_action()


    def game_begin(self, size):
        """ ruudun alustus ja lähtökoordinaatien määritys """
        print(end="\n"*(size+1))
        Ansi.cup(1)
        return size//2, size//2


    def game_over(self, matrix, x, y):
        """ näyttää pelin lopputilanteen ja odottaa nappia """
        self.show_board_with_text(matrix, x, y,
                "KUOLEMA! ...näppäimellä eteenpäin...")


    def game_win(self, matrix, x, y):
        """ näyttäää pelin lopputilanteen ja odottaa nappia """
        self.show_board_with_text(matrix, x, y,
                "VOITTO! ...näppäimellä eteenpäin...")


    def game_end(self, matrix):
        """ pelin lopetus """
        self.show_board_with_text(matrix, -1, -1,
                "PELI OHI! ...näppäimellä eteenpäin...")
        print()
