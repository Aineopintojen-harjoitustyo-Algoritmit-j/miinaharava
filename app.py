""" app.py - pääohjelma """
from board.board import Board, Level
from tui.tui import Tui
from game.game import Game
#from bots.idiot import IdiotBot
from bots.bad import BadBot

# pylint: disable = too-few-public-methods
class App:
    """ App - Luokka pääohjelmalle"""
    def __init__(self):
        self.board = Board(level=Level.BEGINNER)
        self.bot = BadBot()
        self.ui = Tui(self.bot)
        self.game = Game(self.board,self.ui)

    def run(self):
        """ käynnistää pelin """
        while self.game.next():
            pass
