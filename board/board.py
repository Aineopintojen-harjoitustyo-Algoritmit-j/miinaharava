""" board/board.py - Pelilaudan käsittelyyn tarkoitetut jutut """
from random import randrange
from sys import stderr
from copy import deepcopy

class Board():
    """	Board - Luokka joka pitää huolen pelilaudasta ja siihen kohdistuvista
                siirroista.
    """
    def __init__(self, width = 9, height = 9, bombs = 10):
        # Lauta pitää olla vähintään 2x2, jotta on jotain pelattavaa
        #size = 2 if size < 2 else size
        #size = 50 if size > 50 else size
        #self.size = size
        width = 2 if width < 2 else width
        width = 50 if width > 50 else width

        height = 2 if height < 2 else height
        height = 50 if height > 50 else height

        # Pommeja pitää olla vähintään yksi, kuten tyhjiäkin
        #bombs = size*size*size//100 if bombs < 1 else bombs
        bombs = width*height-1 if bombs>=width*height else bombs
        bombs = 1 if bombs == 0 else bombs

        self.__width = width
        self.__height = height
        self.__bombs = bombs
        self.__tiles = None
        self.__masked = None
        self.__initialize_tiles()
        self.__randomize_bombs()
        self.__calculate_neighbours()


    def __initialize_tiles(self):
        """ alustaa pelilaudan matriisit """
        w, h = self.__width, self.__height
        self.__tiles = [[0 for _ in range(h)] for _ in range(w)]
        self.__masked = [[12 for _ in range(h)] for _ in range(w)]


    def __randomize_bombs(self):
        """ arpoo pelilaudalle pommit """
        for _ in range(self.__bombs):
            while True:
                x, y = randrange(0,self.__width), randrange(0,self.__height)
                if self.__tiles[x][y] != 0:
                    continue
                self.__tiles[x][y]=9
                break


    def __calculate_neighbours(self):
        """ laskee naapurissa olevien pommien määrät valmiiksi laudalle """
        for y in range(self.__height):
            for x in range(self.__width):
                if self.__tiles[x][y] == 9:
                    continue
                neighbouring_bombs = 0
                for nx, ny in self.get_neighbours_coords(x,y):
                    if self.__tiles[nx][ny] == 9:
                        neighbouring_bombs += 1
                self.__tiles[x][y] = neighbouring_bombs


    def invalid_coordinates(self, x, y):
        """ onko koordinaatit pelilaudan ulkopuolella """
        return x < 0 or x >= self.__width or y < 0 or y >= self.__height


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
        view = deepcopy(self.__masked)
        for y in range(self.__height):
            for x in range(self.__width):
                if not view[x][y]:
                    view[x][y]=self.__tiles[x][y]
        return view


    def is_winning(self):
        """ tarkistaa onko peli voitettu """
        for y in range(self.__height):
            for x in range(self.__width):
                if self.__tiles[x][y] == 9:
                    if not self.__masked[x][y]:
                        return False
                else:
                    if self.__masked[x][y]:
                        return False
        return True


    def collect_area(self, x, y, area = None):
        """ tunnustelee ja palauttaa tyhjän alueen koordinaatit """
        if area is None:
            area = {(x,y)}
        to_test = []
        for nx, ny in self.get_neighbours_coords(x, y):
            if self.__tiles[nx][ny] == 0 and (nx,ny) not in area:
                to_test.append((nx, ny))
                area.add((nx, ny))
        for tx, ty in to_test:
            area=area.union(self.collect_area(tx, ty, area))
        return area


    def get_mask(self, x, y):
        """ onko ruutu vielä piilossa """
        return self.__masked[x][y]


    def flag(self, x, y, flag=-1):
        """ aseta lippu peitetylle ruudulle"""
        if self.invalid_coordinates(x, y):
            print("Koordinaatit on pelilaudan ulkopuolella", file=stderr)
            return False

        if self.__masked[x][y] not in range(10,14):
            print("Ruudulla odottamaton lippu tai se on avattu", file=stderr)
            return False

        if flag == -1:
            self.__masked[x][y] += 1 if self.__masked[x][y] < 13 else -3
            return True

        if flag not in range(10,14):
            print("Lippua jota asetat ei ole olemassa", file=stderr)
            return False

        self.__masked[x][y]=flag
        return True


    def guess(self, x, y):
        """ tee arvaus """
        if self.invalid_coordinates(x, y):
            print("Koordinaatit on pelilaudan ulkopuolella", file=stderr)
            return False

        if self.__masked[x][y] == 0:
            print("Ruutu on jo avattu", file=stderr)
            return False

        self.__masked[x][y] = 0

        if self.__tiles[x][y] == 9:
            return False

        if self.__tiles[x][y] == 0:
            for cx, cy in self.collect_area( x, y ):
                for nx, ny in self.get_neighbours_coords(cx, cy, True):
                    self.__masked[nx][ny] = 0

        return True

    def reveal(self):
        """ näytä koko lauta """
        w, h = self.__width, self.__height
        self.__masked = [[0 for _ in range(h)] for _ in range(w)]

    def get_width(self):
        """ palauttaa laudan leveyden """
        return self.__width

    def get_height(self):
        """ palauttaa laudan korkeuden """
        return self.__height
