"""test_board.py - Testit pelilaudalle"""

import unittest
from board.board import Board

class TestBoardClass(unittest.TestCase):
    """ pelilauden testit"""
    def test_init(self):
        """ olion luominen onnistuu """
        b = Board()
        self.assertTrue(b.size>0)

    def test_init_with_size(self):
        """ olion luominen onnistuu tietyllä koolla"""
        b = Board(15)
        self.assertEqual(b.size, 15)

    def test_get_view_and_make_guess(self):
        """ laudan näkymä on oikein senkin jälkeen kun on arvattu"""
        b = Board(3)
        b.tiles=[[0,0,0],[0,1,1],[0,1,9]]

        v = b.get_view()
        t = [[10,10,10],[10,10,10],[10,10,10]]
        for i in range(3):
            self.assertEqual(v[i],t[i])

        self.assertTrue(b.make_guess(0,0))
        v = b.get_view()
        t = [[0,0,0],[0,1,1],[0,1,10]]
        for i in range(3):
            self.assertEqual(v[i],t[i])

        self.assertFalse(b.make_guess(2,2))

    def test_is_winning(self):
        """ toimiiko voittotilanteen tunnistus """
        b = Board(2)
        b.tiles=[[1,9],[9,9]]
        b.masked=[[10,10],[10,10]]
        self.assertFalse(b.is_winning())
        b.masked=[[0,10],[10,10]]
        self.assertTrue(b.is_winning())
        b.masked=[[0,0],[10,10]]
        self.assertFalse(b.is_winning())

    def test_error_conditions_in_make_guess(self):
        """ ruudun avaus alueen ulkopuolelta tai avatussa ruudussa ei onnistu"""
        b = Board(2)
        b.tiles=[[1,9],[9,9]]
        self.assertFalse(b.make_guess(2,2))
        self.assertTrue(b.make_guess(0,0))
        self.assertFalse(b.make_guess(0,0))

    def test_get_mask(self):
        """ maski annetaan oikein """
        b = Board(2)
        b.tiles=[[1,9],[9,9]]
        self.assertEqual(b.get_mask(0,0), 10)

    def test_flag_tile(self):
        """ ruudun liputus toimii """
        b = Board(2)
        b.tiles=[[1,9],[9,9]]
        self.assertEqual(b.get_mask(0,0), 10)
        self.assertTrue(b.flag_tile(0,0))
        self.assertEqual(b.get_mask(0,0), 11)
        self.assertTrue(b.flag_tile(0,0))
        self.assertEqual(b.get_mask(0,0), 12)
        self.assertTrue(b.flag_tile(0,0))
        self.assertEqual(b.get_mask(0,0), 10)

    def test_flaf_tile_error_conditions(self):
        """ liputus ei onnistu jos avattu, alueen ulkopuolella, outo arvo """
        b = Board(2)
        b.tiles=[[1,9],[9,9]]
        b.masked[0][0]=14
        self.assertFalse(b.flag_tile(0,0))
        b.masked[0][0]=0
        self.assertFalse(b.flag_tile(0,0))
        self.assertFalse(b.flag_tile(2,2))
        