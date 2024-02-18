""" bots/bot.py - Pohja teköälylle. """
from tui import Action
from board import Tile

class Bot():
    """ Tekoäly luokan runko joka toimii pohjana. Tekoäly palauttaa vihjeitä
    saamansa näkymän mukaan. """
    def __init__(self, **opts):
        self.uncertain = opts['uncertain'] if 'uncertain' in opts else False
        self.safe_tiles = set()
        self.mine_tiles = set()
        self.matrix = []
        self.w, self.h = 0, 0

    def search(self):
        """ Etsii varmoja miinoja ja vapaita ja lisää ne joukkoihin. Palauttaa
        True mikäli etsintä tuotti tulosta. """
        return False

    def lucky_guess(self):
        """ Lisää arvauksen vapaiden laattojen joukkoon ja palauttaa True
        onnistuessaan """
        return False

    def get_hint_from_list(self):
        """ Hakee vihjeen suoraan vapaiden tai miinojen joukoista. """
        for action, tiles in (
                (Action.SAFE, self.safe_tiles),
                (Action.MINE, self.mine_tiles)):
            if tiles:
                return action, *tiles.pop()
        return Action.NOOP, 0, 0	# Tänne ei koskaan päädytä

    def saved_hints(self):
        """ Kertoo onko miinojen tai vapaiden joukossa jäljellä vihjeitä.
        Siivoaa samalla joukoista jo avatut laatat."""
        for tile in list(self.safe_tiles):
            if self.known_tile(tile):
                self.safe_tiles.remove(tile)
        for tile in list(self.mine_tiles):
            if self.known_tile(tile):
                self.mine_tiles.remove(tile)
        return self.safe_tiles or self.mine_tiles

    def hint(self, matrix, cursor_x, cursor_y):
        """ Kysyy tekoälyltä vihjettä. Joko palauttaa vihjeen, arvauksen tai
        vain nykyisen paikan ilman toimintoa. """
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
        """ Apufunktio joka palauttaa pelilaudan mitat. """
        return len(self.matrix), len(self.matrix[0])

    def get_neighbours(self, tile):
        """ Apufunktio joka palauttaa kysytyn laatan naapurit joukkona. """
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
        """ Palauttaa kysytyn laatan tiedot. """
        return self.matrix[tile[0]][tile[1]]

    def remove_number_tiles(self, tiles):
        """ Poistaa vapaat, vapaaksi merkityt ja numerolaatat joukosta. """
        for tile in list(tiles):
            if self.matrix[tile[0]][tile[1]] < Tile.FLAG_MINE:
                tiles.remove(tile)

    def remove_mine_tiles(self, tiles):
        """ Poistaa pommit ja pommiksi merkityt joukosta. """
        count=0
        for tile in list(tiles):
            if self.matrix[tile[0]][tile[1]] in (Tile.MINE, Tile.FLAG_MINE):
                tiles.remove(tile)
                count+=1
        return count

    def known_tile(self, tile):
        """ Kortoo onko laatta merkitty tai avattu. """
        return self.matrix[tile[0]][tile[1]] < Tile.UNOPENED

    def number_tile(self, tile):
        """ Kertoo onko laatta numerolaatta """
        return 0 < self.matrix[tile[0]][tile[1]] < Tile.MINE

    def count_unknowns(self, tiles):
        """ Laskee laatat jotka on sekä avaamattomia että merkitsemättömiä. """
        count=0
        for tile in list(tiles):
            if not self.known_tile(tile):
                count+=1
        return count


    def get_interesting_tiles(self):
        """ Etsii laattojen joukon, jossa jokainen laatta on numerolaatta
        jonka naapurissa vähintään 1 mutta ei kaikki tuntemattomia """
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
        """ Etsii laattojen joukon, joissa jokainen laatta on numerolaatta
        jonka naapurista löytyy tuntematon. """
        tiles = set()
        for x in range(self.w):
            for y in range(self.h):
                if self.number_tile((x,y)):
                    n = self.get_neighbours((x,y))
                    if self.count_unknowns(n):
                        tiles.add((x,y))
        return tiles

    def get_unknown_tiles(self):
        """ Palauttaa kaikkien tuntemattomien laattojen joukon. """
        tiles = set()
        for x in range(self.w):
            for y in range(self.h):
                if not self.known_tile((x,y)):
                    tiles.add((x,y))
        return tiles
