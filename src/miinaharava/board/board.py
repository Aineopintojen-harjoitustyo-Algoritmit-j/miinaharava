""" board/board.py - Pelilaudan käsittelyyn tarkoitetut jutut """
from random import randrange
from sys import stderr
from copy import deepcopy

from .static import Level, Tile, LevelSpecs


class Board():
    """	Board - Luokka joka pitää huolen pelilaudasta ja siihen kohdistuvista
                siirroista.
    """
    def __init__(self,
            level = Level.BEGINNER,
            width = None,
            height = None,
            mines = None,
            board = None):
        # pylint: disable = too-many-arguments

        if ( not width or not height or
                width not in range(2,51) or
                height not in range(2,51) ):
            width, height = None, None

        self.__level = level
        self.__width, self.__height, self.__mines =LevelSpecs[self.__level][:3]

        if width:
            self.__width = width
        if height:
            self.__height = height
        if height or width or mines:
            self.__mines = mines

        if self.__mines not in range(1,self.__width*self.__height):
            self.__mines = self.__width


        if board and self.__validate_board(board):
            self.__width, self.__height = self.__get_board_dimensions(board)
            self.__mines = self.__get_board_mines(board)
        else:
            board = None

        for _, specs in LevelSpecs.items():
            if (self.__width, self.__height, self.__mines) == specs[:3]:
                self.__level_name = specs[3]
                break
        else:
            self.__level_name = "Mukautettu"

        self.__level_name += ( f" ({self.__width}x{self.__height}"
                    f", {self.__mines} miinaa)" )

        self.__tiles = None
        self.__masked = None

        self.__initialize_tiles()
        if board:
            self.__populate_with_board(board)
        else:
            self.__randomize_mines()
        self.__calculate_neighbours()

    def __validate_board(self, board):
        w = len(board[0])
        h = len(board)
        if w not in range(2,51) or h not in range(2,51):
            return False
        for line in board:
            if len(line)!=w:
                return False
        if self.__get_board_mines(board) not in range (1, w*h):
            return False
        return True


    def __get_board_dimensions(self, board):
        return len(board[0]), len(board)


    def __get_board_mines(self, board):
        return sum((sum(x) for x in board))


    def __populate_with_board(self, board):
        for y in range(self.__height):
            for x in range(self.__width):
                if board[y][x]:
                    self.__tiles[x][y] = Tile.MINE

    def __initialize_tiles(self):
        """ alustaa pelilaudan matriisit """
        w, h = self.__width, self.__height
        self.__tiles = [[Tile.BLANK for _ in range(h)] for _ in range(w)]
        self.__masked = [[Tile.UNOPENED for _ in range(h)] for _ in range(w)]


    def __randomize_mines(self):
        """ arpoo pelilaudalle pommit """
        for _ in range(self.__mines):
            while True:
                x, y = randrange(0,self.__width), randrange(0,self.__height)
                if self.__tiles[x][y] != Tile.BLANK:
                    continue
                self.__tiles[x][y] = Tile.MINE
                break


    def __calculate_neighbours(self):
        """ laskee naapurissa olevien pommien määrät valmiiksi laudalle """
        for y in range(self.__height):
            for x in range(self.__width):
                if self.__tiles[x][y] == Tile.MINE:
                    continue
                neighbouring_mines = 0
                for nx, ny in self.get_neighbours_coords(x,y):
                    if self.__tiles[nx][ny] == Tile.MINE:
                        neighbouring_mines += 1
                self.__tiles[x][y] = neighbouring_mines


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
                if self.__tiles[x][y] == Tile.MINE:
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
            if self.__tiles[nx][ny] == Tile.BLANK and (nx,ny) not in area:
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

        if not self.__masked[x][y]:
            print("Ruutu on jo avattu", file=stderr)
            return False

        self.__masked[x][y] = 0

        if self.__tiles[x][y] == Tile.MINE:
            return False

        if self.__tiles[x][y] == Tile.BLANK:
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

    def get_mines(self):
        """ palauttaa pommien määrän """
        return self.__mines

    def get_level_name(self):
        """ palauttaa vaikesutason nimen"""
        return self.__level_name
