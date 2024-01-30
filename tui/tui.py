""" tui/tui.py - runko käyttöliittymälle """
# pylint: disable = multiple-imports
from .static import Action
from .kbd import Kbd, NoKbd
from .ansi_draw import AnsiDraw, SuppressDraw


class Tui():
    """ Tui - Luokka käyttäjän interaktiota varten """
    # pylint: disable = too-many-arguments, too-many-instance-attributes
    def __init__(self,
                bot = None,
                autoplay = False,
                interactive = True,
                suppress = False,
                height = 9,
                level_name = "outo lauta"):

        # jos ei ole bottia pitää olla interaktiivinen
        if bot is None:
            autoplay = False
            interactive = True
            suppress = False

        # jos ei mitään näytetä ei voi olla interaktiivinen
        # pylint: disable = pointless-statement
        (interactive := False) if suppress else ()

        # automaattipeli pitää olla päällä jos ei interaktiivinen
        (autoplay := True) if not interactive else ()

        self.autoplay = autoplay
        self.interactive = interactive
        self.suppress = suppress
        self.height = height
        self.level_name = level_name

        self.bot = bot(uncertain=not self.interactive) if bot else None

        self.kbd = Kbd() if self.interactive else NoKbd()

        if self.suppress:
            self.draw = SuppressDraw()
        else:
            self.draw = AnsiDraw(height=self.height, name=self.level_name)

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
            f"{self.level_name}: " +
            "K  " if self.suppress else f"{'Kuolit!':<30}"
        )
        self.kbd.read_action()

    def game_win(self, matrix, x, y):
        """ tehtävät kun voittaa """
        self.draw.matrix(matrix, x, y)
        self.draw.status_line(
            f"{self.level_name}: " +
            "V  " if self.suppress else "{'Voitit!':<30}"
        )
        self.kbd.read_action()

    def game_end(self, matrix):
        """ tehtävät ihan pelin lopuksi """
        if self.interactive:
            self.draw.matrix(matrix, -1, -1)
            self.draw.status_line(
                f"{self.level_name}: " +
                f"{'Kiitos!':<30}"
            )
