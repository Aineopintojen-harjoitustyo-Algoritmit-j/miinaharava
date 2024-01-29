""" bots/simple.py - yksinkertainen botti joka etsii vain yhdeltä laatalta """
from random import sample
from .bot import Bot

class SimpleBot(Bot):
    """ SimpleBot - perustyhmä botti """

    def search(self):
        """ simple_search - jos viereisten avaamattomien määrä tästmää """
        tiles = self.get_interesting_tiles()
        for tile in tiles:
            c = self.get_value(tile)
            n = self.get_neighbours(tile)
            self.remove_number_tiles(n)
            c -= self.remove_bomb_tiles(n)
            if c == 0:
                for safe in n:
                    self.safe_tiles.add(safe)
            if c == len(n):
                for bomb in n:
                    self.bomb_tiles.add(bomb)
        return self.saved_hints()

    def lucky_guess(self):
        tiles = self.get_unknown_tiles()
        if tiles:
            self.safe_tiles.add(sample(sorted(tiles),1)[0])
            return True
        return False
