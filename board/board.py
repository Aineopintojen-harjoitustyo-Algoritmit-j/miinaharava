from random import randrange
from sys import stderr
from copy import deepcopy

class Board():
    def __init__(self, size = 10):
        self.size = size
        self.tiles = []
        self.masked = []
        self.initialize_tiles( size )
        self.randomize_bombs( size )
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
            
    def calculate_neighbours(self):
        neighbours = (  (-1,-1), (0,-1), (1,-1),
                        (-1, 0),         (1, 0),
                        (-1, 1), (0, 1), (1, 1) )
        for y in range(self.size):
            for x in range(self.size):
                if self.tiles[x][y] == 9:
                    continue
                neighbouring_bombs = 0
                for dx,dy in neighbours:
                    if x+dx < 0 or x+dx >= self.size:
                        continue
                    if y+dy < 0 or y+dy >= self.size:
                        continue
                    if self.tiles[x+dx][y+dy] == 9:
                        neighbouring_bombs += 1
                self.tiles[x][y] = neighbouring_bombs
        
    def reset_guesses(self):
        pass
        
    def get_view(self):
        view = deepcopy(self.masked)
        for y in range(self.size):
            for x in range(self.size):
                if not view[x][y]:
                    view[x][y]=self.tiles[x][y]
        return view
        
    def collect_area(self, x, y, area=set()):
        to_test = []
        for dx, dy in ( (0,-1), (-1,0), (1,0), (0,1) ):
            if x+dx < 0 or x+dx >= self.size:
                continue
            if y+dy < 0 or y+dy >= self.size:
                continue
            if self.tiles[x+dx][y+dy] == 0 and (x+dx,y+dy) not in area:
                area.add((x+dx, y+dy))
                to_test.append((x+dx, y+dy))
        for tx, ty in to_test:
            area.add((x,y))
            area=area.union(self.collect_area(tx, ty, area))
        return area
        
        
    def make_guess(self, x, y):
        if x not in range(self.size) or y not in range(self.size):
            print("Koordinaatit on pelilaudan ulkopuolella", file=stderr)
            return False
            
        if self.masked[x][y] == 0:
            print("Ruutu on jo avattu", file=stderr)
            return False
            
        if self.tiles[x][y] == 9:
            self.masked[x][y] = 0
            return False
            
        if self.tiles[x][y] == 0:
            for cx, cy in self.collect_area( x, y ):
                for dx, dy in ( (0,-1), (-1,0), (0,0), (1,0), (0,1) ):
                    if cx+dx < 0 or cx+dx >= self.size:
                        continue
                    if cy+dy < 0 or cy+dy >= self.size:
                        continue
                    self.masked[cx+dx][cy+dy] = 0
        else:
            self.masked[x][y] = 0
                                
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
    
    
    