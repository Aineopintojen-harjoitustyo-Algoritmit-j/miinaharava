""" ansi.py - ansi ohjauskomentoja. värit jne """

class Ansi:
    """ Ansi - Luokallinen staattisia metodeja ansi komennoille """

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

    @staticmethod
    def color(color):
        """ asettaa tekstin värin """
        if color in range(16):
            print(end=f"\033[{'1;' if color//8 else ''}3{color%8}m")


    @staticmethod
    def bg(color):
        """ asettaa tekstin taustan värin"""
        if color in range(8):
            print(end=f"\033[4{color}m")


    @staticmethod
    def cup(lines):
        """ liikuttaa kursoria ylöspäin"""
        print(end=f"\033[{lines}F")


    @staticmethod
    def reset():
        """ resetoi tekstin värin ja muut attribuutit perusarvoille """
        print(end="\033[0m")
