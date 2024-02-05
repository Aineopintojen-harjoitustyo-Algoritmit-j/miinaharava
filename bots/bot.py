""" bots/bot.py - bottien kantaisä """
from tui import Action
from board import Tile

class Bot():
    """ Bot - perusluokka perittäväksi """
    def __init__(self, **opts):
        self.uncertain = opts['uncertain'] if 'uncertain' in opts else False
        self.safe_tiles = set()
        self.mine_tiles = set()
        self.matrix = []
        self.w = 0
        self.h = 0

    def search(self):
        """ search - etsii pommeja tai vapaita ko joukkoihin """
        return False

    def lucky_guess(self):
        """ lucky_guess - lisää yhden arvatun vapaan vapaiden joukkoon """
        return Action.NOOP, 0, 0

    def get_hint_from_list(self):
        """ palauttaa vihjeen suoraan listalta """
        if self.safe_tiles:
            x, y = self.safe_tiles.pop()
            return Action.SAFE, x, y
        if self.mine_tiles:
            x, y = self.mine_tiles.pop()
            return Action.MINE, x, y
        return Action.NOOP, 0, 0

    def saved_hints(self):
        """ poistetaan auenneet laatat ja palautetaan onko muuveja """
        for tile in list(self.safe_tiles):
            if self.known_tile(tile):
                self.safe_tiles.remove(tile)
        for tile in list(self.mine_tiles):
            if self.known_tile(tile):
                self.mine_tiles.remove(tile)
        return self.safe_tiles or self.mine_tiles

    def hint(self, matrix, cursor_x, cursor_y):
        """ antaa vinkin. tässä tapauksessa ei mitään """
        self.matrix = matrix
        self.w, self.h = self.get_dimensions()

        if self.saved_hints():
            return self.get_hint_from_list()
        if self.search():
            return self.get_hint_from_list()
        if self.uncertain and self.lucky_guess():
            return self.get_hint_from_list()
        return Action.NOOP, cursor_x, cursor_y

    def get_dimensions(self):
        """ palauttaa matriisin dimensiot """
        return len(self.matrix), len(self.matrix[0])

    def get_neighbours(self, tile):
        """ palauttaa viereiset koordinaatit joukkona """
        x, y = tile
        offsets = (
            (-1, -1), ( 0, -1), ( 1, -1),
            (-1,  0),           ( 1,  0),
            (-1,  1), ( 0,  1), ( 1,  1),
        )
        tiles=set()
        for ox, oy in offsets:
            if ox+x in range(self.w):
                if oy+y in range(self.h):
                    tiles.add((ox+x, oy+y))
        return tiles

    def get_value(self, tile):
        """ palauttaa laatan arvon """
        return self.matrix[tile[0]][tile[1]]

    def remove_number_tiles(self, tiles):
        """ poistaa vapaat ja vapaaksi merkityt alueet ja numerolaatat """
        for tile in list(tiles):
            if self.matrix[tile[0]][tile[1]] < Tile.FLAG_MINE:
                tiles.remove(tile)

    def remove_mine_tiles(self, tiles):
        """ poistaa pommit ja pommiksi merkityt """
        count=0
        for tile in list(tiles):
            if self.matrix[tile[0]][tile[1]] in (Tile.MINE, Tile.FLAG_MINE):
                tiles.remove(tile)
                count+=1
        return count

    def known_tile(self, tile):
        """ tutkii onko laatta tiedetty """
        return self.matrix[tile[0]][tile[1]] < Tile.UNOPENED

    def number_tile(self, tile):
        """ tutkii onko numerolaatta """
        return 0 < self.matrix[tile[0]][tile[1]] < Tile.MINE

    def count_unknowns(self, tiles):
        """ laskee tunnistamattomat laatat """
        count=0
        for tile in list(tiles):
            if not self.known_tile(tile):
                count+=1
        return count


    def get_interesting_tiles(self):
        """ palauttaa laatat joiden naapureissa on vaihtelua """
        tiles = set()
        for x in range(self.w):
            for y in range(self.h):
                if self.number_tile((x,y)):
                    n = self.get_neighbours((x,y))
                    l = len(n)
                    r = self.count_unknowns(n)
                    if r in range(1,l-1):
                        tiles.add((x,y))
        return tiles

    def get_border_tiles(self):
        """ palauttaa palauttaa numerolaatat joiden vieressä avaamaton """
        tiles = set()
        for x in range(self.w):
            for y in range(self.h):
                if self.number_tile((x,y)):
                    n = self.get_neighbours((x,y))
                    if self.count_unknowns(n):
                        tiles.add((x,y))
        return tiles

    def get_unknown_tiles(self):
        """ palauttaa kaikki tuntemattomat laatat """
        tiles = set()
        for x in range(self.w):
            for y in range(self.h):
                if not self.known_tile((x,y)):
                    tiles.add((x,y))
        return tiles
