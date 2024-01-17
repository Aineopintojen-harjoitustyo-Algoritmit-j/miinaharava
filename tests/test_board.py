"""test_board.py - Testit pelilaudalle"""

import unittest
from board.board import Board

class TestBoardClass(unittest.TestCase):
    """ pelilauden testit"""
    def test_init(self):
        """ olion luominen onnistuu """
        b = Board()
        self.assertTrue(b.get_width()>0)

    def test_init_with_size(self):
        """ olion luominen onnistuu tietyllä koolla"""
        b = Board(30, 15)
        self.assertEqual(b.get_width(), 30)
        self.assertEqual(b.get_height(), 15)

    def test_get_view_and_guess(self):
        """ laudan näkymä on oikein senkin jälkeen kun on arvattu"""
        b = Board(3,3)
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
        b = Board(2,2)
        b._Board__tiles=[[1,9],[9,9]]
        b._Board__masked=[[12,12],[12,12]]
        self.assertFalse(b.is_winning())
        b._Board__masked=[[0,12],[12,12]]
        self.assertTrue(b.is_winning())
        b._Board__masked=[[0,0],[12,12]]
        self.assertFalse(b.is_winning())

    def test_error_conditions_in_guess(self):
        """ ruudun avaus alueen ulkopuolelta tai avatussa ruudussa ei onnistu"""
        b = Board(2,2)
        b._Board__tiles=[[1,9],[9,9]]
        self.assertFalse(b.guess(2,2))
        self.assertTrue(b.guess(0,0))
        self.assertFalse(b.guess(0,0))

    def test_get_mask(self):
        """ maski annetaan oikein """
        b = Board(2,2)
        b._Board__tiles=[[1,9],[9,9]]
        self.assertEqual(b.get_mask(0,0), 12)

    def test_flag(self):
        """ ruudun liputus toimii """
        b = Board(2,2)
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
        b = Board(2,2)
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
        b = Board(2,2)
        b.reveal()
        t = b._Board__tiles
        v = b.get_view()
        for i in range(2):
            self.assertEqual(v[i],t[i])
        