""" bots/simple.py - yksinkertainen botti joka etsii vain yhdeltä laatalta """
from random import sample

from .bot import Bot

class SimpleBot(Bot):
    """ SimpleBot - perustyhmä botti """

    def search(self):
        """ Etsitään laattoja jotka tietyllä laatalla olevan numeron sekä
        sitä ympäröivien tuntemattomien laattojen määrän johdosta täytyy olla
        joko miinoja tai vapaita. Yhdistetään ne kyseisiin joukkoihin. """
        tiles = self.get_interesting_tiles()
        for tile in tiles:
            c = self.get_value(tile)
            nbrs = self.get_neighbours(tile)
            self.remove_known_safe_tiles(nbrs)
            c -= self.remove_mine_tiles(nbrs)
            if c == 0:
                self.safe_tiles |= nbrs
            if c == len(nbrs):
                self.mine_tiles |= nbrs
        return self.saved_hints()

    def lucky_guess(self):
        """ Arvotaan laatta tuntemattomista ja lisätään vapaiden joukkoon """
        tiles = list(self.get_unknown_tiles())
        if tiles:
            self.safe_tiles.add(sample(tiles,1)[0])
            return True
        return False
