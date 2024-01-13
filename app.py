""" app.py - pääohjelma """
from board.board import Board
from tui.tui import Tui, Action

# pylint: disable = too-few-public-methods
class App:
    """ App - Luokka pääohjelmalle"""
    def __init__(self):
        self.b = Board(13)
        self.t = Tui()

    def run(self):
        """ käynnistää pääohjelman """
        x, y = 0, 0
        # Printataan tyhjää tilaa, jotta pelalauta mahtuu ruudulle
        for _ in range(self.b.size):
            print()

        while True:
            action, x, y = self.t.matrix_selector(self.b.get_view(), x, y)
            match action:
                case Action.QUIT:
                    print("LOPETUS!")
                    break
                case Action.OPEN:
                    if self.b.get_mask(x, y) and not self.b.make_guess(x, y):
                        self.t.draw_matrix(self.b.get_view(), -1, -1)
                        print("KUOLEMA!")
                        break
                    if self.b.is_winning():
                        self.t.draw_matrix(self.b.get_view(), -1, -1)
                        print("VOITTO!")
                        break
                case Action.FLAG:
                    self.b.flag_tile(x, y)
