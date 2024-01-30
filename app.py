""" app.py - pääohjelma """
from board import Board, Level, LevelSpecs
from tui import Tui
from game import Game
from bots import SimpleBot, DSSPBot

# pylint: disable = too-few-public-methods
class App:
    """ App - Luokka pääohjelmalle"""
    def __init__(self, args=None):
        board_opts = {'level': Level.BEGINNER}
        tui_opts = {'bot': DSSPBot}
        if args:
            if args.intermediate:
                board_opts['level'] = Level.INTERMEDIATE
            if args.expert:
                board_opts['level'] = Level.EXPERT
            if args.w:
                board_opts['width'] = args.w
            if args.H:
                board_opts['height'] = args.H
            if args.b:
                board_opts['bombs'] = args.b

            tui_opts['bot'] = SimpleBot if args.simple else DSSPBot
            tui_opts['autoplay'] = args.auto
            tui_opts['interactive'] = not args.uncertain
            tui_opts['suppress'] = args.quiet
            tui_opts['height'] = LevelSpecs[board_opts['level']][1]

        self.board = Board(**board_opts)
        self.ui = Tui(**tui_opts)
        self.game = Game(self.board,self.ui)

    def run(self):
        """ käynnistää pelin """
        while self.game.next():
            pass
        return self.board.is_winning()
