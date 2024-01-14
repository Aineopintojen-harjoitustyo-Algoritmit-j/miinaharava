""" tui/tui.py - teksikäyttöliittymä """
# pylint: disable = multiple-imports
import termios, fcntl, sys, os
from time import sleep
from tui.static import Action, ActionKeys, Colors, TileTypes


class Tui():
    """ Tui - Luokka käyttäjän interaktiota varten """
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
        """ asettaa tekstin värin """
        if color in range(16):
            print(end=f"\033[{'1;' if color//8 else ''}3{color%8}m")


    def set_bg(self, color):
        """ asettaa tekstin taustan värin"""
        if color in range(8):
            print(end=f"\033[4{color}m")


    def cursor_up(self, lines):
        """ liikuttaa kursoria ylöspäin"""
        print(end=f"\033[{lines}F")


    def reset_color(self):
        """ resetoi tekstin värin ja muut attribuutit perusarvoille """
        print(end="\033[0m")


    def draw_tile(self, tile, hilighted):
        """ "piirtää" yhden ruudun """
        for ch, colors in zip(TileTypes[tile].text, TileTypes[tile].colors):
            color, bg = colors
            self.set_color(Colors.BLACK if hilighted else color)
            self.set_bg(Colors.CYAN if hilighted else bg)
            print(end=ch)
            self.reset_color()


    def draw_matrix(self, matrix, hx, hy):
        """ "piirtää" ruudukon """
        self.cursor_up(len(matrix[0]))
        # pylint: disable=consider-using-enumerate
        for y in range(len(matrix[0])):
            for x in range(len(matrix)):
                self.draw_tile(matrix[x][y], x == hx and y == hy)
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
