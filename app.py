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
            # pylint: disable = multiple-statements
            if args.intermediate: board_opts['level'] = Level.INTERMEDIATE
            if args.expert: board_opts['level'] = Level.EXPERT
            if args.width: board_opts['width'] = args.width
            if args.height: board_opts['height'] = args.height
            if args.mines: board_opts['mines'] = args.mines

            if args.simple: tui_opts['bot'] = SimpleBot
            tui_opts['autoplay'] = args.auto
            tui_opts['interactive'] = not args.uncertain
            tui_opts['suppress'] = args.quiet
            tui_opts['height'] = LevelSpecs[board_opts['level']][1]

        self.board = Board(**board_opts)
        tui_opts['level_name']=self.board.get_level_name()
        self.ui = Tui(**tui_opts)
        self.game = Game(self.board,self.ui)

    def run(self):
        """ käynnistää pelin """
        while self.game.next():
            pass
        return self.board.is_winning()
