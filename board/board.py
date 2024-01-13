from random import randrange
from sys import stderr
from copy import deepcopy

class Board():
    def __init__(self, size = 10, bombs = 0):
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
        self.tiles = [[0 for _ in range(size)] for _ in range(size)]
        self.masked = [[10 for _ in range(size)] for _ in range(size)]
        
    def randomize_bombs(self, bomb_count):
        for _ in range(bomb_count):
            while True:
                x, y = randrange(0,self.size), randrange(0,self.size)
                if self.tiles[x][y] != 0:
                    continue
                self.tiles[x][y]=9
                break
                
    def invalid_coordinates(self, x, y):
        return x < 0 or x >= self.size or y < 0 or y >= self.size
        
    def get_neighbours_coords(self, x, y, coordinates = None):
        if not coordinates:
            coordinates=[]
        offsets = (
            (-1,-1), (0,-1), (1,-1),
            (-1, 0),         (1, 0),
            (-1, 1), (0, 1), (1, 1)
        )
        for dx,dy in offsets:
            if not self.invalid_coordinates(x+dx, y+dy):
                coordinates.append( (x+dx, y+dy) )
        return coordinates
            
    def calculate_neighbours(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.tiles[x][y] == 9:
                    continue
                neighbouring_bombs = 0
                for nx, ny in self.get_neighbours_coords(x,y):
                    if self.tiles[nx][ny] == 9:
                        neighbouring_bombs += 1
                self.tiles[x][y] = neighbouring_bombs
        
    def get_view(self):
        view = deepcopy(self.masked)
        for y in range(self.size):
            for x in range(self.size):
                if not view[x][y]:
                    view[x][y]=self.tiles[x][y]
        return view
        
    def is_winning(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.tiles[x][y] != 9 and self.masked[x][y]:
                    return False
        return True
            
        
    def collect_area(self, x, y, area=set()):
        if not area:
            area.add((x,y))
        to_test = []
        for dx, dy in ( (0,-1), (-1,0), (1,0), (0,1) ):
            if self.invalid_coordinates(x+dx, y+dy):
                continue
            if self.tiles[x+dx][y+dy] == 0 and (x+dx,y+dy) not in area:
                to_test.append((x+dx, y+dy))
                area.add((x+dx, y+dy))
        for tx, ty in to_test:
            area=area.union(self.collect_area(tx, ty, area))
        return area
        
    def get_mask(self, x, y):
        return self.masked[x][y]
        
    def make_guess(self, x, y):
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
                for nx, ny in self.get_neighbours_coords(cx, cy, [(0,0)]):
                    self.masked[nx][ny] = 0
                                
        return True
        
        
    
if __name__ == "__main__":
    def print_matrix(m):
        for y in range(len(m)):
            for x in range(len(m[0])):
                print(end=f"[{m[x][y]:x}]")
            print()

    b = Board()
    b.make_guess(5,5)    
    print_matrix(b.get_view())
    
    