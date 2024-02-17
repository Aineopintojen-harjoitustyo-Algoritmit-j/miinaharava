""" tests/test_board.py - Testit pelilaudalle """

import unittest

from board import Board, Level, LevelSpecs

def matrix_equals(m1, m2):
    """ matrix_equals - apufunktio testaa onko matriisit samat """
    if len(m1)!=len(m2):
        return False
    # pylint: disable = consider-using-enumerate
    for i in range(len(m1)):
        if m1[i] != m2[i]:
            return False
    return True

def matrix_swap_xy(m):
    """ matrix_swap_xy - palauttaa matriisin korvattu x -> y ja y -> x """
    if not m:
        return None
    w, h = len(m[0]), len(m)
    ret_m = [[0 for _ in range(h)] for _ in range(w)]
    for y in range(h):
        for x in range(w):
            ret_m[x][y]=m[y][x]
    return ret_m


class TestBoardClass(unittest.TestCase):
    """ pelilauden testit kattava luokka """

    def test_init_works_and_defaults_beginner(self):
        """ pelilautaolion luominen onnistuu ja defaulttaa aloittelijaksi """
        b = Board()
        self.assertEqual(b.get_width(), LevelSpecs[Level.BEGINNER][0])
        self.assertEqual(b.get_height(), LevelSpecs[Level.BEGINNER][1])
        self.assertEqual(b.get_mines(), LevelSpecs[Level.BEGINNER][2])
        self.assertTrue(b.get_width()>0)


    def test_init_with_level(self):
        """ olion luominen onnistuu vaikeustasolla"""
        b = Board(level=Level.EXPERT)
        self.assertEqual(b.get_width(), LevelSpecs[Level.EXPERT][0])
        self.assertEqual(b.get_height(), LevelSpecs[Level.EXPERT][1])
        self.assertEqual(b.get_mines(), LevelSpecs[Level.EXPERT][2])


    def test_init_with_custom_dimentions(self):
        """ mukautetun kentän luominen onnistuu """
        b = Board(width=13, height=14, mines=15)
        self.assertEqual(b.get_width(), 13)
        self.assertEqual(b.get_height(), 14)
        self.assertEqual(b.get_mines(), 15)
        b = Board(width=22, height=12)
        self.assertEqual(b.get_width(), 22)
        self.assertEqual(b.get_height(), 12)
        self.assertEqual(b.get_mines(), 22)


    def test_init_with_incorect_dimensions(self):
        """ luominen ei saa onnitua mahdottomilla mitoilla """
        b = Board(width=1, height=999, mines=0)
        self.assertEqual(b.get_width(), LevelSpecs[Level.BEGINNER][0])
        self.assertEqual(b.get_height(), LevelSpecs[Level.BEGINNER][1])
        self.assertEqual(b.get_mines(), LevelSpecs[Level.BEGINNER][2])


    def test_init_with_valid_board(self):
        """ Pelilaudan luominen onnistuu kelvollisella asettelulla """
        t = [
            [0,0,0,0],
            [0,0,0,1],
            [0,0,0,0]
        ]
        b = Board(board = t)
        self.assertEqual(b.get_width(), 4)
        self.assertEqual(b.get_height(), 3)
        self.assertEqual(b.get_mines(), 1)


    def test_init_with_invalid_board(self):
        """ Yritetään luoda peli kelvottomalla laudalla """
        t = [
            [0,0,0,0,0],
            [0,0,0,1],
            [0,0,0,0,0]
        ]
        b = Board(board = t)
        # Resetoituihan aloittelijan lauta
        self.assertIn(LevelSpecs[Level.BEGINNER][3], b.get_level_name())

        t = [
            [0,1,0,0,0],
        ]
        b = Board(board = t)
        self.assertIn(LevelSpecs[Level.BEGINNER][3], b.get_level_name())

        t = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
        b = Board(board = t)
        self.assertIn(LevelSpecs[Level.BEGINNER][3], b.get_level_name())

        t = [
            [1,1,1],
            [1,1,1],
            [1,1,1]
        ]
        b = Board(board = t)
        self.assertIn(LevelSpecs[Level.BEGINNER][3], b.get_level_name())


    def test_tiles_and_masks_ok(self):
        """ Luohan luokka sisäiset laatat ja maskit oikein """
        # pylint: disable = protected-access
        t = [
            [0,0,0,0],
            [0,0,0,1],
            [0,0,0,0]
        ]
        b = Board(board = t)
        self.assertEqual(b.get_width(), 4)
        self.assertEqual(b.get_height(), 3)
        self.assertEqual(b.get_mines(), 1)

        # testataan onko laatat tallennettu oikein luokkaan
        t = matrix_swap_xy([
            [0,0,1,1],
            [0,0,1,9],
            [0,0,1,1]
        ])
        self.assertTrue(matrix_equals(b._Board__tiles, t))

        # onko maksit asetettu oikein
        t = matrix_swap_xy([
            [12,12,12,12],
            [12,12,12,12],
            [12,12,12,12]
        ])
        self.assertTrue(matrix_equals(b._Board__masked, t))


    def test_get_view_and_guess(self):
        """ laudan näkymä on oikein senkin jälkeen kun on arvattu """

        t = [
            [0,0,1],
            [0,0,0],
            [0,0,0]
        ]
        b = Board(board=t)

        # Antaahan pelikenttä pelkkää maskia aluksi
        t = matrix_swap_xy([
            [12,12,12],
            [12,12,12],
            [12,12,12]
        ])
        self.assertTrue(matrix_equals(b.get_view(), t))

        # avataan yläkulma -> palatuu True
        self.assertTrue(b.guess(0,0))

        # onko näkymä nyt oikein
        t = matrix_swap_xy([
            [0,1,12],
            [0,1,1],
            [0,0,0]
        ])
        self.assertTrue(matrix_equals(b.get_view(), t))

        # avataan alakulma jossa miina -> palautuu False
        self.assertFalse(b.guess(2,0))


    def test_is_winning(self):
        """ toimiiko voittotilanteen tunnistus """

        t = [
            [0,1],
            [0,0],
        ]
        b = Board(board=t)
        self.assertFalse(b.is_winning())

        # Avataan ruutu jolla ei tule viellä voittoa
        t = matrix_swap_xy([
            [1,12],
            [12,12]
        ])
        self.assertTrue(b.guess(0,0))
        self.assertTrue(matrix_equals(b.get_view(), t))
        self.assertFalse(b.is_winning())

        # Avataan loputkin ruudut, jolloin pitäisi voittaa
        t = matrix_swap_xy([
            [1,12],
            [1,1]
        ])
        self.assertTrue(b.guess(0,1))
        self.assertTrue(b.guess(1,1))
        self.assertTrue(matrix_equals(b.get_view(), t))
        self.assertTrue(b.is_winning())

        # Lupuksi avataan miina jolloin voittoa ei enää pitäisi olla
        t = matrix_swap_xy([
            [1,9],
            [1,1]
        ])
        self.assertFalse(b.guess(1,0))
        self.assertTrue(matrix_equals(b.get_view(), t))
        self.assertFalse(b.is_winning())


    def test_error_conditions_in_guess(self):
        """ ruudun avaus alueen ulkopuolelta tai avatussa ruudussa ei onnistu"""
        t = [
            [0,1],
            [0,0],
        ]
        b = Board(board=t)
        self.assertFalse(b.guess(2,2))
        self.assertTrue(b.guess(0,0))
        self.assertFalse(b.guess(0,0))


    def test_get_mask(self):
        """ maski annetaan oikein """
        t = [
            [1,0],
            [0,0],
        ]
        b = Board(board=t)
        self.assertEqual(b.get_mask(1,0), 12)
        self.assertTrue(b.guess(1,0))
        self.assertFalse(b.get_mask(1,0))


    def test_flag(self):
        """ ruudun lipun vaihto ja asetus toimii """
        t = [
            [0,0],
            [0,1],
        ]
        b = Board(board=t)
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
        t = [
            [0,1],
            [1,1],
        ]
        b = Board(board=t)
        self.assertFalse(b.flag(0,0,6))	# Lippu jota ei ole
        self.assertFalse(b.flag(2,2))	# Alueen ulkopuolella
        self.assertTrue(b.guess(0,0))
        self.assertFalse(b.flag(0,0))	# Avattu laatta


    def test_reveal(self):
        """ paljastuksen jälkeen näkyy laatat sellaisenaan """
        t = [
            [0,1],
            [1,1],
        ]
        b = Board(board=t)
        b.reveal()
        t = matrix_swap_xy([
            [3,9],
            [9,9]
        ])
        self.assertTrue(matrix_equals(b.get_view(), t))


    def test_get_level_name(self):
        """ Testataan että nykyinen vaikeustaso palautuu oikein """
        b = Board(level=Level.INTERMEDIATE)
        self.assertIn(LevelSpecs[Level.INTERMEDIATE][3], b.get_level_name())
        b = Board(level=Level.INTERMEDIATE, width=25, mines=2)
        self.assertIn("Mukautettu", b.get_level_name())
