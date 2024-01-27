""" autotui - pelaa botin antamat vinkit jonka jälkeen käyttäjän """
from .tui import Tui
from .static import Action

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
