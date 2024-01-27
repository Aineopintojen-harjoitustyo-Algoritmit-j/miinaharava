""" autotui - pelaa botin antamat vinkit jonka jälkeen käyttäjän """
from .tui import Tui
from .static import Action
from .ansi import Ansi

class AutoTui(Tui):
    """ Tui - Luokka joka tekee botin vinkit ensin """
    def matrix_selector(self, matrix, x, y):
        """ yritetään pyydellä botilta vinkkiä ensin """
        if self.bot is not None:
            action, x, y = self.bot.hint(matrix, x, y)
            if action != Action.NOOP:
                self.draw_matrix(matrix, -1, -1)
                if action==Action.SAFE:
                    action = Action.OPEN
                return action, x, y

        return super().matrix_selector(matrix, x, y)

    def show_board_with_text(self, matrix, x, y, text):
        """ näyttää laudan, tekstin alla (ei odota nappia) """
        self.draw_matrix(matrix, x, y)
        print(text)
        Ansi.cup(1)

    def game_end(self, matrix):
        """ pelin lopetus """
