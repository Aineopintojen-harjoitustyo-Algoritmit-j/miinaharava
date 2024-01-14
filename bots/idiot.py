""" bots/idiot.py - se ensimmäinen botti joka tekee kaiken väärin """
from bots.bot import Bot
from tui.static import Action
class IdiotBot(Bot):
    """ IdiotBot - merkistsee kaikki turvallisiksi avata """
    # pylint: disable = too-few-public-methods

    def hint(self, matrix, x, y):
        """ merkitsee jonkin ruudun """
        super().hint(matrix, x, y)
        # pylint: disable = consider-using-enumerate
        for ty in range(len(matrix[0])):
            for tx in range(len(matrix)):
                if matrix[tx][ty]==10:
                    return(Action.SAFE, tx, ty)
        return (Action.NOOP, x, y)
    