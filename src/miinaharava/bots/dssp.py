""" bots/dssp.py - päättelee kahden vierekkäisen laatan perusteella """
from random import sample

from .simple import SimpleBot

class DSSPBot(SimpleBot):
    """ Kahta pistettä tutkiva tekoäly. Käyttää pohjana SipleBot tekoälyä """

    def get_pairs(self):
        """ Etsii kiinnostavien laattojen joukosta vierekkäiset """
        tiles = list(self.get_interesting_tiles())
        pairs = []
        for i, tile1 in enumerate(tiles):
            for _, tile2 in enumerate(tiles, i+1):
                if self.are_neighbours(tile1,tile2):
                    pairs.append((tile1,tile2))
                    pairs.append((tile2,tile1))
        return pairs

    def search(self):
        """ Etsitään voiko viereisen numerolaatan osoittamat miinat ja
        epävarmat poistamalla päätellä onko jokin nykyisen laatan tuntematon
        vapaa. """
        if super().search():
            return True

        for tile1, tile2 in self.get_pairs():
            c1 = self.get_value(tile1)
            c2 = self.get_value(tile2)
            n1 = self.get_neighbours(tile1)
            n2 = self.get_neighbours(tile2)
            self.remove_known_safe_tiles(n1)
            self.remove_known_safe_tiles(n2)
            c1 -= self.remove_mine_tiles(n1)
            c2 -= self.remove_mine_tiles(n2)

            # otetaan vain alue1:n laatat pois vähennetään se pommeista
            # näin tiedetään montako pommia on jäätävä yhteiselle alueelle
            nc = n1 & n2
            n1 = n1 - nc
            n2 = n2 - nc
            cc = c1 - len(n1)

            # jos yhteiselle alueelle ei jääkkään pommeja
            if cc < 1:
                continue

            # vähennetään yhteinen alue ja sen pommit alueesta 2
            # jos jäljelle ei jää miinoja merkataan alueet seiffeiks
            c2 -= cc

            if c2 == 0:
                self.safe_tiles |= n2

        return self.saved_hints()

    def lucky_guess(self):
        heatmap = dict.fromkeys(self.get_unknown_tiles(), float(0))
        tiles = self.get_border_tiles()
        for tile in tiles:
            n = self.get_neighbours(tile)
            c = self.get_value(tile) - self.remove_mine_tiles(n)
            self.remove_known_safe_tiles(n)
            for ntile in n:
                heatmap[ntile] += c/len(n)

        for tile in heatmap:
            if tile[0] in range(1,self.w-1):
                heatmap[tile]+=0.005
            if tile[1] in range(1,self.h-1):
                heatmap[tile]+=0.005

        best = min((x for _, x in heatmap.items()))
        best_tiles = [x for x,y in heatmap.items() if y == best]

        if best_tiles:
            self.safe_tiles.add(sample(best_tiles,1)[0])
            return True
        return False
