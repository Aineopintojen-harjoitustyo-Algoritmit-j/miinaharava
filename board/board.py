""" board/board.py - Pelilaudan käsittelyyn tarkoitetut jutut """
from random import randrange
from sys import stderr
from copy import deepcopy

class Board():
    """	Board - Luokka joka pitää huolen pelilaudasta ja siihen kohdistuvista
                siirroista.
    """
    def __init__(self, size = 9, bombs = 10):
        # Lauta pitää olla vähintään 2x2, jotta on jotain pelattavaa
        size = 2 if size < 2 else size
        size = 50 if size > 50 else size
        self.size = size

        # Pommeja pitää olla vähintään yksi, kuten tyhjiäkin
        bombs = size*size*size//100 if bombs < 1 else bombs
        bombs = size*size-1 if bombs>=size*size else bombs
        bombs = 1 if bombs == 0 else bombs
        self.bombs = bombs

        self.tiles = []
        self.masked = []
        self.initialize_tiles( size )
        self.randomize_bombs( bombs )
        self.calculate_neighbours()


    def initialize_tiles(self, size):
        """ alustaa pelilaudan matriisit """
        self.tiles = [[0 for _ in range(size)] for _ in range(size)]
        self.masked = [[12 for _ in range(size)] for _ in range(size)]


    def randomize_bombs(self, bomb_count):
        """ arpoo pelilaudalle pommit """
        for _ in range(bomb_count):
            while True:
                x, y = randrange(0,self.size), randrange(0,self.size)
                if self.tiles[x][y] != 0:
                    continue
                self.tiles[x][y]=9
                break


    def calculate_neighbours(self):
        """ laskee naapurissa olevien pommien määrät valmiiksi laudalle """
        for y in range(self.size):
            for x in range(self.size):
                if self.tiles[x][y] == 9:
                    continue
                neighbouring_bombs = 0
                for nx, ny in self.get_neighbours_coords(x,y):
                    if self.tiles[nx][ny] == 9:
                        neighbouring_bombs += 1
                self.tiles[x][y] = neighbouring_bombs


    def invalid_coordinates(self, x, y):
        """ onko koordinaatit pelilaudan ulkopuolella """
        return x < 0 or x >= self.size or y < 0 or y >= self.size


    def get_neighbours_coords(self, x, y, include_home = False):
        """ antaa listan naapureiden koordinaateista """
        offsets = (
            (-1,-1), (0,-1), (1,-1),
            (-1, 0), (0, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)
        ) if include_home else (
            (-1,-1), (0,-1), (1,-1),
            (-1, 0),         (1, 0),
            (-1, 1), (0, 1), (1, 1)
        )
        coordinates=[]
        for dx,dy in offsets:
            if not self.invalid_coordinates(x+dx, y+dy):
                coordinates.append( (x+dx, y+dy) )
        return coordinates


    def get_view(self):
        """ antaa matriisin nykyisestä pelinäkymästä """
        view = deepcopy(self.masked)
        for y in range(self.size):
            for x in range(self.size):
                if not view[x][y]:
                    view[x][y]=self.tiles[x][y]
        return view


    def is_winning(self):
        """ tarkistaa onko peli voitettu """
        for y in range(self.size):
            for x in range(self.size):
                if self.tiles[x][y] == 9:
                    if not self.masked[x][y]:
                        return False
                else:
                    if self.masked[x][y]:
                        return False
        return True


    def collect_area(self, x, y, area = None):
        """ tunnustelee ja palauttaa tyhjän alueen koordinaatit """
        if area is None:
            area = {(x,y)}
        to_test = []
        for nx, ny in self.get_neighbours_coords(x, y):
            if self.tiles[nx][ny] == 0 and (nx,ny) not in area:
                to_test.append((nx, ny))
                area.add((nx, ny))
        for tx, ty in to_test:
            area=area.union(self.collect_area(tx, ty, area))
        return area


    def get_mask(self, x, y):
        """ onko ruutu vielä piilossa """
        return self.masked[x][y]


    def flag(self, x, y, flag=-1):
        """ aseta lippu peitetylle ruudulle"""
        if self.invalid_coordinates(x, y):
            print("Koordinaatit on pelilaudan ulkopuolella", file=stderr)
            return False

        if self.masked[x][y] not in range(10,14):
            print("Ruudulla odottamaton lippu tai se on avattu", file=stderr)
            return False

        if flag == -1:
            self.masked[x][y] += 1 if self.masked[x][y] < 13 else -3
            return True

        if flag not in range(10,14):
            print("Lippua jota asetat ei ole olemassa", file=stderr)
            return False

        self.masked[x][y]=flag
        return True


    def guess(self, x, y):
        """ tee arvaus """
        if self.invalid_coordinates(x, y):
            print("Koordinaatit on pelilaudan ulkopuolella", file=stderr)
            return False

        if self.masked[x][y] == 0:
            print("Ruutu on jo avattu", file=stderr)
            return False

        self.masked[x][y] = 0

        if self.tiles[x][y] == 9:
            return False

        if self.tiles[x][y] == 0:
            for cx, cy in self.collect_area( x, y ):
                for nx, ny in self.get_neighbours_coords(cx, cy, True):
                    self.masked[nx][ny] = 0

        return True

    def reveal(self):
        """ näytä koko lauta """
        self.masked = [[0 for _ in range(self.size)] for _ in range(self.size)]
