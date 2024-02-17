""" tui/kbd.py - näppäimistön käsittellijä """
# pylint: disable = multiple-imports
import termios, fcntl, sys, os, io
from time import sleep
from .static import ActionKeys, Action

class NoKbd():
    """ NoKbd - näppis-ei-käsittelijä """
    # pylint: disable = unused-argument
    def read_action(self):
        """ read_action - ilman näppistä -> loppu """
        return Action.QUIT

    def read_matrix_action(self, w, h, x, y):
        """ read_matrix_action - ilman näppistä -> loppu """
        return Action.QUIT, 0, 0

class Kbd():
    """ Kbd - näppiskäsittelijä """
    def __init__(self):
        # Vaatii hieman terminaaliasetusten muokkaamista jotta yksittäiset
        # napin painallukset voidaan lukea
        # https://stackoverflow.com/questions/983354/how-do-i-wait-for-a-pressed-key
        try:
            fd = sys.stdin.fileno()
            self.oldterm = termios.tcgetattr(fd)

            newattr = termios.tcgetattr(fd)
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, newattr)

            self.oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)
        # Testeissä ei voi mukata termilaalia
        except io.UnsupportedOperation:
            pass

    def __del__(self):
        # palautetaan terminaali takaisin alkupetäiseen uskoon
        try:
            fd = sys.stdin.fileno()
            termios.tcsetattr(fd, termios.TCSAFLUSH, self.oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, self.oldflags)
        # Testeissä ei voi mukata termilaalia
        except io.UnsupportedOperation:
            pass

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

    def read_matrix_action(self, w, h, x, y):
        """ read_matrix_action - lukee actionit ja pitää huolen koordinaat"""
        action = self.read_action()
        match action:
            case Action.QUIT | Action.HINT:
                return (action, x, y)
            case Action.OPEN | Action.FLAG | Action.MINE | Action.SAFE:
                return (action, x, y)
            case Action.UP:
                y = y-1 if y > 0 else 0
            case Action.LEFT:
                x = x-1 if x > 0 else 0
            case Action.DOWN:
                y = y+1 if y < h-1 else y
            case Action.RIGHT:
                x = x+1 if x < w-1 else x
            case Action.TOP:
                y = 0
            case Action.BOTTOM:
                y = h-1
            case Action.BEGIN:
                x = 0
            case Action.END:
                x = w-1
        return (Action.NOOP, x, y)
