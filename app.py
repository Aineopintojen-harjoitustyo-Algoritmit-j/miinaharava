""" app.py - pääohjelma """
from board import Board, Level
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
            if args.mines: board_opts['mines'] = args.mines
            if args.size:
                board_opts['width'] = args.size[0]
                board_opts['height'] = args.size[1]

            if args.bot==0: tui_opts['bot'] = None
            if args.bot==1: tui_opts['bot'] = SimpleBot
            tui_opts['autoplay'] = args.autoplay > 0
            tui_opts['interactive'] = args.autoplay != 2
            tui_opts['suppress'] = args.quiet

        self.board = Board(**board_opts)
        tui_opts['level_name'] = self.board.get_level_name()
        tui_opts['height'] = self.board.get_height()
        self.ui = Tui(**tui_opts)
        self.game = Game(self.board,self.ui)

    def run(self):
        """ käynnistää pelin """
        while self.game.next():
            pass
        return self.board.is_winning()
