""" game/game.py - pelin etenemiseen liittyvä ohjaus """
from tui import Action

class Game:
    """ Game - peli """
    def __init__(self, board, ui):
        self.board = board
        self.ui = ui
        self.x, self.y = board.get_width()//2, board.get_height()//2


    def __del__(self):
        self.board.reveal()
        self.ui.game_end(self.board.get_view())


    def next(self):
        """ seuraava kiitos vai jotain muuta? """
        action, self.x, self.y = self.ui.matrix_selector(
                self.board.get_view(), self.x, self.y
        )
        match action:
            case Action.QUIT:
                return False
            case Action.OPEN:
                if self.board.get_mask(self.x, self.y):
                    if not self.board.guess(self.x, self.y):
                        self.ui.game_over(
                                self.board.get_view(), self.x, self.y
                        )
                        return False
                if self.board.is_winning():
                    self.ui.game_win(self.board.get_view(), self.x, self.y)
                    return False
            case Action.FLAG:
                self.board.flag(self.x, self.y)
            case Action.MINE:
                self.board.flag(self.x, self.y, 10)
            case Action.SAFE:
                self.board.flag(self.x, self.y, 11)
        return True
