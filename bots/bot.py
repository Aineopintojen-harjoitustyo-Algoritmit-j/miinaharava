""" bots/bot.py - bottien kantaisä """
from tui import Action

class Bot():
    """ Bot - perusluokka perittäväksi """
    def __init__(self, **opts):
        self.uncertain = opts['uncertain'] if 'uncertain' in opts else False
        self.hints = 0

    def neighbours(self,dx,dy,x,y):
        """ palauttaa listana viereiset koordinaatit """
        offsets = (
            (-1, -1), ( 0, -1), ( 1, -1),
            (-1,  0),           ( 1,  0),
            (-1,  1), ( 0,  1), ( 1,  1),
        )
        coords=[]
        for ox, oy in offsets:
            if ox+x in range(dx):
                if oy+y in range(dy):
                    coords.append((ox+x, oy+y))
        return coords

    def coordinates_to_tiles(self, matrix, coords):
        """ lukee koordinaateissa olevien ruutujen arvot listaksi """
        return [matrix[x][y] for x,y in coords]

    def hint(self, matrix, cursor_x, cursor_y):
        """ antaa vinkin. tässä tapauksessa ei mitään """
        # pylint: disable = unused-argument
        self.hints += 1
        return Action.NOOP, cursor_x, cursor_y
