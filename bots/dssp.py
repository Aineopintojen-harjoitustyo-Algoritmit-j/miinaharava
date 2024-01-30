""" bots/dssp.py - päättelee kahden vierekkäisen laatan perusteella """
from random import sample
from .simple import SimpleBot

class DSSPBot(SimpleBot):
    """ DSSPBot - perustyhmä botti """

    def search(self):
        """ search - etsii kahden vierekkäisen laatan perusteella"""
        if super().search():
            return True
        tiles = list(self.get_interesting_tiles())
        pairs = []
        # pylint: disable = consider-using-enumerate
        for i in range(len(tiles)):
            for j in range(i+1,len(tiles)):
                if abs(tiles[i][0]-tiles[j][0])==1 or abs(tiles[i][1]-tiles[j][1])==1:
                    pairs.append((tiles[i],tiles[j]))
                    pairs.append((tiles[j],tiles[i]))

        for tile1, tile2 in pairs:
            c1 = self.get_value(tile1)
            c2 = self.get_value(tile2)
            n1 = self.get_neighbours(tile1)
            n2 = self.get_neighbours(tile2)
            self.remove_number_tiles(n1)
            self.remove_number_tiles(n2)
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
            # jos jäljelle ei jää pommeja merkataan seiffeiks
            # jos avaamattomia pommien määrä merkataan pommeiks
            c2 -= cc

            if c2 == 0:
                for safe in n2:
                    self.safe_tiles.add(safe)
            if cc == len(nc) and c2 == len(n2):
                for mine in n2:
                    self.mine_tiles.add(mine)

        return self.saved_hints()

    def lucky_guess(self):
        heatmap = dict.fromkeys(self.get_unknown_tiles(), float(0))
        tiles = self.get_border_tiles()
        for tile in tiles:
            n = self.get_neighbours(tile)
            c = self.get_value(tile) - self.remove_mine_tiles(n)
            self.remove_number_tiles(n)
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
