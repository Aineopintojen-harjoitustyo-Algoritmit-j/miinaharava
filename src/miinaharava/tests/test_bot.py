""" tests/test_bot.py - Testaa botin toimintaa"""
# pylint: disable = missing-class-docstring, too-few-public-methods, protected-access

import unittest

from board import Board, Tile
from bots import DSSPBot, SimpleBot
from tui import Action

class TestBotClass(unittest.TestCase):
    """ botin testit"""
    def test_init(self):
        """ olioden luominen onnistuu """
        DSSPBot()
        SimpleBot()

    def correctly_marking(self, open_free=False, bot_type=DSSPBot):
        """ Testaa onko miinat miinoja ja vapaat vapaita alkuun avatusta """
        for _ in range(500):
            brd = Board()
            # jos ei aukea ylälaidasta otetaan seuraava
            if not brd.guess(0,0):
                continue
            # vain varmat liikut
            bot = bot_type(uncertain=False)

            tested = set()
            while True:
                action, x, y = bot.hint(brd.get_view())
                if (x,y) in tested:
                    break
                tested.add((x,y))
                if action == Action.SAFE:
                    self.assertTrue( brd._Board__tiles[x][y] < Tile.MINE )
                    if open_free:
                        brd.guess(x,y)
                if action == Action.MINE:
                    self.assertTrue( brd._Board__tiles[x][y] == Tile.MINE )

    def test_dssp_marks_correctly_with_open(self):
        """ Testaa onko dssp:n miinat miinoja ja avaa vapaat """
        self.correctly_marking(True, DSSPBot)

    def test_simple_marks_correctly_with_open(self):
        """ Testaa onko dssp:n miinat miinoja ja avaa vapaat """
        self.correctly_marking(True, SimpleBot)

    def test_dssp_marks_correctly(self):
        """ Testaa onko dssp:n miinat miinoja ja vapaat vapaita """
        self.correctly_marking(False, DSSPBot)

    def test_simple_marks_correctly(self):
        """ Testaa onko simple:n miinat miinoja ja vapaat vapaita """
        self.correctly_marking(False, SimpleBot)
