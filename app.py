""" app.py - pääohjelma """
from board import Board, Level, LevelSpecs
from tui import Tui
from game import Game
from bots import SimpleBot, DSSPBot

# pylint: disable = too-few-public-methods
class App:
    """ App - Luokka pääohjelmalle"""
    def __init__(self, args=None):
        level = Level.BEGINNER
        auto, uncertain, quiet = False, False, False
        if args:
            level = Level.EXPERT if args.expert else level
            level = Level.INTERMEDIATE if args.intermediate else level
            level = Level.BEGINNER if args.beginner else level
            width, height, bombs = LevelSpecs[level]
            auto = args.auto
            auto, uncertain = (True, True) if args.uncertain else (auto, False)
            auto, uncertain, quiet = (True, True, True) \
                    if args.quiet else (auto, uncertain, False)
            self.bot = SimpleBot(uncertain=uncertain) if args.simple \
                    else DSSPBot(uncertain=uncertain)
            self.ui = Tui (
                bot=self.bot,
                autoplay=auto,
                interact=not uncertain,
                suppress=quiet,
                width=width,
                height=height,
                bombs=bombs
            )

        self.board = Board(level=level)
        self.bot = DSSPBot(uncertain=uncertain) if self.bot is None \
                else self.bot
        self.ui = Tui(bot=self.bot) if self.ui is None else self.ui
        self.game = Game(self.board,self.ui)

    def run(self):
        """ käynnistää pelin """
        while self.game.next():
            pass
        return self.board.is_winning()
