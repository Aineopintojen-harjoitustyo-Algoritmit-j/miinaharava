"""test_board.py - Testit pelilaudalle"""
# pylint: disable = protected-access

import unittest
from board import Board, Level, LevelSpecs

class TestBoardClass(unittest.TestCase):
    """ pelilauden testit"""
    def test_init(self):
        """ olion luominen onnistuu """
        b = Board()
        self.assertTrue(b.get_width()>0)

    def test_init_with_level(self):
        """ olion luominen onnistuu vaikeustasolla"""
        b = Board(level=Level.EXPERT)
        self.assertEqual(b.get_width(), LevelSpecs[Level.EXPERT][0])
        self.assertEqual(b.get_height(), LevelSpecs[Level.EXPERT][1])
        self.assertEqual(b.get_bombs(), LevelSpecs[Level.EXPERT][2])

    def test_init_with_incorect_dimensions(self):
        """ luominen ei saa onnitua mahdottomilla mitoilla """
        b = Board(width=1, height=999)
        self.assertEqual(b.get_width(), LevelSpecs[Level.BEGINNER][0])
        self.assertEqual(b.get_height(), LevelSpecs[Level.BEGINNER][1])
        self.assertEqual(b.get_bombs(), LevelSpecs[Level.BEGINNER][2])

    def test_get_view_and_guess(self):
        """ laudan näkymä on oikein senkin jälkeen kun on arvattu"""
        b = Board(width=3, height=3)
        b._Board__tiles=[[0,0,0],[0,1,1],[0,1,9]]

        v = b.get_view()
        t = [[12,12,12],[12,12,12],[12,12,12]]
        for i in range(3):
            self.assertEqual(v[i],t[i])

        self.assertTrue(b.guess(0,0))
        v = b.get_view()
        t = [[0,0,0],[0,1,1],[0,1,12]]
        for i in range(3):
            self.assertEqual(v[i],t[i])

        self.assertFalse(b.guess(2,2))

    def test_is_winning(self):
        """ toimiiko voittotilanteen tunnistus """
        b = Board(width=2, height=2)
        b._Board__tiles=[[1,9],[9,9]]
        b._Board__masked=[[12,12],[12,12]]
        self.assertFalse(b.is_winning())
        b._Board__masked=[[0,12],[12,12]]
        self.assertTrue(b.is_winning())
        b._Board__masked=[[0,0],[12,12]]
        self.assertFalse(b.is_winning())

    def test_error_conditions_in_guess(self):
        """ ruudun avaus alueen ulkopuolelta tai avatussa ruudussa ei onnistu"""
        b = Board(width=2, height=2)
        b._Board__tiles=[[1,9],[9,9]]
        self.assertFalse(b.guess(2,2))
        self.assertTrue(b.guess(0,0))
        self.assertFalse(b.guess(0,0))

    def test_get_mask(self):
        """ maski annetaan oikein """
        b = Board(width=2, height=2)
        b._Board__tiles=[[1,9],[9,9]]
        self.assertEqual(b.get_mask(0,0), 12)

    def test_flag(self):
        """ ruudun liputus toimii """
        b = Board(width=2, height=2)
        b._Board__tiles=[[1,9],[9,9]]
        self.assertEqual(b.get_mask(0,0), 12)
        self.assertTrue(b.flag(0,0))
        self.assertEqual(b.get_mask(0,0), 13)
        self.assertTrue(b.flag(0,0))
        self.assertEqual(b.get_mask(0,0), 10)
        self.assertTrue(b.flag(0,0))
        self.assertEqual(b.get_mask(0,0), 11)
        self.assertTrue(b.flag(0,0))
        self.assertEqual(b.get_mask(0,0), 12)
        self.assertTrue(b.flag(0,0,10))
        self.assertEqual(b.get_mask(0,0), 10)

    def test_flag_error_conditions(self):
        """ liputus ei onnistu jos avattu, alueen ulkopuolella, outo arvo """
        b = Board(width=2, height=2)
        b._Board__tiles=[[1,9],[9,9]]
        b._Board__masked[0][0]=6
        self.assertFalse(b.flag(0,0))
        b._Board__masked[0][0]=10
        self.assertFalse(b.flag(0,0,4))
        b._Board__masked[0][0]=0
        self.assertFalse(b.flag(0,0))
        self.assertFalse(b.flag(2,2))

    def test_reveal(self):
        """ paljastuksen jälkeen näkyy laatat sellaisenaan """
        b = Board(width=2, height=2)
        b.reveal()
        t = b._Board__tiles
        v = b.get_view()
        for i in range(2):
            self.assertEqual(v[i],t[i])

    def test_get_level(self):
        """ Testataan että nykyinen vaikeustaso palautuu oikein """
        b = Board(level=Level.INTERMEDIATE)
        self.assertIn(LevelSpecs[Level.INTERMEDIATE][3], b.get_level_name())
        b = Board(level=Level.INTERMEDIATE, width=25, bombs=2)
        self.assertIn("Mukautettu", b.get_level_name())
