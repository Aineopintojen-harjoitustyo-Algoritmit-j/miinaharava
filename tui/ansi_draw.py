""" tui/ansi_draw.py - perustukset ansi tulostelulle """
# pylint: disable = multiple-imports
from .ansi import Ansi
from .static import TileTypes

class AnsiDraw():
    """ AnsiDraw - "piirtelee" näytölle kirjailmilla """
    def __init__(self, height = 9, name = ""):
        print(end='\n'*height+name+": Peli alkaa.")

    def __del__(self):
        print()

    def __tile(self, tile, hilighted):
        """ "piirtää" yhden ruudun """
        for ch, colors in zip(TileTypes[tile].text, TileTypes[tile].colors):
            color, bg = colors
            Ansi.color(Ansi.BLACK if hilighted else color)
            Ansi.bg(Ansi.CYAN if hilighted else bg)
            print(end=ch)
            Ansi.reset()


    def matrix(self, matrix, hx, hy):
        """ "piirtää" ruudukon """
        Ansi.cup(len(matrix[0]))
        # pylint: disable=consider-using-enumerate
        for y in range(len(matrix[0])):
            for x in range(len(matrix)):
                hilight = matrix[x][y] != 9 and x == hx and y == hy
                self.__tile(matrix[x][y], hilight)
            print()


    def status_line(self, text):
        """ draw_status_line - tulostaa pelitietorivin"""
        print(end=text+'\r')

class SuppressDraw():
    """ SuppressDraw - vain status """
    # pylint: disable = unused-argument

    def matrix(self, matrix, hx, hy):
        """ "piirtää" ruudukon """
        return True

    def status_line(self, text):
        """ draw_status_line - tulostaa pelitietorivin"""
        print(end=text+'\r')

class NoDraw():
    """ NoDraw - ei mitään """
    # pylint: disable = unused-argument

    def matrix(self, matrix, hx, hy):
        """ "piirtää" ruudukon """
        return True

    def status_line(self, text):
        """ draw_status_line - tulostaa pelitietorivin"""
        return True
