""" app.py - pääohjelma """
from board import Board, Level
from tui import Tui, AutoTui
from game import Game
from bots import BadBot

# pylint: disable = too-few-public-methods
class App:
    """ App - Luokka pääohjelmalle"""
    def __init__(self, args=None):
        level=Level.BEGINNER
        ui_class=Tui
        if args:
            level = Level.EXPERT if args.expert else level
            level = Level.INTERMEDIATE if args.intermediate else level
            level = Level.BEGINNER if args.beginner else level
            ui_class = AutoTui if args.auto else ui_class

        self.board = Board(level=level)
        self.bot = BadBot()
        self.ui = ui_class(self.bot)
        self.game = Game(self.board,self.ui)

    def run(self):
        """ käynnistää pelin """
        while self.game.next():
            pass
