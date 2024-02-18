""" bots/simple.py - yksinkertainen botti joka etsii vain yhdeltä laatalta """
from random import choice

from .bot import Bot

class SimpleBot(Bot):
    """ SimpleBot - perustyhmä botti """

    def search(self):
        """ Etsitään laattoja jotka tietyllä laatalla olevan numeron sekä
        sitä ympäröivien tuntemattomien laattojen määrän johdosta täytyy olla
        joko miinoja tai vapaita. Yhdistetään ne kyseisiin joukkoihin. """
        tiles = self.get_interesting_tiles()
        for tile in tiles:
            unknowns, minecount = self.get_unknowns_and_minecount(tile)
            if minecount == 0:
                self.safe_tiles |= unknowns
            if minecount == len(unknowns):
                self.mine_tiles |= unknowns
        return self.saved_hints()

    def get_unknowns_and_minecount(self, tile):
        """ Palauttaa tuntemattomat naapurit ja niissä olevien miinojen
        määrän """
        minecount = self.get_value(tile)
        unknowns = self.get_neighbours(tile)
        self.remove_known_safe_tiles(unknowns)
        minecount -= self.remove_mine_tiles(unknowns)
        return unknowns, minecount

    def lucky_guess(self):
        """ Arvotaan laatta tuntemattomista ja lisätään vapaiden joukkoon """
        self.safe_tiles.add(choice(list(self.get_unknown_tiles())))
        return True
