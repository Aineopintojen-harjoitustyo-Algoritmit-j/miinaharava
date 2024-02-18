""" bots/dssp.py - päättelee kahden vierekkäisen laatan perusteella """
from random import choice

from .simple import SimpleBot

class DSSPBot(SimpleBot):
    """ Kahden pisteen naapureita tutkiva tekoäly. Pohjana SipleBot tekoäly."""

    def search(self):
        """ Etsitään voiko viereisen numerolaatan osoittamat miinat ja
        epävarmat poistamalla päätellä onko jokin nykyisen laatan tuntematon
        vapaa. """
        if super().search():
            return True

        for tile1, tile2 in self.get_pairs():
            unknowns1, minecount1 = self.get_unknowns_and_minecount(tile1)
            unknowns2, minecount2 = self.get_unknowns_and_minecount(tile2)
            # Kun 1. alueen miinoista vähennetään vain 1. alueella olevat
            # tuntemattomat laatat saadaan vähimmäismäärä miinoille yhteisellä
            # alueella.
            common_minecount = minecount1 - len(unknowns1-unknowns2)
            # Turha jatkaa jos yhteiselle alueelle ei tarvitse asettaa miinoja.
            if common_minecount < 1:
                continue
            # Vähennetään yhteiset tuntemattomat 2. alueen tuntemattomista.
            unknowns2 = unknowns2 - unknowns1
            # Vähennetään 2. aluuen miinoista ne jotka on pakko sijoittaa
            # yhteiselle alueella
            minecount2 -= common_minecount
            # Jos 2. alueelle ei jää yhtään miinaa tiedetään kaikki
            # tuntemattomat siellä vapaiksi
            if minecount2 == 0:
                self.safe_tiles |= unknowns2
        return self.saved_hints()

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

    def lucky_guess(self):
        """ Tehdään arvaus kylmimpien laattojen joukosta """
        heatmap = dict.fromkeys(self.get_unknown_tiles(), float(0))
        # Lisätään lämpöä viereisten tuntemattomien ja jäljellä olevien
        # miinojen suhteen verran.
        for tile in self.get_border_tiles():
            unknowns, minecount = self.get_unknowns_and_minecount(tile)
            for utile in unknowns:
                heatmap[utile] += minecount/len(unknowns)
        # Lisätään lämpöä keskimmäisiin laattoihin. Kulmat ei saa lämpöä.
        for tile in heatmap:
            if tile[0] in range(1,self.w-1):
                heatmap[tile]+=0.005
            if tile[1] in range(1,self.h-1):
                heatmap[tile]+=0.005
        # Etsitään kylmin arvo ja kylmimmät laatat ja arvotaan niistä yksi.
        coolest_value = min((x for _, x in heatmap.items()))
        coolest_tiles = [x for x,y in heatmap.items() if y == coolest_value]
        self.safe_tiles.add(choice(coolest_tiles))
        return True
