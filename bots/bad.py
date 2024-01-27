""" bots/bad.py - botti joka ehkä osaa merkata jonkun asian """
from random import sample
from tui import Action
from .bot import Bot

class BadBot(Bot):
    """ IdiotBot - merkistsee kaikki turvallisiksi avata """
    # pylint: disable = too-few-public-methods
    def missing_bombs(self, matrix, x, y):
        """ test how many boms are not found at the coordinate """
        dx = len(matrix)
        dy = len(matrix[0])
        bcount = 0
        for nx, ny in self.neighbours(dx, dy, x, y):
            if matrix[nx][ny] in (9,11):
                bcount+=1
        return matrix[x][y]-bcount

    def get_tiles_at_border(self, matrix):
        """ get interesting tiles on the border of cleared and masked area """
        tiles = []
        w = len(matrix)
        h = len(matrix[0])
        for y in range(h):
            for x in range(w):
                if matrix[x][y] < 12:
                    open_tiles=1
                    masked_tiles=0
                else:
                    open_tiles=0
                    masked_tiles=1
                for nx, ny in self.neighbours(w, h, x, y):
                    if matrix[nx][ny] < 12:
                        open_tiles+=1
                    else:
                        masked_tiles+=1
                if open_tiles and masked_tiles:
                    tiles.append( (x,y) )
        return tiles

    def get_unopened_tiles(self, matrix):
        """ get interesting tiles on the border of cleared and masked area """
        tiles = []
        w = len(matrix)
        h = len(matrix[0])
        for y in range(h):
            for x in range(w):
                if matrix[x][y] == 12:
                    tiles.append( (x,y) )
        return tiles

    def hint(self, matrix, cursor_x, cursor_y):
        """ merkitsee jonkin ruudun """
        super().hint(matrix, cursor_x, cursor_y)
        w = len(matrix)
        h = len(matrix[0])
        # pylint: disable = consider-using-enumerate
        for x, y in self.get_tiles_at_border(matrix):
            ncoords=self.neighbours(w,h,x,y)
            ntiles=self.coordinates_to_tiles(matrix,ncoords)
            unopened=ntiles.count(12)
            bombs=ntiles.count(10)
            if unopened:
                if matrix[x][y]<9 and matrix[x][y]==bombs:
                    safe = ncoords[ntiles.index(12)]
                    return(Action.SAFE, safe[0], safe[1])
                if matrix[x][y]-bombs==unopened:
                    bomb = ncoords[ntiles.index(12)]
                    return(Action.BOMB, bomb[0], bomb[1])
        if self.uncertain:
            x, y = sample(self.get_unopened_tiles(matrix),1)[0]
            return (Action.OPEN, x, y)
        return (Action.NOOP, cursor_x, cursor_y)
