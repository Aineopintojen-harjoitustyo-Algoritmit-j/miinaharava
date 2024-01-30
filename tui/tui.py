""" tui/tui.py - runko käyttöliittymälle """
# pylint: disable = multiple-imports
from .static import Action
from .kbd import Kbd, NoKbd
from .ansi_draw import AnsiDraw, SuppressDraw


class Tui():
    """ Tui - Luokka käyttäjän interaktiota varten """
    # pylint: disable = too-many-arguments
    def __init__(self,
                bot = None,
                autoplay = False,
                interactive = True,
                suppress = False,
                height = 9):

        self.autoplay = autoplay
        self.interactive = interactive
        self.suppress = suppress
        self.height = height

        # jos ei oo bottia pitää olla interaktiivinen
        if bot is None:
            self.autoplay = False
            self.interactive = True
            self.suppress = False

        # jos ei mitään näytetä ei voi olla interaktiivinen
        self.interactive = False if self.suppress else self.interactive

        # automaattipeli pitää olla päällä jos ei interaktiivinen
        self.autoplay = self.autoplay if self.interactive else True

        self.bot = bot(uncertain=not self.interactive) if bot else None

        if self.interactive:
            self.kbd = Kbd()
        else:
            self.kbd = NoKbd()

        if self.suppress:
            self.draw = SuppressDraw()
        else:
            self.draw = AnsiDraw(height=self.height)

    def matrix_selector(self, matrix, x, y):
        """ valinta matriisita """

        # automaattipeli avaa botin vinkit heti
        if self.autoplay:
            action, x, y = self.bot.hint(matrix, x, y)
            if action != Action.NOOP:
                self.draw.matrix(matrix, -1, -1)
                return Action.OPEN if action==Action.SAFE else action, x, y


        # ilman näppiskäsittelijää voidaan lopettaa
        if not self.interactive:
            return Action.QUIT, 0, 0

        w, h = len(matrix), len(matrix[0])
        while True:
            self.draw.matrix(matrix, x, y)
            action, x, y = self.kbd.read_matrix_action(w, h, x, y)
            match action:
                case Action.QUIT:
                    return (action, x, y)
                case Action.OPEN | Action.FLAG | Action.BOMB | Action.SAFE:
                    if matrix[x][y] >= 10:
                        return (action, x, y)
                case Action.HINT:
                    if self.bot is not None:
                        return self.bot.hint(matrix, x, y)

    def game_over(self, matrix, x, y):
        """ tehtävät kun kuolee """
        self.draw.matrix(matrix, x, y)
        self.draw.status_line(
            "K  " if self.suppress else "Peli ohitse! Kuolit!"
        )
        self.kbd.read_action()

    def game_win(self, matrix, x, y):
        """ tehtävät kun voittaa """
        self.draw.matrix(matrix, x, y)
        self.draw.status_line(
            "V  " if self.suppress else "Peli ohitse! Voitit!"
        )
        self.kbd.read_action()

    def game_end(self, matrix):
        """ tehtävät ihan pelin lopuksi """
        if self.interactive:
            self.draw.matrix(matrix, -1, -1)
            self.draw.status_line("Kiitos!             ")
