""" bots/bot.py - bottien kantaisä """
from tui.static import Action

class Bot():
    """ Bot - perusluokka perittäväksi """
    # pylint: disable = too-few-public-methods
    def __init__(self):
        self.hints = 0

    def hint(self, matrix, x, y):
        """ antaa vinkin. tässä tapauksessa ei mitään """
        # pylint: disable = unused-argument
        self.hints += 1
        return Action.NOOP, x, y
